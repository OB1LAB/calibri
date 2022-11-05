from datetime import datetime, timedelta


def log_type(log: list[str]) -> dict:
    """
    :param log: Массив строки лога
    :return: Словарь с ключами "type" и "player" (Кто отправил)
    """
    if len(log) == 3 and log[2] == 'зашёл':
        return {
            'type': 'join',
            'player': log[1]
        }
    elif len(log) == 3 and log[2] == 'вышел':
        return {
            'type': 'exit',
            'player': log[1]
        }
    elif len(log) == 3 and log[1] == 'Сервер':
        return {
            'type': 'server_off',
            'player': None
        }
    elif len(log) > 5 and log[2] == 'issued':
        if log[5].lower() == '/vanish':
            return {
                'type': 'Vanish',
                'player': log[1]
            }
        elif (log[5].lower() in ['/tell', '/m', '/w', '/msg', '/pm', '/t', '/whisper', '/mail']
              and len(log) > 7 or log[5].lower() == '/r' and len(log) > 6):
            return {
                'type': 'PM',
                'player': log[1]
            }
        elif log[5].lower() == '/warn' and len(log) > 6:
            return {
                'type': 'Warns',
                'player': log[1]
            }
        elif log[5].lower() == '/mute' and len(log) > 6 or log[5].lower() == '/tempmute' and len(log) > 9:
            return {
                'type': 'Mutes',
                'player': log[1]
            }
        elif log[5].lower() == '/kick' and len(log) > 6:
            return {
                'type': 'Kicks',
                'player': log[1]
            }
        elif log[5].lower() == '/ban' and len(log) > 6 or log[5].lower() == '/tempban' and len(log) > 9:
            return {
                'type': 'Bans',
                'player': log[1]
            }
    elif len(log) > 1 and log[1] == '[L]':
        return {
            'type': 'L',
            'player': log[2].split(':')[0]
        }
    elif len(log) > 1 and log[1] == '[G]':
        return {
            'type': 'G',
            'player': log[2].split(':')[0]
        }
    return {
        'type': None,
        'player': None
    }


def range_days(date_1: str, date_2: str) -> range:
    """Количество дней между двух дат, в виде массива"""
    return range((to_datetime(date_2)-to_datetime(date_1)).days+1)


def to_datetime(date: str) -> datetime:
    """Преобразование строковых даты в формат datetime"""
    return datetime.strptime(date, '%d-%m-%Y')


def date_range_str(date_1: str, date_2: str, with_txt=False) -> list[str]:
    """
    :param date_1: Первая дата в виде строки
    :param date_2: Вторая дата в виде строки
    :param with_txt: Приписывать ли в конце ".txt"
    :return: Массив дат (В виде строк). В формате: день-месяц-Год
    """
    if with_txt:
        return [(to_datetime(date_1) + timedelta(days=day)).strftime('%d-%m-%Y') + '.txt' for day in range_days(date_1,
                                                                                                                date_2)]
    return [(to_datetime(date_1) + timedelta(days=day)).strftime('%d-%m-%Y') for day in range_days(date_1, date_2)]


def date_sort(dates: list[str], reverse_dates=False, date_reverse=False, with_txt=True):
    """
    :param dates: Массив с датами (В виде строки)
    :param reverse_dates: Если возвращаемый формат дат нужен в формате: Год-месяц-день
    :param date_reverse: Если входные даты находятся в следующем формате: Год-месяц-день
    :param with_txt: Приписывать ли в конце всех дат ".txt"
    :return: Массив отсортированных дат (В виде строк). По умолчанию в формате: день-месяц-Год
    """
    if not dates:
        return []
    if '.txt' in dates[0]:
        if date_reverse:
            dates_unix = [datetime.strptime(date, '%Y-%m-%d.txt') for date in dates]
        else:
            dates_unix = [datetime.strptime(date, '%d-%m-%Y.txt') for date in dates]
    else:
        if date_reverse:
            dates_unix = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        else:
            dates_unix = [datetime.strptime(date, '%d-%m-%Y') for date in dates]
    dates_unix.sort()
    if reverse_dates:
        if with_txt:
            return [date.strftime('%Y-%m-%d')+'.txt' for date in dates_unix]
        return [date.strftime('%Y-%m-%d') for date in dates_unix]
    if with_txt:
        return [date.strftime('%d-%m-%Y')+'.txt' for date in dates_unix]
    return [date.strftime('%d-%m-%Y') for date in dates_unix]


def unix_log(date: str, log: str) -> int:
    """
    :param date: Дата строки в формате: день-месяц-Год
    :param log: Строка лога
    :return: Unixtime строки
    """
    unix = int(datetime.strptime(f'{date} {log.split()[0]}', '%d-%m-%Y [%H:%M:%S]').timestamp())
    return unix


def output_time(time: int) -> str:
    """
    :param time: Количество секунд
    :return: Строка времени, в формате - час:минута:секунда (23:59:59)
    """
    hours, time = int(time/3600), time-int(time/3600)*3600
    minutes, seconds = int(time/60), time-int(time/60)*60
    if hours < 10:
        output = f'0{hours}'
    else:
        output = str(hours)
    if minutes < 10:
        output += f':0{minutes}'
    else:
        output += f':{minutes}'
    return output


def diff_times(join_mass: list[int], exit_mass: list[int]) -> int:
    """
    :param join_mass: Массив времени в формате unixtime
    :param exit_mass: Массив времени в формате unixtime
    :return: Разница секунд между массивами
    """
    time = 0
    for line in range(len(join_mass)):
        diff = exit_mass[line]-join_mass[line]
        if diff > 10800:
            diff = 10800
        time += diff
    return time


def get_monday() -> str:
    """Получение даты понедельника текущей недели, в виде строки"""
    today = datetime.now()
    return (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
