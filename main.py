from auto_sed import *
from ryder_graphing import *

pcipath = 'pcigale.ini'
obs_file = 'observations.txt'
cores = '6'

def parse_one(filename):

    # parse file
    header = get_header_lines(filename)
    config = read_simple_ini(filename)

    # set round 1 params for ini generation
    config['data_file'] = obs_file
    config['parameters_file'] = ''
    config['sed_modules'] = 'sfhdelayed, bc03, nebular, dustatt_modified_starburst, dale2014, redshifting'
    config['analysis_method'] = 'pdf_analysis'
    config['cores'] = cores

    # write back to file
    write_simple_ini(filename, config, header_lines=header)

    print(f"Modified {filename}")
    print(f"Parse 1 Complete")

# insert desired modifications to pcigale.ini here
def round_one(filename):
    replacement_values = {
        # [[sfh2exp]]
        "tau_main": "100, 300, 1000, 3000",
        "tau_burst": "10, 30, 100, 300",
        "f_burst": "0.01",
        "age": "100, 300, 1000",
        "burst_age": "10, 30, 50",

        # [[bc03]]
        "imf": "0",
        "metallicity": "0.02",
        "separation_age": "10",

        # sed_modules_params.redshifting -- NEEDS DOUBLE QUOTES
        "redshift": '"eval np.arange(0.8, 10, 0.1)"',

    }

    # evaluate by replacing in file, i don't understand this function, evil regex func
    replace_ini_values(filename, replacement_values)

    print(f"Modified {filename}")
    print(f"Round 1 Complete")

def parse_two(filename):
    # parse file
    header = get_header_lines(filename)
    config = read_simple_ini(filename)

    # set round 1 params for ini generation
    config['data_file'] = obs_file
    config['parameters_file'] = ''
    config['sed_modules'] = 'sfh2exp, bc03, nebular, dustatt_modified_starburst, dale2014, redshifting'
    config['analysis_method'] = 'pdf_analysis'
    config['cores'] = cores

    # write back to file
    write_simple_ini(filename, config, header_lines=header)

    print(f"Modified {filename}")
    print(f"Parse 2 Complete")

def round_two(filename):
    replacement_values = {
        # sed_modules_params.sf2exp
        "tau_main": "100, 300, 1000, 3000",
        "tau_burst": "10, 30, 100, 300",
        "f_burst": "0.01",
        "age": "100, 300, 1000",
        "burst_age": "10, 30, 50",

        # sed_modules_params.bc03
        "imf": "0",
        "metallicity": "0.02",
        "separation_age": "10",

        # sed_modules_params.redshifting -- NEEDS DOUBLE QUOTES
        "redshift": '"eval np.arange(0.8, 10, 0.1)"',

    }

    replace_ini_values(filename, replacement_values)

    print(f"Modified {filename}")
    print(f"Round 2 Complete")

def parse_three(filename):
    # parse file
    header = get_header_lines(filename)
    config = read_simple_ini(filename)

    # set round 1 params for ini generation
    config['data_file'] = obs_file
    config['parameters_file'] = ''
    config['sed_modules'] = 'sfhdelayedbq, bc03, nebular, dustatt_modified_starburst, dale2014, redshifting'
    config['analysis_method'] = 'pdf_analysis'
    config['cores'] = cores

    # write back to file
    write_simple_ini(filename, config, header_lines=header)

    print(f"Modified {filename}")
    print(f"Parse 3 Complete")

def round_three(filename):
    replacement_values = {
        # [[sfhdelayedbq]]
        "tau_main": "100, 300, 1000, 3000",
        "age_main": "100, 300, 1000",
        "age_bq": "10, 30, 100",
        "r_sfr": "100",
        "sfr_A": "1.0",
        "normalise": "True",

        # [[bc03]]
        "imf": "0",
        "metallicity": "0.02",
        "separation_age": "10",

        # [[nebular]]
        "logU": "-2.0",
        "zgas": "0.02",
        "ne": "100",
        "f_esc": "0.0",
        "f_dust": "0.0",
        "lines_width": "300.0",
        "emission": "True",

        # [[dustatt_modified_starburst]]
        "E_BV_lines": "0.3",
        "E_BV_factor": "0.44",
        "uv_bump_wavelength": "217.5",
        "uv_bump_width": "35.0",
        "uv_bump_amplitude": "0.0",
        "powerlaw_slope": "0.0",
        "Ext_law_emission_lines": "1",
        "Rv": "3.1",
        "filters": "B_B90 & V_B90 & FUV",

        # [[redshifting]]
        "redshift": '"eval np.arange(0.8, 10, 0.1)"',
    }

    replace_ini_values(filename, replacement_values)

    print(f"Modified {filename}")
    print("Round 3 Complete")

def main():

    # block one - sfhdelayed
    run_command('pcigale init')
    # generated sfhdelayed ini
    parse_one(pcipath)
    run_command('pcigale genconf')
    # populating variables
    round_one(pcipath)
    # executing .ini
    run_command('pcigale run')

    #reset
    run_command(f'rm -f {pcipath}')
    run_command(f'rm -f {pcipath}.spec')


    # block two - sfh2exp
    run_command('pcigale init')
    # generate sfh2exp ini
    parse_two(pcipath)
    run_command('pcigale genconf')
    # populating variables
    round_two(pcipath)
    # executing .ini
    run_command('pcigale run')

    # reset
    run_command(f'rm -f {pcipath}')
    run_command(f'rm -f {pcipath}.spec')

    # block three - sfhdelayedbq
    run_command('pcigale init')
    # generated sfhdelayed ini
    parse_three(pcipath)
    run_command('pcigale genconf')
    # populating variables
    round_three(pcipath)
    # executing .ini
    run_command('pcigale run')

    # reset
    run_command(f'rm -f {pcipath}')
    run_command(f'rm -f {pcipath}.spec')

    corner_plot()

    print('heck yeah')

if __name__ == "__main__":
    main()
