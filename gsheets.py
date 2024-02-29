import gspread
from datetime import datetime

# Двумерный массив с сопоставлением отдела и ссылки на таблицу
sheets = [
    ["Администрация", "https://docs.google.com/spreadsheets/d/1H00lV5YvAA6wVHLankgA8zp5jHb0ktjMsi9aVrFiJRo"],
    [
        "Администрация эл. журнала",
        "https://docs.google.com/spreadsheets/d/1Fsj8fp93V_R0rLY_xtUeMSKWrqQv5N1Igiy1kTrb9Iw",
    ],
    ["IT отдел", "https://docs.google.com/spreadsheets/d/14NnC9nyCtADkD81q9RMFJKFfNz3RTo_egr3eO8GUQzk"],
    ["Завхоз", "https://docs.google.com/spreadsheets/d/17ZJ6i08O_Ebg2py6FUHqul2Bp-rjbRxUq41mDrHhpN0"],
]

# Привязка токена
gc = gspread.service_account("tokengoogle.json")


# Распределение заявок по таблицам отделов и добавление в таблицы новой строки
def senddata(user_nik, dep, crit, cab, prob):
    for i in range(0, len(sheets)):
        if dep == sheets[i][0]:
            # Окончательное время регистрации заявки
            time = datetime.now().strftime("%d %b %Y, %H:%M")
            # Функция подключения к таблице и получение первого листа
            sh = gc.open_by_url(sheets[i][1]).get_worksheet(0)
            sh.append_row([time, user_nik, cab, crit, prob], value_input_option='RAW', insert_data_option=None)
            print(f"{time}: Оставлена новая заявка в отдел {dep}!")
