import pandas as pd
from obspy.io.xseed import Parser
import os
from functions.laplace_func import read_approx_file

def create_resp(laplace_file : str, channel : str,
                device_type : str,
                freq : int,
                sensitivity : int = 2000,
                resp_folder : str = '.') -> None:
    '''
    

    Parameters
    ----------
    laplace_file  : str
        file name of laplace approx
    channel : str
        name of channel. May be Z or N
    device_type : str
        type of device like CME4211
    freq : int
        frequency like 1 s, 60 s, 120 s
    sensitivity : int, optional
            sensitivity of sensor. The default is 2000
    resp_folder : str
        save folder. The default is '.'

    Returns
    -------
    None
        save RESP file

    '''


    resp_name = f'.{device_type}.{freq}.{sensitivity}'
    
    p = Parser('/home/lapa/Complex-curve-fit/RESP/templates/resp_file')
    blk = p.blockettes
    
    A0, zeros, poles = read_approx_file(laplace_file)
    n_zeros, n_poles = len(zeros), len(poles)
    
    blk[52][0].channel_identifier = 'HH%s' % channel
    blk[53][0].A0_normalization_factor = A0
    blk[53][0].number_of_complex_zeros = n_zeros
    blk[53][0].real_zero = [zero.real for zero in zeros]
    blk[53][0].imaginary_zero = [zero.imag for zero in zeros]
    blk[53][0].real_zero_error = [0]*n_zeros
    blk[53][0].imaginary_zero_error = [0]*n_zeros
            
    blk[53][0].number_of_complex_poles = n_poles
    blk[53][0].real_pole = [pole.real for pole in poles]
    blk[53][0].imaginary_pole = [pole.imag for pole in poles]
    blk[53][0].real_pole_error = [0]*n_poles
    blk[53][0].imaginary_pole_error = [0]*n_poles
    
    blk[58][0].sensitivity_gain = sensitivity
    
    
    p.write_resp(resp_folder)
    old_name = os.path.join(resp_folder, p.get_resp()[0][0])
    new_name = old_name+resp_name
    os.rename(old_name, new_name)