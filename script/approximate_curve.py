import numpy as np
from lmfit import Minimizer, Parameters, report_fit
import pandas as pd
import os
from functions.approximate_func import *

db_dir = '/home/lapa/Complex-curve-fit/RESP/examples'
device_type = '4211'
device_number = '387'
file_name = 'V_calib.dat'
approx_file_name = '4211_50s-60Hz_Vert'
approx_file_path = os.path.join(db_dir, device_type, 
                                '!Device_No-{}'.format(device_number))


path = os.path.join(db_dir, device_type,
        '!Device_No-{}'.format(device_number), file_name)

sensor_data = pd.read_csv(path, sep=' ', header=None)

xdata = sensor_data.iloc[:,0].values
ydata = sensor_data.iloc[:,1].values
xdata_complex =  sensor_data.iloc[:,0].values/2/np.pi*1j    
ydata_complex = ydata * np.exp(1j * sensor_data.iloc[:,3].values)

# plot_appoximation(xdata, ydata, None, ydata_complex, with_approx=False)
n = 8
params = Parameters()

params.add('a',   value= 1*10**15, min=10**8, max=8*10**15)
params.add('n',   value= 8, min=7, max=9)
params.add('real_q1',   value= -0.001,  min=-0.1, max=0.01)
params.add('complex_q2',   value= 0.000001,  min=-1, max=1)
params.add('complex_q3',   value= 0.0065,  min=0.002, max=0.008)
params.add('complex_q4',   value= 0.01,  min=0.001, max=0.02)
params.add('complex_q5',   value= 30,  min=20, max=50)
params.add('complex_q6',   value= 60,  min=10, max=90)
params.add('real_q7',   value= -120,  min=-5000, max=-60)

mini_complex_poles = Minimizer(residuals_compl_poles, params,
                               fcn_args=(xdata_complex, ydata_complex))

result = mini_complex_poles.minimize()

print(report_fit(result))

final = ydata_complex + result.residual.reshape(len(xdata),2)[:,0] + \
                result.residual.reshape(len(xdata),2)[:,1]*1j

plot_appoximation(xdata, ydata, final, ydata_complex,
                  save_fig=True, path=approx_file_path, fig_name=approx_file_name)


approx_file_path += '/' + approx_file_name
save_poles_zeros(result, filename=approx_file_path)