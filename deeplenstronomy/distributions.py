# A module listing all available distribtuions

import numpy as np
import random
from scipy.stats import poisson

try:
    import des_private
except:
    pass

## Single parameter sampling distributions

def uniform(minimum, maximum, bands=''):
    draw = random.uniform(minimum, maximum)
    return [draw] * len(bands.split(','))

def normal(mean, std, bands=''):
    draw = np.random.normal(loc=mean, scale=std)
    return [draw] * len(bands.split(','))

def delta_function(value, bands=''):
    return [value] * len(bands.split(','))


## Grid sampling distributions

def poisson_noise(shape, mean):
    return poisson.rvs(mu=mean, size=shape)


## Empirical distributions

def galaxy_color(bands=''):
    dist = {'g': 18.0, 'r': 19.0, 'i': 19.8, 'z': 21.5, 'Y': 23.5}
    return [dist[b] for b in bands.split(',')]



# des_mag and _des_mag_color are based on currently undistributed DES data
# If you are a DES member, contact the authors to receive the des_private.py file
def des_mag(bands=''):
    try:
        return des_private.des_mag(bands)
    except:
        return galaxy_color(bands=bands)
    
def _des_mag_color(pair):
    try:
        return des_private._des_mag_color(pair)
    except:
        return 0.0

    
def des_sky_brightness(bands=''):
    # Figure 4 in https://arxiv.org/pdf/1801.03181.pdf
    dist = {'g': {'VALUES': [21.016, 21.057, 21.106, 21.179, 21.228, 21.269, 21.326, 
                             21.367, 21.424, 21.465, 21.522, 21.571, 21.62, 21.677, 
                             21.717, 21.774, 21.823, 21.872, 21.921, 21.97, 22.019, 
                             22.068, 22.117, 22.174, 22.215, 22.272, 22.321, 22.378, 
                             22.427, 22.476],
                  'WEIGHTS': [0.0, 0.0, 0.001, 0.001, 0.001, 0.001, 0.002, 0.003, 
                              0.005, 0.007, 0.009, 0.012, 0.016, 0.023, 0.034, 0.048, 
                              0.063, 0.073, 0.081, 0.093, 0.107, 0.099, 0.087, 0.076, 
                              0.061, 0.05, 0.027, 0.013, 0.005, 0.0]},
            'r': {'VALUES': [20.16, 20.209, 20.266, 20.323, 20.372, 20.421, 20.47, 
                             20.519, 20.576, 20.625, 20.674, 20.715, 20.772, 20.821, 
                             20.87, 20.918, 20.976, 21.024, 21.073, 21.122, 21.171, 
                             21.22, 21.269, 21.326, 21.375, 21.424, 21.473, 21.522, 
                             21.571, 21.62, 21.668, 21.726],
                  'WEIGHTS': [0.0, 0.0, 0.001, 0.001, 0.002, 0.002, 0.005, 0.008, 
                              0.011, 0.011, 0.012, 0.02, 0.023, 0.034, 0.043, 0.046, 
                              0.056, 0.07, 0.075, 0.083, 0.093, 0.095, 0.092, 0.078, 
                              0.057, 0.041, 0.024, 0.012, 0.004, 0.001, 0.0, 0.0]},
            'i': {'VALUES': [18.921, 18.978, 19.027, 19.076, 19.125, 19.174, 19.223, 
                             19.272, 19.321, 19.378, 19.418, 19.476, 19.524, 19.573, 
                             19.622, 19.671, 19.728, 19.777, 19.826, 19.875, 19.924, 
                             19.973, 20.022, 20.071, 20.12, 20.177, 20.226, 20.274, 
                             20.323, 20.372, 20.421, 20.478, 20.527, 20.576, 20.617, 
                             20.674, 20.723, 20.772, 20.829],
                  'WEIGHTS': [0.0, 0.0, 0.002, 0.002, 0.001, 0.002, 0.003, 0.005, 
                              0.013, 0.017, 0.018, 0.026, 0.029, 0.035, 0.036, 0.047, 
                              0.053, 0.067, 0.078, 0.084, 0.073, 0.073, 0.063, 0.05, 
                              0.045, 0.039, 0.031, 0.026, 0.021, 0.018, 0.014, 0.009, 
                              0.009, 0.003, 0.002, 0.002, 0.001, 0.0, 0.0]},
            'z': {'VALUES': [17.715, 17.772, 17.804, 17.861, 17.918, 17.976, 18.024, 
                             18.073, 18.122, 18.171, 18.228, 18.277, 18.326, 18.375, 
                             18.424, 18.473, 18.522, 18.579, 18.628, 18.677, 18.726, 
                             18.774, 18.823, 18.872, 18.921, 18.97, 19.019, 19.076, 
                             19.125, 19.174, 19.231, 19.264, 19.329, 19.37, 19.427, 
                             19.467, 19.524, 19.573, 19.63],
                  'WEIGHTS': [0.0, 0.0, 0.0, 0.001, 0.001, 0.004, 0.007, 0.008, 
                              0.012, 0.014, 0.015, 0.022, 0.028, 0.028, 0.033, 0.045, 
                              0.052, 0.058, 0.064, 0.073, 0.082, 0.078, 0.069, 0.059, 
                              0.051, 0.044, 0.036, 0.024, 0.019, 0.018, 0.017, 0.015, 
                              0.01, 0.005, 0.002, 0.002, 0.002, 0.001, 0.0]},
            'Y': {'VALUES': [17.062, 17.128, 17.177, 17.226, 17.274, 17.323, 17.372, 
                             17.421, 17.47, 17.527, 17.576, 17.625, 17.674, 17.723, 
                             17.772, 17.821, 17.878, 17.927, 17.976, 18.024, 18.073, 
                             18.13, 18.179, 18.228, 18.277, 18.326, 18.375, 18.424, 
                             18.473, 18.53, 18.579, 18.628, 18.668, 18.726, 18.774, 
                             18.823, 18.88, 18.929, 18.97, 19.027, 19.076],
                  'WEIGHTS': [0.001, 0.002, 0.002, 0.003, 0.006, 0.008, 0.011, 0.015, 
                              0.02, 0.027, 0.032, 0.041, 0.051, 0.051, 0.05, 0.05, 
                              0.056, 0.066, 0.072, 0.068, 0.056, 0.047, 0.042, 0.033, 
                              0.032, 0.029, 0.024, 0.022, 0.021, 0.02, 0.014, 0.011, 
                              0.006, 0.003, 0.002, 0.001, 0.001, 0.0, 0.002, 0.001, 0.0]}
            }
    return [random.choices(dist[b]['VALUES'], dist[b]['WEIGHTS'])[0] for b in bands.split(',')]


