%%% inter and slope across bundle
load('/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/slopeMeanT1AcrForPy.mat');
load('/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/interMeanT1MRI0AcrForPy.mat')
load('/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Data/tractsAcrForPy.mat');

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
[r,p]=corrcoef(meanMRI0(start:10:ending),slopeMeanT1(start:10:ending))

if n==1
meansAcr=meanMRI0(start:10:ending)
slopeAcr=slopeMeanT1(start:10:ending)
else%elseif cnt~=6 && cnt~=7
meansAcr=[meansAcr;meanMRI0(start:10:ending)] 
slopeAcr=[slopeAcr;slopeMeanT1(start:10:ending)]
end

n=n+1
end

t=repelem([1:24],10,1)
tracts=reshape(t,[240, 1])
t1atBirthVec=meansAcr([1:60, 81:260],1);
t1Slope=slopeAcr([1:60, 81:260],1);

    tbl= table(t1atBirthVec, t1Slope, tracts,'VariableNames',{'t1atBirthVec','t1Slope','tracts'})
    lme1= fitlme(tbl,'t1Slope~ 1+ t1atBirthVec')
    lme2= fitlme(tbl,'t1Slope~ 1 + t1atBirthVec +(1| tracts)')
    comp=compare(lme1,lme2)
    lme2= fitlme(tbl,'t1Slope~ 1+ t1atBirthVec +(1|tracts)')
    lme3= fitlme(tbl,'t1Slope~ 1 + t1atBirthVec +(1+ t1atBirthVec| tracts)')
    comp=compare(lme2,lme3)

    close all
colors=load('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/colors_final.csv')
c=repelem(colors,10,1)
s=scatter(meansAcr,slopeAcr,[],c,'filled')
alpha(s,0.5)
set(gca,'FontSize',20); box off; set(gca,'Linewidth',2);   
xlabel('T1 in newborns [s]','FontSize',22,'FontName','Arial');
ylabel('T1 Slope [s/days]','FontSize',22,'FontName','Arial');
ax = ancestor(s, 'axes')
ax.YAxis.Exponent = 0
%tickformat('%0.0f')
ylim([-0.006, -0.001])
xlim([1.6, 2.6])
pbaspect([1 1.5 1])
    hold on
    x(:) = t1atBirthVec; 
    for i=1:length(x)
    y(i) = lme2.Coefficients.Estimate(1) + x(i)*lme2.Coefficients.Estimate(2);
    end
    plot(x,y,'Linewidth',4,'Color',[0.5 0.5 0.5])
    
    cd('/share/kalanit/biac2/kgs/projects/babybrains/mri/code/babyDWI/CatchUp/Output')
    print(gcf, '-dtiff', 'Fig4b','-r600')
    
    
