
#    parser.add_option("-f","--filepath",   dest="filepath", help="histogram path")
#    parser.add_option("-l","--lumi",   dest="lumi", help="target lumi")
#    parser.add_option("-v","--vname",   dest="vname", help="variable name eg. Event")
#    parser.add_option("-p","--process",   dest="process", help="process name, eg. top")
#    parser.add_option("-r","--runmode",   dest="runmode", help="runmode")
#    parser.add_option("-c","--cutname",   dest="cutname", help="cutname")
#    parser.add_option("-x","--xsec",   dest="xsec", help="xsec")



##Boosted
python CheckEventEff.py -f "rootFile_2016_SigBkgEfficiency_Boosted_HMFull_V11_cprime1.0BRnew0.0_DeepAK8WP2p5_dMchi2Resolution_SR/hadd.root" -l 35.9 -v Event -p ggHWWlnuqq_M3000_S -r yield -c ___Boosted__SR__METOver40__PtOverM04______ -x "6.296492010211201e-06"
