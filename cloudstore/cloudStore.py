import xlsxwriter
import tencent
import excelUtil
import baidu
import alibaba
import huawei

filename = "../cloudStore.xlsx"
workbook = xlsxwriter.Workbook(filename)
sheet = workbook.add_worksheet("云市场")
sheet = excelUtil.ExcelUtil.formatSheet(sheet)
init = ["应用名", "所属云", "价格", "分类", "交付方式", "操作系统", "厂商", "url", "标签"]
num = 2
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
sheet.write_row("A1", init, bold_title)
num = tencent.add(sheet, num, bold)
num = baidu.add(sheet, num, bold)
num = huawei.add(sheet, num, bold)
workbook.close()
