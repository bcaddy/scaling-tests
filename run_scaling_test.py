#!/usr/bin/env python3
"""
================================================================================
 Provide library functions for running scaling tests on Frontier
================================================================================
"""

import pathlib
import os

def ceildiv(a, b):
    """Integer division that gives the ceiling result not the floor. Faster than math.ceil and doesn't run into any
    floating point precision issues.

    Args:
        a (int): The numerator
        b (int): The denominator

    Returns:
        int: ceiling of a/b
    """
    return -(a // -b)

def compute_job_parameters(num_ranks):
    """Compute the number of nodes, resolution, and domain for the job

    Args:
        num_ranks (int): The number of ranks

    Returns:
        int, int, float: The number of nodes, resolution, and domain length for the job
    """

    # Check that the number of ranks is a cube of something
    cube_root_rounded = round(num_ranks**(1./3.))
    if cube_root_rounded ** 3 != num_ranks:
        raise Exception("The number of ranks is not a perfect cube")

    # Determine the number of nodes given that there are 8 GCDs per node on frontier
    ranks_per_node = 8
    num_nodes = ceildiv(num_ranks, ranks_per_node)

    # Determine the resolution with the given resolution per gpu. Note that this
    # is the resolution per side, not total. So the actual number of cells is
    # resolution_per_gpu^3
    resolution_per_gpu = 256
    resolution         = int(resolution_per_gpu * cube_root_rounded)

    # Determine the domain length with the given length per gpu. Note that this
    # is the length per side
    length_per_gpu = 1.0
    domain_length  = length_per_gpu * cube_root_rounded

    return num_nodes, resolution, domain_length

def make_sbatch_command(account, time, nodes, wrap, mail_user=None, job_name=None):
    """Generate the sbatch command to submit a job to the queue on Frontier

    Args:
        account (string): The account to charge the job time to
        time (string): The maximum wall time of the job. Allowed formats are "minutes", "minutes:seconds",
        "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".
        nodes (int): The number of nodes to request
        wrap (string): The command to run within the job, typically an srun command
        mail_user (string, optional): The email address to send alerts to. Defaults to None.
        job_name (string, optional): The name of the job. Defaults to None.

    Returns:
        _type_: _description_
    """
    if mail_user:
        mail = f'--mail-user={mail_user} --mail-type=ALL'
    else:
        mail = ''

    if job_name:
        job_name = f'--job-name={job_name}'
    else:
        job_name = ''

    return f"sbatch --account={account} --nodes={nodes} --time={time} {mail} {job_name} --wrap='{wrap}'"

def make_srun_command(num_nodes, num_ranks):
    """Generate the srun command to launch Cholla

    Args:
        num_nodes (int): The number of nodes to use
        num_ranks (int): The number of ranks to use

    Returns:
        string: The srun command
    """
    return f'srun --nodes={num_nodes} --ntasks={num_ranks} --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest '

def make_cholla_command(executable_path, input_file, resolution, domain_length, num_ranks, scaling_test_directory):
    """Generate the Cholla launch command

    Args:
        executable_path (PosixPath): The path to the Cholla executable
        input_file (PosixPath): The path to the input file
        resolution (int): The per side resolution of the whole simulation
        domain_length (float): The per side size of the domain
        num_ranks (int): The number of MPI ranks
        scaling_test_directory (PosixPath): The path to the directory to run the tests in

    Returns:
        string: The command to run Cholla
    """

    # Determine the output path and ensure it exists
    output_directory = scaling_test_directory / f'ranks_{num_ranks}_resolution_{resolution}'
    pathlib.Path(output_directory).mkdir(exist_ok=True)

    command = ' '.join(
        [
            f'{executable_path}',
            f'{input_file}',
            f'nx={int(resolution)}',
            f'ny={int(resolution)}',
            f'nz={int(resolution)}',
            f'xlen={domain_length}',
            f'ylen={domain_length}',
            f'zlen={domain_length}',
            f'outdir={output_directory}',
        ]
    )

    return command

def submit_job(account, time, num_ranks, executable_path, input_file, scaling_test_directory, job_name=None, mail_user=None, submit=False):

    num_nodes, resolution, domain_length = compute_job_parameters(num_ranks)

    srun_command = make_srun_command(num_nodes, num_ranks)

    cholla_command = make_cholla_command(executable_path, input_file, resolution, domain_length, num_ranks, scaling_test_directory)

    sbatch_command = make_sbatch_command(account, time, num_nodes, srun_command + cholla_command, mail_user, job_name)

    print('The sbatch command is:\n', sbatch_command)

    if submit:
        print('Submitting Job')
        os.system(sbatch_command)
    else:
        print('Job not submitted')
    print()

