import requests
import json

url = 'https://api.ambr.top/v2/en/gcg/1101'

res = requests.get(url)

res.encoding = 'utf-8'

res = json.loads(res.text)

print(res)
