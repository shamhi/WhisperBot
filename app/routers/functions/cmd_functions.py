from datetime import datetime
import random


def get_stat():
    day = random.randint(1, 30)
    current_day = int(datetime.now().strftime('%d'))
    current_month = int(datetime.now().strftime('%m'))
    month = random.randint(current_month, 12)
    year = int(datetime.now().strftime('%Y'))
    if int(month) == current_month:
        day = random.randint(current_day, 30)
    if len(str(month)) != 2:
        month = f'0{str(month)}'
    if len(str(day)) != 2:
        day = f'0{str(day)}'
    rand_date = f'{str(day)}.{str(month)}.{str(year)}'

    now_year = int(datetime.now().strftime('%Y'))
    days_NY = 365 - abs((datetime(now_year, 1, 1) - datetime.now())).days

    random_int = random.randint(1, 2)
    OR = 'орёл' if random_int == 1 else 'решка'

    rand_to_thousand = random.randint(1, 1000)
    rand_to_ten = random.randint(1, 10)

    text = f"Случайная дата: <code>{rand_date}</code>\n\n" \
           f"До Нового года: <code>{days_NY} дн.</code>\n\n" \
           f"Орёл или решка: <code>{OR}</code>\n\n" \
           f"Случайное число до 1000: <code>{rand_to_thousand}</code>\n\n" \
           f"Случайное число до 10: <code>{rand_to_ten}</code>"

    return text





