from __future__ import annotations
from urllib.request import urlopen
from xml.etree import ElementTree as ET
from functools import lru_cache
from typing import Optional
from datetime import timedelta, datetime
import time

@lru_cache(maxsize=10) # кэшируюший декоратор  
def get_currencies(currencies_ids_lst=['R01239', 'R01235', 'R01035', 'R01815']):
	cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")

	result = {}

	cur_res_xml = ET.parse(cur_res_str)

	root = cur_res_xml.getroot()
	valutes = root.findall('Valute')
	for el in valutes:
		curr_id = el.get('ID')

		if str(curr_id) in currencies_ids_lst:
		        	#valute_name = el.find('Name').text
			curr_value = el.find('Value').text
			result[curr_id] = curr_value

	return result

class SingletonMeta(type):
	"""
	Мета-класс для создания класса-синглтона
	"""
	_instance: Optional[Singleton] = None

	def __call__(self) -> Singleton:
		if self._instance is None:
			self._instance = super().__call__()
		return self._instance

class Currency(metaclass=SingletonMeta):
	"""
	Класс-синглтон, в котором хранится информация о валюте и методы для работы с запросами
	"""
	def __init__(self):
		self.curr_name = ["Вон Республики Корея", "Доллар США", "Евро", "Фунт стерлингов Соединенного королевства"]
		self.curr_char = ['R01239', 'R01235', 'R01035', 'R01815']
		self.curr_cache = get_currencies()

	def autoreq(n, f, timeout=60*60*60*24):
		"""
		метод для автоматической отправки запросов
		"""
		first_called=datetime.now()
		print(f())
		num_calls=1
		drift=timedelta()
		time_period=timedelta(seconds=n)
		while 1:
			time.sleep(n-drift.microseconds/1000000.0)
			current_time = datetime.now()
			print(f())
			num_calls += 1
			difference = current_time - first_called
			drift = difference - time_period * num_calls
			if (difference.microseconds >= timedelta(timeout).microseconds):
				break

	def update(self):
		"""
		метод (предполагаемо) для форсированной отправки запросов
		"""
		self.curr_cache.clear()
		self.curr_cache = get_currencies()
		return self.curr_cache

	def check(self, n):
		if (n > 60*60*5):
			self.curr_cache.clear()
			return get_currencies()
		elif (n >=1) and (n<=60):
			return get_currencies()

if __name__ == "__main__":
	Currency.autoreq(5, get_currencies, 20)
	print(get_currencies.cache_info())
