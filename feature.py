import numpy as np

class feature():

    def __init__(self,df,variable):

        self.df = df
        self.variable = variable 

    def feature_zero(self):

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),0,
            self.df[self.variable]
        )
        return self.df[self.variable].isnull().mean()

    def feature_mean(self):

        mean = self.df[self.variable].mean()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            mean,
            self.df[self.variable]
        )
        return self.df[self.variable].isnull().mean()

    def feature_mod(self):

        mod = self.df[self.variable].mode()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            mod,
            self.df[self.variable]
        )

        return self.df[self.variable].isnull().mean()

    def feature_median(self):

        median = self.df[self.variable].median()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            median,
            self.df[self.variable]
        )
    
        return self.df[self.variable].isnull().mean()
    
    def arbitary_value(self,value):

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            value,
            self.df[self.variable]
        )
        print(f"Missing Values fill {value}")

        return self.df[self.variable].isnull().mean()

    def missing_feature(self,nan_cols):

        if len(nan_cols) > 1:

            for cols in nan_cols:
                
              self.df[cols + '_nan'] = np.where(
              self.df[cols].isnull(),1,0)
            miss_id = [cols for cols in self.df.columns if 'nan' in cols]
            
            return self.df[miss_id]
        
        else:
            self.df['missing_indicator'] = np.where(self.df[self.variable].isnull(),1,0)

            return self.df[[self.variable,'missing_indicator']]

    def feature_dist(self, dagılım, distance = 3, low_up = 'up'):

        if dagılım == 'normal':

            mean = self.df[self.variable].mean()
            std = self.df[self.variable].std()
            result = np.add(mean, np.multiply(3,std))

            self.df[self.variable] = np.where(
                self.df[self.variable].isnull(),
                result,
                self.df[self.variable]
            )
        if dagılım == 'carpık':

            Q1 = self.df[self.variable].quantile(0.25)
            Q3 = self.df[self.variable].quantile(0.75)
            IQR = distance * (Q3 - Q1)

            lower = Q1 - IQR
            upper = Q3 + IQR

            if low_up == 'low':

                self.df[self.variable] = np.where(
                    self.df[self.variable].isnull(),
                    lower,
                    self.df[self.variable]
                )
            
            if low_up == 'up':

                self.df[self.variable] = np.where(
                    self.df[self.variable].isnull(),
                    upper,
                    self.df[self.variable]
                )
        else:
           print("Please enter correct parameters!")
        return self.df[self.variable].isnull().mean()
    
    def category_feature(self, plot = False):
        """
        - Kategorik değişkenlerdeki eksik değerlerimizi 'eksik' adında değeri atayacağız.
        """

        if self.df[self.variable].dtypes == 'object':

            self.df[self.variable] = np.where(

                self.df[self.variable].isnull(),
                'Eksik',
                self.df[self.variable]

            )
            return self.df[self.variable].isnull().mean()
            
        else:
            print(f"{self.variable} değişkenin tipi 'object' değildir!")
        
        if plot == True:

            print(self.df[self.variable].value_counts().plot.bar())

    def OneHotEncoder(self, cols, drop_cols = False):

        value = self.df[cols].unique()
        
        for i in value:

            self.df[i] = np.where(

                self.df[cols].isin([i]),1,0
            )

        if drop_cols == True:

            self.df.drop(i, axis=1, inplace = True)
        
        return self.df
    
    def LabelEncoder(self,cols):

        value = self.df[cols].unique()

        count = 0

        for i in value:

            self.df[cols] = np.where(self.df[cols] == i, 
                count,
                self.df[cols]
            )
            count +=1

        return self.df

    def top_features_ohe(self,cols, number = 10 ,show_top10 = False):

        """
        - Kategorik Değişkenimizin değerlerinin top 10 değerlerini alacağız.
        - Bu değerlere One hot encoding uygulayacağız.

        """

        "cols = self.variable"

        top_10 = self.df[cols].value_counts().sort_values(ascending = False).head(int(number)).index
        
        top_10 = [i for i in top_10]

        if show_top10: #Değişkenin top 10 değerlerini görmek istersek.

            print(f" {cols} Değişkenin top 10 değerleri : \n{top_10}")

        for value in top_10:

            self.df[cols + '_' + value] = np.where(
                self.df[cols ] == value, 1, 0
            )

        return self.df[[cols] + [cols + '_' + i for i in top_10]].head(10)
        


        



        










        
