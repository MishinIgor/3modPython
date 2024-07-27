# import json module
import json
 
# list of dictionaries of employee data
data = [{"id": ("1", "2", "3"), "name": ("bhanu", "sivanagulu","И ещё Я"),
         "department": ("HR", "IT")},
        {"id": ("4", "5", "6"), "name": ("sai", "poori"),
         "department": ("HR", "IT")},
        {"id": ("7", "8", "9"), "name": ("teja", "gowtam"),
         "department": ("finance", "IT")},
        {"id": ("10", "11", "12"), "name": ("sai", "jyothi"),
         "department": ("business", "IT")},
        {"id": ("13", "14", "15"), "name": ("prudhvi", "nagendram"),
         "department": ("business", "IT")}]
 
#Запись в файл mydata.json
with open("mydata.json", "w",encoding='utf-8') as final:
    json.dump(data, final)

with open('mydata.json', encoding='utf-8') as f:
    pr_json = json.load(f)
print(pr_json)