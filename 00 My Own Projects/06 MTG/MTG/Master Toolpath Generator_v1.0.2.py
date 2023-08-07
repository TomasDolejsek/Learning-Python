# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:54:56 2023

@author: cz055
"""

#%% Imports
import os
import re
from time import sleep
from math import remainder
import string


try:
    from scipy.io import loadmat
except:
    os.system('py -m pip install scipy')
    from scipy.io import loadmat
    
try:
    import pandas as pd
except:
    os.system('py -m pip install pandas')    
    import pandas as pd
    

#%% Definitions
def done(tim):
    sleep(tim)
    exit(0)
    
def fill_dash_com(stri):
    stri = "*' " + stri + " '*"
    stri.replace('\\\\', '\\')
    stri.replace('\\', chr(92))
    
    if remainder(len(stri),2) == 1:
        stri = stri[:3] + '-' + stri[3:]
    if len(stri)<132:
        maxIns = int((132 - len(stri))/2)
        Sstri = '-'
        for i in range(maxIns-1):
            Sstri = Sstri + '-'
        stri = stri[:3] + Sstri + stri[3:-3] + Sstri + stri[-3:] + '\n'
        
    return stri


#%% Main program

#%%% Path to the LA folder
#path = r'C:\Users\cz055\Documents\LA'



path = input('Insert the path for merging the toolpaths for Laser Ablation:\n')

while not os.path.isdir(path):
    path = input('\nThe path you have inserted is not valid. Insert the correct path:\n')
    
files = os.listdir(path)

RemFile = [x for x in files if 'remov' in x.lower()]
CleanFile = [x for x in files if 'clean' in x.lower()]

if not len(RemFile) and not len(CleanFile):
    print('\nThere are no files for Removal or Cleaning in the folder. The program will quit now.')
    done(5)

Mnr = input("Insert the mold number:\n")
#%%% Selection of Removal and/or Cleaning    
answ = input('\nPlease select the process.\n0\t- Exit the program\n1\t- Only removal\n2\t- Only cleaning\n3\t- Both removal and cleaning\n')


while answ not in [0,1,2,3]:
    print('\nThe process was selected incorrectly')
    answ = input('\nPlease select the process.\n0\t- Exit the program\n1\t- Only removal\n2\t- Only cleaning\n3\t- Both removal and cleaning\n')
    try:
        answ = int(answ)
    except:
        pass

if answ == 0:
    print('\nYou have selected and option to quit program. The program will quit now.')
    done(5)


#%%%Select Layout

path_to_layout = [r'Z:\CZ_Production\Prod_RW\Production', r'K:\R&D\Production']
pathLay = []
while pathLay not in path_to_layout:
    print('\n Select main path:\n')
    for i,x in enumerate(path_to_layout): 
        print(i,'\t',x) 
    answP = input()
    try:
        pathLay = path_to_layout[int(answP)]
    except:
        continue

# pathLay = r'Z:\CZ_Production\Prod_RW\Production'
# pathLay = r'K:\R&D\Production'


subfol = os.listdir(pathLay)
subfol = [x for x in subfol if os.path.isdir(os.path.join(pathLay,x))]
project = []
while project not in subfol:
    print('\n Select project:\n')
    for i,x in enumerate(subfol): 
        print(i,'\t',x) 
    answP = input()
    try:
        project = subfol[int(answP)]
    except:
        continue
pathLay = os.path.join(pathLay,project,'05 Layout')

subfol = os.listdir(pathLay)
subfol = [x for x in subfol if os.path.isdir(os.path.join(pathLay,x))]
layout = []
while layout not in subfol:
    print('\n Select layout:\n')
    for i,x in enumerate(subfol): 
        print(i,'\t',x) 
    answL = input()
    try:
        layout = subfol[int(answL)]
    except:
        continue
    
pathLay = os.path.join(pathLay,layout,'Layout Definition','Matlab','approved')
mat = [x for x in os.listdir(pathLay) if 'mat' in x]
if not len(mat):
    print('No matlab definition file was found. Make sure that it can be found in following location:\n')
    print(pathLay)
    done(20)
    
else:
    if len(mat) == 1:
        mat = mat[0]
    else:
        while not len(mat) == 1:
            print('\n Select matlab definition file:\n')
            for i,x in enumerate(mat): 
                print(i,'\t',x) 
            answL = input()
            try:
                mat = mat[int(answL)]
            except:
                pass

#%%%% Load Layout
matPath = os.path.join(pathLay,mat)
matdat = loadmat(matPath)

matDF = pd.DataFrame(matdat['def'])
matDF0 = matDF[0][0][0][0].tolist()
matDF1 = matDF[1][0][0][0].tolist()

matDF0_side = str(matDF0[3][0])
matDF1_side = str(matDF1[3][0])


sides = [matDF0_side, matDF1_side]

side = []
while side not in sides:
    print('\n Select side of layout:\n')
    for i,x in enumerate(sides): 
        print(i,'\t',x) 
    answS = input()
    try:
        side = sides[int(answS)]
    except:
        continue

if answS == 0:
    matDFU = matDF0
else:
    matDFU = matDF1


matDFU_pitch = matDFU[4][0][0]
matDFU_scaling= matDFU[5][0][0]
matDFU_xnormal = matDFU[6][0]
matDFU_ynormal = matDFU[7][0]
matDFU_type = matDFU[9][0]

matDFU_type = [str(x[0]) for x in matDFU_type]
types = set(matDFU_type)
# types.remove('k')

alphabet = list(string.ascii_lowercase)
typ_dict={}
for typ in alphabet:
    typ_dict[typ] = 0
#     print(typ)
#     print(len([x for x in matDFU_type if x == typ]))


matDFU_x = -matDFU_xnormal * matDFU_pitch * matDFU_scaling
matDFU_y = matDFU_ynormal * matDFU_pitch * matDFU_scaling

matDFU_position = []
matDFU_name = []

Ctyp = ['a','b','c','d','e','f','g']
Rtyp = ['x','y','z']



for i,typ in enumerate(matDFU_type):
    matDFU_name.append("{:0>3d}{}".format(i+1,typ))
    
    typ_dict[typ]= typ_dict[typ] + 1
    if typ in Ctyp:
        Csum = 0
        
        for ttyp in Ctyp:
            try:
                Csum = Csum + typ_dict[ttyp]
            except:
                pass
        matDFU_position.append([matDFU_x[i],matDFU_y[i], "{:0>3d}{}".format(i+1,typ),"C{:0>3d}{}".format(Csum,typ)])
    if typ in Rtyp:
        Rsum = 0
        for ttyp in Rtyp:
            try:
                Rsum = Rsum + typ_dict[ttyp]
            except:
                pass
        matDFU_position.append([matDFU_x[i],matDFU_y[i], "{:0>3d}{}".format(i+1,typ),"R{:0>3d}{}".format(Rsum,typ)])
    if typ not in ['a','b','c','d','e','f','g','x','y','z']:
        matDFU_position.append([matDFU_x[i],matDFU_y[i], "{:0>3d}{}".format(i+1,typ),"F{:0>3d}{}".format(typ_dict[typ],typ)])
    

# for idx in range(len(matDFU_x)):
#     matDFU_position.append([matDFU_x[i],matDFU_y[i], matDFU_name[idx],matDFU_name_type[idx]])
                           
# matDFU_position = np.array(matDFU_position)
# matDFU_position[matDFU_position[:, 0].argsort()]




#%%% Discarding/choosing the Removal and Cleaning toolpaths
RemFile_type_S = {}   
CleanFile_type_S = {}

if abs(remainder(answ, 2)) == 1:
    
    RemFile_types = []
    for typ in types:
        for RFile in RemFile:
            RF = re.search('type-'+typ,RFile)
            if RF:
                RemFile_types.append([typ,RFile])
    # npRemFile_typ = np.array(RemFile_typ)    
    missing = []
    for typ in types:
        RF_typ = [x for x in RemFile_types if typ in x[0]]
        if len(RF_typ)>1:
            answR = 'x'
            while answR not in list(range(0,len(RF_typ))):
                print("There are following files found in the selected folder. Which one is the correct one?")
                for i,x in enumerate(RF_typ):
                    print(i,'\t',x) 
                answR = input()
                try:
                    answR = int(answR)
                except:
                    pass
            RemFile_type_S[typ] = RF_typ[answR][1]
        elif len(RF_typ) ==1:
            RemFile_type_S[typ] = RF_typ[0][1]
        if len (RF_typ) == 0:
            RemFile_type_S[typ] = []
            missing.append(typ)
     
    if len(missing)>0:
        print('\nThere are some Removal toolpaths missing. Namely \t',missing)
        answR = 'x'
        while answR not in [0,1]:
            answR = input ('\nShould they be skipped?\n0\t- the program will quit\n1\t- Skip the toolpaths\n')
            try:
                answR = int(answR)
            except:
                pass
        if answR == 0:
            print('\nThe program will quit now.')
            done(5)
            
            
if answ > 1:
      
      CleanFile_types = []
      for typ in types:
          for CFile in CleanFile:
              CF = re.search('type-'+typ,CFile)
              if CF:
                  CleanFile_types.append([typ,CFile])
      # npRemFile_typ = np.array(RemFile_typ)      
      missing = []
      for typ in types:
          CF_typ = [x for x in CleanFile_types if typ in x[0]]
          if len(CF_typ)>1:
              answR = 'x'
              while answR not in list(range(0,len(CF_typ))):
                  print("There are following files found in the selected folder. Which one is the correct one?")
                  for i,x in enumerate(CF_typ):
                      print(i,'\t',x) 
                  answR = input()
                  try:
                      answR = int(answR)
                  except:
                      pass
              CleanFile_type_S[typ] = CF_typ[answR][1]
          elif len(CF_typ) ==1:
              CleanFile_type_S[typ] = CF_typ[0][1]
          if len (CF_typ) == 0:
              CleanFile_type_S[typ] = []
              missing.append(typ)
       
      if len(missing)>0:
          print('\nThere are some Cleaning toolpaths missing. Namely \t',missing)
          answR = 'x'
          while answR not in [0,1]:
              answR = input ('\nShould they be skipped?\n0\t- the program will quit\n1\t- Skip the toolpaths\n')
              try:
                  answR = int(answR)
              except:
                  pass
          if answR == 0:
              print('\nThe program will quit now.')
              done(5)
              
            
#%%% Position manipulation (rotation, translation)        

trans = 'x'
while type(trans) != float:
    print("\nWhat is the half size of the mold (distance from vision markers' mirror surface to the center of the mold) in [mm]?\n")
    trans = input()
    try:
        trans = float(trans)
    except:
        continue

matDFU_position_Trans = [[x[0], float(x[1])-trans, x[2], x[3]] for x in matDFU_position]

trans = 'x'
while type(trans) != float:
    print('\nWhat is the z-correction from CMM in [mm]?\n')
    trans = input()
    try:
        trans = float(trans)
    except:
        continue

matDFU_position_Trans = [[x[0], float(x[1])+trans, x[2], x[3]] for x in matDFU_position_Trans]


trans = 'x'
while type(trans) != float:
    print('\nWhat is the y-correction from CMM in [mm]?\n')
    trans = input()
    try:
        trans = float(trans)
    except:
        continue

matDFU_position_Trans = [[float(x[0])+trans, x[1], x[2], x[3]] for x in matDFU_position_Trans]


flip = 'x'
while flip not in [0,1]:
    print('\n Should the orientation be flipped?\n')
    print("0\t - No rotation\n")
    print("1\t - 90 deg CW rotation\n")
    flip = input()
    try:
        flip = int(flip)
    except:
        continue
    
if flip:
    matDFU_position_Flip=[]
    for idx in range(len(matDFU_position_Trans)):
        matDFU_position_Flip.append([matDFU_position_Trans[idx][1], -matDFU_position_Trans[idx][0], matDFU_position_Trans[idx][2], matDFU_position_Trans[idx][3]])
else:
    matDFU_position_Flip = matDFU_position_Trans    

matDFU_position_Flip = sorted(matDFU_position_Flip, key=lambda a_entry: a_entry[flip], reverse= 0 )
matDFU_position_Flip = sorted(matDFU_position_Flip, key=lambda a_entry: a_entry[abs(flip-1)], reverse= 0 )


            
#%%% File manipulations

#%%%% Removal toolpath
Removal_file = {}
for typ in types:
    try:
        with open(os.path.join(path,RemFile_type_S[typ]),'r') as f:
             fil = f.readlines()
             for idx in range (len(fil)-1,0,-1):
                 if 'Xaxis' in fil[idx] or 'Yaxis' in fil[idx]:
                     fil.pop(idx)
                 if 'Param' in fil[idx]:
                     Pidx = idx
             for idx in range (Pidx,0,-1):
                 fil.pop(idx)
    except:
        fil = []   
    
    Removal_file[typ] = fil
    del(fil)
    
#%%%% Cleaning toolpath
Cleaning_file = {}
for typ in types:
    try:
        with open(os.path.join(path,CleanFile_type_S[typ]),'r') as f:
             fil = f.readlines()
             for idx in range (len(fil)-1,0,-1):
                 if 'Xaxis' in fil[idx] or 'Yaxis' in fil[idx]:
                     fil.pop(idx)
                 if 'Param' in fil[idx]:
                     Pidx = idx
             for idx in range (Pidx,0,-1):
                 fil.pop(idx)
    except:
        fil = []   
    
    Cleaning_file[typ] = fil
    del(fil)
  
#%%% Master toolpath contruction

with open(os.path.join(path,' '.join([project, side, Mnr, layout,'Master Toolpath.bia'])),'w') as f:
    f.write(fill_dash_com('Master Toolpath'))
    f.write(fill_dash_com('Created using program by JDV'))
    f.write("\n")
    f.write("\n")


    for value in matDFU_position_Flip:
        if abs(remainder(answ, 2)) == 1:
            if len(Removal_file[value[-1][-1]]): 
                pathFile = '_'.join([os.path.join(path,value[-1]),'Removal.bia'])
                f.write(fill_dash_com("START JOB {} {}".format(value[-1],"Removal")))
                f.write("\n")
                f.write("*Param=Removal*\n")
                f.write("\n")
                f.write("*Xaxis={}*\n".format(value[0]))
                f.write("*Yaxis={}*\n".format(value[1]))
                        
                for line in Removal_file[value[-1][-1]]:
                    f.write(line)
                
                f.write("\n")
                f.write("\n")
                f.write("*WriteTimeReport={}*".format(pathFile))
                f.write("\n")
                f.write(fill_dash_com("END JOB {} {}".format(value[-1],"Removal")))
                f.write("\n")
                f.write("\n")
                
        if answ > 1:
            if len(Cleaning_file[value[-1][-1]]): 
                pathFile = '_'.join([os.path.join(path,value[-1]),'Cleaning.bia'])
                f.write(fill_dash_com("START JOB {} {}".format(value[-1],"Cleaning")))
                f.write("\n")
                f.write("*Param=Cleaning*\n")
                f.write("\n")
                f.write("*Xaxis={}*\n".format(value[0]))
                f.write("*Yaxis={}*\n".format(value[1]))
                        
                for line in Cleaning_file[value[-1][-1]]:
                    f.write(line)
                
                f.write("\n")
                f.write("\n")
                f.write("*WriteTimeReport={}*".format(pathFile))
                f.write("\n")
                f.write(fill_dash_com("END JOB {} {}".format(value[-1],"Cleaning")))
                f.write("\n")
                f.write("\n")
                
