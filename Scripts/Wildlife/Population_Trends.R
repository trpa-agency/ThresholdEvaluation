# Clear the workspace
rm(list=ls(all=TRUE))

# Read command line arguments
args <- commandArgs(trailingOnly = TRUE)
csv_file <- args[1]
output_dir <- args[2]

# Read the data
my_data <- read.csv(csv_file, header=TRUE, sep=",")
Observed.t <- my_data$Observed.t
Time.t <- my_data$Time.t

# Initialize variables for calculations
library(MASS)
T.t = Time.t - Time.t[1]
Y.t = log(Observed.t)
q = length(Y.t) - 1
qp1 = q + 1
S.t = T.t[2:qp1] - T.t[1:q]
m = rep(1, qp1)
v = rep(1, qp1)

# Define ML and REML log-likelihood functions
negloglike.ml = function(theta, yt, tt) {
  muu = theta[1]
  sigmasq = exp(theta[2])
  tausq = exp(theta[3])
  xzero = theta[4]
  q = length(yt) - 1
  qp1 = q + 1
  yt = matrix(yt, nrow=qp1, ncol=1)
  vx = matrix(0, qp1, qp1)
  for (ti in 1:q) {
    vx[(ti+1):qp1, (ti+1):qp1] = matrix(1, 1, (qp1-ti)) * tt[ti+1]
  }
  Sigma.mat = sigmasq * vx
  Itausq = matrix(rep(0, (qp1 * qp1)), nrow=q+1, ncol=q+1)
  diag(Itausq) = rep(tausq, q+1)
  V = Sigma.mat + Itausq
  mu = matrix((xzero + muu * tt), nrow=qp1, ncol=1)
  ofn = ((qp1) / 2) * log(2 * pi) + (0.5 * log(det(V))) +
    (0.5 * (t(yt - mu) %*% ginv(V) %*% (yt - mu)))
  return(ofn)
}

negloglike.reml = function(theta, yt, tt) {
  sigsq = exp(theta[1])
  tausq = exp(theta[2])
  q = length(yt) - 1
  qp1 = q + 1
  vx = matrix(0, qp1, qp1)
  for (ti in 1:q) {
    vx[(ti+1):qp1, (ti+1):qp1] = matrix(1, 1, (qp1-ti)) * tt[ti+1]
  }
  Sigma.mat = sigsq * vx
  Itausq = matrix(rep(0, (qp1 * qp1)), nrow=q+1, ncol=q+1)
  diag(Itausq) = rep(tausq, q+1)
  V = Sigma.mat + Itausq
  ss = tt[2:qp1] - tt[1:q]
  D1mat = cbind(-diag(1/ss), matrix(0, q, 1)) + cbind(matrix(0, q, 1), diag(1/ss))
  D2mat = cbind(-diag(1, q-1), matrix(0, q-1, 1)) +
    cbind(matrix(0, q-1, 1), diag(1, q-1))
  Phi.mat = D2mat %*% D1mat %*% V %*% t(D1mat) %*% t(D2mat)
  wt = (yt[2:qp1] - yt[1:q]) / ss
  ut = wt[2:q] - wt[1:q-1]
  ofn = (q / 2) * log(2 * pi) + (0.5 * log(det(Phi.mat))) +
    (0.5 * (ut %*% ginv(Phi.mat) %*% ut))
  return(ofn)
}

# EGOE estimates
Ybar = mean(Y.t)
Tbar = mean(T.t)
mu.egoe = sum((T.t - Tbar) * (Y.t - Ybar)) / sum((T.t - Tbar) * (T.t - Tbar))
x0.egoe = Ybar - mu.egoe * Tbar
ssq.egoe = 0
Yhat.egoe = x0.egoe + mu.egoe * T.t
tsq.egoe = sum((Y.t - Yhat.egoe) * (Y.t - Yhat.egoe)) / (q - 1)

# EGPN estimates
Ttr = sqrt(S.t)
Ytr = (Y.t[2:qp1] - Y.t[1:q]) / Ttr
mu.egpn = sum(Ttr * Ytr) / sum(Ttr * Ttr)
Ytrhat = mu.egpn * Ttr
ssq.egpn = sum((Ytr - Ytrhat) * (Ytr - Ytrhat)) / (q - 1)
tsq.egpn = 0
x0.egpn = Y.t[1]

# Initial values
mu0 = (mu.egoe + mu.egpn) / 2
ssq0 = ssq.egpn / 2
tsq0 = tsq.egoe / 2
x00 = x0.egoe

# The ML estimates.# The ML estimates.
EGSSml = optim(par = c(mu0, log(ssq0), log(tsq0), x00),
               negloglike.ml, NULL, method = "Nelder-Mead", yt = Y.t, tt = T.t);
params.ml = c(EGSSml$par[1], exp(EGSSml$par[2]), exp(EGSSml$par[3]),
              EGSSml$par[4]);
