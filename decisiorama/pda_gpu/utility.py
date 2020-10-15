# -*- coding: utf-8 -*-
""" Utility Module

This module contains utility functions. Current implementation only has the
exponential utility function.

"""

__author__ = "Juan Carlos Chacon-Hurtado"
__credits__ = ["Juan Carlos Chacon-Hurtado", "Lisa Scholten"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Juan Carlos Chacon-Hurtado"
__email__ = "j.chaconhurtado@tudelft.nl"
__status__ = "Development"
__last_update__ = "01-07-2019"

import numpy as np
from numba import cuda, guvectorize, vectorize
import matplotlib.pyplot as plt
import math

#%%
# @guvectorize(['void(float64[:],float64[:],float64[:])', 
#               'void(float32[:],float32[:],float32[:])'], 
#               '(m),(m)->(m)', 
#                target='cuda'
#               )
# def exponential(v, r, out):
#     '''Calculates the exponential utility function

#     Parameters
#     ----------
#     v : float, ndarray
#         Array containing the normalised values
#     r : float, ndarray
#         Exponent parameter

#     returns
#     out : ndarray
#         Utility values

#     Note
#     ----
#     This is executed as a vectorized function

#     '''
#     if r == 0:
#         out[:] = v
#     else:
#         out[:] = (1.0 - np.exp(-r*v)) / (1.0 - np.exp(-r))
        #%%


# define a device function
@cuda.jit('float32(float32, float32, float32)', device=True, inline=True)
def cu_device_fn(x, y, z):
    return x ** y / z

# define a ufunc that calls our device function
@vectorize(['float32(float32, float32, float32)'], target='cuda')
def cu_ufunc(x, y, z):
    return cu_device_fn(x, y, z)



      
 #%%
        
@cuda.jit('float64(float64, float64)', device=True, inline=True)
def _dev_exponential(v, r):
    '''Calculates the exponential utility function

    Parameters
    ----------
    v : float, ndarray
        Array containing the normalised values
    r : float, ndarray
        Exponent parameter

    returns
    out : ndarray
        Utility values

    Note
    ----
    This is executed as a vectorized function

    '''
    # if r == 0.0:
    #     out = v
    # else:
        # out = (1.0 - math.exp(-r*v)) / (1.0 - math.exp(-r))
    return (1.0 - math.exp(-r*v)) / (1.0 - math.exp(-r))
    
#%%
@vectorize('float64(float64,float64)',
            target='cuda')
def exponential(v, r):
    return _dev_exponential(v, r)
    
#%%        
    # def _exponential(v, r):
    #     if v > 1.0 or v < 0.0:
    #         _msj = ('Values passed to the utility function should be ranked '
    #                 'normalised between 0 and 1')
    #         RuntimeWarning(_msj)

    #     if r == 0:
    #         out = v
    #     else:
    #         out = (1.0 - np.exp(-r*v)) / (1.0 - np.exp(-r))
    #     return out

    # _vec_exp = np.vectorize(_exponential)
    # return _vec_exp(v, r)


#example
x = np.linspace(0,1,50000000)
c = np.random.uniform(-20, 20, 50000000)
# c = 3.0*np.ones_like(x)
out = np.empty_like(x)

out = exponential(x, c)

# plt.plot(out)
