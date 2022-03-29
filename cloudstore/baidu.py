import requests
import json
import xlsxwriter

# 目标
sunType0 = {"102003": "代维服务"}
sunType1 = {"110001": "基础环境", "110007": "业务管理", "110020": "集成应用"}
sunType2 = {"115001": "协同办公", "115009": "人事管理", "115030": "财务管理"}
sunType3 = {"120001": "网络安全", "": "", "": "", "": "", "": "", "": "", "": "", "": "", "": "", "": "", "": "", "": ""}
allType = {"102:上云服务": sunType0, "110：镜像环境": sunType1, "115:企业应用": sunType2, "120:安全服务": sunType3, "125": "数据应用",
           "130": "API服务", "135": "人工智能", "140": "区块链", "145": "泛机器人", "150": "公司服务", }


def requestUrl(page, cid):
    header = {
        "Host": "market.baidu.com",
        "Sec-Ch-Ua": "\" Not A;Brand\";v = \"99\", \"Chromium\";v = \"96\"",
        "Accept": "application / json, text / javascript, * / *; q = 0.01",
        "Mode": "cors",
        "Content-Type": "application / json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.baidu.com/list/0?keyword=&label=&cid=102,102&priceFrom=0&pageNo=2&tag=",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    url = "https://market.baidu.com/api/market/web/list/0/products?keyword=&label=&cid=" + str(
        cid) + "&priceFrom=0&pageNo=" + str(page) + "&tag="
    res = requests.get(url, headers=header).text
    return json.loads(res)


baiDuMap = requestUrl(1, 102)
products = baiDuMap["result"]["result"]
for product in products:
    del product["link"]
    del product["digest"]
    del product["thumbnail"]
    print(product)
