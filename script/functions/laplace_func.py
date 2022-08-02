from functions.plote_pole_func import plot_pole
from typing import Tuple, List
from math import pi


def read_approx_file(filename : str) -> Tuple[int, List[complex], List[complex]]:
    '''
    

    Parameters
    ----------
    filename : str
        name of file with path in which approximation paramerets saved

    Returns
    -------
    scale_fac : float
        scale factor
    zeros : List[complex]
        list of zeros
    poles : List[complex]
        list of poles
    '''
    with open(filename, 'r') as f:
        line = f.readline()
        scale_fac, n_zeros = line.replace('\n', '').split(' ')
        scale_fac = float(scale_fac)
        n_zeros = int(n_zeros)
        zeros = [0.0j for _ in range(n_zeros)]
        poles = []
        while True:
            line = f.readline()
            if not line:
                break
            pole = list(map(float, line.replace('\n', '').split(' ')))
            pole = pole[0] + pole[1] * 1j
            poles.append(pole)
    return scale_fac, zeros, poles


def save_laplace(scale_fac : float,
                 n_zeros : int,
                 poles: List[complex],
                 filename : str) -> None:
    '''
    

    Parameters
    ----------
    scale_fac : float
        scale Laplace factor
    n_zeros : int
        number of zeros
    poles : List[complex]
        Laplace poles
    filename : str
        name of file

    Returns
    -------
    None
        save file with Laplace vars

    '''
    with open(filename, 'w') as f:
        f.write(f'{scale_fac} {n_zeros}\n')
        for pole in poles:
            f.write(f'{pole.real:.4f} {pole.imag:.4f}\n')
            

def to_laplace(filename : str, 
               save_file : bool = True) -> Tuple[float, int, List[complex]]:
    '''
    

    Parameters
    ----------
    filename : str
        name of file to read
    save_file : bool, optional
        whether file will be saved. The default is True.

    Returns
    -------
    scale_fac : float
        scale factor Laplace
    n_zeros : int
        number of zeros
    poles : List[complex]]
        list of Laplace poles

    '''
    scale_fac, zeros, poles = read_approx_file(filename)
    n_zeros = len(zeros)
    n_poles = len(poles)
    scale_fac = scale_fac*(2*pi)**(-n_zeros + n_poles)
    poles = [pole*2*pi for pole in poles]
    
    if save_file:
        save_laplace(scale_fac, n_zeros, poles, 'Laplace_' + filename)
    
    return scale_fac, n_zeros, poles



