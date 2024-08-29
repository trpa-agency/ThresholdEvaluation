#  Exponential Growth State Space model:
#  Version Nov.28.2009
#
#  R program for calculating maximum likelihood (ML) and restricted maximum
#  likelihood (REML) estimates of unknown parameters for the Exponential
#  Growth State Space (EGSS) model of stochastic population growth.  
#  The model is
#
#  dX(t) = mu*dt + dB(t)
#               with dB(t) ~ normal(0,ssq*dt),
#  Y(t) = X(t) + F(t)
#               with F(t) ~ normal(0,tsq).
#
#  Here X(t) is log-population abundance, Y(t) is observed or estimated value
#  of X(t), x0, mu, ssq, tsq are parameters.  The parameter ssq is the
#  variance of the process noise, and tsq is the variance of the observation
#  error.
#
#  The model takes population abundance N(t) = exp(X(t)) to be governed by
#  a stochastic, density independent model, with the observed abundances
#  O(t) = N(t)*exp(F(t)) arising from lognormal sampling error.
#
#  User provides time series of observed population abundances o(0), o(1),
#  ..., o(q), which are log-transformed by the program into y(0), y(1), ...,
#  y(q), assumed to be a time series realization of Y(t).  Likelihood
#  function of y(0), y(1), ..., y(q) is that of a multivariate normal
#  distribution.  The observation times t_0, t_1, t_2, ..., t_q can have
#  unequal intervals.
#
#  Program computes initial parameter values for iterations.  The program
#  should be re-run for several sets of initial values, as the likelihood
#  function for the model frequently has multiple local maxima, see program
#  section 4.
#
#  Alternative programs, for observation times with equal intervals,
#  are available as an online appendix to Staples et al. (2004).
#  See also Staudenmayer and Buonaccorsi (2006) for a more theoretical
#  development.
#
#  Program citations:
#    Dennis et al. 2006.   Ecological Monographs.
#    Humbert et al. 2009.  Oikos.
#    Staples et al. 2004.  Ecology.
#    Staudenmayer and Buonaccorsi. 2006.  Biometrics.
#
6
#----------------------------------------------------------------------
#        1. USER INPUT SECTION
#----------------------------------------------------------------------
#  
#  The best way to conduct these analyses is by preparing data in Excel, then
#  saving as a text file.
# 
#  In Excel, in cell A1, type (Exactly) the word "Observed.t", without the
#  quotes. Put the observed abundance in column A, starting with row 2.
#  In cell B1, type (Exactly) the word "Time.t" without the quotes. Put the
#  time step identifiers that correspond to the observed population size in
#  column B, starting  with row 2.
#  Your first time step can be 0, or 1, or anything else (e.g. a year).
#
#  ** NOTE: If you have years with no data, that is fine.  
#  Just omit the year and the associated abundance. However, if you have a
#  year where you sampled but got zero abundance, you cannot use these
#  approaches. **
#
#  Once the data sheet is prepared in Excel, save it as on the C:\ drive
#  as "c:\my_data.txt". It must be a tab delimited text file. 
#  Excel may try to name it my_data.txt.txt or my_data.txt.xls but don't
#  let it! You can confirm that it is, indeed, a text file by double clicking
#  on it and confirming that it opens with Notepad, not Excel.
#
#  ** NOTE: You can change the drive or the name of the input file by
#  changing the second next line. ** 
rm(list=ls(all=TRUE))     
#  Clears all objects from memory

setwd("C:/Users/amcclary/Documents/Analysis/data")


# Read in data set
my_data <- read.csv("osprey.csv", header=T,sep=",")
head(my_data)

Observed.t <- my_data$Observed.t
Time.t <- my_data$Time.t
print.table(cbind(Observed.t,Time.t))

sink(file = "osprey_results.txt", append = FALSE, 
     type = "output", split = T) 
#  OUTPUT: 2 Files will go the same place as the input file:
# GRAPHICS           my_graph.png
# INTERPRET OUTPUT    my_results.txt
#  REST OF THIS SECTION CAN BE IGNORED IF USING EXCEL INPUT
#    Example data below are American Redstart counts from North American
#    Breeding Bird Survey, record # 02014 3328 08636, 1966-95 (Table 1 in
#    Dennis et al. 2006).
#    To run this example, comment out the 5 lines immediately
#    above this paragraph, using the pound sign, and uncomment the 4 lines 
#    immediately below this paragraph, but do not change anything outside 
#    of the user input section.  When you uncomment the lines below, remove
#    only the pound signs at the left side of this document.  Do not remove
#    the pound signs after the semicolons.
#  Observed.t=c(18,10,9,14,17,14,5,10,9,5,11,11,4,5,4,8,2,3,9,2,4,7,4,1,2,
#    4,11,11,9,6);     #  No zeros!  (With zeros, you must use another model)
#  Time.t=c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,

