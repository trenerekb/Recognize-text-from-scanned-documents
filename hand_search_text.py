import pytesseract
import re
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def cleaning_str(str_date):
    str_del_symbols = re.sub(r'[$!_|?‘\\*]', '', str_date)
    str_del_transfer = re.sub(r'\n', ' ', str_del_symbols)

    return str_del_transfer


def change_month_to_number(date):

    months = {'января': '.01.', 'февраля': '.02.', 'марта': '.03.', 'апреля': '.04.', 'мая': '.05.', 'июня': ".06.",
              'июля': '.07.',
              'августа': '.08.', 'сентября': '.09.', 'октября': '.10.', 'ноября': '.11.', 'декабря': '.12.'}

    try:
        if re.search(r'\d{2}[.]\d{2}[.]\d{4}', date):
            invoice_date = re.search(r'\d{2}[.]\d{2}[.]\d{4}', date).group(0)
            invoice_date = re.sub('\s', '', invoice_date)
        else:
            date = re.sub('[.,]', '', date)
            invoice_date = re.sub(r"[а-я]{3,8}", months[re.search('[а-я]{3,8}', date.lower(), re.I).group(0)], date.lower())
            invoice_date = re.sub('\s', '', invoice_date)
    except:
        invoice_date = date
    try:
        invoice_date = invoice_date if invoice_date[-3] == '0' else invoice_date[:-3] + '0' + invoice_date[-2:]
        invoice_date = 'от ' + invoice_date
    except IndexError:
        invoice_date = invoice_date

    return invoice_date


def get_invoice_text_by_hand(img, number_img):

    list_data = pytesseract.image_to_data(img, lang='rus')

    if 'Счет-фактура' in list_data:
        for word in list_data.split('\n'):
            if 'Счет-фактура' in word.split():
                x_invoice, y_invoice, w_invoice, h_invoice = word.split()[6:10]  # x=730, y=410, w=284, h=44

                if int(y_invoice) - 35 >= 0:
                    #                                отступ от верха:высота, отступ от левого края:ширина
                    invoice_img = img[int(y_invoice)-35:int(y_invoice) + int(h_invoice) + 20, int(x_invoice) - 20: 2550]
                elif int(y_invoice) - 20 >= 0:
                    invoice_img = img[int(y_invoice)-20:int(y_invoice) + int(h_invoice) + 20, int(x_invoice) - 20: 2550]
                else:
                    invoice_img = img[int(y_invoice):int(y_invoice) + int(h_invoice) + 20, int(x_invoice) - 20: 2550]
                # cv2.imwrite(f'invoice_coords_hand{number_img}.jpg', invoice_img)
                break

        text_invoice = pytesseract.image_to_string(invoice_img, lang='rus')
        text_invoice = cleaning_str(text_invoice)
        text_invoice = text_invoice[:text_invoice.find('(')]
        text_invoice = re.sub('г', '', text_invoice)

        if re.search('Исправление', text_invoice):
            text_invoice = text_invoice[:text_invoice.find('Исправление')]

        if re.search(r'[№,.]\s[-/\d+\w+]+', text_invoice):
            invoice_number = re.search(r'[№.,]\s[-/\d+\w+]+', text_invoice).group(0)
            invoice_number = re.sub(r'г', '', invoice_number)
        else:
            invoice_number = re.sub(r'[№.,]', '', text_invoice)
            invoice_number = re.sub(r'\bСчет-фактура', '', invoice_number)
            invoice_number = re.sub(r'г', '', invoice_number)
            if re.search(r'[а-я]{1,2}', invoice_number):
                invoice_number = invoice_number[:invoice_number.find(re.search(r'[а-я]{1,2}', invoice_number).group(0))]
                # print('Номер счет-фактура-IF', invoice_number)

        if re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice):
            invoice_date = re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice).group(0)

        else:
            invoice_date = text_invoice[text_invoice.find('от') + 1:]

        if re.search('\d{2}.\d{2}.\d{4}', invoice_date):
            invoice_date = re.sub('[а-я]+', '', invoice_date, re.I)

        invoice_date = change_month_to_number(invoice_date)

    elif 'Счет-фактура' not in list_data:

        invoice_img = img[60:520, 400: 2600]
        text_invoice = pytesseract.image_to_string(invoice_img, lang='rus')
        text_invoice = cleaning_str(text_invoice)

        cv2.imwrite(f'invoice_hand{number_img}.jpg', invoice_img)

        if re.search('Исправление', text_invoice):
            text_invoice = text_invoice[:text_invoice.find('Исправление')]

        if re.search(r'[№,.]\s[-/\d+\w+]+', text_invoice):
            invoice_number = re.search(r'[№.,]\s[-/\d+\w+]+', text_invoice).group(0)

        else:
            invoice_number = re.sub(r'[№.,]', '', text_invoice)
            invoice_number = re.sub(r'\bСчет-фактура', '', invoice_number)

            if re.search(r'[а-я]{1,2}', invoice_number):
                invoice_number = invoice_number[:invoice_number.find(re.search(r'[а-я]{1,2}', invoice_number).group(0))]

        if re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice):
            invoice_date = re.search(r'\d{1,2}.[а-я]{3,}\s\d{4}', text_invoice).group(0)

        else:
            invoice_date = text_invoice[text_invoice.find('от') + 1:text_invoice.find('г')]

        invoice_date = change_month_to_number(invoice_date)

    else:
        invoice_number = '-'
        invoice_date = '-'

    return invoice_number, invoice_date


