#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 09:43:16 2020

@author: grotheer
"""

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat
from matplotlib.lines import Line2D
from matplotlib import markers
import pylab as plot

Md=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/MeanMdForPy.mat')
age=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/AgeForPy.mat')
tracts=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/tractVecForPy.mat')

xReg=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/xRegMdForPy.mat')
yReg=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/yRegMdForPy.mat')
tReg=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/python/data/tractRegMdForPy.mat')

yRegLower=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/yLowerRegMdForPy.mat')
yRegUpper=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/yUpperRegMdForPy.mat')

df=pd.DataFrame(age['age'])
df.columns=['age']
df.insert(1,"tractIdx",tracts['tractVec'])
df.insert(2,"Md",Md['Md_mean_all'])

dfReg=pd.DataFrame(xReg['x'])
dfReg.columns=['xReg']
dfReg.insert(1,"tractIdx",tReg['z'])
dfReg.insert(2,"yReg",yReg['y'])
dfReg.insert(3,"yRegLower",yRegLower['yLower'])
dfReg.insert(4,"yRegUpper",yRegUpper['yUpper'])


tracts=['ATR', 'ATR', 'CS', 'CS', 'CC', 'CC',
        'CH', 'CH', 'FcMa', 'FcMi','IFOF', 'IFOF',
        'ILF', 'ILF', 'SLF', 'SLF','UCI', 'UCI', 
        'AF', 'AF', 'MLF','MLF', 'VOF', 'VOF', 'pAF', 'pAF']

tractPos = {'CS': (0, 0), 'ATR': (0, 1),'VOF': (0, 6), 'pAF': (0, 7),'FcMa': (0,3),'FcMi':(0,4),
           'SLF': (1, 3), 'CC': (1, 4),'ILF': (1, 5), 'MLF': (1, 6),'IFOF': (1, 7),'AF': (1, 0), 'UCI': (1, 1)}
           

color_list_all=sns.color_palette("tab20")+sns.color_palette("tab20b") 
color_list_chosen=color_list_all[0:6]
color_list_chosen.extend(color_list_all[33:34])
color_list_chosen.extend(color_list_all[35:36])
color_list_chosen.extend(color_list_all[6:14]) 
color_list_chosen.extend(color_list_all[16:20]) 
color_list_chosen.extend(color_list_all[24:25]) 
color_list_chosen.extend(color_list_all[27:28]) 
color_list_chosen.extend(color_list_all[20:21]) 
color_list_chosen.extend(color_list_all[23:24])   
color_list_chosen.extend(color_list_all[36:37])
color_list_chosen.extend(color_list_all[39:40])

params={'legend.fontsize':12,'legend.handlelength':1,'legend.labelspacing':0.25, 'legend.columnspacing':0.25, 'legend.handletextpad':0}
plot.rcParams.update(params)

foi=[0,2,4,8,9,10,12,14,16,18,20,22,24]


figsize=(15,6)
fig, axes=plt.subplots(2,8,frameon=False,figsize=figsize)
fig.tight_layout
plt.subplots_adjust(left=0.1,bottom=0.01,right=0.99,top=1,wspace=0.1,hspace=0.1)
sns.despine()

hems=['LH','RH']

for hem in hems:
    
    if hem=='LH':
        foi=[0,2,4,8,9,10,12,14,16,18,20,22,24]

    elif hem=='RH':
        foi=[1,3,5,11,13,15,17,19,21,23,25]
            
            
    for ct in foi:
        
        if hem=='LH':
            col=ct
            m="o"
           # d=[(0,0)]
        else:
            col=ct
            m="X"
            #d=[(1,1)]
            
        if ct==8:
            col=ct
            m="D"
        elif ct==9:
            col=ct-3
            m="D"
        else: col=ct
        

        
                    
        ax=axes[tractPos[tracts[ct]]]
        ax.set_ylim([0.0009,0.0017])
        ax.set_aspect(250000)   
        
        
        currentTract=dfReg.query("tractIdx == @ct")
        g=ax.fill_between(currentTract['xReg'],currentTract['yRegLower'],currentTract['yRegUpper'],alpha=0.15,color=[0.5, 0.5, 0.5])

        
        g=sns.lineplot(x="xReg", y="yReg",
        data=currentTract,hue="tractIdx",
        palette=[color_list_chosen[col]],
        legend=False,ax=ax)
        
        currentTract=df.query("tractIdx == @ct")
        plt=sns.scatterplot(x="age", y="Md",
        data=currentTract,hue="tractIdx",
        palette=[color_list_chosen[col]],
        legend=False,ax=ax,marker=m)
    
    
        ax.set_title(tracts[ct],fontsize=20)
        ax.set_xlabel('age [days]',fontsize=14)
        
        if ct == 2 or ct==3 or ct==22 or ct==23 or ct==8 or ct==18 or ct==19 or ct==14 or ct==15:
            #ax.set_ylabel('Md [mm2/s]',fontsize=14)
            ax.set_ylabel(r'MD [mm$\mathregular{^{2}}/s$]',fontsize=14)
            ax.set_yticks([0.0011,0.0015])
            ax.set_yticklabels([0.0011,0.0015],color=[0,0,0])
            ax.set_xticklabels([0,1,100,200],color=[0,0,0])
        else:
            ax.set_ylabel('',fontsize=14)
            ax.set_yticklabels([])
            ax.set_xticklabels([0,1,100,200],color=[0,0,0])
            ax.spines['left'].set_visible(False)
            ax.tick_params(axis='y',which='both',left=False,right=False)
            
        axes[0, 2].axis("off")
        axes[0, 5].axis("off")
        axes[1, 2].axis("off")
        
        if ct!=8 and ct !=9:
            line1=Line2D([],[],color='w',linestyle=':',marker='o',markerfacecolor=color_list_chosen[col-1],markersize=10)
            line2=Line2D([],[],color='w',linestyle='dashed',marker="X",markerfacecolor=color_list_chosen[col],markersize=10)
            ax.legend([line1,line2],['LH','RH'],loc="lower left",bbox_to_anchor=(0.60,0.60),ncol=1,frameon=False,prop={'size':12},fancybox=True,handlelength=1.5)
                                
fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output/Fig2a_MD.png",format='png')       