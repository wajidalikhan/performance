#! /usr/bin/env python

from ModuleRunner import ModuleRunner

def commandline():
    import argparse
    parser = argparse.ArgumentParser(prog='steer.py')
    parser.add_argument('-c', '--config', default=False, action='store_true')
    parser.add_argument('-t', '--test',   default=False, action='store_true')
    parser.add_argument('-l', '--local',  default=False, action='store_true')
    parser.add_argument('-s', '--submit', default=False, action='store_true')
    parser.add_argument('-p', '--plot',   default=False, action='store_true')
    args = parser.parse_args()
    any_true = any(value for key, value in vars(args).items() if key != 'test' and key != 'config')
    if any_true:
        args.test = False
    return args

def main():

    years = ['2022']
    
    # runs = ['C','D']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} #default
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'} # shoulnd't work

    # runs = ['E','F','G']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} # shouldn't work
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'} # should be better

    # runs = ['C','D','E']
    # campaigns = {'mc': 'Summer22',   'data': 'ReReco'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} # shouldn't work
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'} # better

    # runs = ['F','G']
    # campaigns = {'mc': 'Summer22EE', 'data': 'Prompt'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} # shouldn't work
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'} # better
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Summer22EERun3_RunF_V0_DATA'} # best
    
    # runs = ['C']
    runs = ['D']
    # campaigns = {'mc': 'Summer22'}
    # campaigns = {'mc': 'Summer22_NPVA2p0B0p13'}
    # campaigns = {'mc': 'Summer22_NPVA2p0B0p3'}
    campaigns = {'mc': 'Summer22_NPVA3p0B0p13'}
    
    jecs = {'mc': 'Summer22EERun3_V0_MC'}

    extra_info = {'plot_level': 'partial'}


    # module = 'DY'
    module = 'QCD'
    
    # maxFiles=20
    maxFiles=1

    # extraName="test" # to be used to give extra name to the config and output folder
    args = commandline()
    print(args)

    MR = ModuleRunner(module=module, years=years, runs=runs, campaigns=campaigns, jecs=jecs, extra_info=extra_info)
    if args.config:
        MR.CreateConfigFiles()
    if args.test:
        MR.Test(maxFiles=maxFiles)
    if args.local:
        MR.RunLocal()
        # MR.RunLocal(distributed="parallel")
    if args.submit:
        MR.Submit()
    if args.plot:
        MR.Plot()



if __name__ == '__main__':
    main()


