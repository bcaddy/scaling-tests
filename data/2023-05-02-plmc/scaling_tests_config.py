#!/usr/bin/env python3
"""
================================================================================

================================================================================
"""

import pathlib
import sys
import os

# Load the scaling tests module
script_path = pathlib.Path(__file__).parent.resolve()
repo_path   = script_path.parent.parent
sys.path.insert(0, str(repo_path) + os.sep)

from run_scaling_test import submit_job

# Determine all the parameters
bin_path = script_path / 'cholla' / 'bin'
executable_path = sorted(pathlib.Path(bin_path).glob('cholla.*.*'))[0]

input_file_path = repo_path / 'slow_magnetosonic.txt'

job_name = 'cholla_mhd_scaling_test_'

mail_user = 'r.caddy@pitt.edu'

# Run the scaling Tests
num_ranks = [1, 8, 64, 512, 4096, 32768, 64000, 74088]
for num_rank in num_ranks:
    submit_job(account='csc380',
               time='10',
               num_ranks=num_rank,
               executable_path=executable_path,
               input_file=input_file_path,
               scaling_test_directory=script_path,
               job_name=job_name + str(num_rank),
               mail_user=mail_user,
               submit=False)

