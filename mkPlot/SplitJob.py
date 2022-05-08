###----
import os
import sys
sys.path.append('python_tool/')
from ExportShellCondorSetup import Export
import glob
class splitter:
    def __init__(self,cutspy):
        ##
        self.cutspy=cutspy
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
            commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu')
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)
            ##--2) blind
            WORKDIR="WORKDIR_MKPLOT/"+cutfile+'/blind/'
            commandlist=[]
            commandlist.append('cd '+os.getcwd())
            commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine_blind.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu')
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)
            ##--3) final
            WORKDIR="WORKDIR_MKPLOT/"+cutfile+'/finalbkg/'
            commandlist=[]
            commandlist.append('cd '+os.getcwd())
            commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
            commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=StructureFiles/plot.py --showIntegralLegend=1 --cutsFile '+cutfile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu')
            command='&&'.join(commandlist)
            jobname='plot'+self.Year+bst
            submit=True
            ncpu=1
            Export(WORKDIR,command,jobname,submit,ncpu)



if __name__ == '__main__':
    cutpy=sys.argv[1]
    #run=splitter('cuts_Boosted_Combine.py')
    run=splitter(cutpy)
    #run.RunCuts()
    run.Split()
    run.Submit()
