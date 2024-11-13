#!/usr/bin/env bash


function move_files {
 for file in *.root; do
   echo "Moving $file to /afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/output/17/"
   mv $file /afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/output/17/
 done
}

bambooRun --module=/afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/modules/DYModule.py --distributed=worker --anaConfig=/afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/config/config_DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA.yml --plotIt plotIt --input=/afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/infiles/DY_in_17.txt --output=DY.root --tree=Events --sample=DY && move_files