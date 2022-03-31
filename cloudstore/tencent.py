import time
import requests
import json
import xlsxwriter
import excelUtil

sunType1 = {"1011": "开发者工具", "1012": "安全", "1014": "应用镜像", "1079": "网络组件", "1080": "容灾与高可用"}
sunType2 = {"1092": "账号安全审计", "1093": "应用安全", "1094": "网络安全", "1095": "主机安全", "1096": "安全测评", "1048": "数据安全"}
sunType3 = {"1051": "办公管理", "1087": "财务管理", "1088": "人事管理"}
productType = {"镜像服务": sunType1, "安全": sunType2, "企业应用": sunType3}
allType = {"1001": "镜像服务", "1009": "运行环境", "1015": "操作系统", "1011": "开发者工具", "1012": "安全", "1076": "建站系统",
           "1014": "应用镜像", "1077": "数据与存储", "1078": "运维工具", "1079": "网络组件", "1080": "容灾与高可用", "1091": "安全",
           "1092": "账号安全审计",
           "1093": "应用安全", "1094": "网络安全", "1095": "主机安全", "1096": "安全测评", "1048": "数据安全", "1002": "小程序",
           "1022": "电商/零售", "1023": "餐饮/外卖", "1024": "生活服务", "1027": "政务民生", "1026": "小程序官网", "1028": "游戏",
           "1102": "公众号运营",
           "1025": "定制开发", "1082": "小程序运营", "1029": "其他", "1003": "网站建设", "1034": "企业官网", "1032": "电商网站",
           "1031": "网站模板", "1085": "网站定制", "1086": "网站服务", "1030": "APP开发",
           "1241": "企业邮箱", "1004": "专家服务", "1052": "企业服务", "1038": "上云迁移", "1100": "镜像维护", "1101": "部署实施",
           "1039": "日常代维", "1041": "故障排查", "1042": "专线接入", "1074": "系统保障", "1007": "数据智能", "1005": "企业应用",
           "1051": "办公管理",
           "1050": "销售管理", "1087": "财务管理", "1088": "人事管理", "1089": "生产链管理", "1090": "云通信", "1053": "工具软件",
           "1098": "应用开发", "1006": "API服务", "1056": "电子商务", "1057": "金融理财", "1058": "生活服务", "1059": "企业管理",
           "1060": "公共事务", "1061": "气象水利", "1097": "交通地理", "1062": "人工智能"}
cloudName = "腾讯云"


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
        "Referer": "https://market.cloud.tencent.com/categories",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",

    }

    res = requests.post(url, data=dataL, headers=header).text
    pageMap = json.loads(res)
    return pageMap


def insertExcel(sheet, dataL, num):
    page = 1
    while 1:
        productMap = getMap(dataL)
        dataL["page"] = page
        # 每次请求延迟1秒
        # time.sleep(1)
        productSet = productMap["data"]
        products = productSet["productSet"]
        for product in products:
            print(product)
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
            category = allType[str(categoryId)]
            # 定义插入行
            productList = [productName, cloudName, price, category, deliverType, "OS NULL", isvName, url, "TAGS NULL"]
            site = "A" + str(num)
            num += 1
            sheet.write_row(site, productList, bold)
        pageNum = len(products)
        print(category+">>>获取第：" + str(page) + "页数据结束" + "---本页数据" + str(pageNum) + "条")
        page += 1
        # 测试使用
        # if page == 2:
        #     break
        if pageNum < 15:
            break
    return num


# sheet中插入数据
# def insertSheet(classify, sheetName):
def insertSheet():
    sheet = workbook.add_worksheet("腾讯")
    sheet = excelUtil.ExcelUtil.formatSheet(sheet)
    init = ["应用名", "所属云", "价格", "分类", "交付方式", "操作系统", "厂商", "url", "标签"]
    bold_title = workbook.add_format({
        'bold': True,  # 字体加粗
        'border': 1,  # 单元格边框宽度
        'align': 'center',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
        'fg_color': '#67C5F2',  # 单元格背景颜色
        'text_wrap': False,  # 是否自动换行
    })
    num = 2
    for sunClassify in productType:
        # 初始化第一行
        sheet.write_row("A1", init, bold_title)
        for sun in productType[sunClassify]:
            data = {
                "count": 15, "page": 1, "categoryId": int(sun)
            }
            # print("正在爬取:----中----" + sunClassify[sun] + "---分类" + sun)
            num = insertExcel(sheet, data, num)
    print("请求结束,本次总结" + str(num) + "条数据")


# 创建excle文件
filename = "../tencent.xlsx"
workbook = xlsxwriter.Workbook(filename)
bold = workbook.add_format({
    'bold': False,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#67C5F2',  # 单元格背景颜色
    'text_wrap': False,  # 是否自动换行
})


insertSheet()
workbook.close()
print("运行结束")

