import imdlib as imd
import csv
import pandas as pd
import os, glob
import os.path
from os import path
csv_file = 'latlon-input.csv'
start_yr = int(input("Enter start year : "))
end_yr = int(input("Enter end year(till 2020) : ")) 
lats=[]
lons=[]
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lats.append(float(row.get('lat')))
        lons.append(float(row.get('lon')))
pars = ["rain","tmax","tmin"]
for i in range(len(lats)):
    for variable in pars: 
        lat=lats[i]
        lon=lons[i]
        #variable = 'rain' # other options are ('tmin'/ 'tmax')
        for y in range(start_yr,end_yr+1,1):
            if not path.exists(variable + "\\" + str(y) + ".GRD"):
                print("file: " + variable + "\\" + str(y) + ".GRD" + " doesn't exist, downloading")
                data = imd.get_data(variable, y, y, fn_format='yearwise')
                data = imd.open_data(variable, y, y,'yearwise')
                data.to_csv("temp\\" + variable + '-' + str(y) + '.csv', lat, lon,)
                continue
            print("imd-get- " + str(y))
            data = imd.open_data(variable, y, y,'yearwise')  #data = imd.open_data(variable, start_yr, end_yr,'yearwise')   #ds = data.get_xarray()
            data.to_csv("temp\\" + variable + '-' + str(y) + '.csv', lat, lon,)
        fl = glob.glob(os.path.join("temp\\" + variable + "-*"+ str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv'))
        cb_var=pd.concat([pd.read_csv(f) for f in fl])
        cb_var.to_csv("temp\\" + variable + '_' + str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv', index=False)
        for f in fl:
            os.remove(f)
    f1=pd.read_csv("temp\\" + 'tmax_' + str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv')
    f2=pd.read_csv("temp\\" + 'tmin_' + str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv')
    f3=pd.read_csv("temp\\" + 'rain_' + str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv')
    mer1=f1.merge(f2,on='DateTime')
    mer2=mer1.merge(f3,on='DateTime')
    mer2.to_csv(str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv',header=['Date','Tmax','Tmin','Rain'],index=False)
    
    

    filelist = glob.glob(os.path.join("*_"+ str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv'))
    for f in filelist:
        os.remove(f)
    print("created the file: " + str(f'{lats[i]:.2f}') + '_' + str(f'{lons[i]:.2f}') + '.csv and deleted the temp files') 