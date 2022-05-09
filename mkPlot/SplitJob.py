###----
import os
import sys
sys.path.append('python_tool/')
from ExportShellCondorSetup import Export
import glob
import optparse

class splitter:
    def __init__(self,cutspy,nuisancepy,samples,inputs):
        ##
        self.cutspy=cutspy
        self.nuisancepy=nuisancepy
        if self.nuisancepy:
            self.nuisanceopt="--nuisancesFile="+self.nuisancepy
        else:
            self.nuisanceopt=''
        self.inputs=inputs
        if len(self.inputs.split(','))>1:self.multiopt="--isMultiInputs"

        samples=self.samples
        if self.samples:
            self.samplesopt="--samplesFile="+self.sample
        else:
            self.samplesopt="--samplesFile=samples_'+self.Year+'_dummy.py"
        self.cutfiles=[]
        self.ReadCuts()
    def ReadCuts(self):
        print self.cutspy
        exec(open(self.cutspy))
        #for cut in cuts:
        #    print cut
        self.cuts=cuts
        self.Year=Year
        
    def Split(self):
        os.system('mkdir -p split_plots/')
        f=open(self.cutspy,'r')
        lines=f.readlines()
        for cut in self.cuts:

            newpath='split_plots/'+self.cutspy+'__'+cut+'.py'
            self.cutfiles.append(newpath)
            print newpath
            fnew=open(newpath,'w')
            
            for line in lines:
                fnew.write(line)
            fnew.write('cuts={}\n')
            fnew.write('cuts["'+cut+'"]="'+self.cuts[cut]+'"')
            fnew.close()
    def Submit(self):
        #def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):
        for cutfile in self.cutfiles:
            if 'Boosted' in cutfile:
                bst='Boosted'
            else:
                bst='Resolved'

            ##--1) nominal
            WORKDIR="WORKDIR_MKPLOT/"+cutfile+'/nom/'
            commandlist=[]
            commandlist.append('cd '+os.getcwd())
            if self.inputs:
                commandlist.append('input='+self.inputs)
                    
            else:
                commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)
            ##--2) blind
            WORKDIR="WORKDIR_MKPLOT/"+cutfile+'/blind/'
            commandlist=[]
            commandlist.append('cd '+os.getcwd())
            if self.inputs:
                commandlist.append('input='+self.inputs)
            else:
                commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine_blind.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu_blind '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)
            ##--3) final
            WORKDIR="WORKDIR_MKPLOT/"+cutfile+'/finalbkg/'
            commandlist=[]
            commandlist.append('cd '+os.getcwd())
            if self.inputs:
                commandlist.append('input='+self.inputs)
            else:
                commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --plotFile=StructureFiles/plot.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu_finalbkg '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)



if __name__ == '__main__':
    cutpy=sys.argv[1]
    if len(sys.argv)>2:
        nuisancepy=sys.argv[2]
    else:
        nuisancepy=False
        
    if len(sys.argv)>3:
        samples=sys.argv[3]
    else:
        samples=False

    if len(sys.argv)>4:
        inputs=sys.argv[4]
    else:
        intpus=False


    #run=splitter('cuts_Boosted_Combine.py')
    run=splitter(cutpy,nuisancepy,samples,inputs)
    #run.RunCuts()
    run.Split()
    run.Submit()
