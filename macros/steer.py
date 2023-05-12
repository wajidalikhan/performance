#! /usr/bin/env python

from ModuleRunner import ModuleRunner

def main():

    years = ['2022']
    
    runs = ['C','D']
    campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    jecs = {'mc': 'Winter22Run3_RunF_V0_DATA',   'data': 'Summer22EERun3_V0_MC'}
    # jecs = {'mc': '',   'data': ''}
    
    # runs = ['E','F','G']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}

    # runs = ['C','D','E']
    # campaigns = {'mc': 'Summer22',   'data': 'ReReco'}

    # runs = ['F','G']
    # campaigns = {'mc': 'Summer22EE', 'data': 'Prompt'}
    
    # module = 'DY'
    module = 'QCD'
    
    # maxFiles=10
    maxFiles=1

    # extraName="test" # to be used to give extra name to the config and output folder
    
    MR = ModuleRunner(module=module, years=years, runs=runs, campaigns=campaigns, jecs=jecs)
    MR.CreateConfigFiles()

    MR.Test(maxFiles=maxFiles)
    # MR.RunLocal()
    # MR.Submit()
    # MR.Plot()



if __name__ == '__main__':
    print('Start main')
    main()


