#! /usr/bin/env python

from ModuleRunner import ModuleRunner
from printing_utils import green

def commandline():
    import argparse
    parser = argparse.ArgumentParser(prog='steer.py')
    parser.add_argument('-c', '--config',   default=False, action='store_true')
    parser.add_argument('-t', '--test',     default=False, action='store_true')
    parser.add_argument('-l', '--local',    default=False, action='store_true')
    parser.add_argument('-r', '--runlocal', default=False, action='store_true')
    parser.add_argument('-m', '--merge',    default=False, action='store_true')
    parser.add_argument('-s', '--submit',   default=False, action='store_true')
    parser.add_argument('-p', '--plot',     default=False, action='store_true')
    args = parser.parse_args()
    any_true = any(value for key, value in vars(args).items() if key != 'test' and key != 'config')
    if any_true:
        args.test = False
    return args

def main():
    extra_info = {}

    #### UL18 configs
    years = ['UL18']
    runs = ['D']
    campaigns = {'mc': 'Summer20UL'}
    jecs = {'mc': 'Summer19UL18_V5_MC', 'data': 'Summer19UL18_V5_DATA'}

    #### Run3 22 configs
    # years = ['2022']
    
    ###### prompt data taking
    # runs = ['C','D']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} #default

    # runs = ['E','F','G']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    # jecs = {'mc': 'Winter22Run3_V2_MC',   'data': 'Winter22Run3_RunD_V2_DATA'} # default
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'} # should be better

    #### -- new MC: Summer22
    # runs = ['F','G']
    # campaigns = {'mc': 'Summer22EE', 'data': 'Prompt'}
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Summer22EERun3_RunF_V0_DATA'} # default

    ###### Re-reco data taking
    # runs = ['C','D','E']
    # campaigns = {'mc': 'Summer22',   'data': 'ReReco'}
    # jecs = {'mc': 'Summer22EERun3_V0_MC', 'data': 'Winter22Run3_RunF_V0_DATA'}


    # all jecs: "default" ; User MC truth: ['L2Relative']
    jec_level ='default'
    # jec_level = ['L2Relative']

    # possible plot_level: 'all', 'rawresponse', 'response', 'default'
    extra_info = {'plot_level': 'rawresponse'}


    # module = 'DY'
    module = 'QCD'
    # module = 'test'

    # maxFiles=10
    maxFiles=1

    # extraName="test" # to be used to give extra name to the config and output folder
    args = commandline()
    print(green(args))

    MR = ModuleRunner(module=module, years=years, runs=runs, campaigns=campaigns, jecs=jecs, extra_info=extra_info, jec_level = jec_level)
    if args.config:
        MR.CreateConfigFiles()
    if args.test:
        
        MR.Test(maxFiles=maxFiles, extra_flags='--onlypost')
    if args.local:
        MR.RunLocal()
        # MR.RunLocal(distributed="parallel")
    if args.submit:
        MR.Submit()
    if args.runlocal:
        MR.RunMissingLocal()
    if args.merge:
        MR.Merge()
    if args.plot:
        MR.Plot()



if __name__ == '__main__':
    main()


