from pydantic import BaseModel, Field
from typing import List
import numpy as np
def _gen_mom_list():
   momentum_list: List[str] = [
        "0 0 0", "1 0 0", "-1 0 0",
        "0 1 0", "0 -1 0", "0 0 1",
        "0 0 -1", "2 0 0", "-2 0 0",
        "0 2 0", "0 -2 0", "0 0 2",
        "0 0 -2", "3 0 0", "-3 0 0",
        "0 3 0", "0 -3 0", "0 0 3",
        "0 0 -3"
    ]
   return momentum_list


def  _displacement_list()->List[str]: 
    displacement_list= ['', '1', '2', '3', '1 1', '2 2', '3 3', '1 2', '1 3', '2 1', '2 3', '3 1', '3 2']
    return displacement_list
class Meson(BaseModel):
    '''Meson dataclass matching that of input yaml files 
    Output -> xml file 
    DISTILLATION BASIS GENERATION SHOULD ALWAYS BE RUN FIRST IN THE CHAIN!
    '''
    # universal imports for a given ensemble 
    num_vecs: int 
    NL: int
    NT: int
    Frequency: int
    t_start: int
    ens_short: str
    t_source_list: list #HARDCODED RIGHT NOW 0-64
    meson_nvec: int
    meson_zphases: list
    mom2_min: int 
    mom2_max : int
    momentum_list: List[str] = [
        "0 0 0", "1 0 0", "-1 0 0",
        "0 1 0", "0 -1 0", "0 0 1",
        "0 0 -1", "2 0 0", "-2 0 0",
        "0 2 0", "0 -2 0", "0 0 2",
        "0 0 -2", "3 0 0", "-3 0 0",
        "0 3 0", "0 -3 0", "0 0 3",
        "0 0 -3"
    ]
    displacement_list: List[str] = ['', '1', '2', '3', '1 1', '2 2', '3 3', '1 2', '1 3', '2 1', '2 3', '3 1', '3 2']

    meson_t_fwd: int
    meson_t_back: int 
    meson_chroma_max_tslices_in_contraction: int
    meson_nvec: int
    decay_dir: int 
    num_tries: int 
    max_rhs: int 
    phase: list 
    run_path:str
    #link smearing options 
    LinkSmearingType: str
    link_smear_fact: float
    link_smear_num: int
    no_smear_dir: int
    colorvec_out: str  


    # meson_path: str
    oldscratch_path: str
    cfg_path: str
    colorvec_file: str = 'res/eigs-64.sdb'
    # colorvec_out : str
    
t_source_list = np.array(range(64))
