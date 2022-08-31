import re
import cv2
import pytesseract
from processing_img import processing_scan_img, filter_img_hand
from align import flip90
from hand_search_text import get_invoice_text_by_hand, get_buyer_text_by_hand, cleaning_str, change_month_to_number, get_salesman_text_by_hand


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def get_invoice_text(img, word, number_img):
    x_invoice, y_invoice, w_invoice, h_invoice = word.split()[6:10]  # x=730, y=410, w=284, h=44
    #                                отступ от верха:высота, отступ от левого края:ширина
    invoice_img = img[int(y_invoice) - 70:int(y_invoice) + int(h_invoice) + 20, int(x_invoice) - 20: 2300]
    # cv2.imwrite(f'invoice{number_img}.jpg', invoice_img)
    text_invoice = pytesseract.image_to_string(invoice_img, lang='rus')
    text_invoice = cleaning_str(text_invoice)

    try:
        if re.search(r'[№,.]\s[-/\d+\w+]+', text_invoice):
            invoice_number = re.search(r'[№.,]\s[-/\d+\w+]+', text_invoice).group(0).strip()

        else:
            invoice_number = re.sub(r'[№.,]', '', text_invoice)
            invoice_number = re.sub(r'\bСчет-фактура', '', invoice_number)
            invoice_number = invoice_number.strip()

            if re.search(r'[а-я]{1,2}', invoice_number):
                invoice_number = invoice_number[:invoice_number.find(re.search(r'[а-я]{1,2}', invoice_number).group(0))]
    except:
        invoice_number = '-'

    try:
        if re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice):
            invoice_date = re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice).group(0)
            invoice_date = invoice_date.rstrip()

        else:
            invoice_date = text_invoice[text_invoice.find('от') + 1:text_invoice.find('г')]
            invoice_date = invoice_date.rstrip()

        invoice_date = change_month_to_number(invoice_date)
    except:
        invoice_date = '-'

    return invoice_number, invoice_date


