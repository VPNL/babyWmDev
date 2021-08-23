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

mri0T1=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri0MdForPy.mat')
mri0Tracts=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri0TractsForPy.mat')
mri0Subj=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri0SubjForPy.mat')
mri0Nodes=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri0NodesForPy.mat')

mri3T1=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri3MdForPy.mat')
mri3Tracts=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri3TractsForPy.mat')
mri3Subj=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri3SubjForPy.mat')
mri3Nodes=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri3NodesForPy.mat')

mri6T1=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri6MdForPy.mat')
mri6Tracts=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri6TractsForPy.mat')
mri6Subj=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri6SubjForPy.mat')
mri6Nodes=loadmat('/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Data/mri6NodesForPy.mat')

df0=pd.DataFrame(mri0Subj['mri0_subj'])
df0.columns=['Subj']
df0.insert(1,"tractIdx",mri0Tracts['mri0_tracts'])
df0.insert(2,"Nodes",mri0Nodes['mri0_nodes'])
df0.insert(3,"T1",mri0T1['mri0_Md'])

df3=pd.DataFrame(mri3Subj['mri3_subj'])
df3.columns=['Subj']
df3.insert(1,"tractIdx",mri3Tracts['mri3_tracts'])
df3.insert(2,"Nodes",mri3Nodes['mri3_nodes'])
df3.insert(3,"T1",mri3T1['mri3_Md'])

df6=pd.DataFrame(mri6Subj['mri6_subj'])
df6.columns=['Subj']
df6.insert(1,"tractIdx",mri6Tracts['mri6_tracts'])
df6.insert(2,"Nodes",mri6Nodes['mri6_nodes'])
df6.insert(3,"T1",mri6T1['mri6_Md'])


tracts=['ATR', 'ATR', 'CS', 'CS', 'CC', 'CC',
        'CH', 'CH', 'FcMa', 'FcMi','IFOF', 'IFOF',
        'ILF', 'ILF', 'SLF', 'SLF','UCI', 'UCI', 
        'AF', 'AF', 'MLF','MLF', 'VOF', 'VOF', 'pAF', 'pAF']

tractPos = {'CS': (0, 0), 'ATR': (0, 1),'VOF': (1, 3), 'pAF': (1, 4),
            'AF': (1, 0), 'UCI': (1, 1),'FcMa': (0,3),'FcMi':(0,4),
           'SLF': (2, 0), 'CC': (2, 1),'ILF': (2, 2), 'MLF': (2, 3),'IFOF': (2, 4)}


