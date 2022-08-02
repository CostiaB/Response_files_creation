from functions.create_RESP_func import create_resp
import os


folder = '/home/lapa/Complex-curve-fit/RESP/examples/4211/!Device_No-387'
device_type = 'CME4211'
freq = '60'
sensitivity = 2000

for file in os.listdir(folder):
    
    if 'Laplace_' in file:
        if 'Vert' in file:
            channel = 'Z'
        else:
            channel = 'N'
        file = os.path.join(folder, file)
        create_resp(file, channel, device_type, freq, resp_folder=folder)
