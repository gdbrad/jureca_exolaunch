''''Engine for exolaunch. One must provide a yml input file(for each ensemble) to the engine in order for the correct schemas and corresponding actions to be executed

0. get correct ens input file from cli 
    - fill templates with ens info 

1. Create nested dir structure for each ensemble 
    - create naming convention 
        - if dir exists, check the naming to ensure ubiquity 
    - if already exists, ensure structure integrity 
        - if not, create it 
2. Chroma XML input file generation 
    - check XML naming scheme 
        - modify if errors present 
    - ensure XML file exists for every configuration 
    
   
'''
import argparse
import collections 
import itertools
import re 
import os
import glob
import sys 
import subprocess
from doit import get_var,create_after

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
ens_props = parse_ensemble(args.ens)
print(ens_props)

'''Schemas below
    1. makes sense to first get an inventory of existing files for a given configuration with file sizes, date of creation  
    - clean
    - create 
    - rename
    - launch
    
    '''
regex_cfg = r'_cfg_(\d+)\.lime|conf\.(\d+)'
regex_stout = r'stout.config-(\d+)\.lime|conf\.(\d+)'
regex_eigenvectors = r'eigenvectors.(\d+).095'
regex_phases = r'phases.(\d+).095'

Ensemble = collections.namedtuple('Ensemble', ('name', 'gauges', 'stout', 'eigenvalues', 'perambulators','elementals'))

def inventory():
    '''get inventory of existing files for a given configuration:
        - ini files
        - sh scripts 
        - eigs sdb 
        - peram sdb
        - meson sdb '''
    

    return ensemble

def check_sdb(nvecs:list,objects=None):
    if objects is None:
        # subprocess


    
def launch_sh():

    pass 

def launch_h5():
    pass 

def remove_bad_sdb():

def remove_bad_h5():
    

def relaunch():
    pass 


def create(type:str,ens_file:str):
    create_cmd= "python3 scripts/create_tasks.py --in_file 'ens_files/b3.70_ms0.000_mud-0.022_s32t96.yml' --cfg_i 11 --cfg_f 1991 --cfg_step 10 --run_dir 'res' --overwrite --list_tasks meson chroma_meson --num_vecs 32 64 96 128
    subprocess.check_call(["./scripts/script.ksh", arg1, arg2, arg3], shell=True)

def clean_sdb(type:str,base_dir;str,nvecs:int):


    pass

def clean_h5(type,base_dir):
    return 

def clean_ini(type, base_dir):
    '''
    will execute a command of the following form:
        `clean({type},{base_dir}`
    '''
    if type not in ['eigs', 'peram','peramclov','meson']:
        print("Invalid file type. Please specify 'eigs' 'perams' or 'meson'.")
        return

    cfg_dirs = glob.glob(os.path.join(base_dir, 'cnfg*'))
    for cfg_dir in cfg_dirs:
        nvec_dirs = glob.glob(os.path.join(cfg_dir,'numvec*'))

        for nvec_dir in nvec_dirs:
            xml_pattern = os.path.join(nvec_dir, f'{type}_*.ini.xml')
            sh_pattern = os.path.join(nvec_dir, f'{type}_*.sh')

            xml_files = glob.glob(xml_pattern)
            for xml_file in xml_files:
                try:
                    os.remove(xml_file)
                    print(f'Removed {xml_file}')
                except OSError as e:
                    print(f'Error removing {xml_file}: {e}')

            sh_files = glob.glob(sh_pattern)
            for sh_file in sh_files:
                try:
                    os.remove(sh_file)
                    print(f'Removed {sh_file}')
                except OSError as e:
                    print(f'Error removing {sh_file}: {e}')


def process_args():
    parser = argparse.ArgumentParser(description='Clean XML and shell script files from configuration directories.')
    parser.add_argument('ens',type=str, help="select ensemble short name")
    parser.add_argument('schema',type=str,help="select schema to execute eg. clean,create,rename,launch")
    parser.add_argument('file_type', type=str, help="Type of files to remove ('eigs' 'perams' 'meson')")
    parser.add_argument('--base_dir', type=str, default='.', help='Base directory containing the configuration directories (default: current directory)')

    args = parser.parse_args()

    clean_files(args.file_type, args.base_dir)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == '--test':
        do_test()
    else:
        process_args()