lnlike.ml = -EGSSml$value[1];
AIC.egss = -2 * lnlike.ml + 2 * length(params.ml);
mu.ml = params.ml[1];           # These are the ML estimates.
ssq.ml = params.ml[2];          #          --
tsq.ml = params.ml[3];          #          --
x0.ml = params.ml[4];           #          --

# Define the covariance matrix for ML
vx_ml = matrix(0, qp1, qp1)
for (ti in 1:q) {
  vx_ml[(ti + 1):qp1, (ti + 1):qp1] = matrix(1, 1, (qp1 - ti)) * T.t[ti + 1]
}
Sigma.mat_ml = ssq.ml * vx_ml
Itausq_ml = matrix(rep(0, (qp1 * qp1)), nrow = q + 1, ncol = q + 1)
diag(Itausq_ml) = rep(tsq.ml, q + 1)
V_ml = Sigma.mat_ml + Itausq_ml

# Calculate variance and confidence intervals for ML estimates
Vinv_ml = ginv(V_ml)
Var_mu.ml = 1 / sum(diag(Vinv_ml))
mu_hi.ml = mu.ml + 1.96 * sqrt(Var_mu.ml)
mu_lo.ml = mu.ml - 1.96 * sqrt(Var_mu.ml)

# The REML estimates.
EGSSreml = optim(par = c(log(ssq0), log(tsq0)),
                 negloglike.reml, NULL, method = "Nelder-Mead", yt = Y.t, tt = T.t);
params.reml = c(exp(EGSSreml$par[1]), exp(EGSSreml$par[2]))
ssq.reml = params.reml[1];    #  These are the REML estimates.
tsq.reml = params.reml[2];    #           --

# Define the covariance matrix for REML
vx_reml = matrix(0, qp1, qp1)
for (ti in 1:q) {
  vx_reml[(ti + 1):qp1, (ti + 1):qp1] = matrix(1, 1, (qp1 - ti)) * T.t[ti + 1]
}
Sigma.mat_reml = ssq.reml * vx_reml
Itausq_reml = matrix(rep(0, (qp1 * qp1)), nrow = q + 1, ncol = q + 1)
diag(Itausq_reml) = rep(tsq.reml, q + 1)
V_reml = Sigma.mat_reml + Itausq_reml

D1mat = cbind(-diag(1 / S.t), matrix(0, q, 1)) + cbind(matrix(0, q, 1), diag(1 / S.t))
V1mat = D1mat %*% V_reml %*% t(D1mat)
W.t = (Y.t[2:qp1] - Y.t[1:q]) / S.t
j1 = matrix(1, q, 1)
V1inv = ginv(V1mat)
mu.reml = (t(j1) %*% V1inv %*% W.t) / (t(j1) %*% V1inv %*% j1)
j = matrix(1, qp1, 1)
Vinv = ginv(V_reml)
x0.reml = (t(j) %*% Vinv %*% (Y.t - mu.reml * T.t)) / (t(j) %*% Vinv %*% j)
Var_mu.reml = 1 / (t(j1) %*% V1inv %*% j1)  #  Variance of mu
mu_hi.reml = mu.reml + 1.96 * sqrt(Var_mu.reml)  #  95% CI for mu
mu_lo.reml = mu.reml - 1.96 * sqrt(Var_mu.reml)  #       --

# For EGOE
Var_mu.egoe <- 1 / sum((T.t - Tbar) ^ 2)
mu_hi.egoe <- mu.egoe + 1.96 * sqrt(Var_mu.egoe)
mu_lo.egoe <- mu.egoe - 1.96 * sqrt(Var_mu.egoe)

# For EGPN
Var_mu.egpn <- 1 / sum(Ttr ^ 2)
mu_hi.egpn <- mu.egpn + 1.96 * sqrt(Var_mu.egpn)
mu_lo.egpn <- mu.egpn - 1.96 * sqrt(Var_mu.egpn)

# Prepare output DataFrame
results <- list(
  EGOE = list(
    mu = mu.egoe,
    x0 = x0.egoe,
    ssq = ssq.egoe,
    tsq = tsq.egoe,
    ci_mu = list(
      lower = mu_lo.egoe,
      upper = mu_hi.egoe
    )
  ),
  EGPN = list(
    mu = mu.egpn,
    x0 = x0.egpn,
    ssq = ssq.egpn,
    tsq = tsq.egpn,
    ci_mu = list(
      lower = mu_lo.egpn,
      upper = mu_hi.egpn
    )
  ),
  EGSS_ML = list(
    mu = mu.ml,
    ssq = ssq.ml,
    tsq = tsq.ml,
    x0 = x0.ml,
    ci_mu = list(
      lower = mu_lo.ml,
      upper = mu_hi.ml
    )
  ),
  EGSS_REML = list(
    mu = mu.reml,
    ssq = ssq.reml,
    tsq = tsq.reml,
    x0 = x0.reml,
    ci_mu = list(
      lower = mu_lo.reml,
      upper = mu_hi.reml
    )
  )
)

library(jsonlite)
cat(toJSON(results, auto_unbox = TRUE, pretty = TRUE))
