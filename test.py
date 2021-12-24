import numpy as np
import pandas as pd

#import create feature engineering module for missing 
from feature import feature 

data = pd.read_csv('https://www.openml.org/data/get_csv/16826755/phpMYEkMl')

data = data.replace('?', np.nan)

data.to_csv('titanic.csv',index = False)

#%% 
import pandas as pd

data = pd.read_csv('titanic.csv', usecols= ['age','fare','survived','cabin','embarked'])

data['cabin'] = data['cabin'].astype("str").str[0]

data = data[data['cabin']!= 'T']

data.dropna(subset=['embarked'], inplace=True)

data_house = pd.read_csv('house.csv',usecols= ['Neighborhood','Exterior1st', 'Exterior2nd', 'BsmtQual' ,'SalePrice'])


ky = feature(data,'age')


print(ky.random_sample(cols = 'age'))

#print(ky.feature_zero())

# mean imputation for missing values
#ky.feature_mean()

# mode imputation for missing values
#ky.feature_mod()

# median imputation for missing values
#ky.feature_median()

# missing indicatory create new feature
#ky.missing_feature(nan_cols = ['age'])

# arbitary value imputation for missing values
#print(ky.arbitary_value(value = 20))

#according to  feature distribution value impututation for missing values 
#ky.feature_dist(dagılım ='normal',distance=3, low_up='up')

#ky.prob_ratio_encoding(cols = "cabin",target = "survived")

#ky.mean_target_encoding(cols = 'cabin', target = 'survived')

#print(data.head())

#print(data_house.head())

ky_house = feature(data_house, 'Neighborhood')

#print(ky_house.category_feature(data,'BsmtQual', plot = True))

#ohe_top = ky_house.top_features_ohe(cols = 'Neighborhood', number=10,show_top10=True)

#ky_house.ordinary_encoding(cols= 'Neighborhood', show_dict= True)

#print(ky_house.encoding(cols = 'Neighborhood', how = 'frequency'))

#print(data_house.head())
