clear all;
fatDir=fullfile('Z:\biac2\kgs\projects\babybrains\mri\');

sessid={'bb04\mri0\dwi\' 'bb05\mri0\dwi\' 'bb07\mri0\dwi\',...
    'bb11\mri0\dwi\', 'bb12\mri0\dwi\' 'bb14\mri0\dwi',...
    'bb17\mri0\dwi\' 'bb18\mri0\dwi\' 'bb22\mri0\dwi',...
    'bb02\mri3\dwi\' 'bb04\mri3\dwi\' 'bb05\mri3\dwi\' 'bb07\mri3\dwi\',...
    'bb08\mri3\dwi\' 'bb11\mri3\dwi\' 'bb12\mri3\dwi\',...
    'bb14\mri3\dwi\' 'bb15\mri3\dwi\' 'bb18\mri3\dwi\',...
    'bb02\mri6\dwi\' 'bb04\mri6\dwi\' 'bb05\mri6\dwi\' 'bb07\mri6\dwi\' ,...
    'bb08\mri6\dwi\' 'bb11\mri5\dwi\' 'bb12\mri6\dwi\',...
    'bb14\mri6\dwi\' 'bb15\mri6\dwi\' 'bb19\mri6\dwi\'};


runName={'94dir_run1'};
t1_name=['t2_biascorr_acpc_masked.nii.gz'];

for s=1:9%:length(sessid) %done is: 4,6
    close all;
    for r=1:length(runName)
        session=strsplit(sessid{s},'\')
        fgName=['WholeBrainFG_classified_withBabyAFQ_clean.mat']
        subject=session{1};
        age=session{2};
        anatid=strcat(subject,'\',age,'\preprocessed_acpc\')
        
        
        cd(fullfile(fatDir,sessid{s}, runName{r},'dti94trilin\fibers\afq'))
        qmr=load(strcat('TractQmr_withR1_masked_ventr_',fgName))
        
        idx=0
        nodes=[1:10:100]
        for bundles = [1:6 9:26]
            idx=idx+1
            x_coor_acrossS(:,idx,s)=qmr.SuperFiber(bundles).fibers{1,1}(1,nodes);
            y_coor_acrossS(:,idx,s)=qmr.SuperFiber(bundles).fibers{1,1}(2,nodes);
            z_coor_acrossS(:,idx,s)=qmr.SuperFiber(bundles).fibers{1,1}(3,nodes);
            Md_acrossS(:,idx,s)=qmr.MdAcrNodes(nodes,bundles);
        end
    end
end

x_coor=mean(x_coor_acrossS,3);
y_coor=mean(y_coor_acrossS,3);
z_coor=mean(z_coor_acrossS,3);
Md=mean(Md_acrossS,3);
load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/slopeMeanMdAcrForPy.mat');
Md_slopes_all=slopeMeanMd([1:600, 801:2600],1);
Md_slopes=Md_slopes_all(1:10:2400,1);

colors=load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/colors_final.csv')
c=colors([1:6 9:26],:)
c_rep=repelem([c(:,1),c(:,2),c(:,3)],10,  1)
scatter3(abs(x_coor(:)),y_coor(:),z_coor(:),70,c_rep,'filled')    % draw the scatter plot
ax = gca;
xlabel('x')
ylabel('y')
zlabel('z')
set(gca,'FontSize',20);  box off; set(gca,'Linewidth',2);
colorbar
hold on

%% Md at mri0
%Md=Md/1000
colormap(hot)
caxis([min(Md(:))+0.0001,max(Md(:))+0.0001])
scatter3(abs(x_coor(:)),y_coor(:),z_coor(:),70,Md(:),'filled')    % draw the scatter plot
ax = gca;
colorbar;
xlabel('x')
ylabel('y')
zlabel('z')
xlim([min(abs(x_coor(:))),max(abs(x_coor(:)))])
ylim([min(y_coor(:)),max(y_coor(:))])
zlim([min(z_coor(:)),max(z_coor(:))])
colorbar('off')
%% Md slope
colormap(hot)
caxis([min(Md_slopes(:)),max(Md_slopes(:))])
scatter3(abs(x_coor(:)),y_coor(:),z_coor(:),70,Md_slopes(:),'filled')    % draw the scatter plot
ax = gca;
colorbar
colorbar('on');

%% Fit a linear model
t=repelem([1:24],10,1)
TractsVec=reshape(t,[240, 1])
MdatBirthVec=Md(:);
MdSlopesVec=Md_slopes(:);
xVec=zscore(abs(x_coor(:)));
yVec=zscore(y_coor(:));
zVec=zscore(z_coor(:));

    tbl= table(MdSlopesVec, MdatBirthVec, TractsVec, xVec, yVec, zVec,...
        'VariableNames',{'MdSlope','MdatBirth','Tract','x','y','z'})
    
    
    %without bundle
    tractLME=fitlme(tbl,'MdSlope~ 1+ Tract')
    
    birthDevLME=fitlme(tbl,'MdSlope~ 1+ R1atBirth + (1|Tract)')
    
    spatialY=fitlme(tbl,'MdSlope~ 1 + y')
    spatialZ=fitlme(tbl,'MdSlope~ 1 + z')
    spatialX=fitlme(tbl,'MdSlope~ 1 + x')
    spatialLME=fitlme(tbl,'MdSlope~ 1 + x + y + z + x*y + x*z + y*z + (1|Tract)')
    
    comp=compare(spatialY,spatialLME)
    
    combined = fitlme(tbl,'MdSlope~ 1 + MdatBirth + x + y + z + x*y + x*z + y*z + (1|Tract)')
    comp=compare(spatialLME,combined)
    