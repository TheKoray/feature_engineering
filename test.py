import numpy as np
import pandas as pd

from feature import feature

data = pd.read_csv('https://www.openml.org/data/get_csv/16826755/phpMYEkMl')

data = data.replace('?', np.nan)

data.to_csv('titanic.csv',index = False)

#%% 
import pandas as pd

data = pd.read_csv('titanic.csv', usecols=['age','fare','survived'])

ky = feature(data,'age')

dagılım = ky.feature_dist(dagılım='Normal',distance=3, low_up='up')

print(dagılım)