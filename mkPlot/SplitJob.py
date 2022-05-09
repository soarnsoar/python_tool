###----
import os
import sys
sys.path.append('python_tool/')
from ExportShellCondorSetup import Export
import glob
import optparse

class splitter:
    def __init__(self,cutspy,nuisancepy,samples,inputs,variablepy):
        ##
        self.cutspy=cutspy
        self.nuisancepy=nuisancepy
        if self.nuisancepy:
            self.nuisanceopt="--nuisancesFile="+self.nuisancepy
        else:
            self.nuisanceopt=''


        self.inputs=inputs
        if self.inputs:
            if len(self.inputs.split(','))>1:
                self.multiopt="--isMultiInputs"
        else:
            self.multiopt=""



        self.ReadCuts()

        self.samples=samples
        if self.samples:
            self.samplesopt="--samplesFile="+self.samples
        else:
            self.samplesopt="--samplesFile=samples_"+self.Year+"_dummy.py"

        self.variablepy=variablepy
        self.cutfiles=[]
        self.variablefiles=[]

        if self.variablepy:
            self.ReadVariables()
    def ReadCuts(self):
        print self.cutspy
        exec(open(self.cutspy))
        #for cut in cuts:
        #    print cut
        self.cuts=cuts
        self.Year=Year

    def ReadVariables(self):
        print self.variablepy
        exec(open(self.variablepy))
        #for cut in cuts:
        #    print cut
        self.variables=variables

        
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
        f.close()
        if self.variablepy:
            print self.variablepy
            lines=[]
            f=open(self.variablepy,'r')
            lines=f.readlines()

            for variable in self.variables:
                newpath='split_plots/'+self.variablepy+'__'+variable+'.py'
                self.variablefiles.append(newpath)
                print newpath
                fnew=open(newpath,'w')
                for line in lines:
                    fnew.write(line)
                fnew.write('variables={}\n')
                fnew.write('variables["'+variable+'"]='+str(self.variables[variable]))
                fnew.close()
            f.close()
    def Submit(self):
        if not self.variablepy:
            self.Submit_AllVariables()
        else:
            self.Submit_EachVariables()
    def Submit_EachVariables(self):
        for cutfile in self.cutfiles:
            for variablefile in self.variablefiles:
                if 'Boosted' in cutfile:
                    bst='Boosted'
                else:
                    bst='Resolved'

                ##--1) nominal
                WORKDIR="WORKDIR_MKPLOT/"+cutfile.replace('/','__')+'__'+variablefile.replace('/','__')+'/nom/'
                commandlist=[]
                commandlist.append('cd '+os.getcwd())
                if self.inputs:
                    commandlist.append('input='+self.inputs)
                else:
                    commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
                commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine.py --showIntegralLegend=1 --cutsFile '+cutfile+' --variablesFile='+variablefile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
                command='&&'.join(commandlist)
                jobname='plot'+self.Year+bst
                submit=True
                ncpu=1
                Export(WORKDIR,command,jobname,submit,ncpu)
                ##--2) blind
                WORKDIR="WORKDIR_MKPLOT/"+cutfile.replace('/','__')+'__'+variablefile.replace('/','__')+'/blind/'
                commandlist=[]
                commandlist.append('cd '+os.getcwd())
                if self.inputs:
                    commandlist.append('input='+self.inputs)
                else:
                    commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
                commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --samplesFile=samples_'+self.Year+'_dummy.py --plotFile=plot_elemu_'+bst+'_Combine_blind.py --showIntegralLegend=1 --cutsFile '+cutfile+' '+' --variablesFile='+variablefile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu_blind '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
                command='&&'.join(commandlist)
                jobname='plot'+self.Year+bst
                submit=True
                ncpu=1
                Export(WORKDIR,command,jobname,submit,ncpu)
                ##--3) final
                WORKDIR="WORKDIR_MKPLOT/"+cutfile.replace('/','__')+'__'+variablefile.replace('/','__')+'/finalbkg/'
                commandlist=[]
                commandlist.append('cd '+os.getcwd())
                if self.inputs:
                    commandlist.append('input='+self.inputs)
                else:
                    commandlist.append('input=`ls rootFile*'+bst+'*Combine*/hadd.root`')
                commandlist.append('mkPlot.py --pycfg=configuration_'+bst+'_Combine.py --inputFile=${input} --plotFile=StructureFiles/plot.py --showIntegralLegend=1 --cutsFile '+cutfile+' '+' --variablesFile='+variablefile+' --outputDirPlots=plots_'+self.Year+'_'+bst+'_Combine_elemu_finalbkg '+self.nuisanceopt+" "+self.multiopt+" "+self.samplesopt)
                command='&&'.join(commandlist)
                jobname='plot'+self.Year+bst
                submit=True
                ncpu=1
                Export(WORKDIR,command,jobname,submit,ncpu)



    def Submit_AllVariables(self):
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
        inputs=False

    if len(sys.argv)>5:
        variablepy=sys.argv[5]
    else:
        variablepy=False


    #run=splitter('cuts_Boosted_Combine.py')
    run=splitter(cutpy,nuisancepy,samples,inputs,variablepy)
    #run.RunCuts()
    run.Split()
    run.Submit()
