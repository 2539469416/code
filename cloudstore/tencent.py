import requests
import json


def getMap(page):
    url = "https://market.cloud.tencent.com/ncgi/search/getSearch?t=1648458987437&uin=&csrfCode=&reqSeqId="
    header = {
        "Host": "market.cloud.tencent.com",
        "Cookie": "market-device-id=546b76e27c45dbb08bb0a7abe89d136d",
        "Content-Length": "15",
        "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Geck"
                      "o) Chrome/96.0.4664.45 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Origin": "https://market.cloud.tencent.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.cloud.tencent.com/categories?cid=0&page=3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",

    }
    data = {
        "count": "15",
        "page": page,
    }
    res = requests.post(url, data=data, headers=header).text
    map = json.loads(res)
    return map


map = getMap(1)
print("-------response------")
print(map)
print("---------------------")
productSet = map["data"];
products = productSet["productSet"]
for product in products:
    print(product['productName'])
