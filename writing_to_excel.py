import openpyxl
import datetime
import re


def data_recording_excel(text_dict, count_pages):
    current_date = '.'.join(str(datetime.date.today()).split('-')[::-1])
    book = openpyxl.Workbook()
    sheet = book.active

    sheet['A1'] = 'Дата' #current_date
    sheet['B1'] = 'Организация'
    sheet['C1'] = 'Адрес'
    sheet['D1'] = '№ и Дата УПД'

    row = 2

    for i in range(1, count_pages+1):
        try:
            if not re.search(r'\bальянс|\bбвб|\bаль', text_dict[f'page{i}']['salesman_name'], re.I) and text_dict[f'page{i}']['salesman_name'] != '-':
                sheet[row][0].value = current_date
                sheet[row][1].value = text_dict[f'page{i}']['salesman_name']
                sheet[row][2].value = text_dict[f'page{i}']['salesman_address']
                sheet[row][3].value = f"УПД, {text_dict[f'page{i}']['invoice']}"
            else:
                sheet[row][0].value = current_date
                sheet[row][1].value = text_dict[f'page{i}']['buyer_name']
                sheet[row][2].value = text_dict[f'page{i}']['buyer_address']
                sheet[row][3].value = f"УПД, {text_dict[f'page{i}']['invoice']}"
            row += 1
        except TypeError:
            continue

    book.save(f'doc {current_date}.xlsx')
    book.close()
    name_doc = f'doc {current_date}'

    return name_doc