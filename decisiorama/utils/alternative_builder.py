# -*- coding: utf-8 -*-
""" Utils Module

In this module are stored all of the supporting functions which do not fall
into a specific category.

"""

__author__ = "Juan Carlos Chacon-Hurtado"
__credits__ = ["Juan Carlos Chacon-Hurtado", "Lisa Scholten"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Juan Carlos Chacon-Hurtado"
__email__ = "j.chaconhurtado@tudelft.nl"
__status__ = "Development"
__last_update__ = "01-07-2019"

import json
import glob
from decisiorama.utils import random_instance as ri

def generator(alt_pdf, fileout):
    # generate dictionary
    out = {}
    for elem in alt_pdf:
        _p = list(alt_pdf[elem].__init__.__code__.co_varnames)
        
        # remove the class variables
        _p.remove('self')
        _p.remove('n')
        
        out[elem] = {'function' : alt_pdf[elem].__name__,
                    'parameters' : {key : None for key in _p}
                    }
    json.dump(out, open(fileout, 'w'), indent=4)
        
# alternative_generator(alt_pdf_1, '1_alternatives.json')    

def reader(filein):
    # read the altenratives from the file
    # filein = '1_alternatives.json'
    f = json.load(open(filein, 'r'))
    
    # make the dictionary with the alternatives
    out = {}
    for elem in f:
        _fun = eval('ri.{0}'.format(f[elem]['function']))
        out[elem] = _fun(**f[elem]['parameters']).get
    
    return out

# def set_reader(path):
#     # read all the files in the path
#     fnames = glob.glob('path\*.json')
    
#     out = []
#     for fname in fnames:
#         out.append(reader(fname))
#     return out
#     # Parse the  elements based on the 1st 
# # g = alternative_reader('1_alternatives.json')