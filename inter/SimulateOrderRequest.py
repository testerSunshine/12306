
import copy
import random
import wrapcache
from config import urlConf
from config.TicketEnmu import ticket
from config.emailConf import sendEmail
from config.serverchanConf import sendServerChan
from myUrllib.httpUtils import HTTPClient
from config.configCommon import seat_conf_2
import TickerConfig
import sys
import os
import time
import numpy as np
import math

from myException.ReLoginException import ReLoginException

from myException.ticketIsExitsException import ticketIsExitsException
from myException.ticketNumOutException import ticketNumOutException
from selenium.common.exceptions import TimeoutException
import inter.easing
import asyncio
from pyppeteer import launch
import async_timeout

class SimulateOrderRequest:
	def __init__(self,selectObj,from_station,to_station,from_station_h,to_station_h,_station_seat,station_trains, station_dates,  ticke_peoples_num, train_no  ,secretStr ,set_type ,train_date, passengerTicketStr, oldPassengerStr,start_time):
		self.session = selectObj
		self.urls = urlConf.urls
		self.from_station = from_station
		self.to_station = to_station
		self.from_station_h = from_station_h
		self.to_station_h = to_station_h
		self.station_trains = station_trains
		self._station_seat = _station_seat if isinstance(_station_seat, list) else list(_station_seat)
		self.station_dates = station_dates if isinstance(station_dates, list) else list(station_dates)
		self.ticket_black_list = dict()
		self.ticke_peoples_num = ticke_peoples_num
		self.train_date = train_date
		self.secretStr = secretStr
		self.train_no = train_no
		self.start_time = start_time
		self.passengerTicketStr= passengerTicketStr
		self.oldPassengerStr= oldPassengerStr

		self.set_type = set_type


	async def mouse_slide(self,page=None):
		await asyncio.sleep(0.3)
		try :
			#鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
			await self.page.hover('#nc_1_n1z') 
			await self.page.mouse.down()
			await self.page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
			await self.page.mouse.up()
		except Exception as e:
			print(e, ':验证失败')
			return False,self.page
		return True,self.page



	def get_order_information(self):
		passengers = []
		passengerStrList = self.passengerTicketStr.split('_')
		for eachPassenger in passengerStrList:
				passengerInfo = eachPassenger.split(',')
				if (len(passengerInfo) == 9):
					passengers.append({'type':passengerInfo[0],'name':passengerInfo[3]})
		return passengers

	async def fill_the_page(self):
		TIME_OUT_L = 20
		if TickerConfig.IS_HEADLESS:
			TIME_OUT_L = 3
		try:
			async with async_timeout.timeout(TIME_OUT_L) as cm:
				while not await self.page.querySelector('#normalPassenger_0'):
					pass
		except:
			if cm.expired: #超时，没能进入订单页，可能是session失效
				print("超时未能进入订单页面，重试")
				raise ReLoginException("Need Login")
		passengers = self.get_order_information()
		passenger_num = 1
		for eachPassenger in passengers:
			xpath = "//label[text() = '{0}']".format(eachPassenger['name'])
			while not await self.page.querySelector('#normalPassenger_0'):
				pass
			a = await self.page.xpath(xpath)
			await a[-1].click()
			await self.page.select('select#seatType_'+str(passenger_num),eachPassenger['type'])
			passenger_num += 1
		button = await self.page.J("#submitOrder_id")
		if button:
			print("不需要滑块验证，尝试提交中")
			await button.click()
			#await asyncio.sleep(0.2)
			
			await self.page.waitForSelector('#qr_submit_id', {'visible':True,})
			qr_btn = await self.page.J("#qr_submit_id")
			#asyncio.sleep(120)
			await qr_btn.click()
			asyncio.sleep(30)
			sendEmail(ticket.WAIT_ORDER_SUCCESS.format("1"))
			sendServerChan(ticket.WAIT_ORDER_SUCCESS.format("1"))
			raise ticketIsExitsException(ticket.WAIT_ORDER_SUCCESS.format("1"))
		else:
			slide = await self.page.J("#nc_1_n1z")
			if slide:
				print("需要滑块验证，尝试提交中")
				flag = False
				for i in range(3):
					flag,self.page = await self.mouse_slide(page=self.page) #js拉动滑块过去。
					if flag:
						break
					else: 
						continue
				await self.page.waitForSelector('#qr_submit_id', {'visible':True,})
				qr_btn = await self.page.J("#qr_submit_id")
				await qr_btn.click()
				asyncio.sleep(30)
				sendEmail(ticket.WAIT_ORDER_SUCCESS.format("1"))
				sendServerChan(ticket.WAIT_ORDER_SUCCESS.format("1"))
				raise ticketIsExitsException(ticket.WAIT_ORDER_SUCCESS.format("1"))
			else:
				print("失败：未知原因")
				return


	async def py_delete_all_cookies(self):
		tcookies = await self.page.cookies()
		for a in tcookies:
			await self.page.deleteCookie(a)

	async def py_set_all_cookies(self):
		c = self.session.httpClint.get_cookie_all_items()
		#print(c)
		for x in c:
			if x[0] == 'RAIL_DEVICEID' or x[0] == 'RAIL_EXPIRATION':
				await self.page.setCookie({'name':x[0],'value':x[1],'domain':'.12306.cn','path':'/'})	
			elif x[0] == 'JSESSIONID':
				await self.page.setCookie({'name':x[0],'value':x[1],'path':'/otn','domain': 'kyfw.12306.cn'})	
			else:
				await self.page.setCookie({'name':x[0],'value':x[1],'domain': 'kyfw.12306.cn'})
		#print(await self.page.cookies())

	async def I_AM_NOT_A_ROBOT(self):
		await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''') #以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
		await self.page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
		await self.page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
		await self.page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
 
		await self.page.evaluateOnNewDocument('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''') #以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
		await self.page.evaluateOnNewDocument('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
		await self.page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
		await self.page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
	
	async def start_simulate(self):
		self.driver = await launch({'headless':TickerConfig.IS_HEADLESS ,'args': ['--no-sandbox'], })
		self.page = await self.driver.newPage()
		select_url = copy.copy(self.urls["leftTicketPage"])
		req_url = "https://"+select_url['Host'] +'/'+ select_url['req_url'].format(self.from_station_h+','+self.from_station,self.to_station_h+','+self.to_station,self.train_date)		
		await self.page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

		await self.page.goto(req_url)
		await self.I_AM_NOT_A_ROBOT()
		while not await self.page.querySelector('#query_ticket'):
			pass
		await self.py_delete_all_cookies()
		try:
			while await self.page.cookies():
				pass
		except:
			pass
		await self.py_set_all_cookies()
		try:
			while not await self.page.cookies():
				pass
		except:
			pass
		await self.page.goto(req_url)
		js = "checkG1234(\'"+self.secretStr+"\',\'"+self.start_time+"\',\'"+self.train_no+"\',\'"+self.from_station+"\',\'"+self.to_station+"\')"
		await self.page.evaluate(js)
		try:
			await self.fill_the_page()
		except ReLoginException:
			print("重新登陆中")
			self.session.call_login()
			await self.page.goto(req_url)
			while not await self.page.querySelector('#query_ticket'):
				pass
			await self.py_delete_all_cookies()
			while await self.page.cookies():
				pass
			await self.py_set_all_cookies()
			while not await self.page.cookies():
				pass
			await self.page.goto(req_url)				
			await self.page.evaluate(js)
			try:
				await self.fill_the_page()
			except ReLoginException:
				print("失败，重新查询")
				return

	def Do_simulate(self):
		asyncio.get_event_loop().run_until_complete(self.start_simulate())


            