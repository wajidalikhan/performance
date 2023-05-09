#! /usr/bin/env python

from ModuleRunner import ModuleRunner

def main():

    years = ['2022']
    
    runs = ['C','D']
    campaigns = {'mc': 'Winter22',   'data': 'Prompt'}
    
    # runs = ['E','F','G']
    # campaigns = {'mc': 'Winter22',   'data': 'Prompt'}

    # runs = ['C','D','E']
    # campaigns = {'mc': 'Summer22',   'data': 'ReReco'}

    # runs = ['F','G']
    # campaigns = {'mc': 'Summer22EE', 'data': 'Prompt'}
    
    module = 'DY'
    module = 'QCD'
    
    # maxFiles=10
    maxFiles=1
    
    MR = ModuleRunner(module=module, years=years, runs=runs, campaigns=campaigns)
    MR.CreateConfigFiles()

    MR.Test(maxFiles=maxFiles)
    # MR.RunLocal()
    # MR.Submit()



if __name__ == '__main__':
    print('Start main')
    main()


