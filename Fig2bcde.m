
clear all;
%load the slopes
load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Data/slopeR1ForPy.mat');
load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Data/slopeSeR1ForPy.mat');
load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Data/slopeMdForPy.mat');
load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Data/slopeSeMdForPy.mat');

%loop through the newborns and compute mean R1 and MD
fatDir=fullfile('/share/kalanit/biac2/kgs/projects/babybrains/mri/');

sessid={'bb04/mri0/dwi/' 'bb05/mri0/dwi/' 'bb07/mri0/dwi/',...
    'bb11/mri0/dwi/', 'bb12/mri0/dwi/' 'bb14/mri0/dwi',...
    'bb17/mri0/dwi/' 'bb18/mri0/dwi/' 'bb22/mri0/dwi',...
    'bb02/mri3/dwi/' 'bb04/mri3/dwi/' 'bb05/mri3/dwi/' 'bb07/mri3/dwi/',...
    'bb08/mri3/dwi/' 'bb11/mri3/dwi/' 'bb12/mri3/dwi/',...
    'bb14/mri3/dwi/' 'bb15/mri3/dwi/' 'bb18/mri3/dwi/',...
    'bb02/mri6/dwi/' 'bb04/mri6/dwi/' 'bb05/mri6/dwi/' 'bb07/mri6/dwi/' ,...
    'bb08/mri6/dwi/' 'bb11/mri5/dwi/' 'bb12/mri6/dwi/',...
    'bb14/mri6/dwi/' 'bb15/mri6/dwi/' 'bb19/mri6/dwi/'};

runName={'94dir_run1'};
t1_name=['t2_biascorr_acpc_masked.nii.gz'];

for s=1:9 
    close all;
    for r=1:length(runName)
        session=strsplit(sessid{s},'/')
        fgName=['WholeBrainFG_classified_withBabyAFQ_clean.mat']
        subject=session{1};
        age=session{2};
        anatid=strcat(subject,'/',age,'/preprocessed_acpc/')
        
          
        cd(fullfile(fatDir,sessid{s}, runName{r},'dti94trilin/fibers/afq'))
        qmr=load(strcat('TractQmr_withR1_masked_ventr_',fgName))
        
        if s<10
        mri0.R1(s,:)=qmr.R1Avg;
        mri0.Md(s,:)=qmr.MdAvg; 
        end
        clear qmr
    end
end

%%% Fib 2b R1
R1_mean_mri0=mean(mri0.R1*1000)
R1_se_mri0=std(mri0.R1*1000)/sqrt(8)
R1_mean_mri0=R1_mean_mri0(:,[1:6 9:26])'
R1_se_mri0=R1_se_mri0(:,[1:6 9:26])'

%rank ordered R1 in newborns
colors=load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/colors_final.csv');
c=colors([1:6 9 7 11:26],:)

[meanMri0R1_sorted,order]=sort(R1_mean_mri0,'descend');
R1_se_mri0_sorted=R1_se_mri0(order);
slopeR1_sorted=slopeMeanR1(order);
slopeR1_se_sorted=slopeSeR1(order);
colors_sorted=c(order,:);

fig = figure;
hold on 

x=1:24;
fig=errorbar(meanMri0R1_sorted,R1_se_mri0_sorted,'vertical','o','Color',[0.5,0.5,0.5],'LineWidth',1.5)
hold on
fig=scatter(x,meanMri0R1_sorted,50,colors_sorted,'filled')
set(gca,'FontSize',14); box off; set(gca,'Linewidth',2); 
xlabel('Bundles sorted by R1 in newborns','FontSize',16,'FontName','Arial');
ylabel('R1 in newborns [s^{-1}]','FontSize',16,'FontName','Arial');
xticklabels('')
ylim([0.4 0.58])
xlim([0, 25])
pbaspect([2.5 1 1])
cd('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output')
print(gcf, '-dtiff', 'Fig2b','-r600')
close all;

% Fig 2c R1 slopes
hold off
fig=errorbar(slopeR1_sorted,slopeR1_se_sorted,'vertical','.','Color',[0.5,0.5,0.5],'LineWidth',1.5)
hold on
fig=scatter(x,slopeR1_sorted,50,colors_sorted,'filled','^')

set(gca,'FontSize',14);  box off; set(gca,'Linewidth',2); 
xlabel('Bundles sorted by R1 in newborns','FontSize',16,'FontName','Arial');
ylabel('R1 slope [s^{-1}/d]','FontSize',16,'FontName','Arial');
ylim([0.0005 0.0015])
xlim([0, 25])
pbaspect([2.5 1 1])
cd('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output')
print(gcf, '-dtiff', 'Fig2c','-r600')
close all;


%%% Fib 2d Md
Md_mean_mri0=mean(mri0.Md)
Md_se_mri0=nanstd(mri0.Md)/sqrt(8)
Md_se_mri0=Md_se_mri0(:,[1:6 9:26])'
Md_mean_mri0=Md_mean_mri0(:,[1:6 9:26])'

%rank ordered Md intercepts
[meanMri0Md_sorted,order]=sort(Md_mean_mri0);
slopeMd_sorted=slopeMeanMd(order)
colors_sorted=c(order,:);
Md_se_mri0_sorted=Md_se_mri0(order);
slopeMd_se_sorted=slopeSeMd(order);
colors_sorted=c(order,:);
fig = figure;
x=1:24;
fig=errorbar(meanMri0Md_sorted,Md_se_mri0_sorted,'vertical','o','Color',[0.5,0.5,0.5],'LineWidth',1.5)
hold on
fig=scatter(x,meanMri0Md_sorted,50,colors_sorted,'filled')

set(gca,'FontSize',16); box off; set(gca,'Linewidth',2); 
xlabel('Bundles sorted by MD in newborns','FontSize',16,'FontName','Arial');
ylabel('MD in newborns [mm^{2}/s]','FontSize',16,'FontName','Arial');
xticklabels('')
ylim([0.00115 0.0016])
xlim([0, 25])
cd('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output/')
pbaspect([2.5 1 1])
print(gcf, '-dtiff', 'Fig2d','-r600')
close all;

%fig 2e MD slopes
hold off
fig=errorbar(slopeMd_sorted,slopeMd_se_sorted,'vertical','.','Color',[0.5,0.5,0.5],'LineWidth',1.5)
hold on
fig=scatter(x,slopeMd_sorted,50,colors_sorted,'filled','^')
set(gca,'FontSize',14);  box off; set(gca,'Linewidth',2); 
xlabel('Bundles sorted by MD in newborns','FontSize',16,'FontName','Arial');
ylabel('MD slope [mm^{2}/s/d]','FontSize',16,'FontName','Arial');
ylim([-0.000002 -0.0000005])
xlim([0, 25])
xticklabels('')
cd('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/babyWmDev/Output')
pbaspect([2.5 1 1])
print(gcf, '-dtiff', 'Fig2e','-r600')
close all;



