import os 
from pydantic import BaseModel
import numpy as np

class Perams(BaseModel):
    '''Perambulators dataclass matching that of input yaml files 
    Output -> xml file 
    DISTILLATION BASIS GENERATION SHOULD ALWAYS BE RUN FIRST IN THE CHAIN
    peram_inv.jinja.xml has no free variables, these are the clover inverter params. TODO make these free if need be 
    peram_prop.jinja.xml also has no free variables 
    peram_template.jinja.xml haas free vars -> the base peram.jinja.xml template 

    '''
    # universal imports for a given ensemble 
    num_vecs: int 
    num_vecs_perams: int
    ens_short: str
    colorvec_out: str 
    cfg_name: str 

    # t_source_list: list HARDCODED RIGHT NOW 0-64
    Nt_forward: int
    Nt_backward: int 
    decay_dir: int 
    num_tries: int 
    max_rhs: int 
    phase: list 
    prop_t_sources: str
    prop_t_fwd: int
    prop_t_back: int
    prop_nvec: int
    prop_zphases: float
    prop_mass: str
    prop_clov_coeff: str
    prop_mass_label: str
    prop_mass_light_label: str
    prop_mass_strange_label: str
    prop_mass_charm_label: str


    rho: str
    precision: str
    max_iter: int

    #link smearing options 
    LinkSmearingType: str
    link_smear_fact: float
    link_smear_num: int
    no_smear_dir: int

    # perams_path: str
    cfg_path: str
    run_path:str
    oldscratch_path: str
    # colorvec_out : str
    
t_source_list = np.array(range(64))
