%%
% The goals of this simulation are:
% (1) to understand how  myelin fraction (m) and change in myelin fraction (dm)
% affect R1/T1  and change in these variables dR1/dT1 
% (2) to simulate if we can use R1 and T1 to test developmental hypotheses
% h1: Starts first/finishes first: dm is positively correlated with myelination at birth => that is voxels that are earlier developed will continue to develop at a faster rate
% h2: Speed up: dm is negatively correlated with myelination at birth => that is voxels that are earlier developed will continue to develop at a faster rate
% h3: No relation to myelin at birth. Here we implemented dm constant, as it is independent from the myelin level at birth
% 
% Note that myelin fraction at birth (m) and developmental change in myelin fraction (dm) are independent variables
% that we are trying to assess experimentally by either measuring R1 or T1. 
%
% So the question is whether we can use R1 or T1 or both to measure the
% rate of myelination and if it varies with myelin level at birth
%
% To assess this I calculated
% R1(m) and T1(m) as a function of myelin fraction (m)
% The derivative of R1 and T1 
% dR1(m) and dT1(m) as a fucntion of myelin fraction (m)
% and the relation between change in dR1(m) and dT1(m) and R1(m) or T1(m) at birth
%
% The simiulation assumes a simple voxel with 2 components water and myelin
% that affect relaxation times. 
%
% Simulation done to address reviewer's comment for the revision of babyAFQ paper
%
% KGS April 2021
% Revised August 2021
%
%% Let our voxel have 2 components; water and myelin.
% The myelin fraction is m: 0<m<1
% Let's generate voxels with different fractions of myelin

m=[10^-6, 10^-5, 10^-4, 10^-3, 0.01:.01:0.5];

% R1 relaxation rates of water R1w and myelin R1m at 3T units [1/s]
R1w=0.25; %numbers from Aviv
R1m=2.8;

%% Voxel relaxation rate R1 is linear with myelin fraction (m)

figure('Color', [1 1 1], 'Units', 'norm', 'Position', [0 0 .6 .8], 'Name', 'R1 & development');
subplot (2,2,1)
hold on; 

R1=R1w+(R1m-R1w)*(m);
plot (m,R1,'k-','LineWidth',3);

set(gca, 'Fontsize', 18);
xlabel('myelin fraction [m] in a voxel','Fontsize',18);
ylabel('R1 [s^{-1}]','Fontsize',18);

title(({'R1 is linearly related', 'to myelin fraction (m)'}),'Fontsize',16);


% Here's the calculation of dR1(m)/dm:
% The math shows that change in myelin induce constant change in voxel relaxation rate
% or that dR1(m)/dm = constant and it is not dependent on the myelin
% content. 
% Because dR1(m)/dm  is fixed and not dependent on myelin content
% we cannot assess from dR1 measurements changes in myelin (dm)
%
% Let's plot it!
%
% dm: change in myelin
% dR1dm: change in relaxation rate due to change in myelin
% dR1dm=R1m-R1w;
% This is a constant and should not be dependent on the amount of myelin
% but only on the difference in relaxation rate of myelin and water


%% plot relation between dR1dm and myelin level
% expected change in R1 constant:

subplot (2,2,2)
hold on; 
dR1dm=(R1m-R1w)*ones(size (m)); 
plot (m,dR1dm,'k-','LineWidth',3);
set(gca, 'Fontsize', 18);
xlabel('myelin fraction [m]','Fontsize',18);
ylabel('dR1/dm [s^{-1}/m]','Fontsize',18);
title (({'Change in myelin (dm) produces', 'constant change in R1 (dR1)'}),'Fontsize',16);

%% Now let's simulate our developmental hypotheses
% So far we have generated voxels with different fractions of myelin in
% them (m)
% We are interested to test 3 scenarios on the rate of myelin development
% (dm); 
% h1: Starts first finishes first: dm is positively correlated with myelination at birth; that is, voxels that are earlier developed will continue to develop at a faster rate
% h2: Speed up: dm is negative correlated with myelination at birth; that is, voxels that are earlier developed will continue to develop at a faster rate
% h3: No Relation to myelin at birth. Here we implemented dm constant, as it is independent from the myelin level at birth;
%

r=0.05; % scaling factor of developmental changes; here its a 5% effect

% h1 
dmh1=r*m; % positive with myelin fraction at birth

%h2
dmh2=r*(1-m); % negative with myelin fraction at birth

%h3
dmh3=.5*r*ones(size(m)); % constant

%let's plot
subplot (2,2,3)
hold on; 
% let's plot our hypothesies
plot (m,dmh1,'k-+','Markersize',8);
plot (m,dmh2,'b-o','Markersize',8);
plot (m,dmh3,'cd','Markersize',8);
%h=legend({'h1: start first/finish first', 'h2: speed up','h3: no relation'},'Location','northeast'); set(h,'box','off','FontSize',14 );

axis([0 max(m) 0 r]);
set(gca, 'Fontsize', 18);
xlabel('myelin at birth [m]','Fontsize',18);
ylabel('change in myelin [dm]','Fontsize',18);
title (({'Change in myelin (dm) relative', 'to inital myelin fraction (m)'}),'Fontsize',16);


%% Now let's calculate dR1 according to these 3 hypotheses

dR1=dmh1.*dR1dm;
dR2=dmh2.*dR1dm;
dR3=dmh3.*dR1dm;

% Now let's plot R1 change vs R1 at birth according to each hypothesis
subplot (2,2,4)

