#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:32:08 2020

@author: grotheer
"""
# import all the differt dependencies
import numpy as np
import os
import nibabel as nb
import matplotlib.pyplot as plt 
import seaborn as sns
import scipy
import statsmodels.api as sm
import pandas as pd
from statsmodels.formula.api import ols

fatDir='/share/kalanit/biac2/kgs/projects/babybrains/mri/';
print(fatDir)

sessid=['bb04/mri0/dwi' ,'bb05/mri0/dwi','bb07/mri0/dwi',
    'bb11/mri0/dwi', 'bb12/mri0/dwi', 'bb14/mri0/dwi',
    'bb17/mri0/dwi', 'bb18/mri0/dwi', 'bb22/mri0/dwi']

tract_names=['TR', 'TR', 'CS', 'CS', 'CC', 'CC', 'FMa', 'FMi', 'IFOF', 'IFOF', 'ILF', 'ILF', 'SLF', 'SLF',
    'UCI', 'UCI', 'AF', 'AF', 'pAF', 'pAF'];

os.chdir(fatDir+sessid[0]);

DC_babyAFQ_rh=np.empty([0,0]);
DC_adultAFQ_rh=np.empty([0,0]);
DC_babyAFQ_lh=np.empty([0,0]);
DC_adultAFQ_lh=np.empty([0,0]);

for s in range(0, 9): #the subject range
    
    for fiberNum in range(0, 20):  #the fascicle of interest with both hemispheres

        if fiberNum%2==0: 
            hem='lh';
        else:
            hem='rh';

        nii_manual=nb.load(fatDir+sessid[s]+'/94dir_run1/dti94trilin/fibers/afq/manual_tracts/'+hem+'_'+tract_names[fiberNum]+'.nii.gz')
        nii_babyAFQ=nb.load(fatDir+sessid[s]+'/94dir_run1/dti94trilin/fibers/afq/WholeBrainFG_classified_withBabyAFQ_clean_tracts/'+hem+'_'+tract_names[fiberNum]+'.nii.gz')
        nii_adultAFQ=nb.load(fatDir+sessid[s]+'/94dir_run1/dti94trilin/fibers/afq/WholeBrainFG_classified_clean_tracts/'+hem+'_'+tract_names[fiberNum]+'.nii.gz')
    
        idx_nii_manual=nii_manual.get_fdata()>0
        idx_nii_babyAFQ=nii_babyAFQ.get_fdata()>0
        idx_nii_adultAFQ=nii_adultAFQ.get_fdata()>0
    
        idx_overlap_babyAFQ = np.logical_and(idx_nii_manual, idx_nii_babyAFQ);
        idx_overlap_adultAFQ = np.logical_and(idx_nii_manual, idx_nii_adultAFQ);
    
        if hem=='rh':
            DC_babyAFQ_rh=np.append(DC_babyAFQ_rh,(2*idx_overlap_babyAFQ.sum())/(idx_nii_manual.sum()+idx_nii_babyAFQ.sum()))
            DC_adultAFQ_rh=np.append(DC_adultAFQ_rh,(2*idx_overlap_adultAFQ.sum())/(idx_nii_manual.sum()+idx_nii_adultAFQ.sum()))
        else:
            DC_babyAFQ_lh=np.append(DC_babyAFQ_lh,(2*idx_overlap_babyAFQ.sum())/(idx_nii_manual.sum()+idx_nii_babyAFQ.sum()))
            DC_adultAFQ_lh=np.append(DC_adultAFQ_lh,(2*idx_overlap_adultAFQ.sum())/(idx_nii_manual.sum()+idx_nii_adultAFQ.sum()))

DC_babyAFQ_lh=np.reshape(DC_babyAFQ_lh,[10,s+1],order='F')
DC_babyAFQ_rh=np.reshape(DC_babyAFQ_rh,[10,s+1],order='F')
DC_adultAFQ_lh=np.reshape(DC_adultAFQ_lh,[10,s+1],order='F')
DC_adultAFQ_rh=np.reshape(DC_adultAFQ_rh,[10,s+1],order='F')

fig, ax=plt.subplots()
labels=['ATR', 'CS', 'CC', 'FcMa', 'FcMi', 'IFOF', 'ILF', 'SLF', 'UCI', 'AF', 'pAF']


x=np.arange(len(labels))
width = 0.35

sns.set_context("notebook", font_scale=1.5)

#mean across Sbujects
babyMeans=[np.mean(DC_babyAFQ_lh,1), np.mean(DC_babyAFQ_rh,1)]
adultMeans=[np.mean(DC_adultAFQ_lh,1), np.mean(DC_adultAFQ_rh,1)]

babyMeansLH=np.mean(DC_babyAFQ_lh,1)
adultMeansLH=np.mean(DC_adultAFQ_lh,1)

babyMeansRH=np.mean(DC_babyAFQ_rh,1)
adultMeansRH=np.mean(DC_adultAFQ_rh,1)

babySe=[scipy.stats.sem(DC_babyAFQ_lh,1), scipy.stats.sem(DC_babyAFQ_rh,1)] 
adultSe=[scipy.stats.sem(DC_adultAFQ_lh,1), scipy.stats.sem(DC_adultAFQ_rh,1)] 

babySeLH=scipy.stats.sem(DC_babyAFQ_lh,1)
adultSeLH=scipy.stats.sem(DC_adultAFQ_lh,1)

babySeRH=scipy.stats.sem(DC_babyAFQ_lh,1)
adultSeRH=scipy.stats.sem(DC_adultAFQ_lh,1)

#mean across hemi
babyData=np.mean(babyMeans,0)
adultData=np.mean(adultMeans,0)

babySEM=np.mean(babySe,0)
adultSEM=np.mean(adultSe,0)
                    
babyData=babyData.squeeze()
adultData=adultData.squeeze()

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

ax.set_ylabel('dice coefficient')
ax.set_ylim(0, 1)

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(frameon=False)

fig.tight_layout()     

sns.despine()
plt.show()
ax.set_aspect(20)   
fig.savefig(fatDir+"code/babyDWI/plots/alltracts_plot",format='png')


figsize=(15,4)
fig, ax=plt.subplots(frameon=False,figsize=figsize)
fig.tight_layout
sns.despine()

box1=ax.bar(x[0]-(width/2),adultData[0],width,linewidth=50,color=color_list_chosen[0],yerr=adultSEM[0],ecolor=color_list_chosen[0],capsize=5)
box2=ax.bar(x[0]+(width/2),babyData[0],width,linewidth=50,color=color_list_chosen[1],yerr=babySEM[0],ecolor=color_list_chosen[1],capsize=5)
box3=ax.bar(x[1]-(width/2),adultData[1],width,linewidth=50,color=color_list_chosen[2],yerr=adultSEM[1],ecolor=color_list_chosen[2],capsize=5)
box4=ax.bar(x[1]+(width/2),babyData[1],width,linewidth=50,color=color_list_chosen[3],yerr=babySEM[1],ecolor=color_list_chosen[3],capsize=5)
box5=ax.bar(x[2]-(width/2),adultData[2],width,linewidth=50,color=color_list_chosen[4],yerr=adultSEM[2],ecolor=color_list_chosen[4],capsize=5)
box6=ax.bar(x[2]+(width/2),babyData[2],width,linewidth=50,color=color_list_chosen[5],yerr=babySEM[2],ecolor=color_list_chosen[5],capsize=5)
box7=ax.bar(x[3]-(width/2),adultMeansLH[3],width,linewidth=50,color=color_list_chosen[8],yerr=adultSeLH[3],ecolor=color_list_chosen[8],capsize=5)
box8=ax.bar(x[3]+(width/2),babyMeansLH[3],width,linewidth=50,color=color_list_chosen[9],yerr=babySeLH[3],ecolor=color_list_chosen[9],capsize=5)
box9=ax.bar(x[4]-(width/2),adultMeansRH[3],width,linewidth=50,color=color_list_chosen[6],yerr=adultSeRH[3],ecolor=color_list_chosen[6],capsize=5)
box10=ax.bar(x[4]+(width/2),babyMeansRH[3],width,linewidth=50,color=color_list_chosen[7],yerr=babySeRH[3],ecolor=color_list_chosen[7],capsize=5)
box11=ax.bar(x[5]-(width/2),adultData[4],width,linewidth=50,color=color_list_chosen[10],yerr=adultSEM[4],ecolor=color_list_chosen[10],capsize=5)
box12=ax.bar(x[5]+(width/2),babyData[4],width,linewidth=50,color=color_list_chosen[11],yerr=babySEM[4],ecolor=color_list_chosen[11],capsize=5)
box13=ax.bar(x[6]-(width/2),adultData[5],width,linewidth=50,color=color_list_chosen[12],yerr=adultSEM[5],ecolor=color_list_chosen[12],capsize=5)
box14=ax.bar(x[6]+(width/2),babyData[5],width,linewidth=50,color=color_list_chosen[13],yerr=babySEM[5],ecolor=color_list_chosen[13],capsize=5)
box15=ax.bar(x[7]-(width/2),adultData[6],width,linewidth=50,color=color_list_chosen[14],yerr=adultSEM[6],ecolor=color_list_chosen[14],capsize=5)
box16=ax.bar(x[7]+(width/2),babyData[6],width,linewidth=50,color=color_list_chosen[15],yerr=babySEM[6],ecolor=color_list_chosen[15],capsize=5)
box17=ax.bar(x[8]-(width/2),adultData[7],width,linewidth=50,color=color_list_chosen[16],yerr=adultSEM[7],ecolor=color_list_chosen[16],capsize=5)
box18=ax.bar(x[8]+(width/2),babyData[7],width,linewidth=50,color=color_list_chosen[17],yerr=babySEM[7],ecolor=color_list_chosen[17],capsize=5)
box19=ax.bar(x[9]-(width/2),adultData[8],width,linewidth=50,color=color_list_chosen[18],yerr=adultSEM[8],ecolor=color_list_chosen[18],capsize=5)
box20=ax.bar(x[9]+(width/2),babyData[8],width,linewidth=50,color=color_list_chosen[19],yerr=babySEM[8],ecolor=color_list_chosen[19],capsize=5)
box21=ax.bar(x[10]-(width/2),adultData[9],width,label='AFQ',linewidth=50,color=color_list_chosen[22],yerr=adultSEM[9],ecolor=color_list_chosen[22],capsize=5)
box22=ax.bar(x[10]+(width/2),babyData[9],width,label='babyAFQ',linewidth=50,color=color_list_chosen[23],yerr=babySEM[9],ecolor=color_list_chosen[23],capsize=5)


ax.set_ylabel('dice coefficient',Fontsize=26)
ax.set_ylim(0, 1)

ax.set_xticks(x)
ax.set_xticklabels(labels,Fontsize=26)
ax.legend(frameon=False)

fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Output/Fig1b.png",format='png')

