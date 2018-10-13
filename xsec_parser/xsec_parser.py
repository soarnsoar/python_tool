#!/usr/bin/python

###To analyze  "GenXsecAnalyzer" output


import glob
import os
import re
import math

class output_parser:
    ##This class is for a file
    fs_output = []
    f_current=''
    N_fvalid=0 ## valid file
    xsec_info=[]
    xsec_start_phrase = "GenXsecAnalyzer"
    xsec_end_phrase = "============================================="
    xsec_start_phrase_i = "Process"
    xsec_end_phrase_i = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- "

    txsec_info=[]
    total_xsec_no_merge=0
    N_event_no_merge=0
    total_xsec_start_phrase = "PYTHIA Process Initialization"
    total_xsec_end_phrase = "End PYTHIA Multiparton Interactions Initialization"

    
    N_process=0
    process=[] #####Processes in the file

    process_combine=[] ### combined info using all files in the target directory # size = N processes

    
    
    
    
    class i_process: ####This class is for a process 
 
        def __init__(self,i):
            self.Process=str(i)
            self.xsec_before=0
            self.xsec_before_err=0
            self.passed=0
            self.f_nposw=0 ##after merging
            self.f_nnegw=0
            self.tried=0
            self.i_nposw=0 ##before merging
            self.i_nnegw=0
            self.xsec_match=0
            self.xsec_match_err=0
            self.accepted=0
            self.accepted_err=0    
            self.event_eff=0
            self.event_eff_err=0
       
        def add_info(self,proc):##Use when combine xsec values from various files
            ##What we want to add = proc##
            ##where to add to = self
            Process2=proc.Process
            passed2=proc.passed
            i_nposw2=proc.i_nposw
            i_nnegw2=proc.i_nnegw
            tried2=proc.tried
            f_nposw2=proc.f_nposw
            f_nnegw2=proc.f_nnegw
            xsec_before2=proc.xsec_before
            xsec_before_err2=proc.xsec_before_err
            xsec_match2=proc.xsec_match
            xsec_match_err2=proc.xsec_match_err
            accepted2=proc.accepted
            accepted_err2=proc.accepted_err
            event_eff2=proc.event_eff
            event_eff_err2=proc.event_eff_err
            ########################
            
            if self.Process != Process2: 
                print "Process # is not matched"
            else:
                Process1=self.Process
                passed1=self.passed
                i_nposw1=self.i_nposw
                i_nnegw1=self.i_nnegw
                tried1=self.tried
                f_nposw1=self.f_nposw
                f_nnegw1=self.f_nnegw
                xsec_before1=self.xsec_before
                xsec_before_err1=self.xsec_before_err
                xsec_match1=self.xsec_match
                xsec_match_err1=self.xsec_match_err
                accepted1=self.accepted
                accepted_err1=self.accepted_err
                event_eff1=self.event_eff
                event_eff_err1=self.event_eff_err

                ####Simple #of events values can be added directly###
                self.passed+=passed2
                self.i_nposw+=i_nposw2
                self.i_nnegw+=i_nnegw2
                self.tried+=tried2
                self.f_nposw+=f_nposw2
                self.f_nnegw+=f_nnegw2

                ########################                
                ##order => xsec_before => xsec_before_err => calculate acceptance =>  calculate acceptance_err => calc event_eff=>calc event_eff_err
                #=>xsec_match => xsec_match_err

                ###xsec_before###
                ###
                ##xsec_combine = [ xsec1/(err1)^2 + xsec2/(err2)^2  ]/ ( 1/(err1)^2 + 1/(err2)^2 )
                ##
              
                #xsec_before &xsec_before_err#
                if xsec_before1 == 0 and xsec_before2 != 0:
                    self.xsec_before=xsec_before2
                    self.xsec_before_err=xsec_before_err2

                elif xsec_before1 !=0 and xsec_before2==0:

                    self.xsec_before=xsec_before1
                    self.xsec_before_err=xsec_before_err1

                else :
                    w1=pow(1/xsec_before_err1,2)
                    w2=pow(1/xsec_before_err2,2)
                    numo=xsec_before1*w1 + xsec_before2*w2
                    deno=w1+w2
                
                    self.xsec_before=numo/deno
                    numo=1
                    deno=w1+w2
                    self.xsec_before_err=math.sqrt(numo/deno)
                    
                #accepted
                    wpassed=float(self.f_nposw) - float(self.f_nnegw)
                    wtried=float(self.i_nposw) - float(self.i_nnegw)
                    self.accepted= wpassed/wtried * 100. #in percent
                #accepted_err
                    self.accepted_err=math.sqrt( (1-self.accepted/100.)*self.accepted/100./wtried )*100.
                #event_eff
                    npassed=float(self.f_nposw) + float(self.f_nnegw)
                    ntried=float(self.i_nposw) + float(self.i_nnegw)
                    self.event_eff= npassed/wtried * 100. #in percent
                #event_eff_err
                    self.event_eff_err= math.sqrt( (1-self.event_eff/100.)*self.event_eff/100./ntried ) *100.
                #xsec_match
                    if self.xsec_before == 0 or self.accepted == 0 :
                        self.xsec_match=0
                        self.xsec_match_err=0
                    else:
                        self.xsec_match = self.xsec_before*self.accepted/100.
                #xsec_match_err => sqrt sum of relative err's
                        self.xsec_match_err = self.xsec_match * math.sqrt( pow(self.xsec_before_err/self.xsec_before  ,2 ) + pow(self.accepted_err/self.accepted,2)   )



        
    total_combine=i_process("total")
    

    


    def set_flist(self, _dir_=str(os.getcwd()) ):    
        
        for file in glob.glob(_dir_+"/*.out"):
            self.fs_output.append(file)

        
    def set_file(self,idx):
        self.f_current=self.fs_output[idx]

    def clear_flist(self):
        del self.fs_output[:]
    
    def clear_process_combine(self):
        del self.process_combine[:]
    def clear_total_combine(self):
        del self.totalcombine[:]

    def get_xsec_info(self):
        _file_=self.f_current
        f = open(_file_, 'r')
        lines=f.readlines()
        xseclines = [] 
        txseclines = [] 
        mode=0 # if mode==1, It is a xsec-related value
        mode_t=0 # For  PYTHIA Process Initialization
        for line in lines:

        ######GenXsecAnalyzer BOX#####
            if (self.xsec_start_phrase in line): 
                mode=1

            elif(self.xsec_end_phrase in line): mode=0
  
            if(mode==1):   xseclines.append(line)
        ######END GenXsecAnalyzer BOX#####

        ######PYTHIA Process Initialization#######
            if (self.total_xsec_start_phrase in line):                
                mode_t=1
            elif(self.total_xsec_end_phrase in line): mode_t=0

            if(mode_t==1):

                txseclines.append(line)
        ######END PYTHIA Process Initialization#######




        f.close()
        if xseclines == None: return "NOT a valid file"
        else : 

            self.xsec_info=xseclines
            self.get_xsec_info_i()

            self.txsec_info=txseclines
            self.get_total_xsec_info()

    def get_total_xsec_info(self):

        total_xsec_no_merge=0
        mode=0
        for line in self.txsec_info:

            if "Les Houches User Process(es)" in line : 
                info=line.split()

                self.total_xsec_no_merge=float(info[7])*pow(10,9) ##in pb
    def get_xsec_info_i(self):
        del self.process[:]

        mode=0
        self.N_process=0
        for line in self.xsec_info: ##for each line in xsec box

            if ( (mode==1) and self.xsec_end_phrase_i in line): mode=0
            if( mode==1) :  ## if line is xsec an info of a process
                

             

