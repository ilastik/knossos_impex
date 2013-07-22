# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:31:32 2013
this script converts knossos file folder to 'ilastik' HDF5 file: it repermutes data and forces ilastik volume indexing order xyz, but there is an option to switch that. 
put the data path and start and end indexes of VOI, and it writes to same folder. 
@author: btek
"""

import h5py, numpy
import os,  datetime, knossos_conf_reader
from scipy import misc
from numpy import *

def removeNonFolders(dirPath, listDirectory):
    count = 0
    #print listDirectory,'--********************\n'
    newList = []
    for x  in range(0, len(listDirectory)):
         generateDirName =  os.path.join(dirPath,listDirectory[x])
         #print generateDirName
         if (os.path.isdir(generateDirName)):
             newList.append(listDirectory[x])
             count +=1

    return newList

def writeInChunks(dSet, data3d, destPosition, chunkDims, writeOrder):

    cubeDims = numpy.array(shape(data3d))
    print 'writing chunks'
    #print 'chunkDims=',chunkDims
    dset_x = destPosition[0]
    dset_y = destPosition[1]
    dset_z = destPosition[2]
    numChunks = numpy.array(cubeDims)/numpy.array(chunkDims)
    #print   'numChunks'
    oldcx=0
    cx = 0
    for xite in range(0,numChunks[0]): # x loop
        cx+= chunkDims[0]
        oldcy=0
        cy = 0
        for yite in range(0,numChunks[1]): # y loop
            cy+= chunkDims[1]
            oldcz=0
            cz = 0
            for zite in range(0,numChunks[2]): # x loop
                cz+= chunkDims[2]
                #print 'cx=',cx, 'oldcx=', oldcx,'cy=',cy, 'oldcy=', oldcy,'cz=',cz, 'oldcz=', oldcz
                print '.',
                selz  =  numpy.array([dset_z+oldcz,dset_z+cz])
                sely  = numpy.array([dset_y+oldcy,dset_y+cy])
                selx  =  numpy.array([dset_x+oldcx,dset_x+cx])
    
    
                if writeOrder=='zyx':
                    print   numpy.s_[selz[0]:selz[1],sely[0]:sely[1],selx[0]:selx[1]]
    
                    #dset[dset_z,0:128,0:128] = 0
                    
                    dSet.write_direct(data3d[oldcz:cz,oldcy:cy,oldcz:cz], None, numpy.s_[selz[0]:selz[1],sely[0]:sely[1],selx[0]:selx[1]])
                    print 'Done'
                elif writeOrder =='xyz':
                    dSet[selx[0]:selx[1],sely[0]:sely[1],selz[0]:selz[1]] = data3d[oldcx:cx,oldcy:cy,oldcz:cz]
       #dset.write_direct(cube_data3dt[:,:,oldc:c], None, numpy.s_[selx[0]:selx[1],sely[0]:sely[1],selz[0]:selz[1]])
                oldcz = cz
            oldcy = cy
        oldcx = cx
    return True
                                

#def HDF5VOIfromKnossos(path='',startix=[],endix = [],writeOrder='zyx',chunkZ=-1):
# this is the path of the knossos folder
path = r'D:\mouse_brain\shawnnew\20130506-interareal_mag4\20130506-interareal_mag4'
"""
whole set
#startix = ([0,0,0])
#endix = ([59,6,8])
"""
"""
training set for interareal_mag4\20130506
startix = ([0,0,0])  
endix = ([1,3,4])
"""

startix = ([0,0,0])  
endix = ([1,3,4])
#startix = ([0,10,16])
#endix = ([1,14,21])
#writeOrder = 'zyx'
#startix = ([1,10,16])
#endix = ([2,14,20])
writeOrder = 'xyz'
chunkZ = -1
if(True):

    # convert knossos files to hdf5


# note startix and endix are in the same order or writeOrder
# so if  your writeOrder zyx startix is in zyx order.
    if path=='':
        path = r'D:\mouse_brain\4x-downsampled\20130506-interareal'
    if not os.path.exists(path):
        print path+" is not valid"
    else:
        listDirX = os.listdir(path)
        if 'knossos.conf' in listDirX:
            inf = knossos_conf_reader.read(os.path.join(path,'knossos.conf'))
        else:
            print "no knossos file"

        numFoldersX = len(listDirX)
        firstXIndex = listDirX.index('x0000')
        listDirY = os.listdir(os.path.join(path, listDirX[firstXIndex]))
        numFoldersY = len(listDirY)
        firstYIndex = listDirY.index('y0000')
        listDirZ = os.listdir(os.path.join(path, 'x0000',listDirY[firstYIndex]))
        numFoldersZ = len(listDirZ)

        # x folder might have other files, removing them
        listDirX = removeNonFolders(path,listDirX)
        #print '----------------------------',listDirX


        # now the HDF part
        # numFoldersX-1 because there is the knossfile in the X folder
        totalChunks = numpy.array([numFoldersZ, numFoldersY, numFoldersX])
        cubeDims = numpy.array([128, 128, 128]);  # assuming this from the knossos
       

        chunkSize = numpy.array([64,64, 64])
        
        cubeLength = 1
        cubeLength*= numpy.prod(cubeDims[:])

        if len(startix)==0:
            startix = [0, 0, 0]
        if len(endix) == 0:
            endix = totalChunks.copy() # to have x y z order
        
        startix = numpy.array(startix)
        endix = numpy.array(endix)
        regionShape = tuple((endix-startix)*cubeDims)
        
        if writeOrder=='xyz':
           regionShape = regionShape[::-1]
           regionInfo = "x%d-%d" %(startix[2], endix[2]) + "_y%d-%d" %(startix[1], endix[1])+ "_z%d-%d" %(startix[0],endix[0])
           #print 'none is done'
        elif writeOrder=='zyx':
            # do nothing
            regionInfo = "z%d-%d" %(startix[0],endix[0]), "_y%d-%d" %(startix[1], endix[1]), "_x%d-%d" %(startix[2],endix[2])
        else:
            print writeOrder+'... not known'
        
        
    


        h5Group = '/G1';
        now = datetime.datetime.now()
        dateNow = now.strftime("%Y%m%d_%H%M%S")
        h5DataSet =   h5Group+ "/"+dateNow
        
        h5FileName    = os.path.join(path,inf['exp_name']+dateNow+'-'+regionInfo+".h5")

        f = h5py.File(h5FileName)


        print 'regionShape=',regionShape, 'chunkSize=',chunkSize
        print numpy.rank(regionShape)
        print numpy.rank(chunkSize)
        dset = f.create_dataset(name=h5DataSet,shape=tuple(regionShape), dtype='uint8',data=None,chunks=tuple(chunkSize), compression=1)
            #dset = f.create_dataset(name=h5DataSet,shape=[numFoldersZ, numFoldersY],dtype='uint8', data=None,chunks=tuple(cubeDims), maxshape = None)#, compression='gzip')


        dset.attrs.create("CLASS","IMAGE")
        dset.attrs.create("IMAGE_VERSION","1.2")
        dset.attrs.create("Region Info", regionInfo)
        
        dset.attrs.create("RegionInfo",regionInfo)
        #This is copied from h5 file tracking data. It adds axistags for ilastik
        # otherwise it assumes an xyz order.
        if writeOrder=='zyx':
            dset.attrs.create("axistags",'''{
            "axes": [
            {
              "key": "z",
              "typeFlags": 8,
              "resolution": 0,
              "description": ""
            },
            {
              "key": "y",
              "typeFlags": 2,
              "resolution": 0,
              "description": ""
            },
            {
              "key": "x",
              "typeFlags": 2,
              "resolution": 0,
              "description": ""
            }
          ]
        }''')


        dset_x= 0
        for x in range(startix[2], endix[2]):
            dset_y = 0
            for y in range(startix[1], endix[1]):
                dset_z =0
                for z in range(startix[0], endix[0]):
                    bWritten = False
    #                if x != 6 or y != 12 or z != 35:
    #                    continue

                    filedir =  os.path.join(path,listDirX[x],listDirY[y],listDirZ[z])
                    if (os.path.isdir(filedir)):
                        filename = inf['exp_name']+"_"+listDirX[x]+"_" +listDirY[y]+"_"+listDirZ[z]+".raw"
                        fullfile = os.path.join(filedir,filename)
                        print 'read',filename,'\n'
                        if(os.path.isfile(fullfile)):
                            print x,y,z
                            cube_file = open(fullfile, 'r', 128*128*128)
                            #print cube_file.name
                            cube_data = numpy.fromfile(fullfile, 'uint8', -1)
                            cube_file.close()
                            if(len(cube_data)==cubeLength):
                                 donothing = 1
                            else:
                                cube_data = numpy.concatenate([cube_data, zeros(cubeLength-len(cube_data),'uint8')])
                            if writeOrder=='zyx':
                               cube_data3d = cube_data.reshape(128,128,128)
                            elif writeOrder =='xyz':
                                # must be able to combine both not sure
                               cube_data3dt = cube_data.reshape(128,128,128).transpose()
                               cube_data3d = cube_data3dt


                            destPos = numpy.array([dset_x,dset_y, dset_z])
                            bWritten= writeInChunks(dset, cube_data3d, destPos, chunkSize, writeOrder)
                       # end of Z loop
                    if(bWritten):
                        dset_z+= cubeDims[2]
                # end of Y loop
                if(bWritten):
                    dset_y+=cubeDims[1]
            # end of X loop
            if(bWritten):
                dset_x +=cubeDims[0]









        f.close()
        # or do below to close the file
        listids = h5py.h5f.get_obj_ids()
        for idx in listids:
            idx.close()




