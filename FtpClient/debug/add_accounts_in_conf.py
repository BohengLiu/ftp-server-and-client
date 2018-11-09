import os
import json

accounts ={ 'users':['admin'],
    'data':{
        'admin':{
            'name':'admin',
            'pwd':'123456',
            'Permission':999,
            'space':1073741824,
            'used':0
                },
        'dog1':{
            'name':'dog1',
            'pwd':'dog123',
            'Permission':1,
            'space':1024024,
            'used':0
        }
    }
}
content = json.dumps(accounts)
print(content)

cwd = os.getcwd()
parwd = os.path.dirname(cwd)
filename = os.path.join(parwd,'conf','accounts.json')

with open(filename,'w',encoding='utf-8') as f:
    json.dump(accounts,f)

with open(filename,'r',encoding='utf-8') as f:
    data = json.load(f)
print(data)