##########################Regular Expresstion is hard to understand#################
#                pattern = re.compile(r'''^\s*
#           (\d+) #Process
#           \s+
#           ([+-e.\d]*)#xsec_before
#           \s\+/\-\s # +/- symbol
#           ([+-e.\d]*) #xsec_before_err
#           \s+
#           (\d+) #passed
#           \s+
#           (\d+) #nposw
#           \s+
#           (\d+) #nnegw
#           \s+
#           (\d+) #tried
#           \s+
#           (\d+) #nposw
#           \s+
#           (\d+) #nnegw
#           \s+
#           ([+-e.\d]*) #xsec_match
#           \s\+/\-\s # +/- symbol 
#           ([+-e.\d]*) #xsec_match_err
#           \s+
#           ([+-e.\d]*) #accepted
#           \s\+/\-\s # +/- symbol
#           ([+-e.\d]*) #accepted_err
#           \s+
#           ([+-e.\d]*) #event_eff 
#           \s\+/\-\s # +/- symbol
#           ([+-e.\d]*) #event_eff_err
#          ''', 66)
#                info = pattern.findall(line)
#                
#
#                print "Process="+info[0][0]
#                print "xsec_before="+info[0][1]
#                print "xsec_before_err="+info[0][2]
#                print "passed="+info[0][3]
#                print "nposw="+info[0][4]
#                print "nnegw="+info[0][5]
#                print "tried="+info[0][6]
#                print "nposw="+info[0][7]
#                print "nnegw="+info[0][8]
#                print "xsec_match="+info[0][9]
#                print "xsec_match_err="+info[0][10] 
#                print "accepted="+info[0][11]
#                print "accepted_err="+info[0][12]
#                print "event_eff="+info[0][13]
#                print "event_eff_err="+info[0][14]
##########################End of Regular Expresstion is hard to understand#################        
##########################Use split method in python#####################################

                info=line.split()
