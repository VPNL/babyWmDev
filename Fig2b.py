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
import statsmodels.formula.api as smf

slopeT1Mean=loadmat('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/slopeT1ForPy.mat')
slopeT1Se=loadmat('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/slopeSeT1ForPy.mat')
interT1Mean=loadmat('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/interT1MRI0ForPy.mat')
interT1Se=loadmat('/share/kalanit/biac2/kgs/projects/babybrains/mri/code//babyDWI/CatchUp/Data/interSeT1MRI0ForPy.mat')

tracts=[0,1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
df=pd.DataFrame(interT1Mean['meanMRI0'])
df.columns=['inter']
df.insert(1,"interSe",interT1Se['seMRI0'])
df.insert(2,"slope",slopeT1Mean['slopeMeanT1'])
df.insert(3,"slopeSe",slopeT1Se['slopeSeT1'])
df.insert(4,"tractIdx",tracts)
          
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

params={'legend.fontsize':12,'legend.handlelength':1,'legend.labelspacing':0.25, 'legend.columnspacing':0.25, 'legend.handletextpad':0}
plot.rcParams.update(params)
plot.rcParams["xtick.labeltop"]
plot.rcParams["xtick.top"]

c=color_list_chosen
tracts=['','CS','ATR','VOF','pAF','Fc','AF','UCI','SLF','CC','ILF','MLF','IFOF']
x=np.arange(14)
width = 0.45
figsize=(4,4.5)
fig, ax=plt.subplots(figsize=figsize)
plt.subplots_adjust(left=0.3,bottom=0.1,right=1,top=0.84,wspace=0.3,hspace=0.01)
foi=[2,0,22,24,8,18,16,14,4,12,20,10]
hems=['LH','RH']

counter=0

for ct in foi:
    if ct!=8:
        m="X"
    else:
        m="d"
        
    counter=counter+1
    col=ct  
    currentTract=df.query("tractIdx == @ct")
    p=sns.scatterplot(x="inter", y="slope",
    data=currentTract,hue="tractIdx",
    palette=[color_list_chosen[col]],
    legend=False,ax=ax,marker=m,s=100,alpha=1)
    p=plt.errorbar(currentTract["inter"], currentTract["slope"],xerr=currentTract["interSe"],yerr=currentTract["slopeSe"],
                   ecolor=color_list_chosen[col],fmt='none',alpha=0.5)
    ct=ct+1
    
    if ct!=9:
        col=ct
        m="o"
    else:
        col=ct-3
        m="d"
        
           
    currentTract=df.query("tractIdx == @ct")
    p=sns.scatterplot(x="inter", y="slope",
        data=currentTract,hue="tractIdx",
        palette=[color_list_chosen[col]],
        legend=False,ax=ax,marker=m,s=100,alpha=1)
    
    p=plt.errorbar(currentTract["inter"], currentTract["slope"],xerr=currentTract["interSe"],yerr=currentTract["slopeSe"],
                   ecolor=color_list_chosen[col],fmt='none',alpha=0.5)

 
m,b=np.polyfit(df["inter"],df["slope"],1)
weights=np.polyfit(df["inter"],df["slope"],1)
model=np.poly1d(weights)
results=smf.ols(formula='slope~model(inter)',data=df).fit()
print(results.summary())


xVal=np.array(df["inter"])
        
p=sns.lineplot(xVal, m*xVal+b,data=df,legend=False,ax=ax,alpha=0.25,linewidth=3,color=[0,0,0])

xVal=np.array([1.5,1.75,2,2.5,1.25,1.5,1.75,2,2.5,2.75])       
ax.set_ylabel('T1 Slope [s/days]',fontsize=20)
ax.xaxis.set_label_position('top')
ax.yaxis.set_label_position('left')
ax.set_xlabel('T1 in newborns [s]',fontsize=20)
ax.set_ylim(-0.005, -0.002)
ax.set_xlim(1.80,2.7)
ax.set_xticks([2,2.5])
ax.xaxis.set_ticks_position('top')
ax.yaxis.set_ticks_position('left')
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticklabels([2,2.5],color=[0,0,0],fontsize=16)
ax.set_yticks([-0.005,-0.003])
ax.set_yticklabels([-0.005,-0.003],color=[0,0,0],fontsize=16)

line1=Line2D([],[],color='w',linestyle='',marker='o',markerfacecolor=[0.5,0.5,0.5],markersize=10)
line2=Line2D([],[],color='w',linestyle='',marker="X",markerfacecolor=[0.5,0.5,0.5],markersize=10)
line3=Line2D([],[],color='w',linestyle='',marker="d",markerfacecolor=[0.5,0.5,0.5],markersize=10)
ax.legend([line1,line2],['LH','RH'],loc="lower left",bbox_to_anchor=(0.65,0.70),ncol=1,frameon=False,prop={'size':16},fancybox=True,handlelength=1.5)

fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Output/Fig2b.png",format='png',hue=[0,1,7,8]) 