def get_buyer_text(img, word, number_img):

    x_buyer, y_buyer, w_buyer, h_buyer = word.split()[6:10]  # x=3410, y=565, w=284, h=44
    #                                отступ от верха: высота, отступ от левого края:ширина
    buyer_img = img[int(y_buyer) - 50:int(y_buyer) + int(h_buyer) + 10, int(x_buyer) - 20: 5600]
    # cv2.imwrite(f'buyer{number_img}.jpg', buyer_img)

    #                                отступ от верха: высота, отступ от левого края:ширина
    buyer_address_img = img[int(y_buyer) + 30:int(y_buyer) + int(h_buyer) + 200, int(x_buyer) - 20: 5600]
    # cv2.imwrite(f'buyer_address{number_img}.jpg', buyer_address_img)

    text_buyer = pytesseract.image_to_string(buyer_img, lang='rus')
    text_buyer = cleaning_str(text_buyer)

    text_buyer_address = pytesseract.image_to_string(buyer_address_img, lang='rus')
    text_buyer_address = cleaning_str(text_buyer_address)

    try:
        if re.search(r':\D+["\'”»\(]', text_buyer):
            buyer_name = re.sub(r'[6)(5:\]\[]', '', text_buyer)
            buyer_name = re.sub(r'\bПокупатель', '', buyer_name).lstrip()

        else:
            buyer_name = re.sub(r'[6)(5:\]\[]', '', text_buyer)
            buyer_name = re.sub(r'\bПокупатель', '', buyer_name).lstrip()

        if re.search(r'ООО', buyer_name):
            buyer_name = buyer_name[buyer_name.find('ООО'):]
        if re.search(r'Общество', buyer_name):
            buyer_name = buyer_name[buyer_name.find('Общество'):]

    except:
        buyer_name = '-'

    try:
        buyer_index = re.search(r'\d{6}', text_buyer_address).group(0)
    except:
        buyer_index = '-'

    try:
        if re.search(r'[,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_buyer_address):
            buyer_address = re.search(r'[,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_buyer_address).group(0).replace(',', '', 1)
            buyer_address = buyer_address[:buyer_address.find('(')]
            if re.search(r'инн', buyer_address, re.I):
                buyer_address = buyer_address[:buyer_address.lower().find('инн')]
            buyer_address = re.sub(r'\d{6,}', '', buyer_address)
            buyer_address = re.sub(r'Адрес:', '', buyer_address)

        else:
            buyer_address = re.sub(r'\d{6,}', '', text_buyer_address)
            buyer_address = buyer_address[buyer_address.find(','):]
            if re.search(r'инн', buyer_address, re.I):
                buyer_address = buyer_address[:buyer_address.lower().find('инн')]
            buyer_address = re.sub(r'Адрес:', '', buyer_address)
            # print('Покупатель ADDRESS ELSE:', buyer_address)
    except:
        buyer_address = '-'

    return buyer_name, buyer_index, buyer_address


def get_salesman_text(img, word, number_img):

    x_salesman, y_salesman, w_salesman, h_salesman = word.split()[6:10]  # x=3410, y=565, w=284, h=44
    #                                отступ от верха: высота, отступ от левого края:ширина
    salesman_img = img[int(y_salesman) - 70:int(y_salesman) + int(h_salesman) + 15, int(x_salesman) - 20: 2900]
    # cv2.imwrite(f'salesman{number_img}.jpg', salesman_img)
    #                                отступ от верха: высота, отступ от левого края:ширина
    salesman_address_img = img[int(y_salesman) + 35:int(y_salesman) + int(h_salesman) + 170,
                           int(x_salesman) - 20: 3200]
    # cv2.imwrite(f'salesman_address{number_img}.jpg', salesman_address_img)

    text_salesman = pytesseract.image_to_string(salesman_img, lang='rus')
    text_salesman = cleaning_str(text_salesman)

    text_salesman_address = pytesseract.image_to_string(salesman_address_img, lang='rus')
    text_salesman_address = cleaning_str(text_salesman_address)

    try:
        if re.search(r':.+[\'»”`(]', text_salesman):
            salesman_name = text_salesman[text_salesman.find(':')+1:]
            salesman_name = re.sub('Продавец', '', salesman_name)
            if re.search(r'[(]2[)]', salesman_name):
                salesman_name = salesman_name[:salesman_name.find('(2)')]
            if re.search(r'[(]2б[)]', salesman_name):
                salesman_name = salesman_name[:salesman_name.find('(2б)')]
            if re.search(r'[(]26[)]', salesman_name):
                salesman_name = salesman_name[:salesman_name.find('(26)')]
            if re.search(r'ООО', salesman_name):
                salesman_name = salesman_name[salesman_name.find('ООО'):]
                # print('НАШЕЛ ПО "ООО"', salesman_name)
            if re.search(r'Общество', salesman_name):
                salesman_name = salesman_name[salesman_name.find('Общество'):]

        elif not re.search(r':.+[\'»”`(]', text_salesman):

            if re.search(r'ООО|Общество', text_salesman):
                if re.search(r'ООО', text_salesman):
                    salesman_name = text_salesman[text_salesman.find('ООО'):]
                if re.search(r'Общество', text_salesman):
                    salesman_name = text_salesman[text_salesman.find('Общество'):]
                salesman_name = re.sub(r'[\]\[)(%]', '', salesman_name)
            else:
                salesman_name = re.sub(r'[:\'`(\[]', '',  text_salesman)
                salesman_name = re.sub(r'\bПродавец', '', salesman_name)
                salesman_name = salesman_name.rstrip()
                if re.search(r'000', salesman_name):
                    salesman_name = salesman_name[salesman_name.find('000'):]
                if re.search(r'ООО', salesman_name):
                    salesman_name = salesman_name[salesman_name.find('ООО'):]
                if re.search(r'Общество', salesman_name):
                    salesman_name = salesman_name[salesman_name.find('Общество'):]

            if re.search(r'\bПродавец', salesman_name):
                salesman_name = re.sub(r'\bПродавец', '', salesman_name)

    except:
        salesman_name = '-'
    try:
        salesman_index = re.search(r'\d{6}', text_salesman_address).group(0)
    except:
        salesman_index = '-'

    try:
        if re.search(r'[:,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_salesman_address, re.I):
            salesman_address = re.search(r'[:,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_salesman_address, re.I).group(0).replace(',', '', 1)

            if re.search(r'\d{6}[,.]', salesman_address):
                salesman_address = salesman_address[salesman_address.find(re.search(r'\d{6}[,.]', salesman_address).group(0)):]

            salesman_address = re.sub(r'\d{4,}', '', salesman_address)
            salesman_address = re.sub(r'Адрес', '', salesman_address)
            if re.search('инн', salesman_address, re.I):
                salesman_address = salesman_address[: salesman_address.lower().find('инн')]
            if re.search('[(]2а[)]', salesman_address):
                salesman_address = salesman_address[:salesman_address.find('(2а)')]
            if re.search('[(]26[)]', salesman_address):
                salesman_address = salesman_address[:salesman_address.find('(26)')]
            if re.search('[(]2б[)]', salesman_address):
                salesman_address = salesman_address[:salesman_address.find('(2б)')]
            salesman_address = re.sub(r'[\[(]', '', salesman_address)

        else:
            salesman_address = text_salesman_address[text_salesman_address.find(
                re.search(r'\d{6}', text_salesman_address).group(0))+1: text_salesman_address.find('ИНН')]

    except:
        salesman_address = '-'

    return salesman_name, salesman_index, salesman_address


def get_text(count_pages):

    all_text_from_img = {f'page{x + 1}': [] for x in range(count_pages)}
    all_img_pdf = processing_scan_img(count_pages)

    for i, img in enumerate(all_img_pdf, start=1):
        invoice_flag = False
        buyer_flag = False
        salesman_flag = False

        text_all = pytesseract.image_to_string(img, lang='rus')
        colum_dict = {'invoice': '', 'buyer_name': '', 'buyer_address': '', 'salesman_name': '', 'salesman_address': ''}

        if not re.search(r'Стр\.2|Стр2|Лист', text_all):

            list_data = pytesseract.image_to_data(img, lang='rus')

            for word in list_data.split('\n'):
                if 'Счет-фактура' in word.split() or 'Счет' in word.split():
                    invoice_flag = True
                    invoice_number, invoice_date = get_invoice_text(img, word, i)
                    colum_dict['invoice'] = f'{invoice_number} {invoice_date}'

                elif 'Покупатель:' in word.split():
                    buyer_flag = True
                    buyer_name, buyer_index, buyer_address = get_buyer_text(img, word, i)
                    colum_dict['buyer_name'] = buyer_name
                    colum_dict['buyer_address'] = f'{buyer_index}, {buyer_address}'

                elif 'Продавец:' in word.split():
                    salesman_flag = True
                    salesman_name, salesman_index, salesman_address = get_salesman_text(img, word, i)
                    colum_dict['salesman_name'] = salesman_name
                    colum_dict['salesman_address'] = f'{salesman_index}, {salesman_address}'

            if not all([invoice_flag, buyer_flag, salesman_flag]):

                img = cv2.imread(f'page{i}.jpg')
                img = flip90(img)
                img = filter_img_hand(img)

                text = pytesseract.image_to_string(img, lang='rus')

                if not re.search(r'(Стр\.2)|(Стр2)', text):

                    if not invoice_flag:
                        invoice_img = img.copy()[50: 800, 90: 2600]
                        # cv2.imwrite(f'crop_invoce{i}.jpg', invoice_img)
                        invoice_number, invoice_date = get_invoice_text_by_hand(invoice_img, i)
                        colum_dict['invoice'] = f'{invoice_number} {invoice_date}'

                    if not buyer_flag:
                        buyer_img = img.copy()[50:1070, 400:5600] #[50: 800, 90: 5600]
                        # cv2.imwrite(f'crop_buyer{i}.jpg', buyer_img)
                        buyer_name, buyer_index, buyer_address = get_buyer_text_by_hand(buyer_img, i)
                        colum_dict['buyer_name'] = buyer_name
                        colum_dict['buyer_address'] = f'{buyer_index}, {buyer_address}'

                    if not salesman_flag:
                        salesman_img = img.copy()[50:1070, 300:5600] #[50: 800, 90: 5600]
                        # cv2.imwrite(f'crop_salesman{i}.jpg', salesman_img)
                        salesman_name, salesman_index, salesman_address = get_salesman_text_by_hand(salesman_img, i)
                        colum_dict['salesman_name'] = salesman_name
                        colum_dict['salesman_address'] = f'{salesman_index}, {salesman_address}'
                else:
                    continue
        else:
            continue
        all_text_from_img[f'page{i}'] = colum_dict.copy()

    return all_text_from_img