#                current_proc=self.i_process(float(info[0]))
                current_proc=self.i_process(str(info[0]))
 
#                print "Process="+info[0]
#                print "xsec_before="+info[1]
#                print "plusminus="+info[2]
#                print "xsec_before_err="+info[3]
#                print "passed="+info[4]
#                print "nposw="+info[5]
#                print "nnegw="+info[6]
#                print "tried="+info[7]
#                print "nposw="+info[8]
#                print "nnegw="+info[9]
#                print "xsec_match="+info[10]
#                print "plusminus="+info[11]
#                print "xsec_match_err="+info[12]
#                print "accepted="+info[13]
#                print "plusminus="+info[14]
#                print "accepted_err="+info[15]
#                print "event_eff="+info[16]
#                print "plusminus="+info[17]
#                print "event_eff_err="+info[18]
#                

                current_proc.Process=str(info[0])
                current_proc.xsec_before=float(info[1])
                current_proc.xsec_before_err=float(info[3])
                current_proc.passed=int(info[4])
                current_proc.f_nposw=int(info[5])
                current_proc.f_nnegw=int(info[6])
                current_proc.tried=int(info[7])
                current_proc.i_nposw=int(info[8])
                current_proc.i_nnegw=int(info[9])
                current_proc.xsec_match=float(info[10])
                current_proc.xsec_match_err=float(info[12])
                current_proc.accepted=float(info[13])
                current_proc.accepted_err=float(info[15])
                current_proc.event_eff=float(info[16])
                current_proc.event_eff_err=float(info[18])
                self.process.append(current_proc)

###############################################################


            if(self.xsec_start_phrase_i in line): mode=1
        
        #self.N_event_no_merge=0
        #for proc in self.process:
        #    self.N_event_no_merge=self.N_event_no_merge+proc.tried
        
        self.N_process=len(self.process)

    def set_xsec_start_phrase(self, xsec_start_phrase):
        self.xsec_start_phrase=xsec_start_phrase
    def set_xsec_end_phrase(self, xsec_start_phrase):
        self.xsec_start_phrase=xsec_end_phrase
    def set_xsec_end_phrase_i(self, xsec_start_phrase_i):
        self.xsec_start_phrase_i=xsec_end_phrase_i

    def set_total_xsec_start_phrase(self, total_xsec_start_phrase):
        self.total_xsec_start_phrase=total_xsec_start_phrase
    def set_total_xsec_end_phrase(self, total_xsec_start_phrase):
        self.total_xsec_start_phrase=total_xsec_end_phrase

    def combine_info(self):
        self.N_fvalid=0
        self.clear_process_combine()






        for i in range(len(self.fs_output)) :

            self.set_file(i)
            self.get_xsec_info()
            if self.get_xsec_info()=="NOT a valid file": continue
            ######VALID FILE######
            self.N_fvalid=self.N_fvalid+1
            ######1st file########->initialize combined info

            if self.N_fvalid==1 :
                for ip in range(self.N_process):
                    proc_temp=self.i_process(str(ip))
                    self.process_combine.append(proc_temp)
            #######################

            print str(i)+". "+self.f_current            


            ###for one file, all processes
            for proc in self.process:


                Process=proc.Process
