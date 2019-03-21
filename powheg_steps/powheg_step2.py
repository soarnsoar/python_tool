import os
#instruction
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/PowhegBOXPrecompiled#Step_1_Compiling_the_POWHEG_sour
#processname
#http://cms-project-generators.web.cern.ch/cms-project-generators/slc6_amd64_gcc481/powheg/V2.0/src/processes_rev3429_date20170726.txt

# Definition of the input parameters:
#  (1) -p grid production stage [0]  (compiling source)
#  (2) -i intput card name [powheg.input]
#  (3) -m process name (process defined in POWHEG)
#  (4) -f working folder [my_ggH]
#  (5) -q  job flavor / batch queue name (run locally if not specified)

#step1
#    python ./run_pwg_condor.py -p 0 -i gg_H/gg_H_quark-mass-effects_NNPDF30_13TeV.input -m gg_H_quark-mass-effects -f my_ggH

#step2
#    ON HTCondor:             python ./run_pwg_condor.py -p 123 -i gg_H/gg_H_quark-mass-effects_NNPDF30_13TeV.input -m gg_H_quark-mass-effects -f my_ggH -q workday -n 1000



### input : production/2017/13TeV/Higgs/gg_H_WW_quark-mass-effects_NNPDF31_13TeV/gg_H_WW_quark-mass-effects_NNPDF31_13TeV_M5000.input
name='gg_H_WW_quark-mass-effects_NNPDF31_13TeV_M5000'
processname='gg_H_quark-mass-effects'
powheg_input='production/2017/13TeV/Higgs/gg_H_WW_quark-mass-effects_NNPDF31_13TeV/gg_H_WW_quark-mass-effects_NNPDF31_13TeV_M5000.input'
cmd='python ./run_pwg_condor.py -p 123 -i '+powheg_input+' -m '+processname+' -f workdir_'+name+' -n 50'

os.system(cmd)
