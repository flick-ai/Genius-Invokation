import requests
base_url = 'https://sg-wiki-api.hoyolab.com/hoyowiki/genshin/wapi/get_entry_page_list'

res = requests.post(base_url)

print(res)