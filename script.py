import pandas as pd
from xlrd import *
import numpy as np

bankFile=pd.read_excel(r'C:\Users\mufit\Downloads\/relevedescomptes.xlsx',usecols='C,D,G',skiprows=[0,1,2,3,4,5])
bankFile.dropna(inplace=True)
pd.set_option('display.max_columns',None)

# pd.set_option('max_colwidth',None)
pd.set_option('max_rows',None)


sub=["Delhaize"]

data=bankFile.sort_values("Operation")
li=[]
for i in sub:
    operation_Name=data[data['Operation'].str.contains(i)]
    #print(operation_Name["Amount"])
    amounts=operation_Name["Amount"]
    #print(amounts)
    for row in amounts:
        li.append(row)
        #print(row)

print(sum(li))


#print(data[data['Operation'].str.contains(sub)])


if __name__ == '__main__':
    pass