#                passed=proc.passed
#                i_nposw=proc.i_nposw
#                i_nnegw=proc.i_nnegw
#                tried=proc.tried
#                f_nposw=proc.f_nposw
#                f_nnegw=proc.f_nnegw
#                xsec_before=proc.xsec_before
#                xsec_before_err=proc.xsec_before_err
#                xsec_match=proc.xsec_match
#                xsec_match_err=proc.xsec_match_err
#                accepted=proc.accepted
#                accepted_err=proc.accepted_err
#                event_eff=proc.event_eff
#                event_eff_err=proc.event_eff_err
                 ###Add event info####
#                self.process_combine[Process].passed+=passed
#                self.process_combine[Process].i_nposw+=i_nposw
#                self.process_combine[Process].i_nnegw+=i_nnegw
#                self.process_combine[Process].tried+=tried
#                self.process_combine[Process].f_nposw+=f_nposw
#                self.process_combine[Process].f_nnegw+=f_nnegw
                
                self.process_combine[int(Process)].add_info(proc)
                
        print "# of valid file="+str(self.N_fvalid)


    def total_info(self,processes):
        total=self.i_process("total")## sum of all processes
        Nprocess=len(processes)
        for i in range(Nprocess):
            proc=processes[i]
            total.xsec_before+=proc.xsec_before
            total.xsec_before_err=math.sqrt( pow( total.xsec_before_err,2   ) + pow(proc.xsec_before_err,2)     )
            total.passed+=proc.passed
            total.i_nposw+=proc.i_nposw
            total.i_nnegw+=proc.i_nnegw
            total.tried+=proc.tried
            total.f_nposw+=proc.f_nposw
            total.f_nnegw+=proc.f_nnegw
            total.xsec_match+=proc.xsec_match
            total.xsec_match_err=math.sqrt( pow( total.xsec_match_err,2   ) + pow(proc.xsec_match_err,2)     )
            



        total.accepted=(    (float(total.f_nposw)-float(total.f_nnegw))/(float(total.i_nposw)-float(total.i_nnegw)) )*100.
        total.accepted_err=    math.sqrt( ( 1 - total.accepted /100.   )*total.accepted /100. / float(total.i_nposw-total.i_nnegw) )*100.
        total.event_eff=(   (float(total.f_nposw)+float(total.f_nnegw))/(float(total.i_nposw)+float(total.i_nnegw)) )*100.
        total.event_eff_err=  math.sqrt( ( 1 - total.event_eff/100.   )*total.event_eff/100. / float(total.i_nposw+total.i_nnegw) )*100.
       
        return total
        


    def set_total_combine(self):
        self.total_combine=self.total_info(self.process_combine)
        
    def import_result(self, filename=os.getcwd()+"combine_output.txt"):
        f= open(filename,'w')
        f.write(           
            '''
------------------------------------
GenXsecAnalyzer:
------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Overall cross-section summary 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
''')
        f.write('Process\t\txsec_before [pb]\t\tpassed\tnposw\tnnegw\ttried\tnposw\tnnegw \txsec_match [pb]\t\t\taccepted [%]\t event_eff [%]\n')
        for i in range(len(self.process_combine)): 
            
            proc=self.process_combine[i]
            #print  '%.3e'%proc.xsec_before 
            f.write(
                str(proc.Process)+"\t\t"+
                str( '%.3e'%proc.xsec_before )+" +/- "+
                str( '%.3e'%proc.xsec_before_err)+"\t\t"+
                str(proc.passed)+"\t"+
                str(proc.f_nposw)+"\t"+
                str(proc.f_nnegw)+"\t"+
                str(proc.tried) +"\t"+
                str(proc.i_nposw) +"\t"+
                str(proc.i_nnegw)+"\t"+
                str('%.3e'%proc.xsec_match)+" +/- "+
                str('%.3e'%proc.xsec_match_err)+"\t\t"+
                str(round(proc.accepted,1))+" +/- "+
                str(round(proc.accepted_err,1))+"\t"+
                str(round(proc.event_eff,1))+" +/- " +
                str(round(proc.event_eff_err,1)) +"\n"
                )
        proc=self.total_combine
        f.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        f.write(
            str(proc.Process)+"\t\t"+
            str( '%.3e'%proc.xsec_before )+" +/- "+
            str( '%.3e'%proc.xsec_before_err)+"\t\t"+
            str(proc.passed)+"\t"+
            str(proc.f_nposw)+"\t"+
            str(proc.f_nnegw)+"\t"+
            str(proc.tried) +"\t"+
            str(proc.i_nposw) +"\t"+
            str(proc.i_nnegw)+"\t"+
            str('%.3e'%proc.xsec_match)+" +/- "+
            str('%.3e'%proc.xsec_match_err)+"\t\t"+
            str(round(proc.accepted,1))+" +/- "+
            str(round(proc.accepted_err,1))+"\t"+
            str(round(proc.event_eff,1))+" +/- " +
            str(round(proc.event_eff_err,1)) +"\n"
            )
        f.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('Before matching: total cross section = '+str( '%.3e'%proc.xsec_before )+" +/- "+str( '%.3e'%proc.xsec_before_err)+" pb\n" )
        f.write('After matching: total cross section = '+str( '%.3e'%proc.xsec_match )+" +/- "+str( '%.3e'%proc.xsec_match_err)+" pb\n" )

        f.close()


