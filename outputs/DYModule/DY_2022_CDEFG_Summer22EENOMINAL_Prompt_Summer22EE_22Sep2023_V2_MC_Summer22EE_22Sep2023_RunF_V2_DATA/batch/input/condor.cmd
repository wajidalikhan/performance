universe = vanilla
getenv = True
+JobFlavour = "espresso"
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
success_exit_code = 0
max_retries = 0
arguments      = $(Process)
executable     = /afs/cern.ch/work/w/wajid/METStudies/JMEFrameWrk/jme-validation/outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/input/condor.sh
output         = outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/logs/condor_$(Process).out
error          = outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/logs/condor_$(Process).err
log            = outputs/DYModule/DY_2022_CDEFG_Summer22EENOMINAL_Prompt_Summer22EE_22Sep2023_V2_MC_Summer22EE_22Sep2023_RunF_V2_DATA/batch/logs/condor_$(Process).log
queue 674
