import pandas as pd


lamoda = pd.read_csv('lamoda.csv', index_col='ID')
asos = pd.read_csv('asos_1.csv', index_col='ID')
lamoda_groupby = lamoda.groupby(['Brand', 'Category'])['Price'].agg(['max', 'min', 'median'])
asos_groupby = asos.groupby(['Brand', 'Category'])['Price'].agg(['max', 'min', 'median'])
print(asos_groupby[:100])
asos['site'] = asos.apply(lambda row: 'asos', axis=1)
lamoda['site'] = lamoda.apply(lambda row: 'lamoda', axis=1)

all_clothes = pd.concat([asos, lamoda])
all_clothes_groupby = all_clothes.groupby(['Brand', 'Category', 'site'])['Price'].agg(['max', 'min', 'median'])
print(all_clothes_groupby[:50])
(pd.concat([asos, lamoda])).to_csv('concat.csv', )






