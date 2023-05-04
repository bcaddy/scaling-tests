#!/usr/bin/env python3
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
plt.style.use('dark_background')


import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'




# Globals
filename = 'disk_scaling.log'
plot_grav_over_logN = False

combos = {}
combos['Hydro'] = ['Hydro','Calc_dt']
combos['MPI comm'] = ['Boundaries','Pot_Boundaries','Part_Boundaries','Part_Dens_Transf']
combos['Poisson'] = ['Grav_Potential']
combos['Particles'] = ['Part_Density','Advance_Part_1','Advance_Part_2']

def filename_to_table(filename):

    data = np.loadtxt(filename,skiprows=3,comments=['#'])
    with open(filename,'r') as ofile:
        lines = ofile.readlines()
        #print(lines)
        header = lines[3].split()
    table = {}
    for i in range(len(header)):
        table[header[i]] = data[:,i]

    print(table)
    return table

def access(table, item):
    # If item is a string, plot its average time
    if item in combos:
        total_time = 0
        for subitem in combos[item]:
            total_time += table[subitem]
    elif item in table:
        total_time = table[item]
    else:
        print('Error: missing key:', item)
        return
    x = table['#n_proc']
    y = total_time / table['n_steps']
    order = np.argsort(x)
    return x[order], y[order]





fig = plt.figure(0)
fig.set_size_inches(4,3)
fig.clf()
ax = plt.gca()

c_hydro = 'C0'
c_mpi = 'C4'
c_grav = 'C3'
c_particles = 'C2'
c_total = 'w'
c_total_old = 'grey'

ms = 4


frontier_table = filename_to_table(filename)

def plot(name, color):
    x, y = access(frontier_table,name)
    ax.plot(x, y, '--', c=color, alpha=0.8, marker='o', markersize=ms)



plot('Hydro', c_hydro)
plot('MPI comm', c_mpi)
plot('Poisson', c_grav)
plot('Particles', c_particles)
plot('Total', c_total)

#2019 data for comparison
n_procs_128_2019 = np.array([8, 64, 512, 1024, 2048, 4096, 8192, 16384])
t_total_128_2019 = np.array([347.068, 386.369, 423.309, 439.147, 447.226, 458.162, 464.66, 481.458])
ax.plot( n_procs_128_2019, t_total_128_2019, '--', c=c_total_old, alpha=0.8, marker='o', markersize=ms)



fs = 10
ax.text(0.85, 0.47, 'Hydro', fontsize=fs, color=c_hydro, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

ax.text(0.05, 0.4, 'MPI comm', fontsize=fs, color=c_mpi, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

ax.text(0.05, 0.16, 'Particles', fontsize=fs, color=c_particles, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)



if plot_grav_over_logN:
  ax.text(0.05, 0.37, 'Poisson / log(N)', fontsize=fs, color=c_grav, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
  ax.text(0.05, 0.72, 'Total 2023', fontsize=fs, color=c_total, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

else:
  ax.text(0.3, 0.62, 'Poisson', fontsize=fs, color=c_grav, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
  ax.text(0.05, 0.75, 'Total 2023', fontsize=fs, color=c_total, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

ax.text(0.05, 0.95, 'Total 2019', fontsize=fs, color=c_total_old, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)


ax.set_xlim(6, 100000)
ax.set_ylim(0.1, 1000)
ax.set_yscale('log')

ax.tick_params(axis='both', which='major', direction='in' )
ax.tick_params(axis='both', which='minor', direction='in' )


fs = 10
ax.set_ylabel( r'Milliseconds / 256$^3$ Cells / GPU', fontsize=fs)
ax.set_xlabel( r'Number of GPUs', fontsize=fs)
ax.set_xscale('log')

output_dir = './'



if plot_grav_over_logN: fileName = output_dir + 'scaling_frontier_adiabatic_2023_log_new_logN.png'
else: fileName = output_dir + 'scaling_frontier_adiabatic_2023_dark.png'
fig.savefig(  fileName ,  bbox_inches='tight', dpi=300)
