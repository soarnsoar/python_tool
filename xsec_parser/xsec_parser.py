#!/usr/bin/python
import glob
import os
import re
class output_parser:
    
    fs_output = []
    f_current=''
    xsec_info=[]
    xsec_start_phrase = "GenXsecAnalyzer"
    xsec_end_phrase = "============================================="
    xsec_start_phrase_i = "Process"
    xsec_end_phrase_i = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- "
            
    def set_flist(self, _dir_=str(os.getcwd()) ):    
        for file in glob.glob(_dir_+"/*.out"):
            self.fs_output.append(file)
        
    def set_file(self,idx):
        self.f_current=self.fs_output[idx]

    def clear_flist(self):
        del self.fs_output[:]

    def get_xsec_info(self):
        _file_=self.f_current
        f = open(_file_, 'r')
        lines=f.readlines()
        xseclines = [] 
        mode=0 # if mode==1, It is a xsec-related value
        for line in lines:
            if (self.xsec_start_phrase in line): mode=1        
            elif(self.xsec_end_phrase in line): mode=0
  
            if(mode==1):   xseclines.append(line)

        f.close()
        self.xsec_info=xseclines


    def get_xsec_info_i(self,idx):
        print "analyze each line"
        mode=0

        for line in self.xsec_info:

            if ( (mode==1) and self.xsec_end_phrase_i in line): mode=0
            if( mode==1) : 
#                print line
                pattern = re.compile(r'''^\s*
           (\d+) #Process
           \s+
           ([+-e.\d]*)#xsec_before
           \s\+/\-\s # +/- symbol
           ([+-e.\d]*) #xsec_before_err
           \s+
           (\d+) #passed
           \s+
           (\d+) #nposw
           \s+
           (\d+) #nnegw
           \s+
           (\d+) #tried
           \s+
           (\d+) #nposw
           \s+
           (\d+) #nnegw
           \s+
           ([+-e.\d]*) #xsec_match
           \s\+/\-\s # +/- symbol 
           ([+-e.\d]*) #xsec_match_err
           \s+
           ([+-e.\d]*) #accepted
           \s\+/\-\s # +/- symbol
           ([+-e.\d]*) #accepted_err
           \s+
           ([+-e.\d]*) #event_eff 
           \s\+/\-\s # +/- symbol
           ([+-e.\d]*) #event_eff_err
          ''', 66)
                info = pattern.findall(line)
                

#                print "Process="+info[0][0]
 #               print "xsec_before="+info[0][1]
  #              print "xsec_before_err="+info[0][2]
   #             print "passed="+info[0][3]
    #            print "nposw="+info[0][4]
     #           print "nnegw="+info[0][5]
      #          print "tried="+info[0][6]
       #         print "nposw="+info[0][7]
        #        print "nnegw="+info[0][8]
         #       print "xsec_match="+info[0][9]
          #      print "xsec_match_err="+info[0][10] 
           #     print "accepted="+info[0][11]
            #    print "accepted_err="+info[0][12]
             #   print "event_eff="+info[0][13]
              #  print "event_eff_err="+info[0][14]
        
###############################################################
                if(info[0][0]==str(idx)): 
                    

###############################################################
            if(self.xsec_start_phrase_i in line): mode=1


    def set_xsec_start_phrase(self, xsec_start_phrase):
        self.xsec_start_phrase=xsec_start_phrase

    def set_xsec_end_phrase(self, xsec_start_phrase):
        self.xsec_start_phrase=xsec_end_phrase
    def set_xsec_end_phrase_i(self, xsec_start_phrase_i):
        self.xsec_start_phrase_i=xsec_end_phrase_i


    


if __name__ == "__main__":

    ana = output_parser()
    ana.set_flist() ##input = directory

    ana.set_file(0)
    ana.get_xsec_info()
    ana.get_xsec_info_i(0)   
