#4.096kpc^3 512^3 sim on 8 GCDs at 8pc res
#4.096kpc^3 1024^3 sim on 64 GCDs at 4pc res
#4.096kpc^3 2048^3 sim on 512 GCDs at 2pc res (delta t = ?)
#8.192kpc^3 4096^3 sim on 4096 GCDs at 2pc res
#16.384kpc^3 8192^3 sim on 32768 GCDs at 2pc res
#20.48kpc^3 10240^3 sim on 64000 GCDs at 2pc res

# 8 Nodes per GCD on frontier

import os
import math


block_size = 256
ranks_per_node = 8

runs = [
    [4.096, 256, 1],
    [4.096, 512, 8],
    [4.096, 1024, 64],
    [4.096, 2048, 512],
    [8.192, 4096, 4096],
    [16.384, 8192, 32768],
    [20.48, 10240, 64000]
]

def sanity_check(run):
    domain_length_kpc, domain_length_cells, ranks = run
    print('res kpc:', domain_length_kpc/domain_length_cells)
    print('do ranks match', (domain_length_cells/float(block_size))**3,ranks)

#list(map(sanity_check,runs))

def make_sbatch_command(account, time, nodes, wrap, mail_user = None):
    if mail_user:
        mail = f'--mail-user={mail_user} --mail-type=BEGIN,END'
    else:
        mail = ''
    return f"sbatch -A {account} -N {nodes} -t {time} {mail} --wrap='{wrap}' "


def make_cholla_command(executable, input_file, run, srun=False):
    domain_length_kpc, domain_length_cells, ranks = run

    outdir = f'out/ranks_{ranks}_domain_{domain_length_kpc}_{domain_length_cells}/'

    nodes = math.ceil(ranks / ranks_per_node)
    # Ensure outdir exists
    if not os.path.isdir(outdir):
        os.system(f'mkdir -p {outdir}')

    if srun:
        srun_prefix = f'srun -N{nodes} -n{ranks} -c7 --gpus-per-task=1 --gpu-bind=closest'
    else:
        srun_prefix = ''

    half_kpc = domain_length_kpc/2
    command = ' '.join(
        [
            f'{srun_prefix}',
            f'{executable}',
            f'{input_file}',
            f'nx={domain_length_cells}',
            f'ny={domain_length_cells}',
            f'nz={domain_length_cells}',
            f'xlen={domain_length_kpc}',
            f'ylen={domain_length_kpc}',
            f'zlen={domain_length_kpc}',
            f'xmin=-{half_kpc}',
            f'ymin=-{half_kpc}',
            f'zmin=-{half_kpc}',
            f'outdir={outdir}',
        ]
    )

    return command, nodes

def submit_job(account, time, executable, input_file, run, mail_user=None, srun=False, submit=False):

    wrap, nodes = make_cholla_command(executable, input_file, run, srun=srun)
    command = make_sbatch_command(account, time, nodes, wrap, mail_user=mail_user)
    print(command)
    if submit:
        os.system(command)
    return command