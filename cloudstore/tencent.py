import time

import requests
import json
import xlsxwriter

sunType0 = {}
sunType1 = {"1011": "开发者工具", "1012": "安全", "1014": "应用镜像", "1079": "网络组件", "1080": "容灾与高可用"}
sunType2 = {"1092": "账号安全审计", "1093": "应用安全", "1094": "网络安全", "1095": "主机安全", "1096": "安全测评", "1048": "数据安全"}
sunType3 = {"1051": "办公管理", "1050": "销售管理", "1087": "财务管理", "1088": "人事管理", "1089": "生产链管理", "1090": "云通信",
            "1053": "工具软件", "1098": "应用开发"}
productType = {"全部产品": sunType0, "镜像服务": sunType1, "安全": sunType2, "企业应用": sunType3}


def getMap(dataL):
    url = "https://market.cloud.tencent.com/ncgi/search/getSearch?t=&uin=&csrfCode=&reqSeqId="
    header = {
        "Host": "market.cloud.tencent.com",
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

    res = requests.post(url, data=dataL, headers=header).text
    pageMap = json.loads(res)
    return pageMap


def formatSheet(sheet):
    sheet.set_column('A:A', 60)
    sheet.set_column('B:B', 10)
    sheet.set_column('C:C', 10)
    sheet.set_column('D:D', 20)
    sheet.set_column('E:E', 40)
    sheet.set_column('F:F', 60)
    sheet.set_column('G:G', 10)
    return sheet


def insertLow(sheet, dataL, num, ):
    page = 1
    while 1:
        productMap = getMap(data)
        page += 1
        data["page"] = page
        # 每次请求延迟1秒
        # time.sleep(1)
        print("获取第" + str(page) + "页数据开始")
        productSet = productMap["data"]
        products = productSet["productSet"]
        for product in products:
            # 定义接收数据
            deliverType = product["deliverType"]
            isvName = product["isvName"]
            minPrice = product["minPrice"]
            price = float(minPrice["price"]) / 100
            spec = minPrice["spec"]
            productId = product["productId"]
            productName = product["productName"]
            categoryId = product["categoryId"]
            companyName = product["companyName"]
            comments = product["comments"]
            url = "https://market.cloud.tencent.com/products/" + str(productId)
            # 定义插入行
            productList = [productName, deliverType, price, spec, isvName, url, categoryId]
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


# sheet中插入数据
def insertSheet(classify, sheetName):
    global sun, data
    print("开始爬取:" + sheetName)
    sheet = workbook.add_worksheet(sheetName)
    sheet = formatSheet(sheet)
    num = 2
    # 初始化第一行
    init = ["应用名", "交付方式", "价格", "版本类型", "厂商", "url", "分类"]
    sheet.write_row("A1", init, bold)
    if len(classify) == 0:
        data = {
            "count": 15, "page": 1
        }
        # insertLow(sheet, data, num)
    else:
        for sun in classify:
            data = {
                "count": 15, "page": 1, "categoryId": int(sun)
            }
            print("正在爬取:" + sheetName + "----中----" + classify[sun] + "---分类" + sun)
            insertLow(sheet, data, num)
            # 合并单元格
            rowA = 'A' + str(num)
            rowG = 'G' + str(num)
            row = rowA + ":" + rowG
            num += 1
            sheet.merge_range(rowA, rowG,classify[sun])


filename = "../tencent.xlsx"
workbook = xlsxwriter.Workbook(filename)
bold = workbook.add_format({
    'bold': True,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#67C5F2',  # 单元格背景颜色
    'text_wrap': False,  # 是否自动换行
})
for sunClassify in productType:
    insertSheet(productType[sunClassify], sunClassify)

workbook.close()
print("运行结束")
