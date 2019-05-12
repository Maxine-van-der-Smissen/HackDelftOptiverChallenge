import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import statsmodels.api as sm
from math import floor
plt.style.use('seaborn-whitegrid')
from sklearn import linear_model

class TinderTradingTechnique:

    def __init__(self):
        self.market_data = pd.read_csv("C:/Users/markb/OneDrive/Documents/hackathon/market_data.csv",parse_dates=True, index_col=0)
        #ESX
        self.esx = self.market_data[self.market_data['Instrument'] == 'ESX-FUTURE']
        #SP
        self.sp = self.market_data[self.market_data['Instrument'] == 'SP-FUTURE']
        self.sp_quantity = 0
        self.esx_quantity = 0

    def reg(self, x ,y):
        regr = linear_model.LinearRegression()
        x_constant = pd.concat([x,pd.Series([1]*len(x),index = x.index)], axis=1)
        regr.fit(x_constant, y)    
        beta = regr.coef_[0]
        alpha = regr.intercept_
        spread = y - x*beta - alpha
        return spread
        
    def spread(self):
        return self.reg(np.log(self.esx['Ask Price'].head(11000)), np.log(self.sp['Ask Price'].head(11000))).dropna()

    def check(self):
        self.sp['Ask Price'].plot()
        self.esx['Ask Price'].plot()
        plt.show()
    

    def decide(self, sp, exp):
        if(len(sp) < 250): return
        s = self.spread()
        threshold = 1
        mean = np.mean(s)
        std = np.std(s)
        ratio = floor(sp/exp)
        
        if s.tail(1)[-1] > mean + threshold * std:
            if((not self.esx_quantity > 0) and (not self.sp_quantity < 0)):
                self.sell("sp", 100)
                self.buy("exp",  ratio * 100)
        
        elif s.tail(1)[-1] < mean - threshold * std:
            if((not self.sp_quantity < 0) and (not self.esx_quantity > 0)):
                    self.sell("exp", 100)
                    self.buy("sp", ratio * 100) 

        else:
            self.liquidate()

    def sell(self, index, amount):
        print("selling", index, amount)

    def buy(self, index, amount):
        print("buying", index, amount)

    def liquidate(self):
        print("Selling all")
        self.sell(esx, self.esx_quantity)
        self.sell(sp, self.sp_quantity)
