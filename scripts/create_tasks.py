
import argparse
import os
import jinja2
import yaml
from yml_to_xml import eigs_xml, perams_xml, meson_xml, chroma_sh_xml, disco_xml

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FDIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(FDIR, 'templates')
RESULTPATH = os.path.join(FDIR, 'res')
OUTPATH = os.path.join(RESULTPATH, 'out')
LOGPATH = os.path.join(RESULTPATH, 'log')

class TaskHandler:
    def __init__(self, env):
        self.templates = {
            'eigs': env.get_template('eigs.jinja.xml'),
            'peram_clover': env.get_template('peram_clover.jinja.xml'),
            'peram_charm_clover': env.get_template('peram_charm_clover.jinja.xml'),
            'peram_mg': env.get_template('peram_multigrid.jinja.xml'),
            'peram_strange_mg': env.get_template('peram_strange_multigrid.jinja.xml'),
            'peram_charm_mg': env.get_template('peram_charm_multigrid.jinja.xml'),
            'peram': env.get_template('peram_multigrid.jinja.xml'),
            'meson': env.get_template('meson.jinja.xml'),
            'disco': env.get_template('disco.jinja.xml'),

            'chroma_eigs': env.get_template('eigs_binned.sh.j2'),
            'chroma_peram': env.get_template('peram_juwels.sh.j2'),
            'chroma_peram_mg': env.get_template('peram_juwels.sh.j2'),
            'chroma_peram_charm_mg': env.get_template('peram_charm_mg.sh.j2'),
            'chroma_peram_clover': env.get_template('peram_clover.sh.j2'),
            'chroma_peram_charm_clover': env.get_template('peram_charm_clover.sh.j2'),
            'chroma_meson': env.get_template('meson_jureca.sh.j2'),
            'chroma_disco': env.get_template('disco.sh.j2')
        }
        self.xml_classes = {
            'eigs': eigs_xml.Eigs,
            'peram_mg': perams_xml.Perams,
            'peram_strange_mg': perams_xml.Perams,
            'peram_charm_mg': perams_xml.Perams,
            'peram_clover': perams_xml.Perams,
            'peram_charm_clover': perams_xml.Perams,
            'meson': meson_xml.Meson,
            'disco': disco_xml.Disco,
            'chroma_eigs': chroma_sh_xml.ChromaOptions,
            'chroma_meson': chroma_sh_xml.ChromaOptions,
            'chroma_peram_mg': chroma_sh_xml.ChromaOptions,
            'chroma_peram_charm_mg': chroma_sh_xml.ChromaOptions,
            'chroma_peram_clover': chroma_sh_xml.ChromaOptions,
            'chroma_peram_charm_clover': chroma_sh_xml.ChromaOptions,
            'chroma_disco': chroma_sh_xml.ChromaOptions,


        }