def get_buyer_text_by_hand(img, number_img):

    text_buyer_all = pytesseract.image_to_string(img, lang='rus')
    text_buyer_all = re.sub('\n', ' ', text_buyer_all)

    if re.search('Покупатель:', text_buyer_all):
        list_data = pytesseract.image_to_data(img, lang='rus')
        for word in list_data.split('\n'):
            if 'Покупатель:' in word.split():
                x_buyer, y_buyer, w_buyer, h_buyer = word.split()[6:10]  # x=3410, y=565, w=284, h=44
                #                                отступ от верха: высота, отступ от левого края:ширина
                buyer_img = img[int(y_buyer) - 50: int(y_buyer) + int(h_buyer) + 10, int(x_buyer) - 20: 5600]
                # cv2.imwrite(f'buyer_hand{number_img}.jpg', buyer_img)
                #                                отступ от верха: высота, отступ от левого края:ширина
                buyer_address_img = img[int(y_buyer) + 30:int(y_buyer) + int(h_buyer) + 150,
                                    int(x_buyer) - 20: 5600]
                # cv2.imwrite('buyer_address_hand.jpg', buyer_address_img)
                break

        text_buyer = pytesseract.image_to_string(buyer_img, lang='rus')
        text_buyer = cleaning_str(text_buyer)

        text_buyer_address = pytesseract.image_to_string(buyer_address_img, lang='rus')
        text_buyer_address = cleaning_str(text_buyer_address)
        text_buyer_address = re.sub('Адрес', '', text_buyer_address)

        try:
            if re.search(r':.+[\'»”`(]', text_buyer):
                buyer_name = re.search(r':.+[\'»”`(]', text_buyer).group(0)
                buyer_name = buyer_name[buyer_name.find(':') + 1:buyer_name.find('(') + 1]
                buyer_name = re.sub(r'Продавец', '', buyer_name)
                buyer_name = re.sub(r'Покупатель', '', buyer_name)
                buyer_name = re.sub(r'[(;©%]', '', buyer_name)
                if re.search(r'Общество', text_buyer):
                    buyer_name = buyer_name[buyer_name.find('Общество'):]

            else:
                buyer_name = re.sub(r'[:\'`(%©]', '', text_buyer)
                buyer_name = re.sub(r'Продавец', '', buyer_name)
                buyer_name = buyer_name.rstrip()
                if re.search(r'ООО', text_buyer):
                    buyer_name = buyer_name[buyer_name.find('ООО'):]
        except:
            buyer_name = '-'

        try:
            if re.search('\s\d{6}[.,\s]', text_buyer_address):
                buyer_index = re.search('\s\d{6}[.,\s]', text_buyer_address).group(0)
                buyer_index = buyer_index.strip()
                buyer_index = re.sub('[.,]', '', buyer_index)
            else:
                buyer_index = '-'
        except:
            buyer_index = '-'

        try:
            if re.search(r'[,.:].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_buyer_address, re.I):
                buyer_address = re.search(r'[:,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_buyer_address,
                                             re.I).group(0).replace(',', '', 1)
                buyer_address = buyer_address[:buyer_address.find('(')]
                buyer_address = re.sub(r'\d{4,}', '', buyer_address)
                buyer_address = re.sub(r'\s+', ' ', buyer_address)

                if re.search(r'\bАдрес.', buyer_address):
                    buyer_address = re.sub(r'.+\bАдрес.', '', buyer_address)
                if buyer_address.count(':') >= 0:
                    buyer_address = buyer_address[buyer_address.find(':') + 1:]
                    buyer_address = re.sub(':', '', buyer_address)
                if re.search('ИНН', buyer_address):
                    buyer_address = buyer_address[:buyer_address.find('ИНН')]
            else:
                buyer_address = text_buyer_address[text_buyer_address.find(
                    re.search(r'\d{6}', text_buyer_address).group(0)) + 1: text_buyer_address.find('ИНН')]
        except:
            buyer_address = '-'

    elif not re.search('Покупатель:', text_buyer_all):
        img = img[100:900, 200:5600]
        cv2.imwrite(f'buyer_hand_elif{number_img}.jpg', img)
        text_buyer = pytesseract.image_to_string(img, lang='rus')
        text_buyer = cleaning_str(text_buyer)

        if re.search('ООО|Общество', text_buyer):
            buyer_name = re.findall('ООО\D+|Общество\D+', text_buyer, re.I)
            for i in range(len(buyer_name)):
                try:
                    if re.search('альянс', buyer_name[i], re.I):
                        buyer_name.pop(i)
                except IndexError:
                    pass
            buyer_name = buyer_name[0]
        else:
            buyer_name = '-'

        if re.search('\s\d{6}[.,\s]', text_buyer):
            buyer_index = re.findall('\s\d{6}[.,\s]', text_buyer)

            for i in range(len(buyer_index)):
                try:
                    if re.search('620131', buyer_index[i]):
                        buyer_index.pop(i)
                except IndexError:
                    pass
            buyer_index = buyer_index[0].strip()
            buyer_index = re.sub('[.,]', '', buyer_index)

        else:
            buyer_index = '-'

        if re.search('\s\d{6}[.,\s].+[\[(]', text_buyer):
            buyer_address = re.findall('\s\d{6}[.,\s].+[\[(]', text_buyer)
            buyer_address = buyer_address[0]
            buyer_address = re.sub('\d{6}[.,\s]', '', buyer_address)
            buyer_address = buyer_address[:buyer_address.find('(')]
            buyer_address = buyer_address[:buyer_address.find('[')]
            if re.search('ИНН', buyer_address):
                buyer_address = buyer_address[:buyer_address.find('ИНН')]
        else:
            buyer_address = '-'

    return buyer_name, buyer_index, buyer_address


def get_salesman_text_by_hand(img, number_img):

    text_salesman_all = pytesseract.image_to_string(img, lang='rus')
    text_salesman_all = re.sub('\n', ' ', text_salesman_all)

    if re.search('Продавец:', text_salesman_all):

        list_data = pytesseract.image_to_data(img, lang='rus')

        for word in list_data.split('\n'):
            if 'Продавец:' in word.split():
                x_salesman, y_salesman, w_salesman, h_salesman = word.split()[6:10]  # x=3410, y=565, w=284, h=44
                #                                отступ от верха: высота, отступ от левого края:ширина
                salesman_img = img[int(y_salesman) - 40:int(y_salesman) + int(h_salesman) + 30,
                               int(x_salesman) - 20: 2850]
                # cv2.imwrite(f'salesman_hand{number_img}.jpg', salesman_img)
                #                                отступ от верха: высота, отступ от левого края:ширина
                salesman_address_img = img[int(y_salesman) + 20:int(y_salesman) + int(h_salesman) + 140,
                                       int(x_salesman) - 20: 3050]
                # cv2.imwrite(f'salesman_address_hand{number_img}.jpg', salesman_address_img)
                break

        text_salesman = pytesseract.image_to_string(salesman_img, lang='rus')
        text_salesman = cleaning_str(text_salesman)

        text_salesman_address = pytesseract.image_to_string(salesman_address_img, lang='rus')
        text_salesman_address = cleaning_str(text_salesman_address)
        text_salesman_address = re.sub('Адрес', '', text_salesman_address)

        try:
            if re.search(r':.+[\'»”`(]', text_salesman):
                salesman_name = re.search(r':.+[\'»”`(]', text_salesman).group(0)
                salesman_name = salesman_name[salesman_name.find(':') + 1:salesman_name.find('(') + 1]
                salesman_name = re.sub(r'Продавец', '', salesman_name)
                salesman_name = re.sub(r'Покупатель', '', salesman_name)
                salesman_name = re.sub(r'[(;:]', '', salesman_name)

            else:
                salesman_name = re.sub(r'[:\'`(]', '', text_salesman)
                salesman_name = re.sub(r'Продавец', '', salesman_name)
                salesman_name = salesman_name.rstrip()
            if re.search(r'ООО', salesman_name):
                salesman_name = salesman_name[salesman_name.find('ООО'):]
            if re.search(r'Общество', salesman_name):
                salesman_name = salesman_name[salesman_name.find('Общество'):]
        except:
            salesman_name = '-'

        try:
            if re.search('\s\d{6}[.,\s]', text_salesman_address):
                salesman_index = re.search('\s\d{6}[.,\s]', text_salesman_address).group(0)
                salesman_index = salesman_index.strip()
                salesman_index = re.sub('[.,]', '', salesman_index)
            else:
                salesman_index = '-'
        except:
            salesman_index = '-'

        try:
            if re.search(r'[,.:].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_salesman_address, re.I):
                salesman_address = re.search(r'[:,.].[А-Я].+\d{1,3}.([\{\(]|[\s+\bИНН])', text_salesman_address,
                                             re.I).group(0).replace(',', '', 1)
                if re.search(r'\d{6}[,.\s].+', salesman_address):
                    salesman_address = salesman_address[salesman_address.find(re.search(r'\d{6}', salesman_address).group(0)) + 1: ]
                salesman_address = salesman_address[:salesman_address.find('(')]
                salesman_address = re.sub(r'\d{4,}', '', salesman_address)
                salesman_address = re.sub(r'\s+', ' ', salesman_address)

                if re.search(r'\bАдрес.', salesman_address):
                    salesman_address = re.sub(r'.+\bАдрес.', '', salesman_address)

                if salesman_address.count(':') >= 0:
                    salesman_address = salesman_address[salesman_address.find(':')+1:]
                    salesman_address = re.sub(':', '', salesman_address)
            else:
                salesman_address = text_salesman_address[text_salesman_address.find(
                    re.search(r'\d{6}', text_salesman_address).group(0)) + 1: text_salesman_address.find('ИНН')]
        except:
            salesman_address = '-'

    elif not re.search('Продавец:', text_salesman_all):
        img = img[50:800, 150:5600]
        cv2.imwrite(f'salesman_hand_elif{number_img}.jpg', img)
        text_salesman = pytesseract.image_to_string(img, lang='rus')
        text_salesman = cleaning_str(text_salesman)

        if re.search('ООО|Общество', text_salesman):
            salesman_name = re.findall('ООО\D+|Общество\D+', text_salesman, re.I)

            for i in range(len(salesman_name)):
                try:
                    if re.search('альянс', salesman_name[i], re.I):
                        salesman_name.pop(i)
                except IndexError:
                    pass
            salesman_name = salesman_name[0]
        else:
            salesman_name = '-'

        if re.search('\s\d{6}[.,\s]', text_salesman):
            salesman_index = re.findall('\s\d{6}[.,\s]', text_salesman)

            for i in range(len(salesman_index)):
                try:
                    if re.search('620131', salesman_index[i]):
                        salesman_index.pop(i)
                except IndexError:
                    pass
            salesman_index = salesman_index[0].strip()
            salesman_index = re.sub('[.,]', '', salesman_index)

        else:
            salesman_index = '-'

        if re.search('\s\d{6}[.,\s].+[\[(]', text_salesman):
            salesman_address = re.findall('\s\d{6}[.,\s].+[\[(]', text_salesman)
            salesman_address = salesman_address[0]
            salesman_address = re.sub('\d{6}[.,\s]', '', salesman_address)

            if re.search('инн', salesman_address, re.I):
                salesman_address = salesman_address[:salesman_address.lower().find('инн')]

            salesman_address = salesman_address[:salesman_address.find('(')]
            salesman_address = salesman_address[:salesman_address.find('[')]
        else:
            salesman_address = '-'

    return salesman_name, salesman_index, salesman_address