import requests
import json
import xlsxwriter
import excelUtil

allType = ["1:104:<基础软件>管理与监控", "3:307:<企业应用>协同办公", "3:309:<企业应用>财务管理", "3:304:<企业应用>人力资源", "7:701:<安全>主机安全",
           "7:703:<安全>数据安全", "7:704:<安全>网络安全", "7:702:<安全>应用安全", "7:706:<安全>安全服务", "7:705:<安全>安全管理"]
cloudName = "华为云"
n = 0


def requestUrl(page, typeCode, form):
    header = {
        "Host": "portal.huaweicloud.com",
        "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "Accept": "application/json, text/plain, */*",
        "X-Language": "zh-cn",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Origin": "https://marketplace.huaweicloud.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://marketplace.huaweicloud.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    url = "https://portal.huaweicloud.com/portalsearchqueryservice/marketplacesearch?pageNo=" + str(
        page) + "&pageSize=10&typeCode=" + str(typeCode) + "&form=" + str(
        form) + "&contentMode=-1&priceRange=-1&supportOS=-1&productType=-1&tagIds=&priceStart" \
                "=-1&priceEnd=-1 "
    res = requests.get(url).text
    return json.loads(res)["pagination"]["items"]


def insert(sheet,num,bold):
    for types in allType:
        page = 1
        cList = types.split(":")
        typeCode = cList[0]
        form = cList[1]
        typeName = cList[2]
        while 1:
            products = requestUrl(page, typeCode, form)
            for product in products:
                title = product["title"]
                originalPrice = product["originalPrice"]
                supportos = product["supportos"]
                corporationname = product["corporationname"]
                tagnames = ""
                if "tagnames" in product:
                    tagnames = product["tagnames"]
                url = product["url"]
                data = [title, cloudName, originalPrice, typeName, "", supportos, corporationname, url, tagnames]
                site = "A" + str(num)
                sheet.write_row(site, data, bold)
                num += 1
            pageNum = len(products)
            print(typeName + ">>>" + "获取第：" + str(page) + "页数据结束" + "---本页数据" + str(pageNum) + "条")
            page += 1
            if pageNum < 10:
                break
    print("华为云请求结束,本次总结" + str(num) + "条数据")
    return num


def add(sheet, num, bold):
    n = num - 1
    num = insert(sheet, num, bold)
    print("运行结束")
    return num

# res = requestUrl(1, 1, 104)
# for maps in res:
#     for m in maps:
#         print(m)
#         print(maps[m])
#     break
