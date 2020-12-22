class Elt:
    
    def __init__(self,pandas_obj):
        self.df = pandas_obj
        self._validate(pandas_obj)
    
    @staticmethod
    def _validate(obj):
        # verify the minumum required columns are present in the intial dataframe
        if 'id' not in obj.columns or 'rate' not in obj.columns or 'mean' not in obj.columns or 'sdevi' not in obj.columns or 'sdevc' not in obj.columns or 'exp' not in obj.columns:
            raise AttributeError("dataframe must have id, rate, mean, sdevi, sdevc and exp columns")

    def parameterise(self):
        self.df['mdr'] = self.df['mean']  /self.df['exp']   # calculates the mean damage ratio equivalent to average loss over total exposed
        self.df['sdev'] = self.df['sdevi'] + self.df['sdevc'] # sums up the correlated and independent standard deviations 
        self.df['cov'] = self.df['sdev'] /self.df['mean'] # calculates covariance based on total standard deviation
        self.df['alpha'] = (1 - self.df['mdr']) / (self.df['cov']**2 - self.df['mdr']) # generates an alpha parameter for beta distribution
        #alpha is finite <-0 TODO
        self.df['beta'] = (self.df['alpha'] * (1 - self.df['mdr'])) / self.df['mdr']  # generates a beta parameter for beta distribution
        self.df['rand_num'] = self.df['rate'] / self.df['rate'].sum()  # probability of event occuring = normalised event frequency 
        self.df.index += 1 ### want to set index to start from 1 ( so sampling works)

    @property
    def events(self):
        total = self.df['rate'].sum()
    
        





