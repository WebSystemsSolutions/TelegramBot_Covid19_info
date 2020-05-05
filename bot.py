from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import requests


TG_TOKEN = ''
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/51.0.2704.103 Safari/537.36', 'accept': '*/*'}

URL_API_TOTAL = 'https://coronavirus-19-api.herokuapp.com/all'
URL_API_COUNTRIES = 'https://coronavirus-19-api.herokuapp.com/countries/'


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_massage(massage):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    stat_ua = types.InlineKeyboardButton(text="🇺🇦 Статистика в Україні")
    stat_world = types.InlineKeyboardButton(text="🌎 Світова статистика")
    keyboard.add(stat_ua, stat_world)

    await bot.send_message(massage.chat.id, 'Вітаємо. У цьому боті ви зможете побачити актуальну '
                                      'статистику захворювань на COVID-19 🦠\n\n'
                                      'Для взаємодії з ботом використовуй команди:\n\n'
                                      '/search_country - Пошук країни '
                                      '(введіть назву країни латиницею, або візьміть зі списку. Приклад: Ukraine)\n'
                                      '/list_country - Список доступних країн\n'
                                      '/world_statistic - Загальна світова статистика', reply_markup=keyboard)


@dp.message_handler(commands=['search_country'])
async def hello(massage):
    await bot.send_message(massage.chat.id, 'Введіть назву країни.\n'
                                      'Наприклад: USA, Ukraine, Italy...')


@dp.message_handler()
async def stat_country(massage):
    if massage.text == '🇺🇦 Статистика в Україні':
        url_api = URL_API_COUNTRIES + 'Ukraine'
        corona = requests.get(url_api, headers=HEADERS)
        try:
            country = corona.json()["country"]
            deaths = corona.json()["deaths"]
            recovered = corona.json()["recovered"]
            cases = corona.json()["cases"]
            today_cases = corona.json()["todayCases"]
            today_deaths = corona.json()["todayDeaths"]

            await bot.send_message(massage.chat.id, f'Країна : {country}\n'
            f'Зафіксовано випадків : {cases}\n'
            f'Смертей : {deaths}\n'
            f'Одужало : {recovered}\n'
            f'-----------\n'
            f'За останню добу зафіксовано {today_cases} випадків та {today_deaths} смертей')
        except:
            await bot.send_message(massage.chat.id, f'Країни не знайдено. Спробуйте ще раз!')
    elif massage.text == '🌎 Світова статистика':
        try:
            r_total = requests.get(URL_API_TOTAL, headers=HEADERS)
            total_cases = r_total.json()["cases"]
            total_deaths = r_total.json()["deaths"]
            total_recovered = r_total.json()["recovered"]

            await bot.send_message(massage.chat.id, f'Загальна світова статистика!\n'
            f'-----------\n'
            f'Зафіксованих випадків : {total_cases}\n'
            f'Одужавших : {total_recovered}\n'
            f'Летальних випадків : {total_deaths}\n')
        except:
            await bot.send_message(massage.chat.id, 'Вибачте, сталася помилка! Попробуйте пізніше!')
    else:
        url_api = URL_API_COUNTRIES + massage.text
        corona = requests.get(url_api, headers=HEADERS)
        try:
            country = corona.json()["country"]
            deaths = corona.json()["deaths"]
            recovered = corona.json()["recovered"]
            cases = corona.json()["cases"]
            today_cases = corona.json()["todayCases"]
            today_deaths = corona.json()["todayDeaths"]

            await bot.send_message(massage.chat.id, f'Країна : {country}\n'
            f'Зафіксовано випадків : {cases}\n'
            f'Смертей : {deaths}\n'
            f'Одужало : {recovered}\n'
            f'-----------\n'
            f'За останню добу зафіксовано {today_cases} випадків та {today_deaths} смертей')
        except:
            await bot.send_message(massage.chat.id, f'Країни не знайдено. Спробуйте ще раз!')


@dp.message_handler(commands=['world_statistic'])
async def all_deaths(massage):
    try:
        r_total = requests.get(URL_API_TOTAL, headers=HEADERS)
        total_cases = r_total.json()["cases"]
        total_deaths = r_total.json()["deaths"]
        total_recovered = r_total.json()["recovered"]

        await bot.send_message(massage.chat.id, f'Загальна світова статистика!\n'
                                          f'-----------\n'
                                          f'Зафіксованих випадків : {total_cases}\n'
                                          f'Одужавших : {total_recovered}\n'
                                          f'Летальних випадків : {total_deaths}\n')
    except:
        await bot.send_message(massage.chat.id, 'Вибачте, сталася помилка! Попробуйте пізніше!')


@dp.message_handler(commands=['list_country'])
async def list_country(massage):
    try:
        await bot.send_message(massage.chat.id, 'Зачекайте будь ласка. Запит опрацьовується...')
        corona = requests.get(URL_API_COUNTRIES, headers=HEADERS)
        i = 0
        all_country = []
        while i < len(corona.json()):
            c = corona.json()[i]["country"]
            i = i + 1
            all_country.append(c)

        await bot.send_message(massage.chat.id, f'{all_country}\n')
    except:
        await bot.send_message(massage.chat.id, 'Сталася помилка... Попробуйте пізніше.')


if __name__ == "__main__":
    print("Starting")
    executor.start_polling(dp, skip_updates=True)