#    25,26,27,28,29);  #  Initial time can be nonzero.
#----------------------------------------------------------------------
#        2. PROGRAM INITIALIZATION SECTION
#----------------------------------------------------------------------  
library(MASS);            #  Loads miscellaneous functions (ginv, etc.)
T.t=Time.t-Time.t[1];     #  Time starts at zero.
Y.t=log(Observed.t);      #  Log-transform the observations.
q=length(Y.t)-1;          #  Number of time series transitions, q.
qp1=q+1;                  #  q+1 gets used a lot, too.
S.t=T.t[2:qp1]-T.t[1:q];  #  Time intervals.
m=rep(1,qp1);             #  Will contain Kalman means for Kalman calculations.
v=rep(1,qp1);             #  Will contain variances for Kalman calculations.

#  Tells the program where to write the output
#  ** CHANGE LINE ABOVE IF YOU WANT RESULTS TO GO SOMEWHERE OTHER THAN C:/ DRIVE
#----------------------------------------------------------------------
#        3. SECTION FOR DEFINING ML & REML LOG-LIKELIHOODS
#----------------------------------------------------------------------
#  ML objective function "negloglike.ml" is negative of log-likelihood;
#  the Nelder-Mead optimization routine in R, "optim", is a minimization
#  routine.  The ML objective function uses equations 24-26 from Dennis et
#  al. (2006).  The three function arguments are:  theta, vector of
#  parameters (transformed to the real line), yt, vector of time series
#  observations, and tt, vector of observation times.
negloglike.ml=function(theta,yt,tt)  
{
  muu=theta[1];
  sigmasq=exp(theta[2]);      #  Constrains ssq > 0. 
  tausq=exp(theta[3]);        #  Constrains tsq > 0.
  xzero=theta[4];
  q=length(yt)-1;
  qp1=q+1;
  yt=matrix(yt,nrow=qp1,ncol=1);
  vx=matrix(0,qp1,qp1);
  for (ti in 1:q)
  {
    vx[(ti+1):qp1,(ti+1):qp1]=matrix(1,1,(qp1-ti))*tt[ti+1];
  }
  Sigma.mat=sigmasq*vx;
  Itausq=matrix(rep(0,(qp1*qp1)),nrow=q+1,ncol=q+1);
  diag(Itausq)=rep(tausq,q+1);
  V=Sigma.mat+Itausq;
  mu=matrix((xzero+muu*tt),nrow=qp1,ncol=1);
  ofn=((qp1)/2)*log(2*pi)+(0.5*log(det(V)))+
    (0.5*(t(yt-mu)%*%ginv(V)%*%(yt-mu)));
  return(ofn);
}

