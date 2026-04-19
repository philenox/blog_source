weianthro.txt is the WHO Child Growth Standards weight-for-age LMS table.

Source: https://github.com/WorldHealthOrganization/anthro
Path in source repo: data-raw/growthstandards/weianthro.txt
License: GPL-3.0

Columns (tab-separated):
  sex  - 1 = boy, 2 = girl
  age  - age in days, 0 through 1826 (0-5 years inclusive)
  l    - Box-Cox power (lambda)
  m    - median
  s    - coefficient of variation (sigma)

Z-score formula (LMS method):
  if L != 0:  Z = ((X/M)^L - 1) / (L * S)
  else:       Z = ln(X/M) / S
Percentile = Phi(Z) * 100, where Phi is the standard normal CDF.
