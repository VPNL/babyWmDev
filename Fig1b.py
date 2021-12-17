#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:32:08 2020

@author: grotheer
"""
# import all the dependencies
import numpy as np
import os
import nibabel as nb
import matplotlib.pyplot as plt 
import seaborn as sns
import scipy
import statsmodels.api as sm
import pandas as pd
from statsmodels.formula.api import ols


#set up the data structure
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

#load the data and compute DCs
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

#prepare the colors for the figure
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

#make the actual plot

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


box1=ax.bar(x[0]-(width/2),adultData[0],width,linewidth=50,color=color_list_chosen[0],yerr=adultSEM[0],ecolor=color_list_chosen[0],capsize=5,alpha=0.65)
box2=ax.bar(x[0]+(width/2),babyData[0],width,linewidth=50,color=color_list_chosen[1],yerr=babySEM[0],ecolor=color_list_chosen[1],capsize=5,alpha=0.65)
box3=ax.bar(x[1]-(width/2),adultData[1],width,linewidth=50,color=color_list_chosen[2],yerr=adultSEM[1],ecolor=color_list_chosen[2],capsize=5,alpha=0.65)
box4=ax.bar(x[1]+(width/2),babyData[1],width,linewidth=50,color=color_list_chosen[3],yerr=babySEM[1],ecolor=color_list_chosen[3],capsize=5,alpha=0.65)
box5=ax.bar(x[2]-(width/2),adultData[2],width,linewidth=50,color=color_list_chosen[4],yerr=adultSEM[2],ecolor=color_list_chosen[4],capsize=5,alpha=0.65)
box6=ax.bar(x[2]+(width/2),babyData[2],width,linewidth=50,color=color_list_chosen[5],yerr=babySEM[2],ecolor=color_list_chosen[5],capsize=5,alpha=0.65)
box7=ax.bar(x[3]-(width/2),adultMeansLH[3],width,linewidth=50,color=color_list_chosen[8],yerr=adultSeLH[3],ecolor=color_list_chosen[8],capsize=5,alpha=0.65)
box8=ax.bar(x[3]+(width/2),babyMeansLH[3],width,linewidth=50,color=color_list_chosen[9],yerr=babySeLH[3],ecolor=color_list_chosen[9],capsize=5,alpha=0.65)
box9=ax.bar(x[4]-(width/2),adultMeansRH[3],width,linewidth=50,color=color_list_chosen[6],yerr=adultSeRH[3],ecolor=color_list_chosen[6],capsize=5,alpha=0.65)
box10=ax.bar(x[4]+(width/2),babyMeansRH[3],width,linewidth=50,color=color_list_chosen[7],yerr=babySeRH[3],ecolor=color_list_chosen[7],capsize=5,alpha=0.65)
box11=ax.bar(x[5]-(width/2),adultData[4],width,linewidth=50,color=color_list_chosen[10],yerr=adultSEM[4],ecolor=color_list_chosen[10],capsize=5,alpha=0.65)
box12=ax.bar(x[5]+(width/2),babyData[4],width,linewidth=50,color=color_list_chosen[11],yerr=babySEM[4],ecolor=color_list_chosen[11],capsize=5,alpha=0.65)
box13=ax.bar(x[6]-(width/2),adultData[5],width,linewidth=50,color=color_list_chosen[12],yerr=adultSEM[5],ecolor=color_list_chosen[12],capsize=5,alpha=0.65)
box14=ax.bar(x[6]+(width/2),babyData[5],width,linewidth=50,color=color_list_chosen[13],yerr=babySEM[5],ecolor=color_list_chosen[13],capsize=5,alpha=0.65)
box15=ax.bar(x[7]-(width/2),adultData[6],width,linewidth=50,color=color_list_chosen[14],yerr=adultSEM[6],ecolor=color_list_chosen[14],capsize=5,alpha=0.65)
box16=ax.bar(x[7]+(width/2),babyData[6],width,linewidth=50,color=color_list_chosen[15],yerr=babySEM[6],ecolor=color_list_chosen[15],capsize=5,alpha=0.65)
box17=ax.bar(x[8]-(width/2),adultData[7],width,linewidth=50,color=color_list_chosen[16],yerr=adultSEM[7],ecolor=color_list_chosen[16],capsize=5,alpha=0.65)
box18=ax.bar(x[8]+(width/2),babyData[7],width,linewidth=50,color=color_list_chosen[17],yerr=babySEM[7],ecolor=color_list_chosen[17],capsize=5,alpha=0.65)
box19=ax.bar(x[9]-(width/2),adultData[8],width,linewidth=50,color=color_list_chosen[18],yerr=adultSEM[8],ecolor=color_list_chosen[18],capsize=5,alpha=0.65)
box20=ax.bar(x[9]+(width/2),babyData[8],width,linewidth=50,color=color_list_chosen[19],yerr=babySEM[8],ecolor=color_list_chosen[19],capsize=5,alpha=0.65)
box21=ax.bar(x[10]-(width/2),adultData[9],width,linewidth=50,color=color_list_chosen[24],yerr=adultSEM[9],ecolor=color_list_chosen[24],capsize=5,alpha=0.65)
box22=ax.bar(x[10]+(width/2),babyData[9],width,linewidth=50,color=color_list_chosen[25],yerr=babySEM[9],ecolor=color_list_chosen[25],capsize=5,alpha=0.65)


s1=ax.scatter([x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2),x[0]-(width/2)],(DC_adultAFQ_lh[0]+DC_adultAFQ_rh[0])/2,color=color_list_chosen[0])
s2=ax.scatter([x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2),x[0]+(width/2)],(DC_babyAFQ_lh[0]+DC_babyAFQ_rh[0])/2,color=color_list_chosen[1])
s3=ax.scatter([x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2),x[1]-(width/2)],(DC_adultAFQ_lh[1]+DC_adultAFQ_rh[1])/2,color=color_list_chosen[2])
s4=ax.scatter([x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2),x[1]+(width/2)],(DC_babyAFQ_lh[1]+DC_babyAFQ_rh[1])/2,color=color_list_chosen[3])
s5=ax.scatter([x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2),x[2]-(width/2)],(DC_adultAFQ_lh[2]+DC_adultAFQ_rh[2])/2,color=color_list_chosen[4])
s6=ax.scatter([x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2),x[2]+(width/2)],(DC_babyAFQ_lh[2]+DC_babyAFQ_rh[2])/2,color=color_list_chosen[5])
s7=ax.scatter([x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2),x[3]-(width/2)],DC_adultAFQ_lh[3],color=color_list_chosen[8])
s8=ax.scatter([x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2),x[3]+(width/2)],DC_babyAFQ_lh[3],color=color_list_chosen[9])
s9=ax.scatter([x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2),x[4]-(width/2)],DC_adultAFQ_rh[3],color=color_list_chosen[6])
s10=ax.scatter([x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2),x[4]+(width/2)],DC_babyAFQ_rh[3],color=color_list_chosen[7])
s11=ax.scatter([x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2),x[5]-(width/2)],(DC_adultAFQ_lh[4]+DC_adultAFQ_rh[4])/2,color=color_list_chosen[10])
s12=ax.scatter([x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2),x[5]+(width/2)],(DC_babyAFQ_lh[4]+DC_babyAFQ_rh[4])/2,color=color_list_chosen[11])
s13=ax.scatter([x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2),x[6]-(width/2)],(DC_adultAFQ_lh[5]+DC_adultAFQ_rh[5])/2,color=color_list_chosen[12])
s14=ax.scatter([x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2),x[6]+(width/2)],(DC_babyAFQ_lh[5]+DC_babyAFQ_rh[5])/2,color=color_list_chosen[13])
s15=ax.scatter([x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2),x[7]-(width/2)],(DC_adultAFQ_lh[6]+DC_adultAFQ_rh[6])/2,color=color_list_chosen[14])
s16=ax.scatter([x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2),x[7]+(width/2)],(DC_babyAFQ_lh[6]+DC_babyAFQ_rh[6])/2,color=color_list_chosen[15])
s17=ax.scatter([x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2),x[8]-(width/2)],(DC_adultAFQ_lh[7]+DC_adultAFQ_rh[7])/2,color=color_list_chosen[16])
s18=ax.scatter([x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2),x[8]+(width/2)],(DC_babyAFQ_lh[7]+DC_babyAFQ_rh[7])/2,color=color_list_chosen[17])
s19=ax.scatter([x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2),x[9]-(width/2)],(DC_adultAFQ_lh[8]+DC_adultAFQ_rh[8])/2,color=color_list_chosen[18])
s20=ax.scatter([x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2),x[9]+(width/2)],(DC_babyAFQ_lh[8]+DC_babyAFQ_rh[8])/2,color=color_list_chosen[19])
s21=ax.scatter([x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2),x[10]-(width/2)],(DC_adultAFQ_lh[9]+DC_adultAFQ_rh[9])/2,color=color_list_chosen[24])
s22=ax.scatter([x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2),x[10]+(width/2)],(DC_babyAFQ_lh[9]+DC_babyAFQ_rh[9])/2,color=color_list_chosen[25])


ax.set_ylabel('dice coefficient',Fontsize=26)
ax.set_ylim(0, 1)

ax.set_xticks(x)
ax.set_xticklabels(labels,Fontsize=26)
ax.legend(frameon=False)

#save the plot
fig.savefig("/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output/Fig1b.png",format='png')

