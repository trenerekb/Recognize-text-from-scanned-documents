**РАСПОЗНАВАНИЕ ТЕКСТА С ПОСЛЕДУЮЩЕЙ ЗАПИСЬЮ ДАННЫХ В EXCEL**

`ЗАДАЧА:`
Помощнику бухгалтера ежедневно требуется заполнять excel таблицу данными из физических листов со счетами-фактуры. Требуется автоматизировать и ускорить процесс.

`ПРОБЛЕМЫ:`
Из документов нужно было прочитать номер счета-фактуры, дату, имена продавцов и их адреса. 
Физические листы плохого качества - потеря или искажение букв, шумы, при отсканировании листа сотрудницей получался перекос. 
Это все сказывается на результате распознования текста не в лучшую сторону.

`РЕШЕНИЕ:`
1. Так как организация закрытая и на компьютер сотрудницы ничего нельзя установить мной было принято решение сделать телеграм бот, который принимает pdf файл с отсканированными документами, передает их на мой сервер и отдает уже готовый excel документ с заполненными ячейками.
2. Для распознования текста требуется png или jpg формат. Так же нужно было развернуть на -90 градусов лист. Для конвертации в картинку использовал библиотеку pdf2image.
3. Чтобы текст читался лучше и только в нужных местах, с помощью библиотеки *Open cv и Pytesseract* я:
- повернул картинку на -90 градусов;
- нашел угол искривления с помощью контуров и ядра, затем выровнял;
- сделал картинку в серый цвет, наложил фильтры blur, denoising;
- путем проб и ошибок нашел лучший вариант - покрасить фон в черный, а текст сделать белым с помощью функции bitwise_not;
- нахожу координаты слов "Счет фактуры", "Продавец", "Покупатель" с помощью Pytesseract, затем обрезаю картинку именно по этим координатам для лучшего считывания информации;
- если координаты не нашлись, то обрезаю картинку по "ручным" координатам;
- если это не помогло, то применяю другой фильтр на изображение и проганяю по новой;
- распознанную информацию фильтрую от не нужных символов и применяю поиск по регулярным выражениям;
- полученную информацию записываю в excel таблицу.

`СТЕК:`
- pdf2image
- pytesseract
- opencv
- re
- openpyxl
- datetime
- aiogram