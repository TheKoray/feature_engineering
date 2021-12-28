import numpy as np


class gauss():

    def log_transform(self,df,cols, plt = False):

        df[cols + '_log'] = np.log(df[cols])

        if plt:

            df[cols].hist(bins=30)
        
        return df[[cols,cols + '_log']]

    def Reciprocal(self,df,cols,plt = False):

        df[cols + '_reciprocal'] = np.divide(1,df[cols])

        if plt:

            df[cols + '_reciprocal'].hist(bins=30)
        
        return df[[cols, cols + '_reciprocal']]
    
    def Square_root(self,df,cols):

        df[cols + '_squareRoot'] = df[cols] ** (1/2)

        return df[[cols,cols + '_squareRoot']]
    

