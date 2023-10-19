import requests
import json
import re

url = 'https://sg-wiki-api-static.hoyolab.com/hoyowiki/genshin/wapi/entry_page?entry_page_id=4365'

res = requests.get(url)

res.encoding = 'utf-8'

res = json.loads(res.text)

data = res['data']['page']['modules'][4]['components'][0]['data']

data = json.loads(data)

print(data)

for item in data['list']:
    item['desc'] = ' '.join(re.sub(r'<[^>]*>', ' ', item['desc']).split())
    print(item['desc'])

# data = json.dumps(data)

# with open('data.json', 'w') as f:
#     f.write(data)

# res = json.dumps(res)


# with open('xxx.json', 'w') as f:
#     f.write(res)