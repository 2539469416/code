import xlsxwriter
import json
import requests
import excelUtil

allType = {
    '云安全市场': ['56832023:主机安全', '56846020:应用安全', '56824015:数据安全', '56830014:安全管理', '56820014:网络安全'],
    '企业应用': ['56778013:办公管理', '56764034:财务管理', '56780006:人事管理', '56842010:销售管理'],
}
cloudName = "阿里云"

# 创建excle文件
filename = "../alibaba.xlsx"
workbook = xlsxwriter.Workbook(filename)
# 定义头格式，文本格式
bold_title = workbook.add_format({
    'bold': True,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#67C5F2',  # 单元格背景颜色
    'text_wrap': False,  # 是否自动换行
})
bold = workbook.add_format({
    'bold': False,  # 字体加粗
    'border': 1,  # 单元格边框宽度
    'align': 'center',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'fg_color': '#67C5F2',  # 单元格背景颜色
    'text_wrap': False,  # 是否自动换行
})


# 请求方法 1. 页码 2. 分类
def requestUrl(pageIndex, categoryId):
    header = {
        "Host": "market.aliyun.com",
        "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.aliyun.com/products/53366009?spm=5176.730005.filter.53366009",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    url = "https://market.aliyun.com/api/ajax/product/queryProducts.json?categoryId=" + str(
        categoryId) + "&pageIndex=" + str(pageIndex) + "&pageSize=12"
    res = requests.get(url).text
    return json.loads(res)["result"]["products"]


def insertExcel(sheet, cid, num):
    page = 1
    categoryId = cid.split(":")[0]
    categoryName = cid.split(":")[1]
    while 1:
        products = requestUrl(page, categoryId)
        for product in products:
            name = product["name"]
            price = product["price"]
            types = categoryName
            delivery_method = product["delivery_method"]
            shop_name = product["shop_name"]
            url = "https://market.aliyun.com" + product["url"]
            tagList = product["tagList"]
            tags = str(product["tags"])
            # 定义插入行
            productList = [name,cloudName, price, types, delivery_method, "NULL",shop_name, url, str(tagList)]
            site = "A" + str(num)
            if clearData(tagList, name):
                sheet.write_row(site, productList, bold)
                num += 1
        pageNum = len(products)
        print(categoryName + ">>>" + "获取第页：" + str(page) + "数据结束" + "---本页数据" + str(pageNum) + "条")
        page += 1
        if pageNum < 12:
            break
    return num


def insertSheet():
    sheet = workbook.add_worksheet("阿里")
    num = 2
    # 初始化第一行
    init = ["应用名","所属云","价格","分类","交付方式","操作系统","厂商","url","标签"]
    sheet.write_row("A1", init, bold)
    excelUtil.ExcelUtil.formatSheet(sheet)
    for types in allType:
        for cid in allType[types]:
            num = insertExcel(sheet, cid, num)
    print("请求结束,本次总结"+str(num)+"条数据")


# 数据过滤
def clearData(lists, title):
    if ("办公协同" in lists) or ("销售管理" in lists) or ("OA" in lists) or ("人事管理" in lists) or ("财务管理" in lists) or ("CRM" in lists):
        return True
    if ("代办" in title) or ("营业执照" in title) or ("运行环境" in title) or ("商标注册" in title) or ("定制开发" in title) or ():
        print("title过滤>>>" + title)
        return False
    if ("系统" in title) or ("泛微" in title) or ("OKR" in title)  or ("平台" in title) or (
            "蓝凌" in title) or ("致远" in title) or ("通达" in title) or ("华天动力" in title):
        return True
    if len(lists) == 0:
        print("空标签过滤")
        return False
    if ("安全咨询" in lists) or ("云通信" in lists) or ("邮箱" in lists) or ("企业服务" in lists):
        print("标签过滤>>>" + title)
        return False
    return True


# 按照各大分类去遍历子分类
insertSheet()

# 数据测试
# response = requestUrl(1,53448001)
# for maps in response:
#     for m in maps:
#         print(m+">>>"+str(maps[m]))
#     break
workbook.close()

