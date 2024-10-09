from pydantic import BaseModel,Field
from typing import List 
from typing import Dict,Any,Optional
from decimal import Decimal


class Eigs(BaseModel):
    '''Distillation basis dataclass matching that of input yaml files 
    Output -> xml file 
    DISTILLATION BASIS GENERATION SHOULD ALWAYS BE RUN FIRST IN THE CHAIN
    THERE SHOULD ONLY BE A SINGLE DISTILLATION BASIS FOR EACH ENSEMBLE TODO WHY 
    
    '''
    colorvec_out: str
    cfg_path: str
    run_path:str
    ens_short: str 
    P: int 
    beta: Decimal = Field(max_digits=5, decimal_places=2)
    ms: Decimal = Field(max_digits=5, decimal_places=3)
    mud: Decimal= Field(max_digits=5, decimal_places=3)
    # beta: Annotated[Decimal, Field(default=None,ge=0, decimal_places=3)] | None
    # ms: Annotated[Decimal,  Field(default=None,ge=0, decimal_places=3)] | None
    # mud: Annotated[Decimal,  Field(default=None,ge=0, decimal_places=3)] | None
    Frequency: int
    max_nvec: int # colorvecs to compute
    num_vecs: int # colorvecs to use
    decay_dir: int
    num_iter: int
    num_orthog: int
    t_start: int
    Nt_forward: int
    phase: list
    write_fingerprint: bool
    NL: int
    NT: int
    cfg_i: int 
    cfg_f: int 
    cfg_d: int 
    cfg_range: List[int] =None
    #link smearing options 
    LinkSmearingType: str
    link_smear_fact: float
    link_smear_num: int
    no_smear_dir: int

    cfg_path: str
    colorvec_out : str
    def __post_init__(self):
        self.cfg_range = list(range(self.cfg_i, self.cfg_f, self.cfg_d))

    @property
    def colorvec_file(self):
        return f"res/eigs-{self.num_vecs}.sdb"
