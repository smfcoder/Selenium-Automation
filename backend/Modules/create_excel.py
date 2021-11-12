import xlsxwriter

def create_excel_sheet(filename,data):
    # Create a workbook and add a worksheet.
    name_of_file = filename
    workbook = xlsxwriter.Workbook('./Reports/'+name_of_file+".xlsx")
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True,'border': 1,'align':'center'})
    align = workbook.add_format({'border': 1,'align':'center'})


    # Write some data headers.
    worksheet.write('A1', 'Sr.No', bold)
    worksheet.write('A2', '1', align)

    worksheet.set_column('B:G', 25)
    worksheet.write('B1', 'Application_url', bold)
    worksheet.write('B2', data['Application_url'], align)
    
    worksheet.write('C1', 'Validated_page', bold)
    worksheet.write('C2', data['Validated_page'], align)

    worksheet.write('D1', 'Status', bold)
    worksheet.write('D2', data['Status'], align)

    worksheet.write('E1', 'Comment', bold)
    worksheet.write('E2', data['Comment'], align)

    worksheet.write('F1', 'Validation_time(Seconds)', bold)
    worksheet.write('F2', data['Validation_time'], align)

    worksheet.write('G1', 'Validated_at', bold)
    worksheet.write('G2', data['Validated_at'], align)




    workbook.close()

