import csv
import pandas as pd
import json

# xl = pd.read_excel("./region_code_dropdown.xlsx")
# xl.to_csv("./region_code_dropdown.csv")

f = open('./region_code_dropdown.csv','r', encoding='UTF-8')
region_code_data = csv.reader(f)

region_code_dic = {}

temp1 = []
temp2 = []
temp3 = []

for line in region_code_data:
    if str(line[2]) != '':
        temp1.append(str(line[2]))
    if str(line[3]) != '':  
        temp2.append(str(line[3]))
    if str(line[4]) != '':
        temp3.append(str(line[4]))

region_code_dic['3'] = temp3

with open('./region3.json', 'w', encoding='utf-8') as make_file:
    json.dump(region_code_dic, make_file, ensure_ascii=False)