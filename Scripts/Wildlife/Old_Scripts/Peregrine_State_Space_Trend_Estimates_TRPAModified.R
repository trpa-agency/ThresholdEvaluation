#  Computer program, in the R language, for calculating ML and REML estimates of parameters in the EGSS model.

# Provided by Dr. Barry Noon, Modified by Dan Segan TRPA 

#  Exponential Growth State Space model:
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
#  function for the model frequently has multiple local maxima.
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
#----------------------------------------------------------------------
#        USER INPUT SECTION
#----------------------------------------------------------------------
#  Time series data is read in here. R will print the data to the console
#  immediately after it has read it in, so you can check to see that it is
#  correct.
#
#  Create the following data sheet in Excel, name it pfalcon and save it 
#  as a comma delimited (.CSV) file to the WBIO470 folder on the Y: drive.
#
#  In Excel, in cell A1, type the word "Observed.t", without the quotes. Put the 
#  observed population size in column A, starting with row 2.  You may NOT enter 
#  any zeros in this column.
#  In cell B1, type the word "Time.t" without the quotes. Put the observation
#  times (that correspond to the observed population sizes) in column B, starting 
#  with row 2. Your initial time may or may not equal zero; either is okay.


# remove everything stored
rm(list = ls())

# set WD 
setwd("F:/Research and Analysis/Threshold reporting/Threshold Evaluations/2015 Threshold evaluation/TEVAL Chapters/CHAPTER 8 Wildlife/Analysis/data/")

# Read in data set
my_data <- read.csv("pfalcon.csv", header=T,sep=",")
head(my_data)

   Observed.t <- my_data$Observed.t
   Time.t <- my_data$Time.t
   print.table(cbind(Observed.t,Time.t))

sink(file = "pfalcon_results.txt", append = FALSE, type = "output", split = T)  
# will create a file with your results in wd
 
#  Example data below are American Redstart counts from North American Breeding
#    Bird Survey, record # 02014 3328 08636, 1966-95 (Table 1 in Dennis
#    et al. 2006).  To run this example, comment out the statements above, using 
#    the pound sign, and uncomment the lines below, but do not change anything 
#    outside of the user input section.
 # Observed.t=c(18,10,9,14,17,5,10,9,5,11,11,4,5,4,8,2,3,9,2,4,7,4,1,2,
  #  4,11,11,9,6);     #  No zeros!  (With zeros, you must use another model)
 # Time.t=c(0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
 #   25,26,27,28,29);  #  Initial time can be nonzero.


#----------------------------------------------------------------------
#        PROGRAM INITIALIZATION SECTION
#----------------------------------------------------------------------  
library(MASS);            #  loads miscellaneous functions (ginv, etc.)
T.t=Time.t-Time.t[1];     #  Time starts at zero.
Y.t=log(Observed.t);      #  Log-transform the observations.
q=length(Y.t)-1;          #  Number of time series transitions, q.
qp1=q+1;                  #  q+1 gets used a lot, too.
S.t=T.t[2:qp1]-T.t[1:q];  #  Time intervals.
m=rep(1,qp1);             #  Will contain Kalman means for Kalman calculations.
v=rep(1,qp1);             #  Will contain variances for Kalman calculations.

#----------------------------------------------------------------------
#        SECTION FOR DEFINING ML & REML LOG-LIKELIHOODS
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
#  function uses equations A16-A24 from Humbert et al. (2009).  The three
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
#        SECTION FOR CALCULATING EGOE AND EGPN ESTIMATES
#        (FOR USE AS INITIAL VALUES)  
#----------------------------------------------------------------------
Ybar=mean(Y.t);
Tbar=mean(T.t);
mu.egoe=sum((T.t-Tbar)*(Y.t-Ybar))/sum((T.t-Tbar)*(T.t-Tbar));
x0.egoe=Ybar-mu.egoe*Tbar;
ssq.egoe=0;
Yhat.egoe=x0.egoe+mu.egoe*T.t;
tsq.egoe=sum((Y.t-Yhat.egoe)*(Y.t-Yhat.egoe))/(q-1);

Ttr=sqrt(S.t);
Ytr=(Y.t[2:qp1]-Y.t[1:q])/Ttr;
mu.egpn=sum(Ttr*Ytr)/sum(Ttr*Ttr);
Ytrhat=mu.egpn*Ttr;
ssq.egpn=sum((Ytr-Ytrhat)*(Ytr-Ytrhat))/(q-1);
tsq.egpn=0;
x0.egpn=Y.t[1];

mu0=(mu.egoe+mu.egpn)/2;    #  Initial values for EGSS are averages
ssq0=ssq.egpn/2;            #    of EGOE and EGPN values
tsq0=tsq.egoe/2;            #            --
x00=x0.egoe;                #            --

#----------------------------------------------------------------------
#        SECTION FOR CALCULATING ML & REML PARAMETER ESTIMATES
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
ssq.reml=params.reml[1];   #  These are the REML estimates.
tsq.reml=params.reml[2];   #           --

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
#  for plotting (by commenting out the unwanted).
#  mu=mu.ml;  ssq=ssq.ml;  tsq=tsq.ml;  x0=x0.ml;
mu=mu.reml;  ssq=ssq.reml;  tsq=tsq.reml;  x0=x0.reml;

m[1]=x0;       #  Initial mean of Y(t).
v[1]=tsq;      #  Initial variance of Y(t).

for (ti in 1:q)   #  Loop to generate estimated population abundances
{                 #    using Kalman filter (see equations 6 & 7,
                  #    Dennis et al. (2006).
   m[ti+1]=mu+(m[ti]+((v[ti]-tsq)/v[ti])*(Y.t[ti]-m[ti]));
   v[ti+1]=tsq*((v[ti]-tsq)/v[ti])+ssq+tsq;
}

#  The following statement calculates exp{E[X(t) | Y(t), Y(t-1),...,Y(0)]};
#    see equation 54 in Dennis et al. (2006).  
Predict.t=exp(m+((v-tsq)/v)*(Y.t-m));

#_________________________________________________________________RESULTS
#  Plot the data & model-fitted values
bmp(file = "pfalcon_graph.bmp") # Will save the plot in wd. 
plot(Observed.t,xlab="year",ylab="population abundance",
   type="o",pch=1,cex=2.0);      #  Population data are circles.
par(lty="dashed");               #  Estimated abundances are dashed line.
points(Predict.t, type="l", lwd=2, col="blue")
dev.off()

#  Print the parameter estimates
parms.egoe=c(mu.egoe,ssq.egoe,tsq.egoe); #  Collect for printing
parms.egpn=c(mu.egpn,ssq.egpn,tsq.egpn); #          --
parms.reml=c(mu.reml,ssq.reml,tsq.reml); #          --
#parms.ml=c(mu.ml,ssq.ml,tsq.ml,x0.ml);  #          --
names=c("mu         ","process var.(ssq)","sample var.(tsq)");               
types=c("EGOE","EGPN","EGSS-REML");      #          --
matrix(cbind(parms.egoe,parms.egpn,parms.reml),
   nrow=3,ncol=3,byrow=TRUE,dimnames=list(types,names))   

# Print mu variance
Var_mu.reml

# Print 95% confidence interval for EGSS mu
matrix(cbind(mu_lo.reml,mu_hi.reml),nrow=1,ncol=2,byrow=TRUE,
   dimnames=list("95% CI for MU",c("LO","HI"))); 

####    END    ####
