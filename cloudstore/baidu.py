import requests
import json
import xlsxwriter
import excelUtil

# 目标
# 只有一条有效数据
# sunType0 = {"102003": "代维服务"}
sunType1 = {"110001": "基础环境", "110007": "业务管理", "110020": "集成应用"}
sunType2 = {"115001": "协同办公", "115009": "人事管理", "115030": "财务管理"}
sunType3 = {"120001": "网络安全", "120002": "主机安全", "120004": "数据安全", "120006": "应用安全", "120008": "应用安全",
            "120012": "安全管理", "120013": "认证准入"}
allType = {"110:镜像环境": sunType1, "115:企业应用": sunType2, "120:安全服务": sunType3, }
cloudName = "百度云"
n = 0


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
    return json.loads(res)["result"]["result"]


def insertExcel(sheet, types_key, types_value, num, cid,bold):
    page = 1
    cid = cid + "," + types_key
    while 1:
        products = requestUrl(page, cid)
        for product in products:
            title = product["title"]
            price = product["price"]
            types = types_value
            vendor_name = product["vendorName"]
            url = product["link"]
            scene_keywords = str(product["sceneKeywords"])
            # 定义插入行
            productList = [title, cloudName, price, types, "NULL", "NULL", vendor_name, url, scene_keywords]
            site = "A" + str(num)
            if clearData(scene_keywords, title):
                sheet.write_row(site, productList, bold)
                num += 1
        pageNum = len(products)
        print(types_value+">>>"+"获取第页：" + str(page) + "数据结束" + "---本页数据" + str(pageNum) + "条")
        page += 1
        if pageNum < 10:
            break
    return num


def insertSheet(sheet,num,bold):
    for types in allType:
        lists = types.split(":")
        cid = lists[0]
        if len(lists) < 2:
            print("!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!")
        # 每个sheet中的子分类
        for productType in allType[types]:
            num = insertExcel(sheet, productType, allType[types][productType], num, cid,bold)
    print("请求结束,本次总结" + str(num-n) + "条数据")
    return num


def clearData(lists, title):
    if ("一般纳税人" in lists) or ("法人变更" in lists) or ("短信平台" in lists) or ("员工钱包" in lists) or ("牲畜监管" in lists) or (
            "电商" in lists) or ("Java多版本" in lists) or ("灵活用工" in lists):
        print("标签过滤>>>" + str(lists))
        return False
    if ("Java运行环境" in title) or ("牲畜" in title) or ("茶叶" in title) or ("劳务派遣" in title):
        print("title过滤>>>" + title)
        return False
    return True


def add(sheet, num, bold):
    n = num
    num = insertSheet(sheet, num, bold)
    print("百度云运行结束")
    return num


# baiDuMap = requestUrl(1, 102)
# 测试
# products = baiDuMap["result"]["result"]
# for product in products:
#     del product["link"]
#     del product["digest"]
#     del product["thumbnail"]
#     print(product)
