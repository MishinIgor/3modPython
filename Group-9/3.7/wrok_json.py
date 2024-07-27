# import json module
import json
 
# list of dictionaries of employee data
data = [{"id": ("1", "2", "3"), "name": ("bhanu", "sivanagulu"),
         "department": ("HR", "IT")},
        {"id": ("4", "5", "6"), "name": ("sai", "poori"),
         "department": ("HR", "IT")},
        {"id": ("7", "8", "9"), "name": ("teja", "gowtam"),
         "department": ("finance", "IT")},
        {"id": ("10", "11", "12"), "name": ("sai", "jyothi"),
         "department": ("business", "IT")},
        {"id": ("13", "14", "15"), "name": ("prudhvi", "nagendram"),
         "department": ("business", "IT")}]
 
with open("mydata.json", "w",encoding='utf-8') as final:
   json.dump(data, final,indent=1)
with open("clients_gr5.json",encoding='utf-8') as f:
   my_work = json.load(f)
# display
print(my_work)