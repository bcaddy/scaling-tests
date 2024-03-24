#!/usr/bin/env bash

#SBATCH --job-name=cholla_mhd_strong_scaling      # Job name
#SBATCH --account=ast181
#SBATCH --nodes=1
#SBATCH --time=90
#SBATCH --mail-user=r.caddy@pitt.edu
#SBATCH --mail-type=ALL
#SBATCH --output=/ccs/home/rcaddy/ast181-orion/proj-shared/rcaddy/scaling-tests/data/2024-03-24-strong-scaling-456/slurm.out
#SBATCH --exclude=frontier00066,frontier00186,frontier00219,frontier00250,frontier00312,frontier00516,frontier00532,frontier00897,frontier00902,frontier00951,frontier04778,frontier05546,frontier05547,frontier05803,frontier05932,frontier06411,frontier06442,frontier06706

repo_path="/ccs/home/rcaddy/ast181-orion/proj-shared/rcaddy/scaling-tests"
root_path="${repo_path}/data/2024-03-24-strong-scaling-456"
cholla_path="${root_path}/cholla/bin/cholla.mhd.frontier"

cd "${root_path}"
source "${root_path}/cholla/builds/setup.frontier.cce.sh"


# Running biggest to smallest to (hopefully) save on queue times if one job fails

# 57^3 cells per GPU
# srun --exclusive --nodes=64 --ntasks=512 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_512_cholla.log" 2>&1
# srun --exclusive --nodes=32 --ntasks=256 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_256_cholla.log" 2>&1
# srun --exclusive --nodes=16 --ntasks=128 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_128_cholla.log" 2>&1
# 114^3 cells per GPU
# srun --exclusive --nodes=8 --ntasks=64 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_64_cholla.log" 2>&1
# srun --exclusive --nodes=4 --ntasks=32 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_32_cholla.log" 2>&1
# srun --exclusive --nodes=2 --ntasks=16 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_16_cholla.log" 2>&1
# 228^3 cells per GPU
srun --exclusive --nodes=1 --ntasks=8 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_8_cholla.log" 2>&1
srun --exclusive --nodes=1 --ntasks=4 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_4_cholla.log" 2>&1
srun --exclusive --nodes=1 --ntasks=2 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_2_cholla.log" 2>&1
# 456^3 cells per GPU
srun --exclusive --nodes=1 --ntasks=1 --cpus-per-task=7 --gpus-per-task=1 --gpu-bind=closest "${cholla_path}" "${repo_path}/slow_magnetosonic.txt" nx=456 ny=456 nz=456 xlen=1.0 ylen=1.0 zlen=1.0 wave_length=1.0 tout=2.0 outdir="${root_path}/ranks_XXX/" > "${root_path}/ranks_1_cholla.log" 2>&1


