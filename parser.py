import os
import requests
from time import sleep
from datetime import datetime, timedelta


def to_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%d-%m-%Y')


def range_days(date_1: str, date_2: str) -> range:
    return range((to_datetime(date_2)-to_datetime(date_1)).days+1)


def date_range_str(date_1: str, date_2: str) -> list[str]:
    return [(to_datetime(date_1) + timedelta(days=day)).strftime('%d-%m-%Y') for day in range_days(date_1, date_2)]


def date_sort(dates: list[str], txt=False) -> list:
	if txt:
		dates_unix = [datetime.strptime(date, '%d-%m-%Y.txt') for date in dates]
	else:
		dates_unix = [datetime.strptime(date, '%d-%m-%Y') for date in dates]
	dates_unix.sort()
	return [date.strftime('%d-%m-%Y') for date in dates_unix]


def get_log_content(date) -> list:
	return open(f'{folder}/{date}.txt', 'r', encoding='utf-8').readlines()


if __name__ == '__main__':
	server_url = 'http://192.168.0.102:3001/api/minecraftLogs/tmrpg'
	secret_key = 'super_secret'
	while True:
		response = requests.get(server_url)
		folder = 'logs'
		if response.status_code == 200:
			site_logs = date_sort(response.json())
			server_logs = date_range_str(site_logs[-1], date_sort(os.listdir(folder), txt=True)[-1])
			for date in server_logs:
				response = requests.post(server_url, data = {
					'logs': get_log_content(date),
					'key': secret_key,
					'date': date
				})
		sleep(60)
