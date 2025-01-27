## Exolaunch: houses all of our IO scripts,routines, etc. for performing Chroma measurements with distillation on the JURECA Cluster 

This document contains information regarding our computational workflow for the exotic hadrons project and instructions for use. 

## Summary of aims 
There is a sequential dependency chain when performing computations with `chroma`:

  1. Gauge generation (hmc) - Giovanni has taken care of this 
  ----------------------------------------------------------------------------------------------------
  2. Eigenvector generation (chroma single prec, laplace_eigs)
  3. Distillation objects (meson elementals, perambulators (strange and light)): chroma double prec
  -----------------------------------------------------------------------------------------------------
  4. Corr. func. generation is housed in `exotraction` repository
  5. Analysis

## Input file + SLURM script generation 

1. modify the yaml input file in `scripts/ens_files`. The defaults for our test ensemble are in the `scripts/ens_files/b3.70_ms0.000_mud-0.022_s32t96.yml` file. 
2. Generate the `.ini.xml` and batch scripts for the distillation/eigenbasis:
`./scripts/create-eigs.sh`. User is free to modify the CLI args (just run `python3 create_binned_tasks.py` to see the available options)
This will create an input xml and batch script for each configuration of interest in the directory `ini-eigs` or the provided directory of choice. 
3. In the parent dir, run `./launch_eigs.sh` 
4. Once the scripts are running and `eigs_{cfg#}.sdb` files are written out to $SCRATCH,
- copy eigensystem to $ARCH1 with `rsync --progress -avbh eigs_sdb/* TARGET_DIR`   
- Tar eigensystem to safe storage on cluster 
Now we can run the light and strange perambulators and meson elementals (in tandem, if so desired)
5. run ` python3 scripts/create_binned_tasks.py` to see the options. The default script is `./scripts/create-meson-peram-binned.sh` which calls the former. 
The binned batch scripts should now be written out in the proper dirs. 
6. run `./launch-binned.sh` in the parent dir. There are cli args to be passed 
7. After the runs are complete, run `python3 check-all-files.py -t all` to check existence of the sdb files 
8. to relaunch failed configurations, run `python3 rerun-failed-configs.py`   
 run `./create_distillation_tasks` with the necessary arguments. This will spit out input xml files for chroma tasks and SLURM batch scripts for each configuration for a given ensemble. 

Run `launch_{object}.sh`, where object can be ['eigs','perams','mesons','baryons'] We are currently running on the Jureca. The pipeline adheres to the following sequence. See the [[dependency graph]] for a visual representation: 

1. Generate distillation basis (eigensystem) -> `eigs_{cfg_id}.sdb' for a chosen distillation basis rank (we are using 300 numvecs at the moment)

There __should be__ an option in the master script to save/transfer/or delete the eigensystem sdb files after generation. Obviously, this would occur after the perambulators and elementals are generated. Eigensystems are expensive to store but easy to generate?

  
Take components of `chroma` output :
- quark lines 
- perambulators 
- random vectors 
- eigenvector space 
And implement the tensor contractions. Then we project out the correlators to the respective irreps we are interested in. 

There is no cpp source file that specifies how distillation is carried out in `chroma`. Rather, the means by which distilled objects are index and stored is not obvious, this is hidden within the `harom` external library. The nature of the problem is thus: we must "reverse engineer" the process to characterize the data structures for distilled propagators and the associated perambulators on each time slice. 

This is a recognized issue, according to https://github.com/eromero-vlc/chroma-challenges:

> Minimal support to introspect eigenvectors and distillation objects and check properties; which makes debugging and finding mistakes on the input files cumbersome





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