set(gca, 'Fontsize', 18);
hold on; box off;
R1birth=R1;
plot (R1birth,dR1,'k-+','Markersize',8);
plot (R1birth,dR2,'b-o','Markersize',8);
plot (R1birth,dR3,'cd','Markersize',8);
%h=legend({'h1: starts first/finishes first', 'h2: speed up','h3: no relation'},'Location','northeast'); set(h,'box','off','FontSize', 16);
xlabel('R1 at birth [s^{-1}]','Fontsize',18);
ylabel('dR1 [s^{-1}]','Fontsize',18);
title ({'Change in R1 relative to', 'intial R1 is distinct'},'Fontsize',16);

% :-)
% This plot shows that you can make infererences from this graph relating
% change of R1 to R1 in birth about changes in myelin as a function of
% myelin in birth because there is a 1-to-1 mapping between changes in R1
% and changes in myelin and each of the hypotheses produces a distinct
% prediction in the relation between change in R1 and R1 at birth


%% Now let's switch to T1
% Let's calculate T1  as a fraction of myelin fraction in a voxel (m)
% T1=a./(b+c*m); where a=T1w*T1m; b=T1m; c=T1w-T1m;

m=[0.03:.01:0.43]; % myelin fraction at birth; I made the smallest fraction a bit larger here to match the range of T1 measurements we obtainend

T1w=1/R1w;
T1m=1/R1m;

a=T1w*T1m;
b=T1m;
c=T1w-T1m;


figure('Color', [1 1 1], 'Units', 'norm', 'Position', [0 0 .6 .8],'Name', 'T1 & development');

% Let's plot T1 as a function of myelin 
subplot (2,2,1)
hold on; 
T1=a./(b+c*(m));
plot (m,T1,'k-','LineWidth',3);

set(gca, 'Fontsize', 18);
xlabel('myelin fraction in a voxel (m)','Fontsize',18);
ylabel('T1 [1/s]','Fontsize',18);
title ({'T1 is proporiton to',' 1/myelin fraction'},'Fontsize',16);

% Higher myelin content is associated with lower T1

%% Now let's caculate how the rate of myelin change affects T1 as a function of myelin fraction in a voxel or dT1(m)/dm
%
% Here's the calculation of dT1(m)/dm:
% dT1(m)/dm=-(a*c)/(b+cm)^2
% where
% a=T1w*T1m
% b=T1m;
% c=T1w-T1m
%
% It is interesting that a change in myelin (dm) affects T1 in a way that is dependent on the myelin level in the voxel. 
% In other words changes in the rate of T1 relaxation will depend on 2 independent variables:
% the myelin content (m) and the change in myelin content (dm)


% Let's plot dT1(m) as a function of myelin fraction in a voxel
subplot (2,2,2)
hold on; 
dT1dm=-a*c./((b+c*(m)).^2);
plot (m,dT1dm,'k-','LineWidth',3);

set(gca, 'Fontsize', 18);
xlabel('myelin fraction [m]','Fontsize',18);
ylabel('dT1/dm [s/m]','Fontsize',18);
titlestr=[{'Same change myelin produces greater reduction', 'in T1 with smaller myelin fraction'}];
title (titlestr ,'Fontsize',16);


%% Now let's simulate our developmental hypotheses
% So far we have generated voxels with different fractions of myelin in them (m)
% We are interested to test 3 scenarios on the rate of myelin development (dm): 
% h1: Starts first/finishes first: dm is positively correlated with myelination at birth => that is, voxels that are earlier developed will continue to develop at a faster rate
% h2: Speed up: dm is negative correlated with myelination at birth => that is, voxels that are earlier developed will continue to develop at a faster rate
% h3: No Relation: dm is constant and independent from the myelin level at birth;
%

r=0.05; % scaling factor of developmental changes; here its a 5% effect
% h1 
dmh1=r*m;
%h2
dmh2=r*(1-m);
%h3
dmh3=0.5*r*ones(size(m)); % constant


% let's plot our hypothesies
subplot (2,2,3)
hold on; 
plot (m,dmh1,'k-+','Markersize',8);
plot (m,dmh2,'b-o','Markersize',8);
plot (m,dmh3,'cd','Markersize',8);
%h=legend({'h1: starts first/finish first', 'h2: speed up','h3: no relation'},'Location','northeast'); set(h,'box','off','FontSize', 10);

axis([0 max(m) 0 r]);
set(gca, 'Fontsize', 18);
xlabel('myelin at birth [m]','Fontsize',18);
ylabel(' change in myelin [dm]','Fontsize',18);
title ([{'Change in myelin (dm) relative', 'to initial myelin fraction (m)'}],'Fontsize',16);

%% Let's calculate dT1 as a function of dm for each of these hypotheses
% to do that we do a point by point multiplication of the graphs of each
% hypotheses in subplot 2 3 4 with the graph of dT1/dm in subplot 2 3 2

dT1=dmh1.*dT1dm;
dT2=dmh2.*dT1dm;
dT3=dmh3.*dT1dm;

% Let's plot relationship between dT1 and T1 at birth according to 3 hypotheses
% Now let's see if we can test the developmental hypotheses by relating dT1
% to T1 at birth
% Let's plot this relationship

subplot (2,2,4)
hold on; 
T1birth=T1;
plot (T1birth,dT1,'k-+','Markersize',8);
plot (T1birth,dT2,'b-o','Markersize',8);
plot (T1birth,dT3,'cd','Markersize',8);
%h=legend({'h1: starts first/finish first', 'h2: speed up','h3: no relation'},'Location','southwest'); set(h,'box','off','FontSize', 10);

set(gca, 'Fontsize', 18);
xlabel('T1 at birth [s]','Fontsize',18);
ylabel('dT1[s]','Fontsize',18);
title ([{'Change in T1 relative to initial T1',' is not distinct for the 3 hypotheses'}],'Fontsize',16);

% :-( 
% you cannot compare dT1 to T1 at birth to distinguish developmental hypotheses
% as both h2 & h3 predict a negative correlation between these variables, 
% so they are not distinguishable
