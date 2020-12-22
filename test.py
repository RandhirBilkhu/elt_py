from elt_py.elt import Elt
from elt_py.ylt import Ylt

import pandas as pd

X = pd.read_csv("C:/Users/randz/Desktop/Py_Projects/elt_py/example.csv")

elt = Elt(X)

elt.parameterise()

print(elt.df)

ylt = Ylt(elt.df)

ylt.generate_ylt(sims=2000)

print(ylt.df)

print(ylt.oep())
