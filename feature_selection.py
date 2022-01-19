
class feature_selection():

    def __init__(self,df):

        self.df = df

    def Constant_Features(self, variable, show = False, drop = False):

        if variable == 'numerik':

            num_features = [cols for cols in self.df.columns if self.df[cols].dtypes != 'o']

            constant_num = [cols for cols in num_features if self.df[cols].std() == 0]

            if show == True:

                print(constant_num)

            if drop == True:

                self.df.drop(labels = constant_num, axis =1, inplace = True)
        
        elif variable == 'categorik':

            cat_features = [cols for cols in self.df.columns if self.df[cols].dtypes == 'o']

            constant_cat = [cols for cols in cat_features if self.df[cols].nunique() == 1]

            if show == True:

                print(constant_cat)
            
            if drop == True:

                self.df.drop(labels = constant_cat, axis = 1, inplace = True)









        
        

