import datetime

import os
import copy

class jh_html :
    def __init__(self):
        self.title="NEED_TITLE!!"
        self.output="tmp_Status.html"
        self.tabs=[]
        self.tabs=copy.deepcopy(self.tabs)

    def make(self):

        os.system("rm "+self.output+" 2> /dev/null")
        out = open(self.output,'a')


        title=self.title
        JobStartTime = datetime.datetime.now()
        timestamp =  JobStartTime.strftime('%Y-%m-%d %H:%M:%S')

        ###Title of page and design foramt###                                                                                                                                     
        print >>out,'''                                                                                                                                                           
        <!DOCTYPE html>                                                                                                                                                           
        <html>                                                                                                                                                                    
                                                                                                                                                                                  
        <head>                                                                                                                                                                    
                                                                                                                                                                                  
        <title>Status of MC request</title>                                                                                                                                       
                                                                                                                                                                                  
        <style>                                                                                                                                                                   
        p.Title{                                                                                                                                                                  
        text-align: center;                                                                                                                                                       
        font-size: 40px;                                                                                                                                                          
        }                                                                                                                                                                         
        @-webkit-keyframes blink                                                                                                                                                  
        {                                                                                                                                                                         
        0%     { visibility: hidden }                                                                                                                                             
        50%    { visibility: hidden }                                                                                                                                             
        50.01% { visibility: visible }                                                                                                                                            
        100%   { visibility: visible }                                                                                                                                            
        }                                                                                                                                                                         
        td.Monaco_TotalEvent_Updating{                                                                                                                                            
        -webkit-animation: blink 0.5s infinite linear alternate;                                                                                                                  
        font-family: monaco, Consolas, Lucida Console, monospace;                                                                                                                 
        text-align: right;                                                                                                                                                        
        color: red;                                                                                                                                                               
        }                                                                                                                                                                         
        p.Clock{                                                                                                                                                                  
        text-align: center;                                                                                                                                                       
        font-size: 30px;                                                                                                                                                          
        }                                                                                                                                                                         
                </style>                                                                                                                                                                  
                                                                                                                                                                                  
        </head>                                                                                                                                                                   
        '''

        ##Title##                                                                                                                                                                 
        print >>out,'''<body>                                                                                                                                                     
        <p class="Title"> {1} </p>                                                                                                                                                
        <p class="Clock">Last updated time : {0}</p>                                                                                                                              
        <table border = 1 align="center">                                                                                                                                         
        <tr>'''.format(timestamp,self.title)



        for tab in self.tabs:
            print >>out,'''<th>{0}</th>                                                                                                                                           
            '''.format(tab)


        print >> out,'''</tr>'''


        print >>out,'''                                                                                                                                                           
        <tr>                                                                                                                                                                      
        <th>aa</th>                                                                                                                                                               
        </tr>'''
