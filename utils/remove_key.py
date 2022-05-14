import json

with open('./result.json') as file:
    data = json.load(file)
    
for dato in data:
     dato.pop('latitudine')
     dato.pop('longitudine')
    
with open('./result.json','w') as file_result:
  json.dump(data,file_result)