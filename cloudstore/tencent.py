import requests
import json
import xlsxwriter


def getMap(page):
    url = "https://market.cloud.tencent.com/ncgi/search/getSearch?t=1648518326675&uin=&csrfCode=&reqSeqId="
    header = {
        "Host": "market.cloud.tencent.com",
        "Cookie": "market-device-id=a9e34b98cc63112b11c6c8ae0c70eddb",
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
    pageMap = json.loads(res)
    return pageMap


# def insertList(productList):
#     return 0;
#

count = 0
productMap = getMap(1)
productSet = productMap["data"]
products = productSet["productSet"]
filename = "../tencent.xlsx"
workbook = xlsxwriter.workbook(filename)
sheet = workbook.add_worksheet('全部产品')
# 初始化第一行
init = ["应用名", "交付方式", "价格", "版本类型", "specId", "厂商"]
sheet.write_row("A1", init)
num = 2
for product in products:
    # 定义接收数据
    categoryId = product["categoryId"]
    commentTime = product["commentTime"]
    deliverType = product["deliverType"]
    flags = product["flags"]
    illustrations = product["illustrations"]
    insertTime = product["insertTime"]
    isProprietary = product["isProprietary"]
    isvName = product["isvName"]
    l2Score = product["l2Score"]
    logo = product["logo"]
    minPrice = product["minPrice"]
    price = minPrice["price"]
    spec = minPrice["spec"]
    specId = minPrice["specId"]
    productId = product["productId"]
    productName = product["productName"]
    publishTime = product["publishTime"]
    score = product["score"]
    selectionMaterialsAuditState = product["selectionMaterialsAuditState"]
    sortFactor = product["sortFactor"]
    summary = product["summary"]
    tagIds = product["tagIds"]
    tags = product["tags"]
    times = product["times"]
    tips = product["tips"]
    weight = product["weight"]
    companyName = product["companyName"]
    comments = product["comments"]
    # 定义插入行
    productList = [productName, deliverType, price, spec, specId, isvName, productId]
    site = "A" + num
    num += 1
    sheet.write_row(site, productList)
workbook.close()
