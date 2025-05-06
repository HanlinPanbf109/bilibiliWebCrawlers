import pandas as pd

# 读取CSV文件
df = pd.read_csv('./result/直升机到底安全吗.csv')#替换为文件名

#转化csv文件到xlsx
xlsx_file='./result/直升机到底安全吗.xlsx'
df.to_excel(xlsx_file,index=False)      