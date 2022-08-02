from lxml import etree
import latex2mathml.converter
from typing import Tuple


def latex_to_word(latex_input : str):
    '''
    From https://github.com/python-openxml/python-docx/issues/320#issuecomment-798749198

    Parameters
    ----------
    latex_input : str
        string with latex

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    mathml = latex2mathml.converter.convert(latex_input)
    tree = etree.fromstring(mathml)
    xslt = etree.parse(
        '/home/lapa/Complex-curve-fit/RESP/templates/MML2OMML.XSL'
        )
    transform = etree.XSLT(xslt)
    new_dom = transform(tree)
    return new_dom.getroot()


def scien_format(var : float) -> Tuple[float, int]:
    '''
    

    Parameters
    ----------
    var : float
        variable to convert

    Returns
    -------
    Tuple[float, int]
        return var and power of E. E.g. for var = 12120000 returns 12.12 and 4 

    '''
    y = '%.2E' % var
    x,y = y.split("E+")
    return (float(x), int(y))

def fill_equation(math_equation : str, **kwargs : float) -> str:
    '''
    

    Parameters
    ----------
    math_equation : str
        latex equation
    **kwargs : float
        values to fill equation

    Returns
    -------
    str
        filled equation

    '''
    for val in kwargs:
        if math_equation.find(str(val)) == -1:
            print(f'Variable {val} not exist in this equetion')
            continue
        math_equation = math_equation.replace(str(val), str(kwargs[val]))
    return math_equation