#  REML objective function "negloglike.reml" is negative of log-likelihood
#  for second differences of the log-scale observations.  The REML objective
#  function uses equations A18-A25 from Humbert et al. (2009).  The three
#  function arguments are:  theta, vector of parameters (transformed to the
#  real line), yt, vector of time series observations (log scale), and
#  tt, vector of observation times.  Function performs the differencing.
negloglike.reml=function(theta,yt,tt)
{
  sigsq=exp(theta[1]);         #  Constrains ssq > 0.
  tausq=exp(theta[2]);         #  Constrains tsq > 0.
  q=length(yt)-1;
  qp1=q+1;
  vx=matrix(0,qp1,qp1);
  for (ti in 1:q)
  {
    vx[(ti+1):qp1,(ti+1):qp1]=matrix(1,1,(qp1-ti))*tt[ti+1];
  }
  Sigma.mat=sigsq*vx;
  Itausq=matrix(rep(0,(qp1*qp1)),nrow=q+1,ncol=q+1);
  diag(Itausq)=rep(tausq,q+1);
  V=Sigma.mat+Itausq;
  ss=tt[2:qp1]-tt[1:q];
  D1mat=cbind(-diag(1/ss),matrix(0,q,1))+cbind(matrix(0,q,1),diag(1/ss));
  D2mat=cbind(-diag(1,q-1),matrix(0,q-1,1))+
    cbind(matrix(0,q-1,1),diag(1,q-1));
  Phi.mat=D2mat%*%D1mat%*%V%*%t(D1mat)%*%t(D2mat);
  wt=(yt[2:qp1]-yt[1:q])/ss;
  ut=wt[2:q]-wt[1:q-1];
  ofn=(q/2)*log(2*pi)+(0.5*log(det(Phi.mat)))+
    (0.5*(ut%*%ginv(Phi.mat)%*%ut));
  return(ofn);
}
#----------------------------------------------------------------------
#        4. SECTION FOR CALCULATING EGOE AND EGPN ESTIMATES
#        (FOR USE AS INITIAL VALUES)  
#----------------------------------------------------------------------
# The EGOE estimates
Ybar=mean(Y.t);
Tbar=mean(T.t);
mu.egoe=sum((T.t-Tbar)*(Y.t-Ybar))/sum((T.t-Tbar)*(T.t-Tbar));
x0.egoe=Ybar-mu.egoe*Tbar;
ssq.egoe=0;
Yhat.egoe=x0.egoe+mu.egoe*T.t;
tsq.egoe=sum((Y.t-Yhat.egoe)*(Y.t-Yhat.egoe))/(q-1);
# The EGPN estimates
Ttr=sqrt(S.t);
Ytr=(Y.t[2:qp1]-Y.t[1:q])/Ttr;
mu.egpn=sum(Ttr*Ytr)/sum(Ttr*Ttr);
Ytrhat=mu.egpn*Ttr;
ssq.egpn=sum((Ytr-Ytrhat)*(Ytr-Ytrhat))/(q-1);
tsq.egpn=0;
x0.egpn=Y.t[1];
# Initial values for EGSS are averages of EGOE and EGPN values 
mu0=(mu.egoe+mu.egpn)/2;    #  For ML only 
ssq0=ssq.egpn/2;            #  For ML and REML
tsq0=tsq.egoe/2;            #  For ML and REML
x00=x0.egoe;                #  For ML only     
# To set different initial values for iterations, enter manually a value
#   after the equal sign of the concern parameter instead of the
#   automatically generated value. Then run again the line and the program
#   section 5 below.
#   Initial values near the EGOE and EGPN models are good for exploring
#   possible alternative local maxima. The values which produce the largest
#   log-likelihood should be used. To see the log-likelihood for the REML
#   estimates type:
#   EGSSreml$value[1];
#   See Dennis et al. 2006 for more details.
#----------------------------------------------------------------------
#        5. SECTION FOR CALCULATING ML & REML PARAMETER ESTIMATES
#----------------------------------------------------------------------
# The ML estimates.
EGSSml=optim(par=c(mu0,log(ssq0),log(tsq0),x00),
             negloglike.ml,NULL,method="Nelder-Mead",yt=Y.t,tt=T.t);
params.ml=c(EGSSml$par[1],exp(EGSSml$par[2]),exp(EGSSml$par[3]),
            EGSSml$par[4]);
lnlike.ml=-EGSSml$value[1];
AIC.egss=-2*lnlike.ml+2*length(params.ml);
mu.ml=params.ml[1];           # These are the ML estimates.
ssq.ml=params.ml[2];          #          --
tsq.ml=params.ml[3];          #          --
x0.ml=params.ml[4];           #          --
# The REML estimates.
EGSSreml=optim(par=c(log(ssq0),log(tsq0)),
               negloglike.reml,NULL,method="Nelder-Mead",yt=Y.t,tt=T.t);
params.reml=c(exp(EGSSreml$par[1]),exp(EGSSreml$par[2]))
ssq.reml=params.reml[1];    #  These are the REML estimates.
tsq.reml=params.reml[2];    #           --