def test():

##test_with 1st file
    ana = output_parser()
    ana.set_flist() ##input = directory ##default dir = pwd
    ana.combine_info()
    ana.set_file(0)
    ana.get_xsec_info()
    
#    print ana.process[0]
    Nprocess  = len(ana.process)
    proc=ana.process
    xsec_before_sum=0
    xsec_before_err_sqrsum=0
    xsec_before_err_relsum=0
    xsec_before_relerr_sum=0
    xsec_match_sum=0    
    
    for i in range(Nprocess):
        accepted_cal_i=0
        accepted_err_cal_i=0
        event_eff_cal_i=0
        event_eff_err_cal_i=0
        i_nposw=float(proc[i].i_nposw)
        i_nnegw=float(proc[i].i_nnegw)
        f_nposw=float(proc[i].f_nposw)
        f_nnegw=float(proc[i].f_nnegw)

        event_eff_cal_i = (f_nposw+f_nnegw)/(i_nposw+i_nnegw)
        event_eff_err_cal_i= math.sqrt((1-event_eff_cal_i)*event_eff_cal_i/(i_nposw+i_nnegw)    ) 

        accepted_cal_i=(f_nposw-f_nnegw)/(i_nposw-i_nnegw)
        accepted_err_cal_i= math.sqrt((1-accepted_cal_i)*accepted_cal_i/(i_nposw+i_nnegw)    )



        #######XSEC###########
        xsec_before_err_i=proc[i].xsec_before_err
        xsec_before_err_sqrsum=math.sqrt( pow(xsec_before_err_sqrsum, 2   ) + pow(xsec_before_err_i, 2))
        xsec_before_i=proc[i].xsec_before

        relerr_i = xsec_before_err_i/xsec_before_i
        xsec_before_relerr_sum=math.sqrt( pow(relerr_i,2) + pow(xsec_before_relerr_sum,2) )
        
        
        xsec_before_sum=xsec_before_sum+xsec_before_i
 
        ########################

    #### xsec_match ####
        xsec_match_cal_i=xsec_before_i*accepted_cal_i
        print "xsec_match_cal_i="+str(xsec_match_cal_i)
        if xsec_before_i==0 or accepted_err_cal_i==0:
            xsec_match_relerr_cal_i=0
        else:            
            xsec_match_relerr_cal_i=math.sqrt( pow( xsec_before_err_i/xsec_before_i  ,2) + pow( accepted_err_cal_i/accepted_cal_i,2  )   )
        
        xsec_match_err_cal_i=xsec_match_relerr_cal_i*xsec_match_cal_i
        print "xsec_match_err_cal_i="+str(xsec_match_err_cal_i)
        print "############################"


    print "xsec_before_err_sqrsum="+str(xsec_before_err_sqrsum)
    xsec_before_err_relsum= xsec_before_sum*xsec_before_relerr_sum
    print "xsec_before_sum="+str(xsec_before_sum)


if __name__ == "__main__":
#    test()
    ana = output_parser()
    ana.set_flist('outputs') ##input = directory ##default dir = pwd  
    ana.combine_info()
    ana.set_total_combine()
    ana.import_result('xsec_outputs.txt')###input = where to save the output file

