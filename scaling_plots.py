#!/usr/bin/env python3
import sys, os
import numpy as np
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager
# Matplotlib settings
plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

# Load data
def load_data():
    # Get paths
    directory = str(input('Input directory name: ') or '2023-05-02-plmc')
    data_path = pathlib.Path(__file__).parent.resolve() / 'data' / directory
    data_dirs = sorted(pathlib.Path(data_path).glob('ranks*'))

    # Setup dataframe
    file_name = data_dirs[0] / 'run_timing.log'
    with open(file_name, 'r') as file:
        lines        = file.readlines()
        header       = lines[3][1:].split()
        scaling_data = pd.DataFrame(index=header)

    # Loop through the directories and load the data
    for path in data_dirs:
        file_name = path / 'run_timing.log'
        if file_name.is_file():
            with open(file_name, 'r') as file:
                lines  = file.readlines()
                data   = lines[4].split()
                scaling_data[data[0]] = pd.to_numeric(data)
        else:
            print(f'File: {file_name} not found.')

    return scaling_data

# Instantiate Plot
fig = plt.figure(0)
fig.set_size_inches(4,3)
fig.clf()
ax = plt.gca()

# Set plot settings
color_mhd       = 'C0'
color_mpi       = 'C4'
color_grav      = 'C3'
color_particles = 'C2'
color_total     = 'w'
color_total_old = 'grey'
marker_size     = 4

def plot(scaling_data, name, color, label):
    x = scaling_data.loc['n_proc'].to_numpy()
    y = scaling_data.loc[name].to_numpy() / (scaling_data.loc['n_steps'].to_numpy() - 1)
    x.sort()
    y.sort()
    ax.plot(x, y, '--', c=color, alpha=0.8, marker='o', markersize=marker_size, label=label)

scaling_data = load_data()
plot(scaling_data, 'MHD', color_mhd, 'MHD')
plot(scaling_data, 'Boundaries', color_mpi, 'MPI Comm')
plot(scaling_data, 'Total', color_total, 'Total')

#2019 data for comparison
n_procs_128_2019 = np.array([8, 64, 512, 1024, 2048, 4096, 8192, 16384])
t_total_128_2019 = np.array([347.068, 386.369, 423.309, 439.147, 447.226, 458.162, 464.66, 481.458])
ax.plot( n_procs_128_2019, t_total_128_2019, '--', c=color_total_old, alpha=0.8, marker='o', markersize=marker_size)

font_size = 10
ax.text(0.05, 0.95, 'Total 2019', fontsize=font_size, color=color_total_old, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

ax.tick_params(axis='both', which='major', direction='in' )
ax.tick_params(axis='both', which='minor', direction='in' )

ax.set_xlim(1, 1E5)
ax.set_ylim(1E-2, 1E3)

ax.set_yscale('log')
ax.set_xscale('log')

ax.set_ylabel(r'Milliseconds / 256$^3$ Cells / GPU', fontsize=font_size)
ax.set_xlabel(r'Number of GPUs', fontsize=font_size)

ax.legend()

output_path = pathlib.Path(__file__).parent.resolve() / 'scaling_frontier_mhd.png'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
