from functions.laplace_func import to_laplace
import os

dir_name = '/home/lapa/Complex-curve-fit/RESP/examples/4211/!Device_No-387'
os.chdir(dir_name)
for file in os.listdir():
    if '.' not in file:
        to_laplace(file)
