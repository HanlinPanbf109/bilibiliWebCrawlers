import pandas as pd

# 读取CSV文件
df = pd.read_csv('')#替换为文件名

#转化csv文件到xlsx
xlsx_file='.xlsx'
df.to_excel(xlsx_file,index=False)      
