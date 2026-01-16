import numpy as np
np.random.seed(42)
S0=100; r=0.05; sigma=0.2; T=1; dt=1/252
N=int(T/dt); M=10000
S=np.zeros((M,N)); S[:,0]=S0
for t in range(1,N):
    Z=np.random.standard_normal(M)
    S[:,t]=S[:,t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*Z)
np.save("GBM_stock_data.npy",S)
print("GBM fixed")