figsize=(15,10)
fig, axes=plt.subplots(3,5,frameon=False,figsize=figsize)
fig.tight_layout
plt.subplots_adjust(left=0.1,bottom=0.01,right=0.99,top=1,wspace=0.2,hspace=0.2)
sns.despine()

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
#sns.palplot(color_list_chosen)
sns.palplot(color_list_chosen)



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
                col=ct
            elif ct==9:
                col=col-2
            else:
                col=ct
                
            if hem=='RH':
                col=col-1
                
            colors=sns.color_palette("tab20")
            ax=axes[tractPos[tracts[ct]]]
            ax.clear()
            ax.set_ylim([0.0007,0.002])
            ax.set_aspect(60000)   
            
            if t=="mean":
                currentTract=df0.query("tractIdx == @ct")
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator='mean',ci=95,n_boot=1000,
                              palette=[color_list_chosen[col+1]],
                              legend=False,ax=ax,style=True,dashes=[(2,2)],alpha=0.5)
                
                if ct!=8 and ct!=9:
                    tr=ct+1
                    currentTract=df0.query("tractIdx == @tr")
                    plt=sns.lineplot(x="Nodes", y="T1",
                                  data=currentTract,hue="tractIdx",
                                  estimator='mean',ci=95,n_boot=1000,
                                  palette=[color_list_chosen[col+1]],
                                  legend=False,ax=ax,style=True,dashes=[(2,2)],alpha=0.5)
                    
                
                currentTract=df3.query("tractIdx == @ct")
                sns.set(rc={"lines.linewidth": 3})
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator='mean',ci=95,n_boot=1000,
                              palette=[np.mean([color_list_chosen[col+1],color_list_chosen[col]],axis=0)],
                              legend=False,ax=ax,style=True,dashes=[(4,4)],alpha=0.5)
                
                if ct!=8 and ct!=9:
                    tr=ct+1
                    currentTract=df3.query("tractIdx == @tr")
                    sns.set(style="ticks",rc={"lines.linewidth": 3})
                    plt=sns.lineplot(x="Nodes", y="T1",
                                  data=currentTract,hue="tractIdx",
                                  estimator='mean',ci=95,n_boot=1000,
                                  palette=[np.mean([color_list_chosen[col+1],color_list_chosen[col]],axis=0)],
                                  legend=False,ax=ax,style=True,dashes=[(4,4)],alpha=0.5)
                
                
                currentTract=df6.query("tractIdx == @ct")
                sns.set(style="ticks",rc={"lines.linewidth": 3})
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator='mean',ci=95,n_boot=1000,
                              palette=[color_list_chosen[col]],legend=False,ax=ax,alpha=0.5)
                
                if ct!=8 and ct!=9:
                    tr=ct+1
                    currentTract=df6.query("tractIdx == @tr")
                    sns.set(style="ticks",rc={"lines.linewidth": 3})
                    plt=sns.lineplot(x="Nodes", y="T1",
                                  data=currentTract,hue="tractIdx",
                                  estimator='mean',ci=95,n_boot=1000,
                                  palette=[color_list_chosen[col]],legend=False,ax=ax,alpha=0.5)
                
                
                line1=Line2D([],[],color=color_list_chosen[col],linestyle=':')
                line2=Line2D([],[],color=color_list_chosen[col],linestyle='dashed')
                line3=Line2D([],[],color=color_list_chosen[col],linestyle='-')
                ax.legend([line1,line2,line3],['0m','3m','6m'],loc="upper left",bbox_to_anchor=(0.3,0.22),ncol=3,frameon=False,prop={'size':12},fancybox=True,handlelength=1.5)
        	       
                ax.set_title(tracts[ct],fontsize=25)
                ax.set_xlabel(x_labels[ct],fontsize=20)

                if ct == 2 or ct==14 or ct==18 or ct==8 or ct==22 :
                    ax.set_ylabel(r'MD [mm$\mathregular{^{2}}/s$]',fontsize=20)
                    ax.set_yticks([0.001,0.002])
                    ax.set_yticklabels([0.001,0.002],Fontsize=18)
                else:
                    ax.set_ylabel('',fontsize=14)
                    ax.set_yticks([0.001,0.002])
                    ax.set_yticklabels([],Fontsize=18)
                    ax.spines['left'].set_visible(False)

                ax.set_xticks([1,50,100])
                ax.set_xticklabels([1,50,100],Fontsize=18)
                ax.tick_params(axis='y',which='both',left=False,right=False)
                ax.tick_params(axis='x',which='both',bottom=False,top=False)
            

                axes[0, 2].axis("off")
                axes[1, 2].axis("off")                
                fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/plotting/figs/linePlot_"+t+'_'+hem+"_masked.png",format='png')
                
            else:
               # ax.set_ylim([1,1.8])
                #ax.set_aspect(35)
                #ax.set_ylim([1,2.8])
                sns.set(rc={"lines.linewidth": 2})
                currentTract=df0.query("tractIdx == @ct")
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator=None,units='Subj',
                              palette=[color_list_chosen[col+1]],
                              legend=False,ax=ax,style=True,dashes=[(2,2)])
                
                currentTract=df3.query("tractIdx == @ct")
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator=None,units='Subj',
                              palette=[np.mean([color_list_chosen[col+1],color_list_chosen[col]],axis=0)],
                              legend=False,ax=ax,style=True,dashes=[(4,4)])
                
                currentTract=df6.query("tractIdx == @ct")
                plt=sns.lineplot(x="Nodes", y="T1",
                              data=currentTract,hue="tractIdx",
                              estimator=None,units='Subj',
                              palette=[color_list_chosen[col]],legend=False,ax=ax)
                
                line1=Line2D([],[],color=color_list_chosen[col],linestyle=':')
                line2=Line2D([],[],color=color_list_chosen[col],linestyle='dashed')
                line3=Line2D([],[],color=color_list_chosen[col],linestyle='-')
                ax.legend([line1,line2,line3],['0m','3m','6m'],loc="upper left",borderpad=0.01,bbox_to_anchor=(0.1,0.2),ncol=3,framealpha=0.75,frameon=True,edgecolor=[1,1,1],prop={'size':12},fancybox=True,handlelength=1.5)
                    		   
                ax.set_title(tracts[ct],fontsize=20)
                ax.set_xlabel(x_labels[ct],fontsize=14)
                ax.set_ylabel('MD [mm2/s]',fontsize=14)
                axes[0, 2].axis("off")
                axes[1, 2].axis("off")
            
                
                if hem=='RH':
                    axes[1, 3].axis("off")
                    axes[1, 4].axis("off")
                    
    fig.savefig("/biac2/kgs/Another link to babybrains/mri/code/babyDWI/babyWmDev/Output/Fig3_MD.png",format='png')
    #fig.clf()
    #fig
