import numpy as np
import pandas as pd

#import create feature engineering module for missing 
from feature import feature 

data = pd.read_csv('https://www.openml.org/data/get_csv/16826755/phpMYEkMl')

data = data.replace('?', np.nan)

data.to_csv('titanic.csv',index = False)

#%% 
import pandas as pd

data = pd.read_csv('titanic.csv', usecols=['age','fare','survived'])


ky = feature(data,'age')

# mean imputation for missing_values
ky.feature_mean()

# mode imputation for missing_values
ky.feature_mod()

# median imputation for missing_values
ky.feature_median()

# missing indicatory create new feature
ky.missing_feature()

#according to  feature distribution value impututation for missing values 
ky.feature_dist(dagılım='normal',distance=3, low_up='up')
