import requests
import json
import xlsxwriter

# 目标
sunType0 = {"102003": "代维服务"}
sunType1 = {"110001": "基础环境", "110007": "业务管理", "110020": "集成应用"}
sunType2 = {"115001": "协同办公", "115009": "人事管理", "115030": "财务管理"}
sunType3 = {"120001": "网络安全", "120002": "主机安全", "120004": "数据安全", "120006": "应用安全", "120008": "应用安全", "120011": "安全测试",
            "120012": "安全管理", "120013": "认证准入"}
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
    return json.loads(res)["result"]["result"]


def insertExcel(sheet,types_key,types_value,num,cid):
    page = 1
    cid = cid + "," + types_key
    while 1:
        products = requestUrl(page,cid)
        for product in products:
            title = product["title"]
            price = product["price"]
            types = types_value
            vendor_name = product["vendorName"]
            url = product["link"]
            scene_keywords = str(product["sceneKeywords"])
            # 定义插入行
            productList = [title, price, types, vendor_name, url, scene_keywords]
            site = "A" + str(num)
            num += 1
            sheet.write_row(site, productList, bold)
        pageNum = len(products)
        print("获取第：" + str(page) + "数据结束" + "---本页数据" + str(pageNum) + "条")
        # 测试使用
        # if page == 2:
        #     break
        if pageNum < 15:
            break
    return num


def insertSheet(typesKey,typesValue):
    lists = typesKey.split(":")
    print(lists[0])
    print(lists[1])
    cid = lists[0]
    sheet_name = lists[1]
    if len(lists) < 2:
        print("!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!")
    sheet = workbook.add_worksheet(sheet_name)
    num = 2
    # 初始化第一行
    init = ["应用名", "价格","分类", "厂商", "url", "标签"]
    bold_title = workbook.add_format({
        'bold': True,  # 字体加粗
        'border': 1,  # 单元格边框宽度
        'align': 'center',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
        'fg_color': '#67C5F2',  # 单元格背景颜色
        'text_wrap': False,  # 是否自动换行
    })
    # 每个sheet中的子分类
    for productType in typesValue:
        num = insertExcel(sheet,productType,typesValue[productType],num,cid)


# 创建excle文件
filename = "../baidu.xlsx"
workbook = xlsxwriter.Workbook(filename)
bold = workbook.add_format({
    'bold': False,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#67C5F2',  # 单元格背景颜色
    'text_wrap': False,  # 是否自动换行
})
for types in allType:
    insertSheet(types,allType[types])
workbook.close()
# baiDuMap = requestUrl(1, 102)
# 测试
# products = baiDuMap["result"]["result"]
# for product in products:
#     del product["link"]
#     del product["digest"]
#     del product["thumbnail"]
#     print(product)