vx=matrix(0,qp1,qp1);
for (ti in 1:q)
{
  vx[(ti+1):qp1,(ti+1):qp1]=matrix(1,1,(qp1-ti))*T.t[ti+1];
}
Sigma.mat=ssq.reml*vx;
Itausq=matrix(rep(0,(qp1*qp1)),nrow=q+1,ncol=q+1);
diag(Itausq)=rep(tsq.reml,q+1);
V=Sigma.mat+Itausq;
D1mat=cbind(-diag(1/S.t),matrix(0,q,1))+cbind(matrix(0,q,1),diag(1/S.t));
V1mat=D1mat%*%V%*%t(D1mat);
W.t=(Y.t[2:qp1]-Y.t[1:q])/S.t;
j1=matrix(1,q,1);
V1inv=ginv(V1mat);
mu.reml=(t(j1)%*%V1inv%*%W.t)/(t(j1)%*%V1inv%*%j1);
j=matrix(1,qp1,1);
Vinv=ginv(V);
x0.reml=(t(j)%*%Vinv%*%(Y.t-mu.reml*T.t))/(t(j)%*%Vinv%*%j);
Var_mu.reml=1/(t(j1)%*%V1inv%*%j1);         #  Variance of mu
mu_hi.reml=mu.reml+1.96*sqrt(Var_mu.reml);  #  95% CI for mu
mu_lo.reml=mu.reml-1.96*sqrt(Var_mu.reml);  #       --
#  Calculate estimated population sizes for EGSS model
#    with Kalman filter, for plotting.
#
#  Choose ML or REML estimates here for calculating model values
#  for plotting (by commenting out the unwanted, default is REML).
#  mu=mu.ml;  ssq=ssq.ml;  tsq=tsq.ml;  x0=x0.ml;
mu=mu.reml;  ssq=ssq.reml;  tsq=tsq.reml;  x0=x0.reml;
m[1]=x0;        
#  Initial mean of Y(t).
v[1]=tsq;       
#  Initial variance of Y(t).
for (ti in 1:q)   #  Loop to generate estimated population abundances
{                 #    using Kalman filter (see equations 6 & 7,
  #    Dennis et al. (2006)).
  m[ti+1]=mu+(m[ti]+((v[ti]-tsq)/v[ti])*(Y.t[ti]-m[ti]));
  v[ti+1]=tsq*((v[ti]-tsq)/v[ti])+ssq+tsq;
}
#  The following statement calculates exp{E[X(t) | Y(t), Y(t-1),...,Y(0)]};
#    see equation 54 in Dennis et al. (2006).  
Predict.t=exp(m+((v-tsq)/v)*(Y.t-m));
#  Plot the data & model-fitted values
plot(Observed.t ~ Time.t,xlab="time",ylab="population abundance",
     type="o",lty="solid",pch=1,cex=1);
#  Population data are circles.
points(Predict.t ~ Time.t,type="l",lty="dashed",lwd=1);
#  Estimated abundances are dashed line.
legend("top", c("Observed.t","Predict.t"),lty=c(1,2),pch=c("o",""),bty="n")
#  Graph legend
#  Print the parameter estimates
parms.egoe=c(mu.egoe,ssq.egoe,tsq.egoe,x0.egoe); #  Collect for printing
parms.egpn=c(mu.egpn,ssq.egpn,tsq.egpn,x0.egpn); #          --
11
parms.reml=c(mu.reml,ssq.reml,tsq.reml,x0.reml); #          --
parms.ml=c(mu.ml,ssq.ml,tsq.ml,x0.ml);           #          --
names=c("mu","ssq","tsq","x0");                  #          --
types=c("EGOE","EGPN","EGSS-ML","EGSS-REML");    #          --
#  Print stuff
matrix(cbind(parms.egoe,parms.egpn,parms.ml,parms.reml),
       nrow=4,ncol=4,byrow=TRUE,dimnames=list(types,names)); 
#  Print CI, default is for EGSS-REML
matrix(cbind(mu_lo.reml,mu_hi.reml),nrow=1,ncol=2,byrow=TRUE,
       dimnames=list("95% CI for MU",c("LO","HI")));   
#  Print log-likelihood and AIC for EGSS ML
matrix(cbind(lnlike.ml,AIC.egss),nrow=1,ncol=2,byrow=TRUE,
       dimnames=list("EGSS ML RESULTS",c("LN-LIKELIHOOD","AIC"))); 
#  Plot the data & model-fitted values to a png file
png(file = "C:/Users/amcclary/Documents/my_graph.png")    
#  Open a png file for plotting
#  ** CHANGE LINE ABOVE IF YOU WANT RESULTS TO GO SOMEWHERE OTHER THAN C:/ DRIVE
plot(Observed.t ~ Time.t,xlab="time",ylab="population abundance",
     type="o",lty="solid",pch=1,cex=1);
#  Population data are circles.
points(Predict.t ~ Time.t,type="l",lty="dashed",lwd=1);
#  Estimated abundances are dashed line.
legend("top", c("Observed.t","Predict.t"),lty=c(1,2),pch=c("o",""),bty="n")
#  Graph legend
graphics.off()  
#  Close graphics file
sink()  
#  Remove output diversion to results file so output will
#    be sent back to the screen