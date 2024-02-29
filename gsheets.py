import gspread
from datetime import datetime

# Двумерный массив с сопоставлением отдела и ссылки на таблицу
sheeturl = "https://docs.google.com/spreadsheets/d/1Rgk5rNhDeNd951ksWkwMw0Tm6LG_Nzu16CL2SShZtvk"

# Привязка токена
gc = gspread.service_account("tokengoogle.json")


# Добавление нового желания
def add_new_whish(user_nik, whish):
    # Окончательное время регистрации заявки
    time = datetime.now().strftime("%d %b %Y, %H:%M")
    # Функция подключения к таблице и получение первого листа
    sh = gc.open_by_url(sheeturl).get_worksheet(0)
    sh.append_row([time, whish, user_nik], value_input_option='RAW', insert_data_option=None)
    print(f"{time}: {user_nik} оставил новое желание!")

# Просмотр всех желаний
def get_whishlist(user_nik, mode):
    sh = gc.open_by_url(sheeturl).get_worksheet(0)
    # Заполняемые строчки начинаются с 3
    i = 3
    whishs = []
    while(True):
        values_list = sh.row_values(i)
        if(len(values_list) == 0):
            break
        else:
            if(mode == 1):
                if(values_list[2] == user_nik):
                    whishs.append(values_list[1]) 
            else:
                if(values_list[2] != user_nik):
                    whishs.append(values_list[1])
            i += 1
    return whishs