class ExcelUtil:

    def formatSheet(sheet):
        sheet.set_column('A:A', 50)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 10)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 36)
        sheet.set_column('G:G', 30)
        sheet.set_column('H:H', 100)
        sheet.set_column('I:I', 100)
        return sheet
