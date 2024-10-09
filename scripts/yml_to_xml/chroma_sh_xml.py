'''generate xmls and spawn a chroma instance '''

import os 
from pydantic import BaseModel,Field
#coding: utf-8
from typing import Dict,Any,Optional
from decimal import Decimal
import re 

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
print(PROJECT_DIR)
# CONFS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', 'cfgs'))
FDIR = os.path.dirname(os.path.realpath(__file__))
INFILES = os.path.abspath(os.path.join(FDIR, "ens_files"))
TEMPLATE = os.path.join(FDIR,'templates')
OUTPATH = os.path.join(FDIR,'res/slurm_scripts')
# ENSEMBLES = 

# DATA = os.path.abspath(os.path.join(FDIR, os.pardir, "cfgs"))
# files = os.listdir(CONFS_PATH)
# for file in files:
#     data = [file.rstrip(".lime")]
#     print(data)

def parse_ensemble(short_tag: str) -> Dict[str, Any]:
    # see sim_params.png #
    long_tag = {
        "a125m280": "b3.30_ms-0.057_mud-0.129_s32t64-000-0001-0400",
        "test": "b3.70_ms0.000_mud-0.022_s32t96-000"
        # "a15m310L": "l2448f211b580m013m065m838",
        # "a12m310": "l2464f211b600m0102m0509m635",
        # "a09m310": "l3296f211b630m0074m037m440",
    }
    key = long_tag[short_tag]

    pattern = (
    r"b(?P<beta>[0-9]+\.[0-9]+)"
    r"_ms(?P<ms>[0-9]+\.[0-9]{3})"
    r"_mud-(?P<mud>[0-9]+\.[0-9]{3})"
    r"_s(?P<NL>[0-9]{2})"
    r"t(?P<NT>[0-9]{2})"
    r"-(?P<P>[0-9]{3})"
)
    type_map = {
        "beta": str,
        "NT": int,
        "NL":int,
        "P":str,
        "mud": str,
        "ms": str,
    }

    match = re.match(pattern, key)
    info = (
        {
            key: type_map[key](val)
            for key, val in match.groupdict().items()
            if key in type_map
        }
        if match
        else {}
    )
    return info
ens_props = parse_ensemble("test")
print(ens_props)

class ChromaOptions(BaseModel):
    '''
    load chroma run options from yaml file to pass to launcher shell script 
    last step in sequence prior to running chroma job on cluster
    '''
    user: str
    ens_short: str 
    P: int 
    cfg_i: int  #0001
    cfg_f: int #0400

    max_moms_per_job: int
    machine: str
    momentum_list: list

    mom2_min: int 
    mom2_max : int

    run_eigs: bool
    eigs_slurm_nodes : int
    eigs_chroma_geometry : list
    eigs_chroma_minutes : int
    eigs_transfer_back : bool
    eigs_delete_after_transfer_back : bool

    run_perams: bool
    prop_slurm_nodes: int
    prop_chroma_geometry: list
    prop_chroma_minutes: int 

    run_meson:bool
    meson_slurm_nodes: int
    meson_chroma_max_tslices_in_contraction: int
    meson_nvec: int
    meson_chroma_geometry: list
    meson_chroma_minutes: int
    meson_chroma_parts: int # split the time slices into this many different files

    run_baryon: bool
    baryon_slurm_nodes: int
    baryon_chroma_geometry: list
    baryon_chroma_minutes: int

    #slurm job options 
    run_path: str 
    # oldscratch_path: str
    num_vecs:int
    num_vecs_perams:int

    job_name: str 
    ranks_per_node: int
    nodes: int 
    num_gpu: int 
    account: str 
    proj_name: str 
    facility: str 
    filename_out: str 
    job_name: str 
    superbblas_threads: int 
    omp_threads: int
    #paths to dirs
    code_dir: str 
    base_dir: str 
    metaq_dir: str
    colorvec_out: str 