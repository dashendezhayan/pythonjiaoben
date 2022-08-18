import math
import numpy as np

k1=0.03420523138832998

k2=0.058333333333333334




Cobb =int(math.fabs(np.arctan((k1-k2)/(float(1 + k1*k2)))*180/np.pi)+0.5)
print(Cobb)