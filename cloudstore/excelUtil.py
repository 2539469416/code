import xlsxwriter as xlsx

def excelWrite(data,filename):
    workbook = xlsx.workbook(filename)
    sheet = workbook.add_worksheet('全部产品')
