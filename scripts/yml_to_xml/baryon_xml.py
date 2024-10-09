from pydantic import BaseModel
from typing import List
import numpy as np

class Baryon(BaseModel):
    '''baryon dataclass matching that of input yaml files 
    Output -> xml file 
    DISTILLATION BASIS GENERATION SHOULD ALWAYS BE RUN FIRST IN THE CHAIN!
    '''
    # universal imports for a given ensemble 
    num_vecs: int 
    NL: int
    NT: int
    Frequency: int
    t_start: int 
    baryon_zphases: int

    # t_source_list: list HARDCODED RIGHT NOW 0-64
    mom2_min: int 
    mom2_max : int
    momentum_list: List[str] = [
    f"{x} {y} {z}" for x, y, z in [
        (0, 0, 0), (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0), (0, 0, 1),
        (0, 0, -1), (2, 0, 0), (-2, 0, 0),
        (0, 2, 0), (0, -2, 0), (0, 0, 2),
        (0, 0, -2), (3, 0, 0), (-3, 0, 0),
        (0, 3, 0), (0, -3, 0), (0, 0, 3),
        (0, 0, -3)
    ]
]
    displacement_list: List[str] = ['', '000', '001', '002', '003', '0011', '0012', '0013', '0021', '0022', '0023', '0031', '0032','0033','011','012','013','022','023','033']

    Nt_forward: int
    Nt_backward: int 
    decay_dir: int 
    num_tries: int 
    max_rhs: int 
    phase: list 
    #link smearing options 
    LinkSmearingType: str
    link_smear_fact: float
    link_smear_num: int
    no_smear_dir: int

    baryon_chroma_max_tslices_in_contraction: int #large as possible  
    baryon_chroma_max_moms_in_contraction: int #(0 == do all momenta at once)
    baryon_chroma_max_vecs: int #
    cfg_path: str
    colorvec_file: str = 'res/eigs-64.sdb'
    
t_source_list = np.array(range(64))