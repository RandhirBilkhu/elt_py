import numpy as np
import pandas as pd

class Ylt:
    """
    docstring
    """
    seed = np.random.seed(42)
    
    def __init__(self,pandas_obj):
        self.df = pandas_obj

    def generate_ylt(self, sims=10):

        num_events = np.random.poisson(self.df['rate'].sum(), sims) 

        sample_ids = np.random.choice( a = self.df['id'] , size = num_events.sum() , replace= True, p = self.df['rand_num'] ) 
        self.df = self.df[['id', 'alpha','beta','exp']].iloc[self.df.index.get_indexer(sample_ids)] ### this took some effort! 
        self.df['severity_mdr'] = self.df.apply( lambda x: np.random.beta( x['alpha'] , x['beta']  ) , axis=1 ) ### use apply with axis =1 to use function on each row
        self.df['severity'] = self.df['severity_mdr'] * self.df['exp'] ### this gives us severity for each event

        year = np.arange(1, sims + 1, 1) # start (included): 0, stop (excluded): 10, step:1
        all_years = pd.DataFrame(year , columns=['year'])

        self.df['year'] = np.repeat(year, num_events)
        self.df = self.df[['year', 'severity']]
        self.df = pd.merge(self.df, all_years, how='right').fillna(0)

    def oep(self):
        
        rp = pd.DataFrame([10000,5000,1000,500,250,200,100,50, 25,10,5,2], columns=['return_period'])
        rp['ntile'] = 1 - 1 / rp['return_period'] 
        return(self.df.groupby(['year'])['severity'].max().quantile(rp['ntile']))


    



    