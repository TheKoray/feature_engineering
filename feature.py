import numpy as np
import pandas as pd 

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
        - NaN --> 'Eksik'
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
        
        if plot:

            return self.df[self.variable].value_counts().plot().bar()


    def random_sample(self,cols):
        
        self.df[cols + '_imputed'] = self.df[cols].copy()

        random_sample = self.df[cols].dropna().sample(self.df[cols].isnull().sum(),random_state = 0)

        random_sample.index = self.df[self.df[cols].isnull()].index
        
        self.df.loc[self.df[cols].isnull(), [cols + '_imputed']] = random_sample

        return self.df[[cols, cols + '_imputed']]

    "------------------------------ Encoding İşlemleri ----------------------------------------------"

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

    def ordinary_encoding(self, cols ,show_dict = False):

        """
        - Datamızın kategorik değişkenlerinin değerlerini numaralandırıyoruz.
        - O numalaralar ile o değişken değerlerini değiştiriyoruz.
        - LabelEncoder() işlemi gibi aslında.
        - show_dict = Etiketleri değiştireceğimiz sayısal değerleri görmemizi sağlar

          - False = Sayısal değerleri göstermez. Default değeridir.
          - True = Sayısal değerleri gösterir.
        """
        
        cols = self.variable

        ordinal_map = {v:k
            for k,v in enumerate(self.df[cols].unique(),0)
        }
        
        self.df[self.variable] = self.df[cols].map(ordinal_map)

        if show_dict:

            print(ordinal_map)

    def encoding(self, cols, how):

        """
        - Kategorik değişkenimizin etiketlerini sayısal değerlerle,
        - Kategorik değişkenimizin etiketlerini frekans değerleriyle
        değiştirebiliriz.
        - how = Etiktlerini ne ile değiştirmek istiyorsak onun bilgisini veririz.
           - number = Sayısal Değerler için
           - frequency = Frekans Değerler için
        """

        if how == 'number':

            ordinal_map = {

                v:k
                for k,v in enumerate(self.df[cols].unique())
            }
            
            self.df[cols] = self.df[cols].map(ordinal_map)

        elif how == 'frequency':

            frekans = (self.df[cols].value_counts() / len(self.df)).to_dict()

            self.df[cols] = self.df[cols].map(frekans)
        
        else :

            print("Please Enter Correct Parameter!")

    def mean_target_encoding(self,cols,target):

        """
        - Kategorinin değerleri için ortalama hedef değerle değiştirilmesi anlamına gelir.
        - target = Veri Setinde ki Hedef Değişkenimiz.
        """
        ordered = self.df.groupby(cols)[target].mean().to_dict()

        self.df[cols] = self.df[cols].map(ordered)

    def prob_ratio_encoding(self,cols,target):

        """
        - Bu kodlama yalnızca target değişkeninin binary olduğu durumlarda gerçekleşir.
        - Her değer için P(1) ve P(0) değerleri hesaplanır.
        - P(1) / P(0) ile dolduruz.
        - target = Veri Setinde ki hedef değişkenimiz.Değerleri "Binary" olmak zorunda.
        """

        #Target 1 olma olasılığı 
        prob_df = pd.DataFrame(self.df.groupby(cols)[target].mean())

        #target 0 olma olasılığı
        prob_df['zero'] = 1 - prob_df[target]
        
        #Olasılık Oran Değerleri
        prob_df['ratio'] = prob_df[target] / prob_df['zero']

        #Olasılık oran değerlerini dictionary haline çeviriyoruz.
        prob_ratio = prob_df['ratio'].to_dict()
        
        self.df[cols] = self.df[cols].map(prob_ratio)

    def rare_encoding(self,cols,tolerance,plot = False):

        temp_df = pd.Series(self.df[cols].value_counts() / len(self.df))

        rare_labels = temp_df[temp_df < tolerance].index.tolist()

        for value in rare_labels:

            self.df[cols] = np.where(self.df[cols].isin([value]), 'rare', self.df[cols])

        if plot:

            fig = self.df[cols].value_counts() / len(self.df).plot.bar()

            fig.set_xlabel(cols)
            fig.set_axhline(y = 0.05, color = 'red')
            plt.show()

        return self.df[cols]

    "------------------------------ Normal Dağılım Dönüşümü -------------------------------------------"

    