def main(options):
    with open(os.path.join(options.in_file)) as f:
        dataMap = yaml.safe_load(f)
    missing_values = [key for key in ['run_path', 'cfg_path'] if key not in dataMap]

    if missing_values:
        for key in missing_values:
            value = input(f"you forgot to include '{key}' in your infile dummy!: ")
            dataMap[key] = value

        # Rewrite the YAML file with added values
        with open(options.in_file, 'w') as f:
            yaml.safe_dump(dataMap, f)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE), undefined=jinja2.StrictUndefined)
    handler = TaskHandler(env)
    run_objects = []
    for task in options.list_tasks:
        if 'eigs' in task:
            run_objects.append('eigs')
            run_objects.append('chroma_eigs')
        if 'peram_mg' in task:
            run_objects.append('peram_mg')
            run_objects.append('chroma_peram_mg')
        if 'peram_strange_mg' in task:
            run_objects.append('peram_strange_mg')
            run_objects.append('chroma_peram_mg')
        if 'peram_charm_mg' in task:
            run_objects.append('peram_charm_mg')
            run_objects.append('chroma_peram_charm_mg')
        if 'peram_clover' in task:
            run_objects.append('peram_clover')
            run_objects.append('chroma_peram_clover')
        if 'peram_charm_clover' in task:
            run_objects.append('peram_charm_clover')
            run_objects.append('chroma_peram_charm_clover')
        if 'peram' in task:
            run_objects.append('peram')
            run_objects.append('chroma_peram')
        if 'meson' in task:
            run_objects.append('meson')
            run_objects.append('chroma_meson')
        if 'disco' in task: 
            run_objects.append('disco')
            run_objects.append('chroma_disco')

    # tsrc_values = generate_time_sources(options.tsrc_values)

    for cfg_id in range(options.cfg_i, options.cfg_f, options.cfg_step):
        print('Creating scripts for configuration', cfg_id)
        for flavor, beta, quarktype in [('light', 0.022, 'ud'), ('strange', 0.000, 's')]:
            cfg_dir = os.path.realpath(os.path.join('..', options.ini_path, f'cnfg{cfg_id:02d}'))
            rundir = os.path.join(options.run_dir, cfg_dir)
            outfile = f'../outputs/run_{cfg_id:02d}.out'

            for obj in run_objects:
                obj_dir = os.path.join(cfg_dir)
                os.makedirs(obj_dir, exist_ok=True)
                if options.num_vecs:
                    for nvec in options.num_vecs:
                        nvec_dir = os.path.join(obj_dir, f'numvec{nvec}')
                        os.makedirs(nvec_dir, exist_ok=True)

                        if obj in ['chroma_eigs','chroma_disco']:
                            ini_out = f'{obj.split("_")[1]}_cfg{cfg_id:02d}.sh'
                        elif obj!= 'chroma_eigs' and obj.startswith('chroma'):
                            ini_out = f'{obj.split("_")[1]}_{nvec}_cfg{cfg_id:02d}.sh'
                        elif obj in ['disco','eigs']:
                            ini_out = f'{obj}_cfg{cfg_id:02d}.ini.xml'
                        else:
                            ini_out = f'{obj}_{nvec}_cfg{cfg_id:02d}.ini.xml'
                        #eigs_disco = ['eigs','disco']

                        if obj.__contains__('eigs|disco'):
                            ini_out_path = os.path.join(obj_dir, ini_out)
                        else:
                            ini_out_path = os.path.join(nvec_dir, ini_out)

                        with open(options.in_file) as f:
                            dataMap = yaml.safe_load(f)
                # else:

                        if obj in options.list_tasks:
                            base = handler.xml_classes[obj]
                            # if dataMap['facility'] in ['jureca', 'juwels']:
                            #     expected_keys = base.__fields__.keys()
                            # else:
                            expected_keys = base.model_fields.keys()
                            filtered_data = {k: v for k, v in dataMap.items() if k in expected_keys}
                            filtered_data['cfg_id'] = f'{cfg_id:02d}'
                            moms = meson_xml._gen_mom_list()
                            disp = meson_xml._displacement_list()
                            disco_disp = disco_xml._displacement_list()
                            filtered_data['momentum_list'] = moms
                            filtered_data['displacement_list'] = disp
                            filtered_data['disco_displacement_list'] = disco_disp

                            filtered_data['disco_t_sources'] = disco_disp
                            filtered_data['tsrc'] = 24
                            # filtered_data['t_sources'] = " ".join(map(str, tsrc_values))
                            # default value in yml file is overridden by the nvec loop for nvec study
                            filtered_data['num_vecs_perams'] = nvec
                            filtered_data['meson_nvec'] = nvec
                            ens_props = chroma_sh_xml.parse_ensemble(short_tag=filtered_data['ens_short'])
                            filtered_data.update(ens_props)
                            output_xml = handler.templates[obj].render(filtered_data)
                            
                            # Debugging info
                            print(f"Writing file {ini_out_path} for object {obj}")
                            
                            with open(ini_out_path, 'w') as f:
                                f.write(output_xml)
    os.makedirs(LOGPATH, exist_ok=True)
    os.makedirs(OUTPATH, exist_ok=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', type=str, required=True)
    parser.add_argument('--cfg_i', type=int, required=True)
    parser.add_argument('--cfg_f', type=int, required=True)
    parser.add_argument('--cfg_step', type=int, nargs='?', default=10, help='default: %(default)s')
    parser.add_argument('--ini-path', type=str, required=True)
    parser.add_argument('-l', '--list_tasks', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-nv', '--num_vecs', nargs='+', help='<Optional> vary nvecs for perams and mesons, must match', required=False, type=int)
    parser.add_argument('--overwrite', type=bool, nargs='?', default=False, help='if true, overwrite existing xml and sh scripts for chroma task of interest')
    parser.add_argument('--cfg_path', default='/p/project1/exotichadrons/pederiva/6stout/beta_3.70/ms_0.000/mud_-0.022/s32t96/cnfg/', help='default: %(default)s')
    parser.add_argument('--run_dir', default='', help='default: %(default)s')
    parser.add_argument('--test', action='store_true', help='if true, run in test mode')
    options = parser.parse_args()

    main(options)
