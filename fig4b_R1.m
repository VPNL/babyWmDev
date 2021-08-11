%%% inter and slope across bundle
load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/slopeMeanR1AcrForPy.mat');
load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/interMeanR1MRI0AcrForPy.mat')
load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/python/data/tractsAcrForPy.mat');

%extract only every 10th node
n=1
for cnt=[0,2,4,6,8,9,10,12,14,16,18,20,22,24]
    if cnt ~=8 && cnt~=9
start=min(find(tracts==cnt | tracts==cnt+1))
ending=max(find(tracts==cnt | tracts==cnt+1))
    else
  start=min(find(tracts==cnt))
ending=max(find(tracts==cnt))
    end
[r,p]=corrcoef(meanMRI0R1(start:10:ending),slopeMeanR1(start:10:ending))

if n==1
meansAcr=meanMRI0R1(start:10:ending)
slopeAcr=slopeMeanR1(start:10:ending)
else%elseif cnt~=6 && cnt~=7
meansAcr=[meansAcr;meanMRI0R1(start:10:ending)] 
slopeAcr=[slopeAcr;slopeMeanR1(start:10:ending)]
end

n=n+1
end

t=repelem([1:24],10,1)
tracts=reshape(t,[240, 1])
R1atBirthVec=meansAcr([1:60, 81:260],1);
R1Slope=slopeAcr([1:60, 81:260],1);

    tbl= table(R1atBirthVec, R1Slope, tracts,'VariableNames',{'R1atBirthVec','R1Slope','tracts'})
    lme1= fitlme(tbl,'R1Slope~ 1+ R1atBirthVec')
    lme2= fitlme(tbl,'R1Slope~ 1 + R1atBirthVec +(1| tracts)')
    comp=compare(lme1,lme2)
    lme2= fitlme(tbl,'R1Slope~ 1+ R1atBirthVec +(1|tracts)')
    lme3= fitlme(tbl,'R1Slope~ 1 + R1atBirthVec +(1+ R1atBirthVec| tracts)')
    comp=compare(lme2,lme3)

    close all
colors=load('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/colors_final.csv')
c=repelem(colors,10,1)
s=scatter(meansAcr,slopeAcr,[],c,'filled')
alpha(s,0.5)

%ax.YAxis.Exponent = 0
set(gca,'FontSize',20); box off; set(gca,'Linewidth',2); 
ax.XAxis.Exponent = 0
set(gca,'XAxisLocation','top')
set(gca,'YAxisLocation','left')
xlabel('R1 in newborns [1/s]','FontSize',22,'FontName','Arial');
ylabel('R1 Slope [1/s/days]','FontSize',22,'FontName','Arial');

%tickformat('%0.0f')
ylim([0.0003,0.0017])
xlim([0.35, 0.65])
pbaspect([1 1.5 1])
    hold on
    x(:) = R1atBirthVec; 
    for i=1:length(x)
    y(i) = lme2.Coefficients.Estimate(1) + x(i)*lme2.Coefficients.Estimate(2);
    end
    plot(x,y,'Linewidth',4,'Color',[0.5 0.5 0.5])
    
    [R,p]=corrcoef(R1atBirthVec, R1Slope);
    cd('Z:/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Output')
    print(gcf, '-dtiff', 'Fig4b_R1','-r600')
    
    
