#coding:utf-8
import os
import datetime
import logging
import logging.config

current_path = os.path.realpath(__file__)
father_path = os.path.dirname(os.path.dirname(current_path))
file_path = os.path.join(father_path, 'log')

class log:
	def __init__(self, logger_name=None, over_write=False):
		'''

		:param over_write:
		:return:
		'''
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		# 终端Handler
		consoleHandler = logging.StreamHandler()
		consoleHandler.setLevel(logging.DEBUG)

		# 文件Handler
		#文件保存地址
		now_time = datetime.datetime.now().strftime('%Y-%m-%d')
		file_name = os.path.join(file_path, now_time + '_%s_log.log'%logger_name)
		#文件保存格式，'a'为增加，'w'为覆盖
		if over_write:
			mode = 'w'
		else:
			mode = 'a'
		fileHandler = logging.FileHandler(file_name, mode=mode, encoding='UTF-8')
		fileHandler.setLevel(logging.NOTSET)

		# Formatter
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		consoleHandler.setFormatter(formatter)
		fileHandler.setFormatter(formatter)

		# 添加到Logger中
		self.logger.addHandler(consoleHandler)
		self.logger.addHandler(fileHandler)