#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 09:19:29 2020

@author: grotheer
"""
import numpy as np
import seaborn as sns
#import afqbrowser as afq
#from afqbrowser import browser
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat
from matplotlib.lines import Line2D
import pylab as plot
from numpy.matlib import repmat
from itertools import repeat

T1Inter=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/interMeanR1MRI0AcrForPy.mat')
T1InterSe=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/interSeR1MRI0AcrForPy.mat')
T1Slope=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/slopeMeanR1AcrForPy.mat')
T1SlopeSe=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/slopeSeR1AcrForPy.mat')
Tracts=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/tractsAcrForPy.mat')
Nodes=loadmat('/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/nodesAcrForPy.mat')

df=pd.DataFrame(T1Inter['meanMRI0R1'])
df.columns=['R1Inter']
df.insert(1,"R1InterSe",T1InterSe['seMRI0R1'])
df.insert(2,"R1Slope",T1Slope['slopeMeanR1'])
df.insert(3,"R1SlopeSe",T1SlopeSe['slopeSeR1'])
df.insert(4,"tractIdx",Tracts['tracts'])
df.insert(5,"Nodes",Nodes['nodes'])


tracts=['ATR', 'ATR', 'CS', 'CS', 'CC', 'CC',
        'CH', 'CH', 'FcMa', 'FcMi','IFOF', 'IFOF',
        'ILF', 'ILF', 'SLF', 'SLF','UCI', 'UCI', 
        'AF', 'AF', 'MLF','MLF', 'VOF', 'VOF', 'pAF', 'pAF']

tractPos = {'CS': (0, 0), 'ATR': (0, 1),'VOF': (2, 3), 'pAF': (2, 4),
           'SLF': (1, 0), 'CC': (1, 1),'ILF': (1, 2), 'MLF': (1, 3),'IFOF': (1, 4),
           'AF': (2, 0), 'UCI': (2, 1),'FcMa': (0,3),'FcMi':(0,4)}


figsize=(15,10)
fig, axes=plt.subplots(3,5,frameon=False,figsize=figsize)
fig.tight_layout
plt.subplots_adjust(left=0.09,bottom=0.07,right=0.90,top=0.95,wspace=0.1,hspace=1)

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
sns.palplot(color_list_chosen)
sns.palplot(color_list_all)



x_labels=['Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (inf -> sup)','Node (inf -> sup)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (lh -> rh)','Node (lh -> rh)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (pos -> ant)', 'Node (pos -> ant)',
          'Node (inf -> sup)','Node (inf -> sup)',
          'Node (inf -> sup)','Node (inf -> sup)']

params={'legend.fontsize':12,'legend.handlelength':1,'legend.labelspacing':0.25, 'legend.columnspacing':0.25, 'legend.handletextpad':0}
plot.rcParams.update(params)

type=['mean']
hems=['LH']

for hem in hems:
    
    if hem=='LH':
        foi=[0,2,4,8,9,10,12,14,16,18,20,22,24]
    else:
        foi=[1,3,5,11,13,15,17,19,21,23,25]
    
    for t in type:
        for ct in foi:
  
            
            if ct==8:
                col=ct-2
            elif ct==9:
                col=col+2
            else:
                col=ct
                
            if hem=='RH':
                col=col-1
                
            colors=sns.color_palette("tab20")
            ax=axes[tractPos[tracts[ct]]]

            ax.clear()
            ax2=ax.twinx()
            ax.set_ylim([0.3,0.75])
            ax2.set_ylim([0.0005,0.001])
            ax.set_aspect(300)   
            
            
            if t=="mean":
                currentTract=df.query("tractIdx == @ct")

                g=sns.lineplot(x="Nodes", y="R1Inter",
                              data=currentTract,hue="tractIdx",
                              palette=[color_list_chosen[col+1]],
                              legend=False,ax=ax,style=True,alpha=0.75,linewidth=6)
                #g=ax.fill_between(currentTract['Nodes'],currentTract['R1Inter']-currentTract['R1InterSe'],currentTract['R1Inter']+currentTract['R1InterSe'],color=[color_list_chosen[col+1]],alpha=0.25)
                
                g=sns.lineplot(x="Nodes", y="R1Slope",
                              data=currentTract,hue="tractIdx",
                              palette=[color_list_chosen[col+1]],
                              legend=False,ax=ax2,style=True,alpha=0.75,dashes=[(2,2)],linewidth=6)
                #g=ax2.fill_between(currentTract['Nodes'],currentTract['T1Slope']-currentTract['T1SlopeSe'],currentTract['T1Slope']+currentTract['T1SlopeSe'],color=[color_list_chosen[col+1]],alpha=0.25)

                if ct!=8 and ct!=9:
                    tr=ct+1
                    currentTract=df.query("tractIdx == @tr")
                    g=sns.lineplot(x="Nodes", y="R1Inter",
                                  data=currentTract,hue="tractIdx",
                                  palette=[color_list_chosen[col+1]],
                                  legend=False,ax=ax,style=True,alpha=0.75,linewidth=6)
                   # g=ax.fill_between(currentTract['Nodes'],currentTract['T1Inter']-currentTract['T1InterSe'],currentTract['T1Inter']+currentTract['T1InterSe'],color=[color_list_chosen[col+1]],alpha=0.25)

                    g=sns.lineplot(x="Nodes", y="R1Inter",
                                  data=currentTract,hue="tractIdx",
                                  palette=[color_list_chosen[col+1]],
                                  legend=False,ax=ax,style=True,alpha=0.75,linewidth=6)
                    #g=ax.fill_between(currentTract['Nodes'],currentTract['T1Inter']-currentTract['T1InterSe'],currentTract['T1Inter']+currentTract['T1InterSe'],color=[color_list_chosen[col+1]],alpha=0.25)
                    
                    g=sns.lineplot(x="Nodes", y="R1Slope",
                                  data=currentTract,hue="tractIdx",
                                  palette=[color_list_chosen[col+1]],
                                  legend=False,ax=ax2,style=True,alpha=0.75,dashes=[(2,2)],linewidth=6)
                    #g=ax2.fill_between(currentTract['Nodes'],currentTract['T1Slope']-currentTract['T1SlopeSe'],currentTract['T1Slope']+currentTract['T1SlopeSe'],color=[color_list_chosen[col+1]],alpha=0.25)


                ax.set_title(tracts[ct],fontsize=25)
                ax.set_xlabel(x_labels[ct],fontsize=18)
                
                
                axes[0, 2].axis("off")
                axes[2, 2].axis("off")
                
                
            if ct == 2 or ct==14 or ct==18:
                ax.set_ylabel('R1 in newborns [1/s]',fontsize=18)
                ax.set_yticks([0.4,0.5, 0.6])
                ax.set_yticklabels([0.4,0.5, 0.6],Fontsize=16)
                
            else:
                ax.set_ylabel('',fontsize=14)
                ax.set_yticks([0.4,0.5, 0.6])
                ax.set_yticklabels([])
                ax.spines['left'].set_visible(False)
                ax2.spines['left'].set_visible(False)
 
            if ct==10 or ct==9 or ct==24:
                ax2.set_ylabel('R1 Slope [1/s/days]',fontsize=18)
                ax2.set_yticks([0.0001,0.002])
                ax2.set_yticklabels([0.0001, 0.002],Fontsize=16)
            else:
                ax2.set_ylabel('',fontsize=14)
                ax2.set_yticks([0.0001,0.002])
                ax2.set_yticklabels([])
                ax.spines['right'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                

                

                #plt.locator_params(axis='both', nbins=0.5)
            if hem=='RH':
                    axes[0, 2].axis("off")
                    axes[2, 2].axis("off")          
                
            ax.set_xticks([1,50,100])
            ax.set_xticklabels([1,50,100],Fontsize=18)
            ax.spines['top'].set_visible(True)
            ax2.spines['top'].set_visible(True)
            ax.tick_params(axis='y',which='both',left=False,right=False)
            ax2.tick_params(axis='y',which='both',left=False,right=False)
            ax.tick_params(axis='x',which='both',bottom=False,top=False)
            ax2.tick_params(axis='x',which='both',bottom=False,top=False)
            
            line1=Line2D([],[],color=color_list_chosen[col+1],linestyle='-')
            line2=Line2D([],[],color=color_list_chosen[col+1],linestyle='dashed')

            ax.legend([line1,line2],['0m','slope'],loc="upper left",borderpad=0.01,bbox_to_anchor=(0.15,0.99),ncol=2,framealpha=0.75,frameon=True,edgecolor=[1,1,1],prop={'size':16},fancybox=True,handlelength=1.5)
     
            fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output/Fig4_R1`.png",format='png',dpi=300)
                
 