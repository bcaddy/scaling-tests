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
                scaling_data[int(data[0])] = pd.to_numeric(data)
        else:
            print(f'File: {file_name} not found.')

    scaling_data = scaling_data.reindex(sorted(scaling_data.columns), axis=1)
    return scaling_data

def Scaling_Plot(scaling_data, y_title, filename, plot, old_data, old_label_position, xlims, ylims, skipped_fields=[]):
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
    alpha           = 0.9

    ax.set_alpha(alpha)

    if 'Total' not in skipped_fields:
        ax = plot(scaling_data, 'Total', color_total, 'Total', ax, alpha, marker_size)
    if 'MHD' not in skipped_fields:
        ax = plot(scaling_data, 'MHD', color_mhd, 'MHD', ax, alpha, marker_size)
    if 'MPI Comm' not in skipped_fields:
        ax = plot(scaling_data, 'Boundaries', color_mpi, 'MPI Comm', ax, alpha, marker_size)

    #2019 data for comparison
    n_procs_128_2019 = np.array([8, 64, 512, 1024, 2048, 4096, 8192, 16384])
    t_total_128_2019 = np.array([347.068, 386.369, 423.309, 439.147, 447.226, 458.162, 464.66, 481.458])
    if (old_data == 'rescale'):
        t_total_128_2019 = (256**3) / t_total_128_2019 * 1000
    ax.plot( n_procs_128_2019, t_total_128_2019, '--', c=color_total_old, alpha=alpha, marker='o', markersize=marker_size)

    font_size = 10
    ax.text(old_label_position[0], old_label_position[1],
            'Total Hydro 2019',
            fontsize=font_size,
            color=color_total_old,
            horizontalalignment='left',
            verticalalignment='center',
            transform=ax.transAxes)

    ax.tick_params(axis='both', which='major', direction='in' )
    ax.tick_params(axis='both', which='minor', direction='in' )

    ax.set_xlim(xlims[0], xlims[1])
    ax.set_ylim(ylims[0], ylims[1])

    ax.set_yscale('log')
    ax.set_xscale('log')

    fig.suptitle('MHD Weak Scaling on Frontier', fontsize=font_size, alpha=alpha)
    ax.set_ylabel(y_title, fontsize=font_size, alpha=alpha)
    ax.set_xlabel(r'Number of GPUs', fontsize=font_size, alpha=alpha)

    legend = ax.legend(fontsize=0.75*font_size, frameon=False)
    for t in legend.texts:
        t.set_alpha(alpha)

    output_path = pathlib.Path(__file__).parent.resolve() / filename
    fig.savefig(output_path, bbox_inches='tight', dpi=300)

def ms_per_256_per_gpu(scaling_data, name, color, label, ax, alpha, marker_size):
    x = scaling_data.loc['n_proc'].to_numpy()
    y = scaling_data.loc[name].to_numpy() / (scaling_data.loc['n_steps'].to_numpy() - 1)

    ax.plot(x, y, '--', c=color, alpha=alpha, marker='o', markersize=marker_size, label=label)

    return ax

def cells_per_second_per_gpu(scaling_data, name, color, label, ax, alpha, marker_size):
    x = (scaling_data.loc['n_proc'].to_numpy())

    cells_per_gpu = ( scaling_data.loc['nx'].to_numpy()
                    * scaling_data.loc['ny'].to_numpy()
                    * scaling_data.loc['nz'].to_numpy()) / x

    avg_time_step = scaling_data.loc[name].to_numpy() / (scaling_data.loc['n_steps'].to_numpy() - 1)
    avg_time_step /= 1000 # convert to seconds from ms

    y = cells_per_gpu / avg_time_step

    ax.plot(x, y, '--', c=color, alpha=alpha, marker='o', markersize=marker_size, label=label)

    return ax

def main():
    scaling_data = load_data()

    Scaling_Plot(scaling_data=scaling_data,
                 y_title=r'Milliseconds / 256$^3$ Cells / GPU',
                 filename='ms_per_gpu',
                 plot=ms_per_256_per_gpu,
                 old_data='keep',
                 old_label_position=[0.03, 0.96],
                 xlims=[0.7, 1E5],
                 ylims=[7E-3, 1E3])

    Scaling_Plot(scaling_data=scaling_data,
                 y_title=r'Cells / Second / GPU',
                 filename='cells_per_second',
                 plot=cells_per_second_per_gpu,
                 old_data='rescale',
                 old_label_position=[0.65, 0.20],
                 xlims=[0.7, 1E5],
                 ylims=[1E7, 1E9],
                 skipped_fields=['Total', 'MPI Comm'])

main()