import optparse
import ROOT

def SysChecker(sysname,cut,variable,proc,filepath):
    print filepath
    mytfile=ROOT.TFile.Open(filepath)
    nompath='/'.join([cut,variable,'histo_'+proc])
    print nompath
    hnom=mytfile.Get(nompath)
    uppath='/'.join([cut,variable,'histo_'+proc+'_'+sysname+'Up'])
    hup=mytfile.Get(uppath)
    downpath='/'.join([cut,variable,'histo_'+proc+'_'+sysname+'Down'])
    hdown=mytfile.Get(downpath)


    try:
        nom=hnom.Integral()
        up=hup.Integral()
        down=hdown.Integral()
    except:
        print "no histogram for->",nompath
        nom=0.
        up=0.
        down=0.
    if nom!=0:
        upvar=abs(nom-up)/nom
        downvar=abs(nom-down)/nom
    else:
        upvar=0.
        downvar=0.
    var=max(upvar,downvar)

    var100=var*100.


    return var,upvar,downvar



if __name__ == '__main__':
    
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-s","--sysname",   dest="sysname", help="Nuisancename")
    parser.add_option("-c","--cut",   dest="cut")
    parser.add_option("-v","--variable",   dest="variable")
    parser.add_option("-p","--proc",   dest="proc")
    parser.add_option("-f","--filepath",   dest="filepath")
    (options, args) = parser.parse_args()


    #options.want_remove
    sysname=options.sysname
    cut=options.cut
    variable=options.variable
    proc=options.proc
    filepath=options.filepath


    #mytfile=ROOT.TFile.Open(filepath)
    
    
    var,upvar,downvar=SysChecker(sysname,cut,variable,proc,filepath)
    print "-------------"
    print sysname
    if var>0.3:
        print "!!!!!!!!!!!too large!!!!!!!!!!!!!"
        print var,upvar,downvar
