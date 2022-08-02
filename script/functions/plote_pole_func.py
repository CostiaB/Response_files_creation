import matplotlib.pyplot as plt
import numpy as np
from obspy.signal.invsim import paz_to_freq_resp
from typing import List, Tuple




def plot_pole(poles : List[complex], 
              zeros : List[complex], 
              scale_fac : float,
              name : str,
              figsize : Tuple[int] = (16, 10),
              save_fig : bool = False) -> None:
    '''
    

    Parameters
    ----------
    poles : List[complex]
        list of sensor poles
    zeros : List[complex]
        list of sensor zeros
    scale_fac : float
        scale factor
    name : str
        name of sensor
    figsize : Tuple[int], optional
        figure size. The default is (16, 10).
    save_fig : bool, optional
        whether plot will be saved to current dir. The default is False.

    Returns
    -------
    None
        plot frequency responce of sensor

    ''' 

    h, f = paz_to_freq_resp(poles, zeros, scale_fac, 0.005, 10**6, freq=True)
    title = f'Frequency Response of {name}'
    plt.figure(figsize = figsize)
    plt.subplot(121)
    plt.loglog(f, abs(h))
    plt.xlabel('Frequency, Hz')
    plt.ylabel(r'Amplitude, $\frac{V}{(\frac{m}{s^2})}$')
    
    plt.subplot(122)
    phase = np.angle(h)
    plt.semilogx(f*2*np.pi, phase)
    plt.xlabel('Frequency, Hz')
    plt.ylabel(r'Phase, rad')
    plt.suptitle(title)
    plt.subplots_adjust(wspace=0.3)
    
    if save_fig:
        plt.savefig(title.replace(' ', '_'))
    plt.show()