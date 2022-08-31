from aiogram import Bot, Dispatcher, types, executor
from convert import converter
from text_search import get_text
from writing_to_excel import data_recording_excel
from config import token
# from main import logging
# import os


bot = Bot(token)
dp = Dispatcher(bot)


async def send_file(chat_id, name_doc):

    with open(f"{name_doc}.xlsx", 'rb') as file:
        await bot.send_document(chat_id, file)
        # logging.info(f'id: {chat_id}; принял: {track}')
        await bot.send_message(chat_id, f'Готово😘\n\n')


async def run(chat_id):
    count_pages = converter()
    write_data = get_text(count_pages)
    name_doc = data_recording_excel(write_data, count_pages)
    await send_file(chat_id, name_doc)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_file(message: types.Message):
    chat_id = message.chat.id
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.send_message(chat_id, f'Принял😉👍\nНачинаю распознавать текст...⏱')
    await bot.download_file(file_path, r'images\doc.pdf')
    await run(chat_id)


# def del_documents(path):
#     os.remove(f"{path}\\{}.pdf")


if __name__ == '__main__':
    # logging.info('Старт')
    executor.start_polling(dp, skip_updates=True)
