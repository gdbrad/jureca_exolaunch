## Exolaunch: houses all of our IO scripts,routines, etc. for performing Chroma measurements with distillation 

This document contains information regarding our computational workflow for the exotic hadrons project and instructions for use. 

## Summary of aims 
There is a sequential dependency chain when performing computations with `chroma`:

  1. Gauge generation (hmc) - Giovanni has taken care of this 
  2. Eigenvector generation (chroma single prec, laplace_eigs)
  3. Distillation objects (baryon, meson, props, genprops): chroma double prec, harom
  4. Corr. func. generation: redstar, colorvec, harom
  5. Analysis
  
Take components of `chroma` output :
- quark lines 
- perambulators 
- random vectors 
- eigenvector space 
And implement the tensor contractions. Then we project out the correlators to the respective irreps we are interested in. 

There is no cpp source file that specifies how distillation is carried out in `chroma`. Rather, the means by which distilled objects are index and stored is not obvious, this is hidden within the `harom` external library. The nature of the problem is thus: we must "reverse engineer" the process to characterize the data structures for distilled propagators and the associated perambulators on each time slice. 

This is a recognized issue, according to https://github.com/eromero-vlc/chroma-challenges:

> Minimal support to introspect eigenvectors and distillation objects and check properties; which makes debugging and finding mistakes on the input files cumbersome

### Input file + SLURM script generation 

First, run `./create_distillation_tasks` with the necessary arguments. This will spit out input xml files for chroma tasks and SLURM batch scripts for each configuration for a given ensemble. 

Run `launch_{object}.sh`, where object can be ['eigs','perams','mesons','baryons'] We are currently running on the Jureca. The pipeline adheres to the following sequence. See the [[dependency graph]] for a visual representation: 

1. Generate distillation basis (eigensystem) -> `eigs_{cfg_id}.sdb' for a chosen distillation basis rank (we are using 300 numvecs at the moment)

There __should be__ an option in the master script to save/transfer/or delete the eigensystem sdb files after generation. Obviously, this would occur after the perambulators and elementals are generated. Eigensystems are expensive to store but easy to generate?



2. copy eigensystem to $SCRATCH 
If saving eigensystem for reuse, 
3. Tar eigensystem to safe storage on cluster 
Else:
4. Generate perambulators using eigensystem
The perambulators are created by the gauge configuration and the distillation basis. These objects will then be tied together with meson elementals to form distilled meson interpolating operators. 
5. Delete eigensystem from run directory 
6. Copy perambulators to $SCRATCH 
At this point, a series of checks should be performed as surely everything did not proceed without flaw. This may include, but not limited to: 
- relaunch of troubled configurations with different solvers 
- file movement
-  

7. Compute $\dagger{V}V$ 
8. run contractions (Exotract)
9. Delete perambulators from SCRATCH 
10. Delete $\dagger{V}V$ from SCRATCH 
11. Copy contractions to run directory 
12. Run projections 
13. Delete contractions from run directory 


----------------------------------------------
# Exosuite documentation 

## Contractions 
TASKS: 
- modify current einsum contractions to use opt_einsum instead, can this talk with superbblas? 

We employ the `opt_einsum' python library to perform quark contractions -> meson-meson elementals. 

Here we describe the necessary ingredients:
### Gamma conventions
Nothing groundbreaking here, just defining various gamma conventions in order to create different mesons eg. pseudoscalars and scalars. 


## Study: Optimal rank of distillation basis
Armed with healthy looking 2pt correlators, we will perform a study to determine the optimal number of eigenvectors, or the rank of the distillation basis which will in turn generate our interpolating operators. We will perform benchmarking on 4 different sizes of the distillation basis, eg. the number of num_vecs used to calculate the perambulators and meson objects -> perambulators. We generated the eigenvector basis using 300 num_vecs which will be be truncated to the set ${32,64,96,128}$ for the elementals and perambulators. 
Namely, we want to study how the determination of the meson spectrum varies when the number of distillation vectors varies, along with the computational cost. 