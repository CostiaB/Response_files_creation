def sign(number) -> str:
    '''
    

    Parameters
    ----------
    number : TYPE
        number to define the sign

    Returns
    -------
    str
        sign of number

    '''
    if number < 0:
        return '-'
    else:
        return '+'
    
    
def get_pole_dict(poles : list, i : int) -> dict:
    '''
    

    Parameters
    ----------
    poles : list
        list of poles
    i : int
        number of element

    Returns
    -------
    dict
        dictionary with pole information

    '''
    
    pole_dict = dict()
    pole_dict['poles_list'] = [i+1]
    pole_dict['real'] = poles[i].real
    pole_dict['sign'] = set(sign(poles[i].imag))
    pole_dict['imag'] = poles[i].imag*1j   
    return pole_dict
        
def get_poles_table(poles : list) -> list:
    '''
    

    Parameters
    ----------
    poles : list
        list of poles

    Returns
    -------
    list
        list of dicts with grouped poles

    '''
    
    poles_for_table = []
    i = 0
    
    while i <= len(poles) - 1:
        if i == 0:
            poles_for_table.append(get_pole_dict(poles, i))
        else:
            if poles_for_table[-1]['real'] == poles[i].real \
                and poles_for_table[-1]['imag'].imag == abs(poles[i].imag):
                    
                    poles_for_table[-1]['poles_list'].append(i+1)
                    poles_for_table[-1]['sign'].add(sign(poles[i].imag))
            else:
                poles_for_table.append(get_pole_dict(poles, i))
        i += 1
    return poles_for_table  


