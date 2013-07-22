# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\btek\.spyder2\.temp.py
"""

#import os
#import fnmatch
#
#os.path.exists(path)
#for dirpath, dirs, files in os.walk(path):
#    for filename in fnmatch.filter(files, '*.raw'):
#        with open(os.path.join(dirpath, filename)):
#             close(os.path.join(dirpath,filename))
#             for files in os.walk(os.curdir):
#                 print dirs,files,len(files), "non-directory files"
        
def read(file):
    inf = {}
    fid = open(file,'r')
    print fid,"\n"
    lines = fid.readlines()
    #print lines, "\n----------------------"
    for str in lines:
        str1 =str.replace(';',' ')
     #   print str1,
        if str.find('experiment')>=0:
            inf['exp_name']=str1.split('\"')[1]
        elif str.find('scale x')>=0:
            inf['scaleX']= float(str1.split()[2])
        elif str.find('scale y')>=0:
            inf['scaleY']= float(str1.split()[2])   
        elif str.find('scale z')>=0:
            inf['scaleZ']= float(str1.split()[2])
        elif str.find('boundary x')>=0:
            inf['boundaryX']= float(str1.split()[2])
        elif str.find('boundary y')>=0:
            inf['boundaryY']= float(str1.split()[2])
        elif str.find('magnification')>=0:
            inf['magnification'] = int(str1.split()[1])
    print "inf:", inf
    fid.close()
    return inf

                 
#knossos_conf_reader(r'D:\mouse_brain\4x-downsampled\20130506-interareal\knossos.conf')
 