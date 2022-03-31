import excelUtil
import json
import xlsxwriter
import requests
from urllib import parse


def requestUrl():
    header = {
        "Host": "appcenter.qingcloud.com",
        "Content-Length": "490",
        "Cookie": "csrftoken=K5lhEPWtB5Y3UaLsFslJGztqgkgIpn5i; gr_user_id=7688e695-042f-4a50-bef2-afef22441931; _ga=GA1"
                  ".2.966909176.1648433857; sid=dsq0a5iqzx3nji8qwpfw0aw72svwa3fg; bad_id0deb3fb0-5803-11ec-8cb1-39ae2a5"
                  "1e49d=5c791541-ae3d-11ec-a365-5b7375bec0a5; ab7e0583a75979c5_gr_last_sent_cs1=usr-d5G3EMW0; bad_id2f"
                  "6d1c60-92f7-11ec-bcef-27fecfd15522=69851451-ae3d-11ec-a365-5b7375bec0a5; _gid=GA1.2.663374608.164863"
                  "1694; _gcl_au=1.1.1778624267.1648633028; sk=gc9vaC6G6rVrc8hBljsPKYqt2SIXjJuL; lang=zh-cn; gr_session"
                  "_id_ab7e0583a75979c5=5434d28f-c11b-44a5-a3f2-6c8d516ddbcd; Hm_lvt_17a3a88cbe9f9c8808943e8ed1c7155a="
                  "1648433857,1648631694,1648713673; gr_session_id_ab7e0583a75979c5_5434d28f-c11b-44a5-a3f2-6c8d516ddb"
                  "cd=true; ab7e0583a75979c5_gr_session_id=d5803447-816a-41ae-8cdd-88008f1b09f2; ab7e0583a75979c5_gr_l"
                  "ast_sent_sid_with_cs1=d5803447-816a-41ae-8cdd-88008f1b09f2; ab7e0583a75979c5_gr_cs1=usr-d5G3EMW0; a"
                  "b7e0583a75979c5_gr_session_id_d5803447-816a-41ae-8cdd-88008f1b09f2=true; Hm_lpvt_17a3a88cbe9f9c8808"
                  "943e8ed1c7155a=1648713716; nice_id0deb3fb0-5803-11ec-8cb1-39ae2a51e49d=d7866661-b0c8-11ec-a37a-dbe5"
                  "8413aaa8",
        "Sec-Ch-Ua": "\"Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.46"
                      "64.45 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*",
        "X-Requested-With": "XMLHttpRequest",
        "X-Csrftoken": "5wdC5xSNfFcw1ovNvo70Ac0f1zDAqsx6",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Origin": "https://appcenter.qingcloud.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://appcenter.qingcloud.com/search/category/bigdata",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }
    data = {
        "method": "GET",
        "params": {"limit": 20, "category": "shield", "sort_key": "status_time", "reverse": 1, "offset": 40,
                   "action": "DescribeApps", "app_type": ["cluster", "web", "saas", "image", "license"],
                   "status": ["active"],
                   "exclude_apps": ["app-cqkewf6m", "app-3nfkjxro", "app-tvzuxbp0", "app-ckd27cjj", "app-njfztji5",
                                    "app-01rrm0as", "app-o6lvbkhm"]}
    }
    url = "https://appcenter.qingcloud.com/api"
    res = requests.post(url, headers=header, data=data)
    print(res.text)
    return json.loads(res.text)


print(requestUrl())
