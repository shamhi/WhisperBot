from datetime import date
import random
import calendar


def get_stat():
    current_date = date.today()
    current_day = current_date.day
    current_month = current_date.month
    current_year = current_date.year

    r_month = random.randint(current_month, 12)
    month_days = calendar.monthrange(current_year, r_month)[1]
    r_day = random.randint(current_day, month_days) if current_month == r_month else random.randint(1, month_days)

    rand_date = f'{r_day:02d}.{r_month:02d}.{current_year}'

    days_NY = (date(current_year, 1, 1) - current_date).days

    OR = 'орёл' if random.randint(1, 2) == 1 else 'решка'

    rand_to_thousand = random.randint(1, 1000)
    rand_to_ten = random.randint(1, 10)

    text = f"Случайная дата: <code>{rand_date}</code>\n\n" \
           f"До Нового года: <code>{days_NY} дн.</code>\n\n" \
           f"Орёл или решка: <code>{OR}</code>\n\n" \
           f"Случайное число до 1000: <code>{rand_to_thousand}</code>\n\n" \
           f"Случайное число до 10: <code>{rand_to_ten}</code>"

    return text
