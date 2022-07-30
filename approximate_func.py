import numpy as np
from typing import List, Tuple
from lmfit import Parameters
import matplotlib.pyplot as plt






def poles_to_poly(x : np.ndarray,
                  n : int,
                  a : float,
                  p : List[Parameters]) -> np.ndarray:
    '''
    

    Parameters
    ----------
    x : np.ndarray
        array of frequency points
    n : int
        number of poles
    a : float
        scale factor
    p : List[Parameters]
        list of parametrs of poles

    Returns
    -------
    np.ndarray
        current responce

    '''
    
    numerator = a * (x) ** n
    denom1= np.polyval(np.poly(p), x)
    denom2 = np.polyval(np.poly(np.conj(p)), x)
    
    return numerator / denom1 / denom2


def split_params(params : Parameters) -> (int, 
                                          List[Parameters]):
    '''
    

    Parameters
    ----------
    params : Parameters
        parameters to approximation

    Returns
    -------
    a : int
        scale factor
    n : int
        number of poles
    q_list : List[Parameters]
        list of parametrs of poles

    '''
    
    q_list = []
    for param_name in params:
        if param_name == 'a':
            a = params[param_name]
        elif param_name == 'n':
            n = params[param_name]
        elif '_q' in param_name:
            q = params[param_name]
            if 'complex' in param_name:
                q = -q + 1j * q
            q_list.append(q)
            
    return a, n, q_list


def residuals_compl_poles(params : Parameters, 
                          xdata_complex : np.ndarray,
                          ydata_complex : np.ndarray) -> np.ndarray :
    '''
    

    Parameters
    ----------
        numder of poles
    xdata_complex : np.ndarray
        calibr data 1
    ydata_complex : np.ndarray
        calibr data 2

    Returns
    -------
    np.ndarray
        residulas

    '''
    
    a, n, q_list = split_params(params)
    x = xdata_complex*2*np.pi
    diff = poles_to_poly(x, n, a, q_list) - ydata_complex
    resid = diff.view(np.float64)
        
    return resid



def plot_appoximation(xdata : np.ndarray,
                      ydata : np.ndarray,
                      final : np.ndarray,
                      ydata_complex : np.ndarray,
                      points : List[float] = [0.008,0.16,1,10,50,100],
                      figsize : Tuple[int] = (16,10),
                      with_approx : bool = True,
                      save_fig: bool = False,
                      fig_name: str = 'sensor_plot') -> None:
    '''
    

    Parameters
    ----------
    xdata : np.ndarray
        calibration data
    ydata : np.ndarray
        calibration data
    final : np.ndarray
        approximated data
    ydata_complex : np.ndarray
        calibration data
    points : List[float], optional
        points that will be show of plot. The default is [0.008,0.16,1,10,50,100].
    figsize : Tuple[int], optional
        plot size. The default is (16,10).
    with_approx : bool 
        wether approximation will be plot. The defaultt is True   
    save_fig : bool
        if plot shoud be saved to folder. The default is False
    fig_name : str
        name of figure when saved. The default is 'sensor_plot'
    
        

    Returns
    -------
    None
        show frequency and amplitude plot

    '''
    
    points_str = list(map(str, points))
    
    plt.figure(figsize = figsize)
    plt.rc('ytick', labelsize = 12)
    
    plt.subplot(2,1,1)
    plt.loglog(xdata, ydata, 'b', label = "calibrated sensor")
    if with_approx:
        plt.loglog(xdata, abs(final), 'r', label = "fitted sensor")
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    plt.yticks([10,100,2000],['10','100','2000'])
    plt.xticks(points , points_str)
    plt.title("Sensors frequency response", fontsize=20)
    plt.ylabel(r'Amplitude, $\frac{V}{(\frac{m}{s^2})}$', fontsize=10)
    plt.xlabel('Frequency, Hz', fontsize=10)
    plt.legend(loc = 'upper right')
    
    plt.subplot(2,1,2)
    plt.semilogx(xdata,np.angle(ydata_complex),'b', label = "calibrated sensor")
    if with_approx:
        plt.semilogx(xdata,np.angle(final),'r', label = "fitted sensor")
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    plt.xticks(points, points_str,fontsize=10)
    plt.yticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi],
               ['$\pi$',r'$-\frac{\pi}{2}$','0',r'$\frac{\pi}{2}$','$\pi$'])
    plt.title("Sensors phase", fontsize=20)
    plt.ylabel(r'Phase, rad', fontsize=10)
    plt.xlabel('Frequency, Hz', fontsize=10)
    plt.legend(loc = 'upper right')
    plt.tight_layout()
    
    if save_fig:
        plt.savefig(f"./{fig_name }.png")
    plt.show()
        