def des_exposure_time(bands=''):
    # https://arxiv.org/pdf/1801.03181.pdf
    return [45.0 if b == 'Y' else 90.0 for b in bands.split(',')]

def des_seeing(bands=''):
    #Figure 3 in https://arxiv.org/pdf/1801.03181.pdf
    dist = {'g': {'VALUES': [0.56, 0.579, 0.601, 0.621, 0.642, 0.662, 0.679, 0.703, 0.72,
                             0.742, 0.761, 0.783, 0.822, 0.841, 0.863, 0.882, 0.902, 0.921,
                             0.943, 0.962, 0.982, 1.001, 1.021, 1.04, 1.062, 1.081, 1.101,
                             1.122, 1.139, 1.161, 1.181, 1.2, 1.219, 1.241, 1.261, 1.282,
                             1.302, 1.319, 1.341, 1.36, 1.379, 1.399, 1.418, 1.44, 1.479,
                             1.501, 1.52, 1.539, 1.559, 1.578, 1.598, 1.619, 1.639, 1.658,
                             1.678, 1.697, 1.719, 1.738, 1.758, 1.777, 1.799, 1.82],
                  'WEIGHTS': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001, 0.001, 0.002,
                              0.004, 0.005, 0.008, 0.011, 0.015, 0.02, 0.025, 0.029, 0.034, 
			      0.038, 0.042, 0.045, 0.046, 0.047, 0.045, 0.044, 0.041, 0.04, 
                              0.037, 0.033, 0.031, 0.028, 0.026, 0.025, 0.023, 0.021, 0.019, 
                              0.018, 0.017, 0.016, 0.015, 0.014, 0.014, 0.013, 0.012, 0.012, 
                              0.011, 0.01, 0.009, 0.009, 0.008, 0.007, 0.007, 0.006, 0.005, 
                              0.004, 0.003, 0.002, 0.001, 0.001, 0.0]},
            'r': {'VALUES': [0.56, 0.579, 0.601, 0.621, 0.642, 0.662, 0.679, 0.703, 0.72, 
                             0.742, 0.761, 0.783, 0.822, 0.841, 0.863, 0.882, 0.902, 0.921, 
                             0.943, 0.962, 0.982, 1.001, 1.021, 1.04, 1.062, 1.081, 1.101, 
                             1.122, 1.139, 1.161, 1.181, 1.2, 1.219, 1.241, 1.261, 1.282, 
                             1.302, 1.319, 1.341, 1.36, 1.379, 1.399, 1.418, 1.44, 1.479, 
                             1.501, 1.52, 1.539, 1.559, 1.578, 1.598, 1.619, 1.639, 1.658, 
                             1.678, 1.697, 1.719, 1.738, 1.758, 1.777, 1.799, 1.82],
                  'WEIGHTS': [0.0, 0.0, 0.0, 0.0, 0.0, 0.001, 0.002, 0.004, 0.007, 0.012, 
                              0.019, 0.027, 0.036, 0.043, 0.051, 0.057, 0.062, 0.063, 0.061, 
                              0.058, 0.054, 0.048, 0.044, 0.04, 0.036, 0.032, 0.028, 0.025, 
                              0.022, 0.019, 0.018, 0.015, 0.014, 0.012, 0.011, 0.01, 0.009, 
                              0.008, 0.008, 0.007, 0.006, 0.005, 0.004, 0.004, 0.003, 0.003, 
                              0.002, 0.002, 0.002, 0.002, 0.002, 0.001, 0.001, 0.0, 0.0, 
                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
            'i': {'VALUES': [0.56, 0.579, 0.601, 0.621, 0.642, 0.662, 0.679, 0.703, 0.72, 
                             0.742, 0.761, 0.783, 0.822, 0.841, 0.863, 0.882, 0.902, 0.921, 
                             0.943, 0.962, 0.982, 1.001, 1.021, 1.04, 1.062, 1.081, 1.101, 
                             1.122, 1.139, 1.161, 1.181, 1.2, 1.219, 1.241, 1.261, 1.282, 
                             1.302, 1.319, 1.341, 1.36, 1.379, 1.399, 1.418, 1.44, 1.479, 
                             1.501, 1.52, 1.539, 1.559, 1.578, 1.598, 1.619, 1.639, 1.658, 
                             1.678, 1.697, 1.719, 1.738, 1.758, 1.777, 1.799, 1.82],
                  'WEIGHTS': [0.0, 0.0, 0.0, 0.001, 0.002, 0.005, 0.01, 0.017, 0.027, 0.038, 
                              0.049, 0.061, 0.067, 0.072, 0.076, 0.075, 0.071, 0.066, 0.058, 
                              0.05, 0.045, 0.038, 0.032, 0.026, 0.021, 0.017, 0.014, 0.011, 
                              0.009, 0.008, 0.007, 0.005, 0.004, 0.003, 0.003, 0.002, 0.002, 
                              0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.0, 0.0, 
                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                              0.0, 0.0, 0.0, 0.0]},
            'z': {'VALUES': [0.56, 0.579, 0.601, 0.621, 0.642, 0.662, 0.679, 0.703, 0.72, 
                             0.742, 0.761, 0.783, 0.822, 0.841, 0.863, 0.882, 0.902, 0.921, 
                             0.943, 0.962, 0.982, 1.001, 1.021, 1.04, 1.062, 1.081, 1.101, 
                             1.122, 1.139, 1.161, 1.181, 1.2, 1.219, 1.241, 1.261, 1.282, 
                             1.302, 1.319, 1.341, 1.36, 1.379, 1.399, 1.418, 1.44, 1.479, 
                             1.501, 1.52, 1.539, 1.559, 1.578, 1.598, 1.619, 1.639, 1.658, 
                             1.678, 1.697, 1.719, 1.738, 1.758, 1.777, 1.799, 1.82],
                  'WEIGHTS': [0.0, 0.0, 0.001, 0.003, 0.008, 0.016, 0.027, 0.039, 0.054, 
                              0.066, 0.073, 0.077, 0.077, 0.073, 0.069, 0.061, 0.054, 0.045, 
                              0.037, 0.032, 0.026, 0.022, 0.019, 0.017, 0.014, 0.013, 0.011, 
                              0.009, 0.008, 0.007, 0.007, 0.005, 0.004, 0.003, 0.003, 0.003, 
                              0.003, 0.002, 0.002, 0.002, 0.002, 0.001, 0.001, 0.001, 0.001, 
                              0.001, 0.001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
            'Y': {'VALUES': [0.56, 0.579, 0.601, 0.621, 0.642, 0.662, 0.679, 0.703, 0.72, 
                             0.742, 0.761, 0.783, 0.822, 0.841, 0.863, 0.882, 0.902, 0.921, 
                             0.943, 0.962, 0.982, 1.001, 1.021, 1.04, 1.062, 1.081, 1.101, 
                             1.122, 1.139, 1.161, 1.181, 1.2, 1.219, 1.241, 1.261, 1.282, 
                             1.302, 1.319, 1.341, 1.36, 1.379, 1.399, 1.418, 1.44, 1.479, 
                             1.501, 1.52, 1.539, 1.559, 1.578, 1.598, 1.619, 1.639, 1.658, 
                             1.678, 1.697, 1.719, 1.738, 1.758, 1.777, 1.799, 1.82],
                  'WEIGHTS': [0.0, 0.001, 0.001, 0.004, 0.008, 0.014, 0.023, 0.032, 0.038, 
                              0.045, 0.049, 0.051, 0.051, 0.048, 0.046, 0.043, 0.039, 0.036, 
                              0.033, 0.031, 0.028, 0.026, 0.023, 0.021, 0.019, 0.018, 0.017, 
                              0.016, 0.016, 0.014, 0.013, 0.013, 0.012, 0.011, 0.01, 0.01, 
                              0.01, 0.01, 0.009, 0.008, 0.008, 0.007, 0.008, 0.008, 0.007, 
                              0.007, 0.007, 0.006, 0.006, 0.006, 0.006, 0.006, 0.005, 0.004, 
                              0.003, 0.003, 0.002, 0.002, 0.001, 0.001, 0.0, 0.0]}
            }
    return [random.choices(dist[b]['VALUES'], dist[b]['WEIGHTS'])[0] for b in bands.split(',')]

def des_ccd_gain(bands=''):
    # Figure 2 in https://arxiv.org/pdf/1501.02802.pdf
    return [5.033 if b == 'Y' else 6.083 for b in bands.split(',')]

def des_num_exposures(bands=''):
    # Figure 5 in https://arxiv.org/pdf/1501.02802.pdf
    dist = {'g': {'VALUES': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  'WEIGHTS': [0.040, 0.113, 0.267, 0.311, 0.178, 0.062, 0.019, 0.007, 0.003]},
            'r': {'VALUES': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  'WEIGHTS': [0.041, 0.119, 0.284, 0.321, 0.167, 0.046, 0.014, 0.006, 0.002]},
            'i': {'VALUES': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  'WEIGHTS': [0.043, 0.121, 0.291, 0.334, 0.165, 0.033, 0.009, 0.003, 0.001]},
            'z': {'VALUES': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  'WEIGHTS': [0.039, 0.106, 0.272, 0.332, 0.183, 0.048, 0.013, 0.005, 0.002]},
            'Y': {'VALUES': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                  'WEIGHTS': [0.034, 0.074, 0.195, 0.305, 0.241, 0.099, 0.035, 0.012, 0.005]}
            }
    return [random.choices(dist[b]['VALUES'], dist[b]['WEIGHTS'])[0] for b in bands.split(',')]