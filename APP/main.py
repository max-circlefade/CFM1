import os
os.environ['KIVY_GL_BACKEND']='gl'

# CFM1 APP version 1.2

import kivy
import platform
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.animation import  Animation
from decimal import *
import operator
import json
import multiprocessing
import mido
import serial
import rtmidi
import numpy
from iconfonts import *
from os.path import join, dirname
from math import *
import random


register('default_font', 'Icons.ttf',
			 join(dirname(__file__), 'Icons.fontd'))
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

rpi = 0
if platform.system()=='Linux':
	try:
		from RPi import GPIO
		rpi = 1
	except:
		pass

print(("rpi detected:",rpi))
if rpi==1:
	import smbus
	from RPi import GPIO
	ser=serial.Serial('/dev/ttyAMA0', 38400)
	bus = smbus.SMBus(1)
	clk = 21
	dt = 20
	sw = 16
	pwm = 13
	jackstart = 12
	ldac1= 17
	ldac2= 27
	ldac3= 22
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pwm,GPIO.OUT)
	GPIO.setup(jackstart,GPIO.OUT)
	pwmsync = GPIO.PWM(13,4)
	GPIO.setup(ldac1, GPIO.OUT)
	GPIO.setup(ldac2, GPIO.OUT)
	GPIO.setup(ldac3, GPIO.OUT)	
	GPIO.output(ldac1, 0)  
	GPIO.output(ldac2, 0)  
	GPIO.output(ldac3, 0)  

if rpi==0:
	pass



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class ParamScreen(Screen):


	def on_enter(self):
		global rangeMidi
		global rangeCV
		global rangeCVTrack
		global playing
		v1.value=0
		playing=0
		rangeCVTrack=0
		rangeMidi=0
		rangeCV=0
		self.midiupdate()
		self.CVupdate()
		self.convert()
		self.syncupdate()
		self.versionupdate()
		self.b1000005.pos=320,1170
		Clock.schedule_interval(self.listening, 0.002)
		w1.value=0	

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'		

	def versionupdate(self):
		self.b1000004.text='CFM1 Version '+str(version)

	def midiupdate(self):
		self.b1001.text=paramcf1["midi-map"][rangeMidi]["port"]
		self.b1002.text=paramcf1["midi-map"][rangeMidi+1]["port"]
		self.b1003.text=paramcf1["midi-map"][rangeMidi+2]["port"]
		self.b1004.text=paramcf1["midi-map"][rangeMidi+3]["port"]
		self.b1005.text=paramcf1["midi-map"][rangeMidi+4]["port"]
		self.b1006.text=paramcf1["midi-map"][rangeMidi+5]["port"]
		self.b2001.text=paramcf1["midi-map"][rangeMidi]["channel"]
		self.b2002.text=paramcf1["midi-map"][rangeMidi+1]["channel"]
		self.b2003.text=paramcf1["midi-map"][rangeMidi+2]["channel"]
		self.b2004.text=paramcf1["midi-map"][rangeMidi+3]["channel"]
		self.b2005.text=paramcf1["midi-map"][rangeMidi+4]["channel"]
		self.b2006.text=paramcf1["midi-map"][rangeMidi+5]["channel"]
		self.lbl1.text = 'Track' + str(rangeMidi + 1)+':'
		self.lbl2.text = 'Track' + str(rangeMidi + 2)+':'
		self.lbl3.text = 'Track' + str(rangeMidi + 3)+':'
		self.lbl4.text = 'Track' + str(rangeMidi + 4)+':'
		self.lbl5.text = 'Track' + str(rangeMidi + 5)+':'
		self.lbl6.text = 'Track' + str(rangeMidi + 6)+':'


	def syncupdate(self):
		print("here sync")
		if paramcf1["sync"][0]["midi-din"]=="on": self.b100001.text="On"
		else: self.b100001.text="Off"
		if paramcf1["sync"][1]["midi-usb"]=="on": self.b100002.text="On"
		else: self.b100002.text="Off"
		self.b100003.text=paramcf1["sync"][2]["ppq"]
		if paramcf1["sync"][3]["BPMmult"]=="1": self.b100004.text="24"
		else: self.b100004.text="48"
		if paramcf1["sync"][4]["USBstate"]=="in": self.b100005.text="In"
		else: self.b100005.text="Out"		




	def CVupdate(self):
		self.b10001.text=paramcf1["CV-map"][rangeCV]["Type"]
		self.b10002.text=paramcf1["CV-map"][rangeCV+1]["Type"]
		self.b10003.text=paramcf1["CV-map"][rangeCV+2]["Type"]
		self.b10004.text=paramcf1["CV-map"][rangeCV+3]["Type"]
		self.b10005.text=paramcf1["CV-map"][rangeCV+4]["Type"]
		self.b10006.text=paramcf1["CV-map"][rangeCV+5]["Type"]
		self.b20001.text=paramcf1["CV-map"][rangeCV]["Track"]
		self.b20002.text=paramcf1["CV-map"][rangeCV+1]["Track"]
		self.b20003.text=paramcf1["CV-map"][rangeCV+2]["Track"]
		self.b20004.text=paramcf1["CV-map"][rangeCV+3]["Track"]
		self.b20005.text=paramcf1["CV-map"][rangeCV+4]["Track"]
		self.b20006.text=paramcf1["CV-map"][rangeCV+5]["Track"]
		self.b30001.text=paramcf1["CV-map"][rangeCV]["Voltage"]
		self.b30002.text=paramcf1["CV-map"][rangeCV+1]["Voltage"]
		self.b30003.text=paramcf1["CV-map"][rangeCV+2]["Voltage"]
		self.b30004.text=paramcf1["CV-map"][rangeCV+3]["Voltage"]
		self.b30005.text=paramcf1["CV-map"][rangeCV+4]["Voltage"]
		self.b30006.text=paramcf1["CV-map"][rangeCV+5]["Voltage"]
		self.VoltageHide()
		self.lbl10.text = 'CV' + str(rangeCV + 1)+':'
		self.lbl20.text = 'CV' + str(rangeCV + 2)+':'
		self.lbl30.text = 'CV' + str(rangeCV + 3)+':'
		self.lbl40.text = 'CV' + str(rangeCV + 4)+':'
		self.lbl50.text = 'CV' + str(rangeCV + 5)+':'
		self.lbl60.text = 'CV' + str(rangeCV + 6)+':'

	def VoltageHide(self):
		if self.b10001.text=="PITCH": self.b30001.pos=479,320
		else: self.b30001.pos=1479,320
		if self.b10002.text=="PITCH": self.b30002.pos=479,260
		else: self.b30002.pos=1479,320
		if self.b10003.text=="PITCH": self.b30003.pos=479,200
		else: self.b30003.pos=1479,320
		if self.b10004.text=="PITCH": self.b30004.pos=479,140
		else: self.b30004.pos=1479,320
		if self.b10005.text=="PITCH": self.b30005.pos=479,80
		else: self.b30005.pos=1479,320
		if self.b10006.text=="PITCH": self.b30006.pos=479,20
		else: self.b30006.pos=1479,320
		#self.NoneHide()

	def NoneHide(self):
		if self.b20001.text!="NONE": self.b10001.pos=328,320
		else: self.b10001.pos=1479,320
		if self.b20002.text!="NONE": self.b10002.pos=328,260
		else: self.b10002.pos=1479,320
		if self.b20003.text!="NONE": self.b10003.pos=328,200
		else: self.b10003.pos=1479,320
		if self.b20004.text!="NONE": self.b10004.pos=328,140
		else: self.b10004.pos=1479,320
		if self.b20005.text!="NONE": self.b10005.pos=328,80
		else: self.b10005.pos=1479,320
		if self.b20006.text!="NONE": self.b10006.pos=328,20
		else: self.b10006.pos=1479,320		


	def midiportselect(self):
		self.b4000.pos=328,120
		self.b4001.pos=329,121
		self.b4002.pos=329,182
		self.b4003.text="MIDI PORT:"
		self.b4001.text="DIN"
		self.b4002.text="USB"
		self.b4003.pos=329,243
		self.b3005.pos=0,0


	def midichannelselect(self):
		self.b5017.pos=310,305
		self.b5017.text="MIDI CHANNEL:"
		self.b5000.pos=138,31
		self.b5001.pos=139,236
		self.b5005.pos=139,168
		self.b5009.pos=139,100
		self.b5013.pos=139,32
		self.b5002.pos=269,236
		self.b5006.pos=269,168
		self.b5010.pos=269,100
		self.b5014.pos=269,32
		self.b5003.pos=399,236
		self.b5007.pos=399,168
		self.b5011.pos=399,100
		self.b5015.pos=399,32
		self.b5004.pos=529,236
		self.b5008.pos=529,168
		self.b5012.pos=529,100
		self.b5016.pos=529,32
		self.b3005.pos=0,0
		self.b5001.text="1"
		self.b5005.text="5"
		self.b5009.text="9"
		self.b5013.text="13"
		self.b5002.text="2"
		self.b5006.text="6"
		self.b5010.text="10"
		self.b5014.text="14"
		self.b5003.text="3"
		self.b5007.text="7"
		self.b5011.text="11"
		self.b5015.text="15"
		self.b5004.text="4"
		self.b5008.text="8"
		self.b5012.text="12"
		self.b5016.text="16"

	def CVTypeselect(self,b):
		self.CVselected(b)
		self.b4000.pos=328,120
		self.b4002.pos=329,182	
		self.b4003.text="CV TYPE:"
		self.b4003.pos=329,243
		self.b3005.pos=0,0		
		if str(paramcf1["CV-map"][CVselectedparam-1]["Track"])!= "NONE":
	
			#print('trackmode',trackmode)
			#print(paramcf1["CV-map"][CVselectedparam-1]["Track"])
			if trackmode[int(paramcf1["CV-map"][CVselectedparam-1]["Track"])-1]==1 or trackmode[int(paramcf1["CV-map"][CVselectedparam-1]["Track"])-1]==4:
				self.b4001.text="PITCH"
				self.b4002.text="GATE"
				self.b4001.pos=329,121
			elif trackmode[int(paramcf1["CV-map"][CVselectedparam-1]["Track"])-1]==2:
				self.b4002.text="LFO"
			elif trackmode[int(paramcf1["CV-map"][CVselectedparam-1]["Track"])-1]==3:
				self.b4002.text="ADSR"
			elif trackmode[int(paramcf1["CV-map"][CVselectedparam-1]["Track"])-1]==5:
				self.b4002.text="GATE"				

		else:
			self.b4001.text="GATE"
			self.b4002.text="PITCH"
			self.b4001.pos=329,121

	def CVtrack(self):
		#CVselectedparam
		pass

	def CVTrackselect(self):
		global rangeCVTrack
		rangeCVTrack=0
		self.b5017.pos=310,305
		self.b5017.text="TRACK:"
		self.b5000.pos=138,31
		self.b5001.pos=139,236
		self.b5005.pos=139,168
		self.b5009.pos=139,100
		self.b5013.pos=139,32
		self.b5002.pos=269,236
		self.b5006.pos=269,168
		self.b5010.pos=269,100
		self.b5014.pos=269,32
		self.b5003.pos=399,236
		self.b5007.pos=399,168
		self.b5011.pos=399,100
		self.b5015.pos=399,32
		self.b5004.pos=529,236
		self.b5008.pos=529,168
		self.b5012.pos=529,100
		self.b5016.pos=529,32
		self.b3005.pos=0,0
		self.b5001.text="1"
		self.b5005.text="5"
		self.b5009.text="9"
		self.b5013.text="13"
		self.b5002.text="2"
		self.b5006.text="6"
		self.b5010.text="10"
		self.b5014.text="14"
		self.b5003.text="3"
		self.b5007.text="7"
		self.b5011.text="11"
		self.b5015.text="15"
		self.b5004.text="4"
		self.b5008.text="8"
		self.b5012.text="12"
		self.b5016.text="16"

	def PPQselect(self):
		self.b5017.pos=310,305
		self.b5017.text="PPQ:"
		self.b5000.pos=138,31
		self.b5001.pos=139,236
		self.b5005.pos=139,168
		self.b5009.pos=139,100
		self.b5013.pos=139,32
		self.b5002.pos=269,236
		self.b5006.pos=269,168
		self.b5010.pos=269,100
		self.b5014.pos=269,32
		self.b5003.pos=399,236
		self.b5007.pos=399,168
		self.b5011.pos=399,100
		self.b5015.pos=399,32
		self.b5004.pos=529,236
		self.b5008.pos=529,168
		self.b5012.pos=529,100
		self.b5016.pos=529,32
		self.b3005.pos=0,0
		self.b5001.text="/48"
		self.b5005.text="/4"
		self.b5009.text="4"
		self.b5013.text="32"
		self.b5002.text="/24"
		self.b5006.text="/2"
		self.b5010.text="8"
		self.b5014.text="48"
		self.b5003.text="/16"
		self.b5007.text="1"
		self.b5011.text="16"
		self.b5015.text="64"
		self.b5004.text="/8"
		self.b5008.text="2"
		self.b5012.text="24"
		self.b5016.text="96"



	def CVVoltageselect(self):
		self.b4000.pos=328,120
		self.b4001.pos=329,121
		self.b4002.pos=329,182
		self.b4001.text="[ -5V ; 5V ]"
		self.b4002.text="[ 0V ; 10V ]"
		self.b4003.pos=329,243
		self.b4003.text="VOLTAGE:"
		self.b3005.pos=0,0


	def trackselected(self,button):
		global trackselectedparam
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		trackselectedparam=int(ID[-3:])+rangeMidi
		#print(trackselectedparam)


	def CVselected(self,button):
		global CVselectedparam
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		CVselectedparam=int(ID[-2:])+rangeCV
		#print('CVselectedparam',CVselectedparam)

	def port1(self,button):
		global Sendinfo
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		new=(ID[-1:])
		if self.b4003.text=="MIDI PORT:":
			if int(new)==1: paramcf1["midi-map"][trackselectedparam-1]["port"] = "USB"
			if int(new)==2: paramcf1["midi-map"][trackselectedparam-1]["port"] = "DIN"
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)				
			self.midiupdate()
			self.convert()
		if self.b4003.text=="VOLTAGE:":
			if int(new)==1: paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ 0V ; 10V ]"
			if int(new)==2: paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()
		if self.b4003.text=="CV TYPE:":
			if self.b4001.text=="PITCH" and int(new)==2:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "PITCH"
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "PITCH" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1
			if self.b4002.text=="LFO" and int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "LFO"
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "LFO" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1
			if self.b4002.text=="ADSR" and int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "ADSR"
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "ADSR" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1									
			if self.b4002.text=="GATE" and int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "GATE"
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "GATE" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()
			#print(Sendinfo)


	def port2(self,button):
		global Sendinfo
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		new=int((ID[-2:]))
		if self.b5017.text=="TRACK:":
			new=int(new)+rangeCVTrack
			paramcf1["CV-map"][CVselectedparam-1]["Track"] = str(new)
			paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
			i=0
			while i<12:
				if paramcf1["CV-map"][i]["Track"]== str(new) and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Type"]==paramcf1["CV-map"][CVselectedparam-1]["Type"]:
					paramcf1["CV-map"][i]["Track"] = "NONE"
					break
				i+=1
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()
		if self.b5017.text=="MIDI CHANNEL:":
			paramcf1["midi-map"][trackselectedparam-1]["channel"] = str(new)
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			self.midiupdate()
			self.convert()
			print(Sendinfo)
		if self.b5017.text=="PPQ:":
			table=["/48","/24","/16","/8","/4","/2","1","2","4","8","16","24","32","48","64","96"]
			print((str(table[new-1])))
			paramcf1["sync"][2]["ppq"] = str(table[new-1])
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile: json.dump(paramcf1, jsonFile)				
			self.syncupdate()
			self.convertsync()
		#print(Sendinfo)

	def convert(self):
		i=0
		j=0
		k=0
		while j<len(Sendinfo):
			Sendinfo[j]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			j+=1
		while i<12:
			if paramcf1["CV-map"][i]["Type"]=="PITCH" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][1]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][2]=CVinfo[i][1]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][7]=CVinfo[i][2]
				if paramcf1["CV-map"][i]["Voltage"]=="[ 0V ; 10V ]":
					Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=5

			if paramcf1["CV-map"][i]["Type"]=="GATE" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][3]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][4]=CVinfo[i][1]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][8]=CVinfo[i][2]


			if paramcf1["CV-map"][i]["Type"]=="LFO" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][9]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][10]=CVinfo[i][1]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][11]=CVinfo[i][2]

			if paramcf1["CV-map"][i]["Type"]=="ADSR" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][12]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][13]=CVinfo[i][1]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][14]=CVinfo[i][2]

				
			i+=1

		while k<len(Sendinfo):
			Sendinfo[k][0]=int(paramcf1["midi-map"][k]["channel"])
			if paramcf1["midi-map"][k]["port"]=="USB": Sendinfo[k][6]=1
			if paramcf1["midi-map"][k]["port"]=="DIN": Sendinfo[k][6]=2
			k+=1
		if start==1:
			q4.put(Sendinfo)
			r1.put(Sendinfo)
			s1.put(Sendinfo)			
		return Sendinfo

	def convertsync(self):
		table=["/48","/24","/16","/8","/4","/2","1","2","4","8","16","24","32","48","64","96"]
		#pulse per quarter note => x4 = pulses per note => xBPM= pulses per minutes
		#tableinv=[1/720,1/360,1/240,1/120,1/60,2/60,4/60,8/60,16/60,32/60,64/60,96/60,128/60,192/60,256/60,384/60]
		tableinv=[0.00138888,0.00277777,0.00416666,0.00833333,0.01666666,0.03333333,0.06666666,0.13333333,0.26666666,0.53333333,1.06666666,1.6,2.13333333,3.2,4.26666666,6.4]
		if paramcf1['sync'][0]["midi-din"]=="on": Syncinfo[0]=1
		else: Syncinfo[0]=0
		if paramcf1['sync'][1]["midi-usb"]=="on": Syncinfo[1]=1
		else: Syncinfo[1]=0
		for i,elem in enumerate(table):
			if paramcf1['sync'][2]["ppq"]==str(elem): Syncinfo[2]=tableinv[i]
		if paramcf1['sync'][3]["BPMmult"]=="1": Syncinfo[3]=1
		else: Syncinfo[3]=2
		if paramcf1['sync'][4]["USBstate"]=="in": Syncinfo[4]=1
		else: Syncinfo[4]=0			
		#print(Syncinfo)
		if start==1:
			q5.put(Syncinfo)
			r3.put(Syncinfo)
			s3.put(Syncinfo)					
		return Syncinfo

	def MIDIsync(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100001.text=='Off':
					print ("on")
					self.b100001.text='On'
					paramcf1["sync"][0]["midi-din"] = "on"
				else:
					print("off")
					self.b100001.text='Off'
					paramcf1["sync"][0]["midi-din"] = "off"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100001.text=='Off':
					print ("on")
					self.b100001.text='On'
					paramcf1["sync"][0]["midi-din"] = "on"
				else:
					print("off")
					self.b100001.text='Off'
					paramcf1["sync"][0]["midi-din"] = "off"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()

	def USBsync(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100002.text=='Off':
					self.b100002.text='On'
					print ("on")
					paramcf1["sync"][1]["midi-usb"] = "on"
				else:
					print("off")
					self.b100002.text='Off'
					paramcf1["sync"][1]["midi-usb"] = "off"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100002.text=='Off':
					self.b100002.text='On'
					print ("on")
					paramcf1["sync"][1]["midi-usb"] = "on"
				else:
					print("off")
					self.b100002.text='Off'
					paramcf1["sync"][1]["midi-usb"] = "off"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()


	def DINin(self):
		if self.b100006.text=='Off':
			self.b100006.text='On'
			x1.value=1
		else:
			self.b100006.text='Off'
			x1.value=0
		print(x1.value)

	def SyncIn(self):
		if self.b100007.text=='Off':
			self.b100007.text='USB'
			y1.value=1

		elif self.b100007.text=='USB':
			self.b100007.text='DIN'
			y1.value=2
		else:
			self.b100007.text='Off'
			y1.value=0

	def BPMmult(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100004.text=='24':
					self.b100004.text='48'
					print ("x2")
					paramcf1["sync"][3]["BPMmult"] = "2"
				else:
					print("x1")
					self.b100004.text='24'
					paramcf1["sync"][3]["BPMmult"] = "1"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100004.text=='24':
					self.b100004.text='48'
					print ("x2")
					paramcf1["sync"][3]["BPMmult"] = "2"
				else:
					print("x1")
					self.b100004.text='24'
					paramcf1["sync"][3]["BPMmult"] = "1"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()

	def USBstate(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100005.text=='In':
					self.b100005.text='Out'
					print ("out")
					paramcf1["sync"][4]["USBstate"] = "out"
				else:
					print("in")
					self.b100005.text='In'
					paramcf1["sync"][4]["USBstate"] = "in"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100005.text=='In':
					self.b100005.text='Out'
					print ("out")
					paramcf1["sync"][4]["USBstate"] = "out"
				else:
					print("in")
					self.b100005.text='In'
					paramcf1["sync"][4]["USBstate"] = "in"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()				

	def closemenu(self):
		self.b4000.pos=1328,1120
		self.b4001.pos=1329,1121
		self.b4002.pos=1329,1182
		self.b4003.pos=1329,1243
		self.b5017.pos=1329,305
		self.b5000.pos=1228,61
		self.b5001.pos=1229,245
		self.b5005.pos=1229,184
		self.b5009.pos=1229,123
		self.b5013.pos=1229,62
		self.b5002.pos=1329,245
		self.b5006.pos=1329,184
		self.b5010.pos=1329,123
		self.b5014.pos=1329,62
		self.b5003.pos=1429,245
		self.b5007.pos=1429,184
		self.b5011.pos=1429,123
		self.b5015.pos=1429,62
		self.b5004.pos=1529,245
		self.b5008.pos=1529,184
		self.b5012.pos=1529,123
		self.b5016.pos=1529,62
		self.b3005.pos=1000,0
		self.clear()

	def clearStep(self,button):
		button.state="normal"


	def clear(self):
		for val in list(self.ids.items()):
			if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'): pass
			else: self.clearStep(val[1])

	def scrollDownMIDI(self):
		global rangeMidi
		if rangeMidi <  10:
			self.b2001.text = paramcf1['midi-map'][rangeMidi + 1]["channel"]
			self.b2002.text = paramcf1['midi-map'][rangeMidi + 2]["channel"]
			self.b2003.text = paramcf1['midi-map'][rangeMidi + 3]["channel"]
			self.b2004.text = paramcf1['midi-map'][rangeMidi + 4]["channel"]
			self.b2005.text = paramcf1['midi-map'][rangeMidi + 5]["channel"]
			self.b2006.text = paramcf1['midi-map'][rangeMidi + 6]["channel"]
			self.b1001.text = paramcf1['midi-map'][rangeMidi + 1]["port"]
			self.b1002.text = paramcf1['midi-map'][rangeMidi + 2]["port"]
			self.b1003.text = paramcf1['midi-map'][rangeMidi + 3]["port"]
			self.b1004.text = paramcf1['midi-map'][rangeMidi + 4]["port"]
			self.b1005.text = paramcf1['midi-map'][rangeMidi + 5]["port"]
			self.b1006.text = paramcf1['midi-map'][rangeMidi + 6]["port"]
			self.lbl1.text = 'Track' + str(rangeMidi + 2)+':'
			self.lbl2.text = 'Track' + str(rangeMidi + 3)+':'
			self.lbl3.text = 'Track' + str(rangeMidi + 4)+':'
			self.lbl4.text = 'Track' + str(rangeMidi + 5)+':'
			self.lbl5.text = 'Track' + str(rangeMidi + 6)+':'
			self.lbl6.text = 'Track' + str(rangeMidi + 7)+':'
			rangeMidi+= 1

	def scrollUpMIDI(self):
		global rangeMidi
		if rangeMidi >  0:
			self.b2001.text = paramcf1['midi-map'][rangeMidi - 1]["channel"]
			self.b2002.text = paramcf1['midi-map'][rangeMidi]["channel"]
			self.b2003.text = paramcf1['midi-map'][rangeMidi + 1]["channel"]
			self.b2004.text = paramcf1['midi-map'][rangeMidi + 2]["channel"]
			self.b2005.text = paramcf1['midi-map'][rangeMidi + 3]["channel"]
			self.b2006.text = paramcf1['midi-map'][rangeMidi + 4]["channel"]
			self.b1001.text = paramcf1['midi-map'][rangeMidi - 1]["port"]
			self.b1002.text = paramcf1['midi-map'][rangeMidi]["port"]
			self.b1003.text = paramcf1['midi-map'][rangeMidi + 1]["port"]
			self.b1004.text = paramcf1['midi-map'][rangeMidi + 2]["port"]
			self.b1005.text = paramcf1['midi-map'][rangeMidi + 3]["port"]
			self.b1006.text = paramcf1['midi-map'][rangeMidi + 4]["port"]
			self.lbl1.text = 'Track' + str(rangeMidi)+':'
			self.lbl2.text = 'Track' + str(rangeMidi + 1)+':'
			self.lbl3.text = 'Track' + str(rangeMidi + 2)+':'
			self.lbl4.text = 'Track' + str(rangeMidi + 3)+':'
			self.lbl5.text = 'Track' + str(rangeMidi + 4)+':'
			self.lbl6.text = 'Track' + str(rangeMidi + 5)+':'
			rangeMidi-= 1


	def scrollDownCV(self):
		global rangeCV
		if rangeCV <  6:
			self.b20001.text = paramcf1['CV-map'][rangeCV + 1]["Track"]
			self.b20002.text = paramcf1['CV-map'][rangeCV + 2]["Track"]
			self.b20003.text = paramcf1['CV-map'][rangeCV + 3]["Track"]
			self.b20004.text = paramcf1['CV-map'][rangeCV + 4]["Track"]
			self.b20005.text = paramcf1['CV-map'][rangeCV + 5]["Track"]
			self.b20006.text = paramcf1['CV-map'][rangeCV + 6]["Track"]
			self.b10001.text = paramcf1['CV-map'][rangeCV + 1]["Type"]
			self.b10002.text = paramcf1['CV-map'][rangeCV + 2]["Type"]
			self.b10003.text = paramcf1['CV-map'][rangeCV + 3]["Type"]
			self.b10004.text = paramcf1['CV-map'][rangeCV + 4]["Type"]
			self.b10005.text = paramcf1['CV-map'][rangeCV + 5]["Type"]
			self.b10006.text = paramcf1['CV-map'][rangeCV + 6]["Type"]
			self.b30001.text = paramcf1['CV-map'][rangeCV + 1]["Voltage"]
			self.b30002.text = paramcf1['CV-map'][rangeCV + 2]["Voltage"]
			self.b30003.text = paramcf1['CV-map'][rangeCV + 3]["Voltage"]
			self.b30004.text = paramcf1['CV-map'][rangeCV + 4]["Voltage"]
			self.b30005.text = paramcf1['CV-map'][rangeCV + 5]["Voltage"]
			self.b30006.text = paramcf1['CV-map'][rangeCV + 6]["Voltage"]
			self.lbl10.text = 'CV' + str(rangeCV + 2)+':'
			self.lbl20.text = 'CV' + str(rangeCV + 3)+':'
			self.lbl30.text = 'CV' + str(rangeCV + 4)+':'
			self.lbl40.text = 'CV' + str(rangeCV + 5)+':'
			self.lbl50.text = 'CV' + str(rangeCV + 6)+':'
			self.lbl60.text = 'CV' + str(rangeCV + 7)+':'
			rangeCV+= 1
		self.VoltageHide()

	def scrollUpCV(self):
		global rangeCV
		if rangeCV >  0:
			self.b20001.text = paramcf1['CV-map'][rangeCV - 1]["Track"]
			self.b20002.text = paramcf1['CV-map'][rangeCV]["Track"]
			self.b20003.text = paramcf1['CV-map'][rangeCV + 1]["Track"]
			self.b20004.text = paramcf1['CV-map'][rangeCV + 2]["Track"]
			self.b20005.text = paramcf1['CV-map'][rangeCV + 3]["Track"]
			self.b20006.text = paramcf1['CV-map'][rangeCV + 4]["Track"]
			self.b10001.text = paramcf1['CV-map'][rangeCV - 1]["Type"]
			self.b10002.text = paramcf1['CV-map'][rangeCV]["Type"]
			self.b10003.text = paramcf1['CV-map'][rangeCV + 1]["Type"]
			self.b10004.text = paramcf1['CV-map'][rangeCV + 2]["Type"]
			self.b10005.text = paramcf1['CV-map'][rangeCV + 3]["Type"]
			self.b10006.text = paramcf1['CV-map'][rangeCV + 4]["Type"]
			self.b30001.text = paramcf1['CV-map'][rangeCV - 1]["Voltage"]
			self.b30002.text = paramcf1['CV-map'][rangeCV]["Voltage"]
			self.b30003.text = paramcf1['CV-map'][rangeCV + 1]["Voltage"]
			self.b30004.text = paramcf1['CV-map'][rangeCV + 2]["Voltage"]
			self.b30005.text = paramcf1['CV-map'][rangeCV + 3]["Voltage"]
			self.b30006.text = paramcf1['CV-map'][rangeCV + 4]["Voltage"]
			self.lbl10.text = 'CV' + str(rangeCV)+':'
			self.lbl20.text = 'CV' + str(rangeCV + 1)+':'
			self.lbl30.text = 'CV' + str(rangeCV + 2)+':'
			self.lbl40.text = 'CV' + str(rangeCV + 3)+':'
			self.lbl50.text = 'CV' + str(rangeCV + 4)+':'
			self.lbl60.text = 'CV' + str(rangeCV + 5)+':'
			rangeCV-= 1
		self.VoltageHide()

	def scrollDownCVTrack(self):
		global rangeCVTrack
		if rangeCVTrack <  83:
			self.b5001.text=str(rangeCVTrack+1)
			self.b5005.text=str(rangeCVTrack+5)
			self.b5009.text=str(rangeCVTrack+9)
			self.b5013.text=str(rangeCVTrack+13)
			self.b5002.text=str(rangeCVTrack+2)
			self.b5006.text=str(rangeCVTrack+6)
			self.b5010.text=str(rangeCVTrack+10)
			self.b5014.text=str(rangeCVTrack+14)
			self.b5003.text=str(rangeCVTrack+3)
			self.b5007.text=str(rangeCVTrack+7)
			self.b5011.text=str(rangeCVTrack+11)
			self.b5015.text=str(rangeCVTrack+15)
			self.b5004.text=str(rangeCVTrack+4)
			self.b5008.text=str(rangeCVTrack+8)
			self.b5012.text=str(rangeCVTrack+12)
			self.b5016.text=str(rangeCVTrack+16)
			rangeCVTrack+= 1

	def scrollUpCVTrack(self):
		global rangeCVTrack
		if rangeCVTrack >  0:
			self.b5001.text=str(rangeCVTrack-1)
			self.b5005.text=str(rangeCVTrack+3)
			self.b5009.text=str(rangeCVTrack+7)
			self.b5013.text=str(rangeCVTrack+11)
			self.b5002.text=str(rangeCVTrack)
			self.b5006.text=str(rangeCVTrack+4)
			self.b5010.text=str(rangeCVTrack+8)
			self.b5014.text=str(rangeCVTrack+12)
			self.b5003.text=str(rangeCVTrack+1)
			self.b5007.text=str(rangeCVTrack+5)
			self.b5011.text=str(rangeCVTrack+9)
			self.b5015.text=str(rangeCVTrack+13)
			self.b5004.text=str(rangeCVTrack+2)
			self.b5008.text=str(rangeCVTrack+6)
			self.b5012.text=str(rangeCVTrack+10)
			self.b5016.text=str(rangeCVTrack+14)
			rangeCVTrack-= 1

	def kill(self):
		print("poweroff")
		if rpi==1: os.system("sudo poweroff")


	def update(self):
		print("updating.........")
		if rpi==1:
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			#print(location)
			if len(location)<1:
				print('no usb stick detected')
				self.b1000005.pos=320,170
				self.b1000005.text='No USB stick detected'
			else:
				for root, dirs, files in os.walk("/media/pi/"+location):
					if "CFM1update.zip" in files:
						print("Updating.. Do not power off")
						self.b1000005.pos=320,170
						self.b1000005.text="Updating.. Do not power off"
						try:
							os.system("cp /media/pi/"+location+"/CFM1update.zip ~/Desktop2")
							os.system("unzip ~/Desktop2/CFM1update.zip -d ~/Desktop2")
							from distutils.dir_util import copy_tree
							try:
								copy_tree("/home/pi/Desktop2/CFM1update", "/home/pi/Desktop2/UIP")
								os.system('rm /home/pi/Desktop2/CFM1update.zip')
								os.system('rm -rf /home/pi/Desktop2/CFM1update')
								os.system("sudo reboot")
							except: print("copy tree error")
						except: print("error updating")						
						break
					else:
						print("Update file not detected")
						self.b1000005.pos=320,170
						self.b1000005.text="Update file not detected"


	def brightness(self,value):
		command="sudo rpi-backlight -b"
		brightness=str(value*2)
		print((command + " " + brightness))
		if rpi==1: os.system(command + " " + brightness)

	def close(self):
		if rpi==1:
			GPIO.cleanup()
			print("cleaned")			
			os.system('killall python')

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if self.b000000001.current_tab.text=="MIDI": buttonparam=0
		elif self.b000000001.current_tab.text=="CV": buttonparam=1
		if buttonparam==0:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollDownMIDI()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollUpMIDI()
		if buttonparam==1:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollDownCV()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollUpCV()

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule param")


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class SongScreen(Screen):


	def on_enter(self):
		global seqbuttonmodesong
		seqbuttonmodesong=0
		self.mode(4)
		self.b003.text=str(BPM)
		self.loadseq()
		#print(song)
		Clock.schedule_interval(self.listening, 0.002)
		w1.value=0
		self.b004.text=str(loopsizeS/64)
		self.loopbar()
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.movebar, 0.002)
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
			self.movebarenter()
		self.infos()
		if y1.value!=0:self.b0003.pos=185,419
		else:self.b0003.pos=1185,419
		global projectmode
		projectmode=0


	def infos(self):
		listinfo=[self.lbl8,self.lbl7,self.lbl6,self.lbl5,self.lbl4,self.lbl3,self.lbl2,self.lbl1]
		if displayinfo==1:
			for n,elem in enumerate(listinfo):
				if trackmode[n+rangeYs]==1: 
					elem.text="SEQUENCE"
					elem.pos[0]=46
				elif trackmode[n+rangeYs]==2: 
					elem.text="LFO"
					elem.pos[0]=18
				elif trackmode[n+rangeYs]==3: 
					for i,value in enumerate(ADSRtrig):
						if value==n+rangeYs+1:
							elem.text="ADSR, TRIGGERED BY TRACK: " + str(i+1)
							if i+1>9:elem.pos[0]=132
							else:elem.pos[0]=128
							break
						else:
							elem.text="ADSR, NO TRIGGER"
							elem.pos[0]=79
				elif trackmode[n+rangeYs]==4: 
					elem.text="RANDOM"
					elem.pos[0]=38
				elif trackmode[n+rangeYs]==5: 
					elem.text="EUCLIDEAN"
					elem.pos[0]=48				
		else:
			for n,elem in enumerate(listinfo):
				elem.pos[0]=1000

	def displayinfo(self):
		global displayinfo
		if displayinfo==0:
			displayinfo=1
			self.b0140.text="INFOS: ON"
		else:
			displayinfo=0
			self.b0140.text="INFOS: OFF"
		self.infos()




	def menu(self):
		if self.b007.state=="down":
			#self.b008.pos= 648,360
			self.b009.pos= 648,360
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b0140.pos= 344,900			
			self.b019.pos=1300,1120
			self.b020.pos=1301,1121
			self.b021.pos=1301,1182
			self.b022.pos=1301,1243
			self.b0222.pos=1301,1243
			self.b0223.pos=1301,1243
			self.b0224.pos=1301,1243
			self.b0225.pos=1301,1243			
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b800.state="normal"
			self.b700.state="normal"
			self.b600.state="normal"
			self.b500.state="normal"
			self.b400.state="normal"
			self.b300.state="normal"
			self.b200.state="normal"
			self.b100.state="normal"
		else:
			#self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0

	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,301
			self.b012.pos= 496,360
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b0140.pos= 344,900			
			self.b019.pos=1300,1120
			self.b020.pos=1301,1121
			self.b021.pos=1301,1182
			self.b022.pos=1301,1243
			self.b0222.pos=1301,1243
			self.b0223.pos=1301,1243
			self.b0224.pos=1301,1243
			self.b0225.pos=1301,1243			
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b800.state="normal"
			self.b700.state="normal"
			self.b600.state="normal"
			self.b500.state="normal"
			self.b400.state="normal"
			self.b300.state="normal"
			self.b200.state="normal"
			self.b100.state="normal"
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0

	def file(self):
		if self.b005.state=="down":
			self.b013.pos= 344,301
			self.b014.pos= 344,360
			self.b0140.pos= 344,242		
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b019.pos=1300,1120
			self.b020.pos=1301,1121
			self.b021.pos=1301,1182
			self.b022.pos=1301,1243
			self.b0222.pos=1301,1243
			self.b0223.pos=1301,1243	
			self.b0224.pos=1301,1243
			self.b0225.pos=1301,1243					
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
			self.b800.state="normal"
			self.b700.state="normal"
			self.b600.state="normal"
			self.b500.state="normal"
			self.b400.state="normal"
			self.b300.state="normal"
			self.b200.state="normal"
			self.b100.state="normal"
		else:
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b0140.pos= 344,900			
			self.b010.pos= 1000,0

	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.file()
		self.b019.pos=1300,1120
		self.b020.pos=1301,1121
		self.b021.pos=1301,1182
		self.b022.pos=1301,1243
		self.b0222.pos=1301,1243
		self.b0223.pos=1301,1243	
		self.b0224.pos=1301,1243
		self.b0225.pos=1301,1243			
		self.b010.pos= 1000,0
		self.b800.state="normal"
		self.b700.state="normal"
		self.b600.state="normal"
		self.b500.state="normal"
		self.b400.state="normal"
		self.b300.state="normal"
		self.b200.state="normal"
		self.b100.state="normal"

	def start(self):
		global playing
		if self.b001.state=="down":
			self.b001.text="%s"%(icon('icon-pause', 22))
			playing=1
			v1.value=1
			Clock.schedule_interval(self.movebar, 0.002)
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2
			Clock.unschedule(self.movebar)

	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		Clock.unschedule(self.movebar)
		position=0
		self.b015.pos=50,0
		playing=0
		v1.value=0


	def moveXrgh(self):
		global rangeXs
		if (rangeXs+16)*4<=1021:
			self.b901.text=str((rangeXs+1)*4+1)
			self.b902.text=str((rangeXs+2)*4+1)
			self.b903.text=str((rangeXs+3)*4+1)
			self.b904.text=str((rangeXs+4)*4+1)
			self.b905.text=str((rangeXs+5)*4+1)
			self.b906.text=str((rangeXs+6)*4+1)
			self.b907.text=str((rangeXs+7)*4+1)
			self.b908.text=str((rangeXs+8)*4+1)
			self.b909.text=str((rangeXs+9)*4+1)
			self.b910.text=str((rangeXs+10)*4+1)
			self.b911.text=str((rangeXs+11)*4+1)
			self.b912.text=str((rangeXs+12)*4+1)
			self.b913.text=str((rangeXs+13)*4+1)
			self.b914.text=str((rangeXs+14)*4+1)
			self.b915.text=str((rangeXs+15)*4+1)
			self.b916.text=str((rangeXs+16)*4+1)
			rangeXs=rangeXs+1
			print(rangeXs)
		self.loadseq()

	def moveXlft(self):
		global rangeXs
		if rangeXs>=1:
			self.b901.text=str((rangeXs-1)*4+1)
			self.b902.text=str((rangeXs)*4+1)
			self.b903.text=str((rangeXs+1)*4+1)
			self.b904.text=str((rangeXs+2)*4+1)
			self.b905.text=str((rangeXs+3)*4+1)
			self.b906.text=str((rangeXs+4)*4+1)
			self.b907.text=str((rangeXs+5)*4+1)
			self.b908.text=str((rangeXs+6)*4+1)
			self.b909.text=str((rangeXs+7)*4+1)
			self.b910.text=str((rangeXs+8)*4+1)
			self.b911.text=str((rangeXs+9)*4+1)
			self.b912.text=str((rangeXs+10)*4+1)
			self.b913.text=str((rangeXs+11)*4+1)
			self.b914.text=str((rangeXs+12)*4+1)
			self.b915.text=str((rangeXs+13)*4+1)
			self.b916.text=str((rangeXs+14)*4+1)
			rangeXs=rangeXs-1
		self.loadseq()

	def moveYup(self):
		global rangeYs
		if rangeYs<=7:
			self.b100.text=str(rangeYs+9)
			self.b200.text=str(rangeYs+8)
			self.b300.text=str(rangeYs+7)
			self.b400.text=str(rangeYs+6)
			self.b500.text=str(rangeYs+5)
			self.b600.text=str(rangeYs+4)
			self.b700.text=str(rangeYs+3)
			self.b800.text=str(rangeYs+2)
			rangeYs=rangeYs+1
		self.loadseq()
		self.infos()

	def moveYdw(self):
		global rangeYs
		if rangeYs>=1:
			self.b100.text=str(rangeYs+7)
			self.b200.text=str(rangeYs+6)
			self.b300.text=str(rangeYs+5)
			self.b400.text=str(rangeYs+4)
			self.b500.text=str(rangeYs+3)
			self.b600.text=str(rangeYs+2)
			self.b700.text=str(rangeYs+1)
			self.b800.text=str(rangeYs)
			rangeYs=rangeYs-1
		self.loadseq()
		self.infos()

	def loadseq(self):
		self.clear()
		i=0
		#print('looading song',song)
		while i <16:
			for elem in song[rangeXs+i]:
				elemY=elem-rangeYs
				elemX=i+1
				if elemY <=8:
					elemY=-(int(elemY)-9)
					if elemX<10: b="b"+str(elemY)+"0"+str(elemX)
					else: b="b"+str(elemY)+str(elemX)
					self.findButton(b)
			i+=1
		self.loopbar()
		self.movebar()


	def findButton(self,button):
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.state="down"



	def loopbar(self):
		loopbar_pos=v3.value/16
		if loopbar_pos<=(rangeXs+16)*4:
			if 48+(loopbar_pos/4-rangeXs)*47>=5: self.b017.pos=48+(loopbar_pos/4-rangeXs)*47,0
			else: self.b017.pos=1000,1000
		else: self.b017.pos=1000,1000

	def movebarenter(self):
		countbar=v2.value%loopsizeS
		speed=47.1/64
		position=int(50+round((countbar-rangeX*64)*speed))
		position=(position/12)*12
		if position<50: self.b015.pos=1000,0
		else: self.b015.pos=position,0


	def movebar(self, *args):
		countbar=v2.value%loopsizeS
		speed=47.1/64
		position=int(50+round((countbar-rangeXs*64)*speed))
		if v2.value%16==0:
			if position<50: self.b015.pos=1000,0
			else: self.b015.pos=position,0


	def clearStep(self,button):
		button.state="normal"


	def clear(self):
		for val in list(self.ids.items()):
			if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'): pass
			else: self.clearStep(val[1])

	def monitor(self, button):
		global song
		global buttonpushedsong
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		y=int(ID[1])
		yp=-(y-8)
		x=int(ID[-2:])
		buttonpushedsong=ID
		if button.state=="normal":
			song[x+rangeXs-1].remove(yp+rangeYs+1)
		else:
			song[x+rangeXs-1].append(yp+rangeYs+1)
			song[x+rangeXs-1]=sorted(song[x+rangeXs-1])
		q3.put(song)


	def trackmenu(self,button):
		global trackselected
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		trackselected=-(int(ID[1])-9)+rangeYs
		r2.put(trackselected)
		s2.put(trackselected)		
		v5.value=trackselected
		self.b010.pos=0,0	
		self.b019.pos=300,120
		self.b020.pos=301,121
		self.b021.pos=301,182				
		if trackmode[trackselected-1]==1:
			self.b022.pos=301,243
		elif trackmode[trackselected-1]==2:
			self.b0222.pos=301,243
		elif trackmode[trackselected-1]==3:
			self.b0223.pos=301,243
		elif trackmode[trackselected-1]==4:
			self.b0224.pos=301,243
		elif trackmode[trackselected-1]==5:
			self.b0225.pos=301,243

	def cleartrack(self):
		global song
		for elem in song:
			if trackselected in elem: elem.remove(trackselected)
		q3.put(song)
		self.loadseq()


	def on_touch_move(self, touch):
		global buttonpushedsong
		if self.collide_point(*touch.pos):
			x=touch.pos[0]-50
			y=touch.pos[1]
			bx=int(x/47+1)
			by=int(y/47+1)
			byc=8-by
			if (bx>int(buttonpushedsong[-2:]) and by==int(buttonpushedsong[1])):
				if bx<=9: b="b"+str(by)+"0"+str(bx)
				else: b="b"+str(by)+str(bx)
				for val in list(self.ids.items()):
					if val[0]==b:
						if val[1].state=='normal':
							val[1].state='down'
							song[bx+rangeXs-1].append(byc+rangeYs+1)
							song[bx+rangeXs-1]=sorted(song[bx+rangeXs-1])
		q3.put(song)

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule song")


	def mode(self,num):
		global seqbuttonmodesong
		if num==2:
			if seqbuttonmodesong==2:
				seqbuttonmodesong=0
				self.b003.state='normal'
			else:
				seqbuttonmodesong=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if seqbuttonmodesong==3:
				seqbuttonmodesong=0
				self.b004.state='normal'
			else:
				seqbuttonmodesong=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			seqbuttonmodesong=0
			self.b003.state='normal'
			self.b004.state='normal'
		print("button mode",seqbuttonmodesong)

	def listening(self,*args):
		global wheel
		global seqbuttonmodesong
		global loopsizeS
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if seqbuttonmodesong==0:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1: self.moveXrgh()
					else: self.moveYup()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1: self.moveXlft()
					else: self.moveYdw()

		if seqbuttonmodesong==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				seqbuttonmodesong=0
				self.b003.state='normal'

		if seqbuttonmodesong==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS<256*64:
						loopsizeS+=64
						v3.value=loopsizeS
						self.b004.text=str(loopsizeS/64)
						self.loopbar()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS>64:
						loopsizeS-=64
						v3.value=loopsizeS
						self.b004.text=str(loopsizeS/64)
						self.loopbar()
			if encoderpushed==1:
				seqbuttonmodesong=0
				self.b004.state='normal'
		global playing
		if v1.value==1 and playing==0:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			Clock.schedule_interval(self.movebar, 0.002)
		elif v1.value==0 and playing==1:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2	
			Clock.unschedule(self.movebar)	
			self.b015.pos=50,0				


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class SeqScreen(Screen):


	def on_enter(self):
		global start
		global rangeY
		global rangeX
		global zoom
		global trackmode
		global seqbuttonmode
		seqbuttonmode=0
		if trackmode[trackselected-1]!=1:clearsequence()
		trackmode[trackselected-1]=1
		print('trackmode',trackmode[trackselected-1])
		print('trackselected',trackselected)
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		#self.deleteADSR()
		#self.deleteLFO()
		deleteLFO()
		deleteADSR()

		
		if start > 0:
			self.mode(4)
			rangeY=36
			rangeX=0
			zoom=4
			self.LoopSdisplay()
			self.b003.text=str(BPM)
			self.loadseq()
			self.b901.text=timerange[rangeX]
			self.b902.text=timerange[rangeX+1*(zoom)]
			self.b903.text=timerange[rangeX+2*(zoom)]
			self.b904.text=timerange[rangeX+3*(zoom)]
			self.b905.text=timerange[rangeX+4*(zoom)]
			self.b906.text=timerange[rangeX+5*(zoom)]
			self.b907.text=timerange[rangeX+6*(zoom)]
			self.b908.text=timerange[rangeX+7*(zoom)]
			self.b909.text=timerange[rangeX+8*(zoom)]
			self.b910.text=timerange[rangeX+9*(zoom)]
			self.b911.text=timerange[rangeX+10*(zoom)]
			self.b912.text=timerange[rangeX+11*(zoom)]
			self.b913.text=timerange[rangeX+12*(zoom)]
			self.b914.text=timerange[rangeX+13*(zoom)]
			self.b915.text=timerange[rangeX+14*(zoom)]
			self.b916.text=timerange[rangeX+15*(zoom)]
			self.b100.text=keyrange[rangeY][0]
			self.b200.text=keyrange[rangeY+1][0]
			self.b300.text=keyrange[rangeY+2][0]
			self.b400.text=keyrange[rangeY+3][0]
			self.b500.text=keyrange[rangeY+4][0]
			self.b600.text=keyrange[rangeY+5][0]
			self.b700.text=keyrange[rangeY+6][0]
			self.b800.text=keyrange[rangeY+7][0]
			if keyrange[rangeY][1]==0:
				self.b100.background_color= (0,0,0,0.7)
				self.b100.color= 1,1,1,1
			else:
				self.b100.background_color= 255,255,255,0.8
				self.b100.color= 0,0,0,1
			if keyrange[rangeY+1][1]==0:
				self.b200.background_color= (0,0,0,0.7)
				self.b200.color= 1,1,1,1
			else:
				self.b200.background_color= 255,255,255,0.8
				self.b200.color= 0,0,0,1
			if keyrange[rangeY+2][1]==0:
				self.b300.background_color= (0,0,0,0.7)
				self.b300.color= 1,1,1,1
			else:
				self.b300.background_color= 255,255,255,0.8
				self.b300.color= 0,0,0,1
			if keyrange[rangeY+3][1]==0:
				self.b400.background_color= (0,0,0,0.7)
				self.b400.color= 1,1,1,1
			else:
				self.b400.background_color= 255,255,255,0.8
				self.b400.color= 0,0,0,1
			if keyrange[rangeY+4][1]==0:
				self.b500.background_color= (0,0,0,0.7)
				self.b500.color= 1,1,1,1
			else:
				self.b500.background_color= 255,255,255,0.8
				self.b500.color= 0,0,0,1
			if keyrange[rangeY+5][1]==0:
				self.b600.background_color= (0,0,0,0.7)
				self.b600.color= 1,1,1,1
			else:
				self.b600.background_color= 255,255,255,0.8
				self.b600.color= 0,0,0,1
			if keyrange[rangeY+6][1]==0:
				self.b700.background_color= (0,0,0,0.7)
				self.b700.color= 1,1,1,1
			else:
				self.b700.background_color= 255,255,255,0.8
				self.b700.color= 0,0,0,1
			if keyrange[rangeY+7][1]==0:
				self.b800.background_color= (0,0,0,0.7)
				self.b800.color= 1,1,1,1
			else:
				self.b800.background_color= 255,255,255,0.8
				self.b800.color= 0,0,0,1			
			if playing==1:
				self.b001.state="down"
				self.b001.text="%s"%(icon('icon-pause', 22))
				Clock.schedule_interval(self.movebar, 0.002)
			else:
				self.b001.state="normal"
				self.b001.text="%s"%(icon('icon-play', 22))
				self.movebarenter()
			self.b006.text=str(trackselected)+ ": SEQUENCE"
			if y1.value!=0:self.b0003.pos=185,419
			else:self.b0003.pos=1185,419
		else: start = start +1

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")

	def monitor(self, button):
		global sequencepool2
		global sequencepool3
		global buttonpushed
		global xseq
		global yseq
		for key, val in list(self.ids.items()):
			if val==button: ID=key
		yseq=int(ID[1])
		xseq=int(ID[-2:])
		buttonpushed=ID

		if button.state=="normal":
			print(("x",(xseq-1)*zoom+rangeX+1))
			print(("y",yseq+rangeY-1))
			for elem in sequencepool2[trackselected-1]:
				if elem[0]==(xseq-1)*zoom+rangeX+1 and elem[1]==yseq+rangeY-1 and elem[2]==1:
					duration=elem[3]
					break
			try:
				sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration])
				sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+duration,yseq+rangeY-1,0,duration])
			except:
				print("******* Note 2 error ********")
			for elem in sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]:
				if sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX][0]==yseq+rangeY-1:
					duration=elem[2]
					break
			try:
				sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].remove([yseq+rangeY-1,1,duration])
				sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration].remove([yseq+rangeY-1,0,duration])
			except: print("******* Note 3 error ********")
			self.loadseq()
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])

		if button.background_color==[0.3, 0.7, 1, 1]:
			i=0
			for elem in sequencepool2[trackselected-1]:
				if elem[1]==yseq+rangeY-1 and elem[2]==1: result=i
				if elem[0]>(xseq-1)*zoom+rangeX+1: break
				i+=1
			try:
				i=result
				removed=sequencepool2[trackselected-1][i]
				sequencepool2[trackselected-1].remove(removed)
				removed[0]=removed[0]+removed[3]
				removed[2]=0
				sequencepool2[trackselected-1].remove(removed)
			except: print("******* Chords 2 error ********")


			j=0
			for elem in sequencepool3[trackselected-1]:
				if len(elem)>0:
					if j > (xseq-1)*zoom+rangeX+1: break					
					for elem2 in elem:
						if elem2[0]==yseq+rangeY-1 and elem2[1]==1: result2=j
				j+=1
			try:	
				for elem in sequencepool3[trackselected-1][result2]:
					if elem[0]==yseq+rangeY-1 and elem[1]==1:
						duration=elem[2]
						break
			except: print("******* Chords 3 error ********")
			try:
				sequencepool3[trackselected-1][result2].remove([yseq+rangeY-1,1,duration])
				sequencepool3[trackselected-1][result2+duration].remove([yseq+rangeY-1,0,duration])
			except: print("******* Chords 3 error ********")
			#print(sequencepool3[trackselected-1])
			self.loadseq()
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])


		if button.state=="down":
			sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
			sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
			sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom].append([yseq+rangeY-1,0,zoom])
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom],key=operator.itemgetter(1,0))
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].append([yseq+rangeY-1,1,zoom])
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX],key=operator.itemgetter(1,0))
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])



	def clearsequence(self):
		global sequencepool2
		global sequencepool3
		sequencepool2[trackselected-1]=[]
		for i,elem in enumerate(sequencepool3[trackselected-1]): sequencepool3[trackselected-1][i]=[]
		q1.put(sequencepool2)
		q6.put(sequencepool3[trackselected-1])
		print((sequencepool3[trackselected-1]))


	def clearStep(self,button):
		button.state="normal"


	def clear(self):
		for val in list(self.ids.items()):
			if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004' or val[0]=='b020'):pass
			else:
				if int(val[0][1])>0 and int(val[0][1])<9 and int(val[0][-2:])>0:
					self.clearStep(val[1])
					val[1].background_color= .68,.68,.84,1
				else: self.clearStep(val[1])

	def zoomstep(self,button,text):
		button.text=text

	def zoom(self):
		global rangeX
		for val in list(self.ids.items()):
			bty=int(val[0][1])
			btx=int(val[0][-2:])
			if bty ==9:
				if rangeX+16*(zoom)<=rangeXmax:
					if rangeX%zoom == 0:
						btn=(btx-1)*zoom+rangeX
						self.zoomstep(val[1],timerange[btn])
					else:
						rangeX = rangeX-(rangeX%zoom)
						btn=(btx-1)*zoom+rangeX
						print("not multiple")
						self.zoomstep(val[1],timerange[btn])
				else:
					rangeX=128*7
					btn=(btx-1)*zoom+rangeX
					print("resized")
					self.zoomstep(val[1],timerange[btn])
		self.loadseq()

	def zoomout(self):
		global zoom
		global rangeX
		if zoom <8:
			zoom = 2*zoom
			self.zoom()

	def zoomin(self):
		global zoom
		global rangeX
		if zoom >1:
			zoom = zoom/2
			self.zoom()

	def moveXrgh(self):
		global rangeX
		if rangeX+16*(zoom)<=rangeXmax:
			self.b901.text=timerange[rangeX+1*(zoom)]
			self.b902.text=timerange[rangeX+2*(zoom)]
			self.b903.text=timerange[rangeX+3*(zoom)]
			self.b904.text=timerange[rangeX+4*(zoom)]
			self.b905.text=timerange[rangeX+5*(zoom)]
			self.b906.text=timerange[rangeX+6*(zoom)]
			self.b907.text=timerange[rangeX+7*(zoom)]
			self.b908.text=timerange[rangeX+8*(zoom)]
			self.b909.text=timerange[rangeX+9*(zoom)]
			self.b910.text=timerange[rangeX+10*(zoom)]
			self.b911.text=timerange[rangeX+11*(zoom)]
			self.b912.text=timerange[rangeX+12*(zoom)]
			self.b913.text=timerange[rangeX+13*(zoom)]
			self.b914.text=timerange[rangeX+14*(zoom)]
			self.b915.text=timerange[rangeX+15*(zoom)]
			self.b916.text=timerange[rangeX+16*(zoom)]
			rangeX=rangeX+zoom
		self.loadseq()

	def moveXlft(self):
		global rangeX
		if rangeX>=1:
			self.b901.text=timerange[rangeX-1*(zoom)]
			self.b902.text=timerange[rangeX]
			self.b903.text=timerange[rangeX+1*(zoom)]
			self.b904.text=timerange[rangeX+2*(zoom)]
			self.b905.text=timerange[rangeX+3*(zoom)]
			self.b906.text=timerange[rangeX+4*(zoom)]
			self.b907.text=timerange[rangeX+5*(zoom)]
			self.b908.text=timerange[rangeX+6*(zoom)]
			self.b909.text=timerange[rangeX+7*(zoom)]
			self.b910.text=timerange[rangeX+8*(zoom)]
			self.b911.text=timerange[rangeX+9*(zoom)]
			self.b912.text=timerange[rangeX+10*(zoom)]
			self.b913.text=timerange[rangeX+11*(zoom)]
			self.b914.text=timerange[rangeX+12*(zoom)]
			self.b915.text=timerange[rangeX+13*(zoom)]
			self.b916.text=timerange[rangeX+14*(zoom)]
			rangeX=rangeX-zoom
		self.loadseq()


	def moveYup(self):
		global rangeY
		if rangeY<=87:
			self.b100.text=keyrange[rangeY+1][0]
			self.b200.text=keyrange[rangeY+2][0]
			self.b300.text=keyrange[rangeY+3][0]
			self.b400.text=keyrange[rangeY+4][0]
			self.b500.text=keyrange[rangeY+5][0]
			self.b600.text=keyrange[rangeY+6][0]
			self.b700.text=keyrange[rangeY+7][0]
			self.b800.text=keyrange[rangeY+8][0]
			if keyrange[rangeY+1][1]==0:
				self.b100.background_color= (0,0,0,0.7)
				self.b100.color= 1,1,1,1
			else:
				self.b100.background_color= 255,255,255,0.8
				self.b100.color= 0,0,0,1
			if keyrange[rangeY+2][1]==0:
				self.b200.background_color= (0,0,0,0.7)
				self.b200.color= 1,1,1,1
			else:
				self.b200.background_color= 255,255,255,0.8
				self.b200.color= 0,0,0,1
			if keyrange[rangeY+3][1]==0:
				self.b300.background_color= (0,0,0,0.7)
				self.b300.color= 1,1,1,1
			else:
				self.b300.background_color= 255,255,255,0.8
				self.b300.color= 0,0,0,1
			if keyrange[rangeY+4][1]==0:
				self.b400.background_color= (0,0,0,0.7)
				self.b400.color= 1,1,1,1
			else:
				self.b400.background_color= 255,255,255,0.8
				self.b400.color= 0,0,0,1
			if keyrange[rangeY+5][1]==0:
				self.b500.background_color= (0,0,0,0.7)
				self.b500.color= 1,1,1,1
			else:
				self.b500.background_color= 255,255,255,0.8
				self.b500.color= 0,0,0,1
			if keyrange[rangeY+6][1]==0:
				self.b600.background_color= (0,0,0,0.7)
				self.b600.color= 1,1,1,1
			else:
				self.b600.background_color= 255,255,255,0.8
				self.b600.color= 0,0,0,1
			if keyrange[rangeY+7][1]==0:
				self.b700.background_color= (0,0,0,0.7)
				self.b700.color= 1,1,1,1
			else:
				self.b700.background_color= 255,255,255,0.8
				self.b700.color= 0,0,0,1
			if keyrange[rangeY+8][1]==0:
				self.b800.background_color= (0,0,0,0.7)
				self.b800.color= 1,1,1,1
			else:
				self.b800.background_color= 255,255,255,0.8
				self.b800.color= 0,0,0,1
			rangeY=rangeY+1
		self.loadseq()

	def moveYdw(self):
		global rangeY
		if rangeY>=1:
			self.b100.text=keyrange[rangeY-1][0]
			self.b200.text=keyrange[rangeY][0]
			self.b300.text=keyrange[rangeY+1][0]
			self.b400.text=keyrange[rangeY+2][0]
			self.b500.text=keyrange[rangeY+3][0]
			self.b600.text=keyrange[rangeY+4][0]
			self.b700.text=keyrange[rangeY+5][0]
			self.b800.text=keyrange[rangeY+6][0]
			if keyrange[rangeY-1][1]==0:
				self.b100.background_color= (0,0,0,0.7)
				self.b100.color= 1,1,1,1
			else:
				self.b100.background_color= 255,255,255,0.8
				self.b100.color= 0,0,0,1
			if keyrange[rangeY][1]==0:
				self.b200.background_color= (0,0,0,0.7)
				self.b200.color= 1,1,1,1
			else:
				self.b200.background_color= 255,255,255,0.8
				self.b200.color= 0,0,0,1
			if keyrange[rangeY+1][1]==0:
				self.b300.background_color= (0,0,0,0.7)
				self.b300.color= 1,1,1,1
			else:
				self.b300.background_color= 255,255,255,0.8
				self.b300.color= 0,0,0,1
			if keyrange[rangeY+2][1]==0:
				self.b400.background_color= (0,0,0,0.7)
				self.b400.color= 1,1,1,1
			else:
				self.b400.background_color= 255,255,255,0.8
				self.b400.color= 0,0,0,1
			if keyrange[rangeY+3][1]==0:
				self.b500.background_color= (0,0,0,0.7)
				self.b500.color= 1,1,1,1
			else:
				self.b500.background_color= 255,255,255,0.8
				self.b500.color= 0,0,0,1
			if keyrange[rangeY+4][1]==0:
				self.b600.background_color= (0,0,0,0.7)
				self.b600.color= 1,1,1,1
			else:
				self.b600.background_color= 255,255,255,0.8
				self.b600.color= 0,0,0,1
			if keyrange[rangeY+5][1]==0:
				self.b700.background_color= (0,0,0,0.7)
				self.b700.color= 1,1,1,1
			else:
				self.b700.background_color= 255,255,255,0.8
				self.b700.color= 0,0,0,1
			if keyrange[rangeY+6][1]==0:
				self.b800.background_color= (0,0,0,0.7)
				self.b800.color= 1,1,1,1
			else:
				self.b800.background_color= 255,255,255,0.8
				self.b800.color= 0,0,0,1
			rangeY=rangeY-1
		self.loadseq()

	def findButton(self,button):
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.state="down"

	def findButtonC(self,button):
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.background_color=[0.3, 0.7, 1, 1]

	def findButtonCi(self,button):
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.state="down"


	def loadseq(self):
		global sequencepool2
		self.clear()
		sequence=sequencepool2[trackselected-1]
		i=1
		while i <= len(sequence):
			if sequence[i-1][2]==1:
				Xc=sequence[i-1][0]-rangeX
				Yc=sequence[i-1][1]-rangeY+1
				j=0
				while j < sequence[i-1][3]:
					if (Xc>=0 and Xc <= 16*zoom and (sequence[i-1][0]-1)%zoom ==0):
						if (Yc >= 1 and Yc <=8):
							Xcp=int(Xc/(zoom+0.0000000000001))+1
							if Xcp<=9: b="b"+str(Yc)+"0"+str(Xcp)
							else: b="b"+str(Yc)+str(Xcp)
							if sequence[i-1][3]>zoom:
								if j==0: self.findButtonCi(b)
								else: self.findButtonC(b)
							else: self.findButton(b)
					Xc+=zoom
					j+=zoom
			i+=1
		self.loopbar()
		self.movebar()



	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b023.pos= 496,900
			self.b024.pos= 496,900
			self.b025.pos= 496,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900			
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b012.pos= 496,301
			self.b023.pos= 496,242
			self.b024.pos= 496,183
			self.b025.pos= 496,124
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900			
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b023.pos= 496,900
			self.b024.pos= 496,900
			self.b025.pos= 496,900
			self.b010.pos= 1000,0

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360
			self.b014.pos= 344,301
			self.b016.pos= 344,242
			self.b020.pos= 344,183
			self.b022.pos= 344,124
			self.b023.pos= 496,900
			self.b024.pos= 496,900	
			self.b025.pos= 496,900					
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
		else:
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900			
			self.b010.pos= 1000,0

	def recordingbut(self):
		global recordingON
		if self.b022.text=='REC OFF':
			self.b022.text='REC ON'
			recordingON=1
		else:
			self.b022.text='REC OFF'
			recordingON=0	
		print(recordingON)		


	def mode(self,num):
		global seqbuttonmode
		if num==1:
			if seqbuttonmode==1:
				seqbuttonmode=0
				self.b020.state='normal'
			else:
				seqbuttonmode=1
				self.b020.state='down'
				w2.value=0
		if num==2:
			if seqbuttonmode==2:
				seqbuttonmode=0
				self.b003.state='normal'
			else:
				seqbuttonmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if seqbuttonmode==3:
				seqbuttonmode=0
				self.b004.state='normal'
			else:
				seqbuttonmode=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			seqbuttonmode=0
			self.b003.state='normal'
			self.b004.state='normal'
			self.b020.state='normal'
		print(("buton mode",seqbuttonmode))



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.movebar, 0.002)
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			Clock.unschedule(self.movebar)
			v1.value=2		

	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		Clock.unschedule(self.movebar)
		v1.value=0
		playing=0
		self.b015.pos=50,0

	def movebarenter(self):
		countbar=v2.value%loopsize[trackselected-1]
		speed=47.1/zoom
		position=int(50+round((countbar-rangeX)*speed))
		position=(position/189)*189+50
		if position<50: self.b015.pos=1000,0
		else: self.b015.pos=position,0


	def movebar(self, *args):
		countbar=v2.value%loopsize[trackselected-1]
		speed=47.1/zoom
		position=int(50+round((countbar-rangeX)*speed))
		if v2.value%16==0:
			if position<50: self.b015.pos=1000,0
			else: self.b015.pos=position,0



	def loopbar(self):
		global loopsize
		loopbar_pos=loopsize[trackselected-1]
		if loopbar_pos<=rangeX+16*zoom:
			if 48+(loopbar_pos-rangeX)/zoom*47>=5: self.b017.pos=48+(loopbar_pos-rangeX)/zoom*47,0
			else: self.b017.pos=1000,1000
		else: self.b017.pos=1000,1000
		self.gridbar()

	def gridbar(self):
		#print(rangeX)
		if (rangeX-3*zoom)%(4*zoom)==0: self.ids.b018.pos = 94,0
		if (rangeX-2*zoom)%(4*zoom)==0: self.ids.b018.pos = 141,0
		if (rangeX-1*zoom)%(4*zoom)==0: self.ids.b018.pos = 188,0
		if rangeX%(4*zoom)==0: self.ids.b018.pos = 235,0

	def on_touch_move(self, touch):
		global buttonpushed
		global sequencepool2
		global erased
		global stoplong
		if self.collide_point(*touch.pos):
			x=touch.pos[0]-50
			y=touch.pos[1]
			bx=int(x/47+1)
			by=int(y/47+1)
			if (bx>int(buttonpushed[-2:]) and by==int(buttonpushed[1])):
				if bx<=9: b="b"+str(by)+"0"+str(bx)
				if bx==10: b="b"+str(by)+"10"
				if bx>10: b="b"+str(by)+str(bx)
				for val in list(self.ids.items()):
					if val[0]==b:
						if val[1].state=='normal'and stoplong==0: val[1].background_color=[0.3, 0.7, 1, 1]
						if val[1].state=='down': stoplong=1
					if val[0]==buttonpushed and erased==0:
						val[1].state=='normal'
						try:
							sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
							sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom].remove([yseq+rangeY-1,0,zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].remove([yseq+rangeY-1,1,zoom])
							erased=1
							q1.put(sequencepool2)
							q6.put(sequencepool3[trackselected-1])							
						except:
							print("************* Touch move remove error ***********")
							erased=0
			if by!=int(buttonpushed[1]):
				stoplong=1


	def on_touch_up(self,touch):
		global buttonpushed
		global erased
		global stoplong
		if self.collide_point(*touch.pos):
			x=touch.pos[0]-50
			y=touch.pos[1]
			bx=int(x/47+1)
			by=int(y/47+1)
			if (bx>int(buttonpushed[-2:]) and by==int(buttonpushed[1]))and stoplong==0:
				if bx<=9: b="b"+str(by)+"0"+str(bx)
				else: b="b"+str(by)+str(bx)
				for val in list(self.ids.items()):
					if val[0]==b and erased==1:
						erased=0
						binit=int(buttonpushed[-2:])
						duration=(bx-binit)+1
						try:
							sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration*zoom])
							sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+duration*zoom,yseq+rangeY-1,0,duration*zoom])
							sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].append([yseq+rangeY-1,1,duration*zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom].append([yseq+rangeY-1,0,duration*zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX], key=operator.itemgetter(1,0))
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom], key=operator.itemgetter(1,0))
							#print(sequencepool3[trackselected-1])
						except:
							print("****************************************")
						q1.put(sequencepool2)
						q6.put(sequencepool3[trackselected-1])
				#self.loadseq()
			if 0<bx<17 and 0<by<9: self.loadseq()
			erased=0
			stoplong=0


	def recording(self):
		while s4.empty() is False:
				noterec=s4.get()
				self.recordingnote(noterec)
		while r4.empty() is False:
				noterec=r4.get()
				self.recordingnote(noterec)
				

	def recordingnote(self,noterec):
		step=v2.value%loopsize[trackselected-1]
		step=step/4 *4
		if recordingON==1:
			if [step+1,noterec-24,1,4] not in sequencepool2[trackselected-1]:
				sequencepool2[trackselected-1].append([step+1,noterec-24,1,4])
				sequencepool2[trackselected-1].append([step+5,noterec-24,0,4])
				sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
				sequencepool3[trackselected-1][step].append([noterec-24,1,4])
				sequencepool3[trackselected-1][step+4].append([noterec-24,0,4])
				sequencepool3[trackselected-1][step]=sorted(sequencepool3[trackselected-1][step], key=operator.itemgetter(1,0))
				sequencepool3[trackselected-1][step+4]=sorted(sequencepool3[trackselected-1][step+4], key=operator.itemgetter(1,0))					
				self.loadseq()
				q1.put(sequencepool2)
				q6.put(sequencepool3[trackselected-1])	

	def listening(self,*args):
		global wheel
		global seqbuttonmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		self.recording()
		if seqbuttonmode==0:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1: self.moveXrgh()
					else: self.moveYup()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1: self.moveXlft()
					else: self.moveYdw()
		if seqbuttonmode==1:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.zoomin()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.zoomout()
			if encoderpushed==1:
				seqbuttonmode=0
				self.b020.state='normal'
				self.closemenus()
		if seqbuttonmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				seqbuttonmode=0
				self.b003.state='normal'
		if seqbuttonmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<64*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)
						self.LoopSdisplay()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>16:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()
			if encoderpushed==1:
				seqbuttonmode=0
				self.b004.state='normal'
		global playing
		if v1.value==1 and playing==0:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			Clock.schedule_interval(self.movebar, 0.002)
		elif v1.value==0 and playing==1:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2	
			Clock.unschedule(self.movebar)	
			self.b015.pos=50,0


	def LoopSdisplay(self):
		a,b=divmod(loopsize[trackselected-1],16)
		b=b/4
		#self.b004.text=str(a) + "." +str(b)
		self.b004.text=str(a)
		self.loopbar()

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

class SaveSeq(Screen):

	def on_enter(self):
		global rangeFile
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)		
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		print(chosen)
		if self.b001.state=="down":
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedseq.json', "w") as s:
					saved["savedseq"][chosen+rangeFile*4-1]["sequence"] = sequencepool2[trackselected-1]
					json.dump(saved, s)
			else:
				with open('savedseq.json', "w") as s:
					saved["savedseq"][chosen+rangeFile*4-1]["sequence"] = sequencepool2[trackselected-1]
					json.dump(saved, s)	
		else:
			from midi import MIDIFile
			track    = 0
			channel  = 0
			time     = 0
			tempo    = 120
			volume   = 100
			MyMIDI = MIDIFile(1)
			MyMIDI.addTempo(track, time, tempo)			
			for elem in sequencepool2[trackselected-1]:
				if elem[2]==1: MyMIDI.addNote(track, channel, elem[1]+24, Decimal(elem[0]-1)/16, Decimal(elem[3])/16, volume)
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
			try:
				with open(filetext, "wb") as output_file:
					MyMIDI.writeFile(output_file)
			except: print("error usb")
		self.leaving()


	def up(self):
		global rangeFile
		if rangeFile<21:
			rangeFile+=1
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1		
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		if rpi==1:self.usbcheck()

	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="EXPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="EXPORT"

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule SaveSeq")

class LoadSeq(Screen):

	def on_enter(self):
		global rangeFile
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)		
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		print(chosen)
		if self.b001.state=="down":
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedseq.json') as s:
					saved = json.load(s)
					print((saved["savedseq"][chosen+rangeFile*4-1]["sequence"]))
					sequencepool2[trackselected-1]=saved["savedseq"][chosen+rangeFile*4-1]["sequence"]
					q1.put(sequencepool2)
			else:
				with open('savedseq.json') as s:
					saved = json.load(s)
					print((saved["savedseq"][chosen+rangeFile*4-1]["sequence"]))
					sequencepool2[trackselected-1]=saved["savedseq"][chosen+rangeFile*4-1]["sequence"]
					q1.put(sequencepool2)
		else:
			from midiconvert import MIDIconvert
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
				try:
					sequencepool2[trackselected-1]=MIDIconvert(filetext)
					print(sequencepool2)
				except:
					print('no such file')
					sequencepool2[trackselected-1]=[]
			else: sequencepool2[trackselected-1]=[]
		self.convert()
		self.leaving()

	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="IMPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="IMPORT"

	def convert(self):
		for i,elem in enumerate(sequencepool3[trackselected-1]): sequencepool3[trackselected-1][i]=[]
		for elem in sequencepool2[trackselected-1]: sequencepool3[trackselected-1][elem[0]-1].append([elem[1],elem[2],elem[3]])
		q6.put(sequencepool3[trackselected-1])

	def up(self):
		global rangeFile
		if rangeFile<21:
			rangeFile+=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		if rpi==1:self.usbcheck()


	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule LoadSeq")



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

class SaveSong(Screen):

	def on_enter(self):
		global rangeFile
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		print(chosen)
		if self.b001.state=="down":
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedsong.json', "w") as s2:
					savedsong["savedsong"][chosen+rangeFile*4-1]["song"] = song
					savedsong["savedsong"][chosen+rangeFile*4-1]["seq"] = sequencepool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["LFO"] = EnvPool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["ADSR"] = ADSRPool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["TRIG"] = ADSRtrig	
					savedsong["savedsong"][chosen+rangeFile*4-1]["MODE"] = trackmode
					savedsong["savedsong"][chosen+rangeFile*4-1]["PHASE"] = Phase																								
					json.dump(savedsong, s2)
				with open('/home/pi/Desktop2/UIP/savedsong2.json', "w") as s3:
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["soopsize"] = loopsize
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsizeS"] = loopsizeS
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["pulseeucli"] = pulseeucli
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["stepeucli"] = stepeucli
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliOffset"] = EucliOffset	
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomDensity"] = RandomDensity
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomTemp"] = RandomTemp
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomRatchet"] = RandomRatchet
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliPool2"] = EucliPool2																									
					json.dump(savedsong2, s3)					
			else:
				with open('savedsong.json', "w") as s2:
					savedsong["savedsong"][chosen+rangeFile*4-1]["song"] = song
					savedsong["savedsong"][chosen+rangeFile*4-1]["seq"] = sequencepool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["LFO"] = EnvPool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["ADSR"] = ADSRPool2
					savedsong["savedsong"][chosen+rangeFile*4-1]["TRIG"] = ADSRtrig	
					savedsong["savedsong"][chosen+rangeFile*4-1]["MODE"] = trackmode
					savedsong["savedsong"][chosen+rangeFile*4-1]["PHASE"] = Phase																	
					json.dump(savedsong, s2)
				with open('savedsong2.json', "w") as s3:
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsize"] = loopsize
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsizeS"] = loopsizeS
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["pulseeucli"] = pulseeucli
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["stepeucli"] = stepeucli
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliOffset"] = EucliOffset	
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomDensity"] = RandomDensity
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomTemp"] = RandomTemp
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomRatchet"] = RandomRatchet	
					savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliPool2"] = EucliPool2																								
					json.dump(savedsong2, s3)	
		"""
		else:
			from midi import MIDIFile
			track    = 0
			channel  = 0
			time     = 0
			tempo    = 120
			volume   = 100
			MyMIDI = MIDIFile(1)
			MyMIDI.addTempo(track, time, tempo)
			for elem in sequencepool2[trackselected-1]:
				if elem[2]==1: MyMIDI.addNote(track, channel, elem[1]+24, Decimal(elem[0]-1)/16, Decimal(elem[3])/16, volume)
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
			try:
				with open(filetext, "wb") as output_file:
					MyMIDI.writeFile(output_file)
			except: print("error usb")
		"""
		self.leaving()


	def up(self):
		global rangeFile
		if rangeFile<6:
			rangeFile+=1
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		if rpi==1:self.usbcheck()

	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="EXPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="EXPORT"

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule SaveSeq")



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

class LoadSong(Screen):

	def on_enter(self):
		global rangeFile
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		global song
		global EnvPool2
		global ADSRPool2
		global trackmode
		global ADSRtrig		
		global sequencepool2
		global Phase
		global loopsizeS
		global loopsize
		global pulseeucli
		global stepeucli
		global EucliOffset
		global RandomRatchet
		global RandomDensity
		global RandomTemp
		global EucliPool2

		print(chosen)
		if self.b001.state=="down":
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedsong.json') as s2:
					savedsong = json.load(s2)
					#print((savedsong["savedsong"][chosen+rangeFile*4-1]["song"]))
					song=savedsong["savedsong"][chosen+rangeFile*4-1]["song"]
					sequencepool2=savedsong["savedsong"][chosen+rangeFile*4-1]["seq"]					
					EnvPool2=savedsong["savedsong"][chosen+rangeFile*4-1]["LFO"]
					ADSRPool2=savedsong["savedsong"][chosen+rangeFile*4-1]["ADSR"]
					trackmode=savedsong["savedsong"][chosen+rangeFile*4-1]["MODE"]
					ADSRtrig=savedsong["savedsong"][chosen+rangeFile*4-1]["TRIG"]	
					Phase=savedsong["savedsong"][chosen+rangeFile*4-1]["PHASE"]									
				with open('/home/pi/Desktop2/UIP/savedsong2.json') as s3:
					savedsong2 = json.load(s3)
					#print((savedsong["savedsong"][chosen+rangeFile*4-1]["song"]))
					loopsize=savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsize"]
					loopsizeS=savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsizeS"]					
					pulseeucli=savedsong2["savedsong2"][chosen+rangeFile*4-1]["pulseeucli"]
					stepeucli=savedsong2["savedsong2"][chosen+rangeFile*4-1]["stepeucli"]
					EucliOffset=savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliOffset"]
					RandomDensity=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomDensity"]	
					RandomTemp=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomTemp"]	
					RandomRatchet=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomRatchet"]
					EucliPool2=savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliPool2"]			

			else:
				with open('savedsong.json') as s2:
					savedsong = json.load(s2)
					#print((savedsong["savedsong"][chosen+rangeFile*4-1]["song"]))
					song=savedsong["savedsong"][chosen+rangeFile*4-1]["song"]
					sequencepool2=savedsong["savedsong"][chosen+rangeFile*4-1]["seq"]
					EnvPool2=savedsong["savedsong"][chosen+rangeFile*4-1]["LFO"]
					ADSRPool2=savedsong["savedsong"][chosen+rangeFile*4-1]["ADSR"]
					trackmode=savedsong["savedsong"][chosen+rangeFile*4-1]["MODE"]
					ADSRtrig=savedsong["savedsong"][chosen+rangeFile*4-1]["TRIG"]
					Phase=savedsong["savedsong"][chosen+rangeFile*4-1]["PHASE"]							
					#print(sequencepool2)
				with open('savedsong2.json') as s3:
					savedsong2 = json.load(s3)
					#print((savedsong["savedsong"][chosen+rangeFile*4-1]["song"]))
					loopsize=savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsize"]
					loopsizeS=savedsong2["savedsong2"][chosen+rangeFile*4-1]["loopsizeS"]					
					pulseeucli=savedsong2["savedsong2"][chosen+rangeFile*4-1]["pulseeucli"]
					stepeucli=savedsong2["savedsong2"][chosen+rangeFile*4-1]["stepeucli"]
					EucliOffset=savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliOffset"]
					RandomDensity=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomDensity"]	
					RandomTemp=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomTemp"]	
					RandomRatchet=savedsong2["savedsong2"][chosen+rangeFile*4-1]["RandomRatchet"]
					EucliPool2=savedsong2["savedsong2"][chosen+rangeFile*4-1]["EucliPool2"]
			q3.put(song)
			q2.put(loopsize)
			v3.value=loopsizeS
			q9.put(ADSRtrig)


		"""
		else:
			from midiconvert import MIDIconvert
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
				try:
					sequencepool2[trackselected-1]=MIDIconvert(filetext)
					print(sequencepool2)
				except:
					print('no such file')
					sequencepool2[trackselected-1]=[]
			else: sequencepool2[trackselected-1]=[]
		"""
		self.clearseq()
		self.convertsequence()
		self.convertlfo()
		self.convertadsr()
		self.leaving()
		self.converteucli()
		q10.put(sequencepool3)	


	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="IMPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="IMPORT"

	def clearseq(self):
		global sequencepool3
		i=0
		while i<16:
			for a,elem in enumerate(sequencepool3[i]): sequencepool3[i][a]=[]
			i+=1		

	def convertsequence(self):
		global sequencepool3
		i=0
		while i<16:
			#for a,elem in enumerate(sequencepool3[i]): sequencepool3[i][a]=[]
			for elem in sequencepool2[i]:sequencepool3[i][elem[0]-1].append([elem[1],elem[2],elem[3]])
			#for elem in sequencepool2[i]:print(elem)
			#print("UPDATED: channel:", i,sequencepool3[i])
			i+=1
		#print("sequencepool3",sequencepool3)
		#q10.put(sequencepool3)			


	def converteucli(self):
		global sequencepool3
		j=0
		while j<16:

			for i in range(64):
				if EucliPool2[j][i%stepeucli[j]]==1:
					sequencepool3[j][i*4].append([36,1,4])
					sequencepool3[j][i*4+4].append([36,0,4])
					sequencepool3[j][i*4]=sorted(sequencepool3[j][i*4],key=operator.itemgetter(1,0))
					sequencepool3[j][i*4+4]=sorted(sequencepool3[j][i*4+4],key=operator.itemgetter(1,0))
			j+=1
		#q10.put(sequencepool3)


	def convertlfo(self):
		global EnvPool3
		i=0
		#print(EnvPool2)
		while i<16:
			if EnvPool2[i]!=[] and EnvPool2[i]!=[0] and EnvPool2[i]!=0 and trackmode[i]==2:
				print(EnvPool2[i])
				X=(((EnvPool2[i][0][0]-40)/700)+0.001)*loopsize[i]
				Y=((EnvPool2[i][0][1]-195.2)/37)
				a1=2*Y/X
				b1=-Y
				a2=2*Y/(X-loopsize[i]+1)
				b2=Y-a2*X
				PHASE=(Phase[i]+0.001-40)/700*loopsize[i]-1.37
				a=0
				while a<loopsize[i]:
					n=(a+PHASE)%loopsize[i]
					if n<X:
						EnvPool3[i][a]=(a1*n+b1)*3/5
					else:
						EnvPool3[i][a]=(a2*n+b2)*3/5
					a+=1
			i+=1
		q11.put(EnvPool3)

	def convertadsr(self):
		global ADSRPool3
		i=0
		while i<16:
			if ADSRPool2[i]!=0 and ADSRPool2[i]!=[0] and trackmode[i]==3:
				lps=loopsize[i]
				p1=[0,0]
				p2=[(ADSRPool2[i][0]-41)/700*lps+1,(ADSRPool2[i][1])/330]
				p3=[(ADSRPool2[i][2]-52)/700*lps,(ADSRPool2[i][3])/330]
				p4=[(ADSRPool2[i][4]-52)/700*lps,(ADSRPool2[i][5])/330]
				p5=[(ADSRPool2[i][6]-52)/700*lps,(ADSRPool2[i][7])/330]	
				#print("P",p1,p2,p3,p4,p5)					
				j=0
				a1=self.coefs(p1,p2)
				a2=self.coefs(p2,p3)
				a3=self.coefs(p3,p4)
				a4=self.coefs(p4,p5)
				while j<lps:
					if j < p2[0]:
						r=a1*j
						if r>0:ADSRPool3[i][j]=r
						else:ADSRPool3[i][j]=0
						x=j
					elif p2[0] <= j <= p3[0]:
						r=a2*(j-x)+ADSRPool3[i][x]
						if r>0: ADSRPool3[i][j]=r
						else:ADSRPool3[i][j]=0
						x=j
					elif p3[0] <= j <= p4[0]:
						r=a3*(j-x)+ADSRPool3[i][x]
						if r>0: ADSRPool3[i][j]=r
						else:ADSRPool3[i][j]=0
						x=j
					elif p4[0] <= j <= p5[0]:
						r=a4*(j-x)+ADSRPool3[i][x]
						if r>0: ADSRPool3[i][j]=r
						else:ADSRPool3[i][j]=0
						x=j
					elif j>p5[0]:ADSRPool3[i][j]=0
					j+=1
			i+=1
		#print("adsr",ADSRPool3)
		q12.put(ADSRPool3)	


	def coefs(self,p1,p2):
		coef=(p2[1]-p1[1])/(p2[0]-p1[0])*5
		#print(coef)
		return coef

	def up(self):
		global rangeFile
		if rangeFile<6:
			rangeFile+=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		if rpi==1:self.usbcheck()


	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule LoadSeq")




##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################




class LFOScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
		global Lline1
		global Lline4
		global Lline7											
		Lline1 = self.ids.w_canvas.canvas.get_group('a')[0]			
		Lline4 = self.ids.w_canvas.canvas.get_group('b')[0]
		Lline7 = self.ids.w_canvas.canvas.get_group('g')[0]
		global trackmode
		global loopsize
		if trackmode[trackselected-1]!=2:
			loopsize[trackselected-1]=64
			self.reset()
			q2.put(loopsize)
		trackmode[trackselected-1]=2
		print('trackmode',trackmode[trackselected-1])
		global lfobutmode
		lfobutmode=0
		self.mode(0)
		print(trackselected-1)
		self.LoopSdisplay()
		self.b025.pos[0]=Phase[trackselected-1]
		clearsequence()
		deleteADSR()
		self.move_button(Lline7.pos[1])
		self.b006.text=str(trackselected)+ ": LFO"
		if y1.value!=0:self.b0003.pos=185,419
		else:self.b0003.pos=1185,419

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b013.pos= 344,900		
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,900	
			self.b027.pos= 496,900
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b012.pos= 496,301
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 496,242	
			self.b015.pos= 496,183			
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,900	
			self.b027.pos= 496,124
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b027.pos= 496,900

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360		
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,301
			self.b027.pos= 496,900
		else:
			self.b013.pos= 344,900			
			self.b010.pos= 1000,0	
			self.b026.pos= 344,900	


	def mode(self,num):
		global lfobutmode
		if num==0:
			self.b003.state='normal'
			self.b004.state='normal'
			self.b025.state='normal'
		if num==2:
			if lfobutmode==2:
				lfobutmode=0
				self.b003.state='normal'
			else:
				lfobutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if lfobutmode==3:
				lfobutmode=0
				self.b004.state='normal'
			else:
				lfobutmode=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			if lfobutmode==4:
				lfobutmode=0
				self.b025.state='normal'
			else:
				lfobutmode=4
				self.b025.state='down'
				w2.value=0
		print(("buton mode",lfobutmode))



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2



	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0

	def reset(self):
		global EnvPool2
		global Phase
		EnvPool2[trackselected-1]=[[400,380]]
		Phase[trackselected-1]=55
		self.UIrefresh(EnvPool2[trackselected-1])
		self.updateEnv()
		self.convert2to3()
		self.move_button(Lline7.pos[1])	
		self.b025.pos[0]=55


	def listening(self,*args):
		global wheel
		global lfobutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if lfobutmode==0: pass
		if lfobutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				lfobutmode=0
				self.b003.state='normal'
		if lfobutmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<16*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)	
						self.LoopSdisplay()				
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>16:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()
			if encoderpushed==1:
				lfobutmode=0
				self.b004.state='normal'
		if lfobutmode==4:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.Phase(20)
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.Phase(-20)
			if encoderpushed==1:
				lfobutmode=0
				self.b025.state='normal'
				self.closemenus()
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2

	def on_touch_move(self, touch):
			global EnvPool2
			global buttonpos 
			buttonpos=touch.pos[1]-10
			if 50 <= touch.pos[0] <= 750:
				if 20 <= touch.pos[1] <= 380:
					self.UIrefresh([touch.pos])
					self.move_button(Lline7.pos[1])
					self.updateEnv()

	def encadrement_lfo(self, x, y, buttonpos):
		txt = (buttonpos-x)*(100.0/(y-x))
		return txt


	def move_button(self, buttonpos):
		txt=self.encadrement_lfo(190, 370, buttonpos)
		if buttonpos >= 190:
			self.b024.pos=(1,buttonpos)
			self.b024.text=str(int(txt))
		elif buttonpos < 190:			
			self.b024.pos=(1,380 - buttonpos)
			self.b024.text=str(int(-1 * txt))

	def UIrefresh(self,Coord):
		Lline7.pos=(Coord[0][0]-10,Coord[0][1]-10)	
		Lline1.points=[(50,400 - Coord[0][1]),(Coord[0][0],Coord[0][1])]
		Lline4.points=[(750,400 - Coord[0][1]),(Coord[0][0],Coord[0][1])]


	def updateEnv(self):
		global EnvPool2
		EnvPool2[trackselected-1]=[]
		EnvPool2[trackselected-1].append([Lline7.pos[0],Lline7.pos[1]])
		#print(EnvPool2)
		self.convert2to3()


	def convert2to3(self):
		global EnvPool2
		global EnvPool3
		#print(EnvPool2)
		X=(((EnvPool2[trackselected-1][0][0]-40)/700)+0.001)*loopsize[trackselected-1]
		Y=((EnvPool2[trackselected-1][0][1]-195.2)/37)
		a1=2*Y/X
		b1=-Y
		a2=2*Y/(X-loopsize[trackselected-1]+1)
		b2=Y-a2*X
		#print(X,Y)
		#print(a1,b1,a2,b2)
		PHASE=(Phase[trackselected-1]+0.001-40)/700*loopsize[trackselected-1]-1.37
		#print(PHASE)
		i=0
		
		while i<loopsize[trackselected-1]:
			n=(i+PHASE)%loopsize[trackselected-1]
			if n<X:
				EnvPool3[trackselected-1][i]=(a1*n+b1)*3/5
			else:
				EnvPool3[trackselected-1][i]=(a2*n+b2)*3/5
			i+=1
		q7.put(EnvPool3[trackselected-1])
		#print(EnvPool3[trackselected-1])
		#print(EnvPool3[trackselected-1][0],EnvPool3[trackselected-1][63])		


	def LoopSdisplay(self):
		self.l1.text=str(loopsize[trackselected-1]/16)
		self.convert2to3()
		self.b004.text=str(loopsize[trackselected-1]/16)

	def Phase(self,move):
		global Phase
		if move <0 and self.b025.pos[0]>70 or move >0 and self.b025.pos[0]<730:
			self.b025.pos[0]+=move
			Phase[trackselected-1]=self.b025.pos[0]
			#print(Phase[trackselected-1])
			self.convert2to3()


	def test1(self):
		self.Phase(20)

	def test2(self):
		self.Phase(-20)

	def polarity(self):
		global polaritylfo
		if polaritylfo[trackselected-1]==0:
			polaritylfo[trackselected-1]=1
			self.b026.text="UNIPOLAR"
			self.UIrefresh(EnvPool2[trackselected-1])
		else:
			polaritylfo[trackselected-1]=0
			self.b026.text="BIPOLAR"
			self.UIrefresh(EnvPool2[trackselected-1])



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################




class DRAWScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
		global Lline7
		global Point1
		global Point2
		global Point3
		global Point4
		global Point5
		global Point6
		global Point7
		global Point8	
		global Lline1
		global Lline2
		global Lline3
		global Lline4
		global Lline5
		global Lline6
		global Lline8										
		Lline7 = self.ids.w_canvas.canvas.get_group('g')[0]
		Point1 = self.ids.w_canvas.canvas.get_group('h')[0]
		Point2 = self.ids.w_canvas.canvas.get_group('i')[0]
		Point3 = self.ids.w_canvas.canvas.get_group('j')[0]
		Point4 = self.ids.w_canvas.canvas.get_group('k')[0]
		Point5 = self.ids.w_canvas.canvas.get_group('l')[0]
		Point6 = self.ids.w_canvas.canvas.get_group('m')[0]
		Point7 = self.ids.w_canvas.canvas.get_group('n')[0]
		Point8 = self.ids.w_canvas.canvas.get_group('o')[0]
		Lline1 = self.ids.w_canvas.canvas.get_group('a')[0]	
		Lline2 = self.ids.w_canvas.canvas.get_group('q')[0]	
		Lline3 = self.ids.w_canvas.canvas.get_group('r')[0]	
		Lline4 = self.ids.w_canvas.canvas.get_group('b')[0]	
		Lline5 = self.ids.w_canvas.canvas.get_group('t')[0]	
		Lline6 = self.ids.w_canvas.canvas.get_group('u')[0]	
		Lline8 = self.ids.w_canvas.canvas.get_group('w')[0]	
		global trackmode
		global loopsize
		if trackmode[trackselected-1]!=2:
			loopsize[trackselected-1]=64
			self.reset()
		trackmode[trackselected-1]=2
		print('trackmode',trackmode[trackselected-1])
		global lfobutmode
		lfobutmode=6
		print(trackselected-1)
		self.LoopSdisplay()
		self.b025.pos[0]=Phase[trackselected-1]
		self.clearsequence()
		self.deleteADSR()
		self.move_button(Lline7.pos[1])
		global DrawPoints

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'

	def clearsequence(self):
		global sequencepool2
		global sequencepool3
		sequencepool2[trackselected-1]=[]
		for i,elem in enumerate(sequencepool3[trackselected-1]): sequencepool3[trackselected-1][i]=[]
		q1.put(sequencepool2)
		q6.put(sequencepool3[trackselected-1])
		#print(sequencepool3[trackselected-1])


	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b013.pos= 344,900		
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,900	
			self.b027.pos= 496,900
			self.b028.pos= 344,900
			self.b029.pos= 344,900
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b027.pos= 496,301
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b012.pos= 496,242	
			self.b014.pos= 496,183			
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,900
			self.b015.pos= 496,124
			self.b028.pos= 344,900	
			self.b029.pos= 344,900
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b027.pos= 496,900

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360		
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
			self.b026.pos= 344,301
			self.b027.pos= 344,900
			self.b028.pos= 344,242
			self.b029.pos= 419,242
		else:
			self.b013.pos= 344,900			
			self.b010.pos= 1000,0
			self.b026.pos= 344,900	
			self.b027.pos= 344,900
			self.b028.pos= 344,900
			self.b029.pos= 344,900


	def mode(self,num):
		global lfobutmode
		if num==1:
			if lfobutmode==1:
				lfobutmode=0
				self.b020.state='normal'
			else:
				lfobutmode=1
				self.b020.state='down'
				w2.value=0
		if num==2:
			if lfobutmode==2:
				lfobutmode=0
				self.b003.state='normal'
			else:
				lfobutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if lfobutmode==3:
				lfobutmode=0
				self.b004.state='normal'
			else:
				lfobutmode=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			if lfobutmode==4:
				lfobutmode=0
				self.b025.state='normal'
			else:
				lfobutmode=4
				self.b025.state='down'
				w2.value=0
		if num==5:
			if lfobutmode==5:
				lfobutmode=0
				self.b024.state='normal'
			else:
				lfobutmode=5
				self.b024.state='down'
				w2.value=0				
		if num==6:
			lfobutmode=6
			self.b003.state='normal'
			self.b004.state='normal'
			self.b020.state='normal'
		print(("buton mode",lfobutmode))



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2



	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0

	def reset(self):
		global EnvPool2
		EnvPool2[trackselected-1]=[[400,380]]
		self.UIrefresh(EnvPool2[trackselected-1])
		self.updateEnv()
		self.convert2to3()
		self.move_button(Lline7.pos[1])		

	def delete(self):
		global EnvPool2
		global EnvPool3
		EnvPool2[trackselected-1]=[0]
		EnvPool3[trackselected-1]=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		#print("deleted",EnvPool3[trackselected-1])
		#print("EnvPool0",EnvPool0)
		q7.put(EnvPool3[trackselected-1])

	def deleteADSR(self):
		global ADSRPool2
		global ADSRPool3
		ADSRPool2[trackselected-1]=[0]
		ADSRPool3[trackselected-1]=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		q8.put(ADSRPool3[trackselected-1])


	def listening(self,*args):
		global wheel
		global lfobutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if lfobutmode==0: pass
		if lfobutmode==1:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.rgt()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.lft()
			if encoderpushed==1:
				lfobutmode=0
				self.b023.state='normal'
				self.closemenus()

		if lfobutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				lfobutmode=0
				self.b003.state='normal'

		if lfobutmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<16*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)	
						self.LoopSdisplay()				
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>16:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()
			if encoderpushed==1:
				lfobutmode=0
				self.b004.state='normal'

		if lfobutmode==4:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.Phase(20)
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.Phase(-20)
			if encoderpushed==1:
				lfobutmode=0
				self.b025.state='normal'
				self.closemenus()
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2

	def on_touch_move(self, touch):
			global EnvPool2
			global buttonpos 
			buttonpos=touch.pos[1]-10
			if 50 <= touch.pos[0] <= 750:
				if 20 <= touch.pos[1] <= 380:
					self.UIrefresh([touch.pos])
					self.move_button(Lline7.pos[1])
					self.updateEnv()

	def encadrement_lfo(self, x, y, buttonpos):
		txt = (buttonpos-x)*(100.0/(y-x))
		return txt


	def move_button(self, buttonpos):
		txt=self.encadrement_lfo(190, 370, buttonpos)
		if buttonpos >= 190:
			self.b024.pos=(1,buttonpos)
			self.b024.text=str(int(txt))
		elif buttonpos < 190:			
			self.b024.pos=(1,380 - buttonpos)
			self.b024.text=str(int(-1 * txt))

	def UIrefresh(self,Coord):
		if polaritylfo[trackselected-1]==0:
			Lline7.pos=(Coord[0][0]-10,Coord[0][1]-10)	
			Lline1.points=[(50,400 - Coord[0][1]),(Coord[0][0],Coord[0][1])]
			Lline4.points=[(750,400 - Coord[0][1]),(Coord[0][0],Coord[0][1])]
		else:
			Lline7.pos=(Coord[0][0]-10,Coord[0][1]-10)
			Lline1.points=[(50,20),(Coord[0][0],Coord[0][1])]
			Lline4.points=[(750,20),(Coord[0][0],Coord[0][1])]
		#print(polaritylfo)



	def updateEnv(self):
		global EnvPool2
		EnvPool2[trackselected-1]=[]
		EnvPool2[trackselected-1].append([Lline7.pos[0],Lline7.pos[1]])
		#print(EnvPool2)
		self.convert2to3()


	def convert2to3(self):
		global EnvPool2
		global EnvPool3
		#print(EnvPool2)
		X=(((EnvPool2[trackselected-1][0][0]-40)/700)+0.001)*loopsize[trackselected-1]
		Y=((EnvPool2[trackselected-1][0][1]-195.2)/37)
		a1=2*Y/X
		b1=-Y
		a2=2*Y/(X-loopsize[trackselected-1]+1)
		b2=Y-a2*X
		#print(X,Y)
		#print(a1,b1,a2,b2)
		PHASE=(Phase[trackselected-1]+0.001-40)/700*loopsize[trackselected-1]-1.37
		#print(PHASE)
		i=0
		
		while i<loopsize[trackselected-1]:
			n=(i+PHASE)%loopsize[trackselected-1]
			if n<X:
				EnvPool3[trackselected-1][i]=(a1*n+b1)*3/5
			else:
				EnvPool3[trackselected-1][i]=(a2*n+b2)*3/5
			i+=1
		q7.put(EnvPool3[trackselected-1])
		#print(EnvPool3[trackselected-1])
		#print(EnvPool3[trackselected-1][0],EnvPool3[trackselected-1][63])		


	def LoopSdisplay(self):
		self.l1.text=str(loopsize[trackselected-1]/16)
		self.convert2to3()
		self.b004.text=str(loopsize[trackselected-1]/16)

	def Phase(self,move):
		global Phase
		if move <0 and self.b025.pos[0]>70 or move >0 and self.b025.pos[0]<730:
			self.b025.pos[0]+=move
			Phase[trackselected-1]=self.b025.pos[0]
			#print(Phase[trackselected-1])
			self.convert2to3()


	def test1(self):
		self.Phase(20)

	def test2(self):
		self.Phase(-20)

	def polarity(self):
		global polaritylfo
		if polaritylfo[trackselected-1]==0:
			polaritylfo[trackselected-1]=1
			self.b026.text="UNIPOLAR"
			self.UIrefresh(EnvPool2[trackselected-1])
		else:
			polaritylfo[trackselected-1]=0
			self.b026.text="BIPOLAR"
			self.UIrefresh(EnvPool2[trackselected-1])

	def addpoint(self):
		global point
		point=[Point1,Point2, Point3, Point4, Point5, Point6, Point7, Point8]
		DrawPoints[trackselected-1] = DrawPoints[trackselected-1] + 1
		for i in range(DrawPoints[trackselected-1]):
			point[i].pos=100+(100*i),100
		print(DrawPoints)

	def rempoint(self):
		DrawPoints[trackselected-1] = DrawPoints[trackselected-1] - 1
		for i in range(DrawPoints[trackselected-1]):
			point[DrawPoints[trackselected-1]].pos=900,100
		print(DrawPoints)






##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################



class ADSRScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
		global Lline1
		global Lline2
		global Lline3
		global Lline4
		global Lline5
		global Lline6	
		global Lline7
		global Lline8									
		Lline1 = self.ids.w_canvas.canvas.get_group('a')[0]
		Lline2 = self.ids.w_canvas.canvas.get_group('b')[0]
		Lline3 = self.ids.w_canvas.canvas.get_group('c')[0]				
		Lline4 = self.ids.w_canvas.canvas.get_group('d')[0]
		Lline5 = self.ids.w_canvas.canvas.get_group('e')[0]
		Lline6 = self.ids.w_canvas.canvas.get_group('f')[0]
		Lline7 = self.ids.w_canvas.canvas.get_group('g')[0]
		Lline8 = self.ids.w_canvas.canvas.get_group('h')[0]		
		global adsrbutmode
		adsrbutmode=0
		self.mode(0)
		print(trackselected-1)
		global trackmode
		global loopsize
		if trackmode[trackselected-1]!=3:
			loopsize[trackselected-1]=64
			self.reset()
			q2.put(loopsize)
		trackmode[trackselected-1]=3
		print('trackmode',trackmode[trackselected-1])
		self.triginfo()
		clearsequence()
		deleteLFO()
		self.UIrefresh()
		self.LoopSdisplay()
		self.b006.text=str(trackselected)+ ": ADSR"
		if y1.value!=0:self.b0003.pos=185,419
		else:self.b0003.pos=1185,419

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'

	def closemenu(self):
		self.b5017.pos=1329,305
		self.b5000.pos=1228,61
		self.b5001.pos=1229,245
		self.b5005.pos=1229,184
		self.b5009.pos=1229,123
		self.b5013.pos=1229,62
		self.b5002.pos=1329,245
		self.b5006.pos=1329,184
		self.b5010.pos=1329,123
		self.b5014.pos=1329,62
		self.b5003.pos=1429,245
		self.b5007.pos=1429,184
		self.b5011.pos=1429,123
		self.b5015.pos=1429,62
		self.b5004.pos=1529,245
		self.b5008.pos=1529,184
		self.b5012.pos=1529,123
		self.b5016.pos=1529,62
		self.b3005.pos=1000,0



	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900	
			self.b018.pos= 496,900	
			self.b019.pos= 496,900	
			self.b023.pos= 496,900			
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b012.pos= 496,301
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900
			self.b018.pos= 496,242	
			self.b019.pos= 496,183	
			self.b023.pos= 496,124				
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b018.pos= 496,900	
			self.b019.pos= 496,900	
			self.b023.pos= 496,900
			self.b010.pos= 1000,0

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360
			self.b014.pos= 344,301
			#self.b016.pos= 344,242
			#self.b020.pos= 344,183
			#self.b022.pos= 344,124			
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b018.pos= 496,900	
			self.b019.pos= 496,900
			self.b023.pos= 496,900	
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
		else:
			self.b013.pos= 344,900
			self.b014.pos= 344,900
			self.b016.pos= 344,900
			self.b020.pos= 344,900
			self.b022.pos= 344,900			
			self.b010.pos= 1000,0


	def trig(self):
		self.b5017.pos=310,305
		self.b5017.text="ADSR TRIGGERED BY TRACK:"
		self.b5000.pos=138,31
		self.b5001.pos=139,236
		self.b5005.pos=139,168
		self.b5009.pos=139,100
		self.b5013.pos=139,32
		self.b5002.pos=269,236
		self.b5006.pos=269,168
		self.b5010.pos=269,100
		self.b5014.pos=269,32
		self.b5003.pos=399,236
		self.b5007.pos=399,168
		self.b5011.pos=399,100
		self.b5015.pos=399,32
		self.b5004.pos=529,236
		self.b5008.pos=529,168
		self.b5012.pos=529,100
		self.b5016.pos=529,32
		self.b3005.pos=0,0
		self.b5001.text="1"
		self.b5005.text="5"
		self.b5009.text="9"
		self.b5013.text="13"
		self.b5002.text="2"
		self.b5006.text="6"
		self.b5010.text="10"
		self.b5014.text="14"
		self.b5003.text="3"
		self.b5007.text="7"
		self.b5011.text="11"
		self.b5015.text="15"
		self.b5004.text="4"
		self.b5008.text="8"
		self.b5012.text="12"
		self.b5016.text="16"

	def port2(self,button):
		global ADSRtrig
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		new=int((ID[-2:]))
		#print(new)
		for n,value in enumerate(ADSRtrig):
			if trackselected==value:ADSRtrig[n]=0
		ADSRtrig[new-1]=trackselected
		#print(ADSRtrig)
		q9.put(ADSRtrig)
		self.triginfo()
	
	def triginfo(self):
		self.b014.text="TRIG: NONE"
		for n,value in enumerate(ADSRtrig):
			if value==trackselected:
				trig=n+1
				self.b014.text="TRIG: "+str(trig)

	def mode(self,num):
		global adsrbutmode
		if num==0:
			self.b003.state='normal'
			self.b004.state='normal'
		if num==2:
			if adsrbutmode==2:
				adsrbutmode=0
				self.b003.state='normal'
			else:
				adsrbutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if adsrbutmode==3:
				adsrbutmode=0
				self.b004.state='normal'
			else:
				adsrbutmode=3
				self.b004.state='down'
				w2.value=0
		print(("buton mode",adsrbutmode))

	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2



	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0

	def reset(self):
		global ADSRPool2
		ADSRPool2[trackselected-1]=[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0]
		self.UIrefresh()
		self.convert2to3()


	def listening(self,*args):
		global wheel
		global adsrbutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if adsrbutmode==0: pass


		if adsrbutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				adsrbutmode=0
				self.b003.state='normal'
		if adsrbutmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<16*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)
						self.LoopSdisplay()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>64:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()
			if encoderpushed==1:
				adsrbutmode=0
				self.b004.state='normal'						
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2

	def LoopSdisplay(self):
		self.l1.text=str(loopsize[trackselected-1]/16)
		self.convert2to3()
		self.b004.text=str(loopsize[trackselected-1]/16)


	def encadrement_lfo(self, x, y, buttonpos):
		
		txt = (buttonpos-x)*(100.0/(y-x))
		return txt


	def move_button(self, buttonpos):
		#txt = (buttonpos - 190) * (100/180)
		txt=self.encadrement_lfo(20, 370, buttonpos)
		if buttonpos == Lline5.pos[1]:
			self.b024.pos=(-25,buttonpos-35)
			self.b024.text=str(int(txt))
		if buttonpos == Lline6.pos[1]:
			self.b028.pos=(-25,buttonpos-35)
			self.b028.text=str(int(txt))
		#if buttonpos == Lline7.pos[1]:
			#self.b026.pos=(17,buttonpos)
			#self.b026.text=str(int(txt))
	def UIrefresh(self):
		#print(ADSRPool2[trackselected-1])
		Lline5.pos=(ADSRPool2[trackselected-1][0],ADSRPool2[trackselected-1][1])		
		Lline6.pos=(ADSRPool2[trackselected-1][2],ADSRPool2[trackselected-1][3])
		Lline7.pos=(ADSRPool2[trackselected-1][4],ADSRPool2[trackselected-1][5])
		Lline8.pos=(ADSRPool2[trackselected-1][6],ADSRPool2[trackselected-1][7])
		self.displaylines()		
		self.move_button(Lline5.pos[1])
		self.move_button(Lline6.pos[1])		


	def on_touch_move(self, touch):
		ecart76 = Lline7.pos[0]-Lline6.pos[0]
		ecart75 = Lline7.pos[0]-Lline5.pos[0]
		ecart85 = Lline8.pos[0]-Lline5.pos[0]
		ecart86 = Lline8.pos[0]-Lline6.pos[0]
		ecart87=Lline8.pos[0]-Lline7.pos[0]
		ecart = Lline6.pos[0]-Lline5.pos[0]
		rayon=50
		#print(touch.pos)
		if (Lline5.pos[0] - rayon) <= touch.pos[0] <= (Lline5.pos[0] + rayon):
			if (Lline5.pos[1] - rayon) <= touch.pos[1] <= (Lline5.pos[1] + rayon):
				if 52 <= touch.pos[0] <= Lline6.pos[0]:
					if Lline6.pos[1]+10 <= touch.pos[1] <= 390:
						if touch.pos[0]+ecart85 <= 750:
								Lline5.pos=(touch.pos[0]-10,touch.pos[1]-10)
								if Lline5.pos[1]>370:
									Lline5.pos=(touch.pos[0]-10,370)								
								Lline6.pos=(Lline5.pos[0]+ecart, Lline6.pos[1])
								Lline7.pos=(Lline6.pos[0]+ecart76, Lline6.pos[1])
								Lline8.pos=(Lline5.pos[0]+ecart85, Lline8.pos[1])
								self.move_button(Lline5.pos[1])
								self.updateADSR()
						else:
							if ecart87 >= 50:
								Lline5.pos=(touch.pos[0]-10,touch.pos[1]-10)
								if Lline5.pos[1]>370:
									Lline5.pos=(touch.pos[0]-10,370)								
								Lline6.pos=(Lline5.pos[0]+ecart, Lline6.pos[1])
								Lline7.pos=(Lline6.pos[0]+ecart76, Lline6.pos[1])
								Lline8.pos=(740, Lline8.pos[1])	
								self.move_button(Lline5.pos[1])
								self.updateADSR()
					elif 30 <= touch.pos[1]<= 390:
						if touch.pos[0]+ecart85 <= 750:
								Lline5.pos=(touch.pos[0]-10,touch.pos[1]-10)
								if Lline5.pos[1]>370:
									Lline5.pos=(touch.pos[0]-10,370)								
								Lline6.pos=(Lline5.pos[0]+ecart, Lline5.pos[1])
								Lline7.pos=(Lline6.pos[0]+ecart76, Lline5.pos[1])
								Lline8.pos=(Lline5.pos[0]+ecart85, Lline8.pos[1])
								self.move_button(Lline5.pos[1])
								self.updateADSR()
						else:
							if ecart87 >= 50:
								Lline5.pos=(touch.pos[0]-10,touch.pos[1]-10)
								if Lline5.pos[1]>370:
									Lline5.pos=(touch.pos[0]-10,370)								
								Lline6.pos=(Lline5.pos[0]+ecart, Lline5.pos[1])
								Lline7.pos=(Lline6.pos[0]+ecart76, Lline5.pos[1])
								Lline8.pos=(740, Lline8.pos[1])	
								self.move_button(Lline5.pos[1])
								self.updateADSR()
		elif (Lline6.pos[0] - rayon) <= touch.pos[0] <= (Lline6.pos[0] + rayon):
			if (Lline6.pos[1] - rayon) <= touch.pos[1] <= (Lline6.pos[1] + rayon):
				if Lline5.pos[0]+10 <= touch.pos[0] <= Lline7.pos[0]+10:
					if 29 <= touch.pos[1] <= Lline5.pos[1]+10:
						if touch.pos[0]+ecart76 <= Lline8.pos[0]+10:
							if touch.pos[0]+ecart86 <= 750:
								Lline6.pos=(touch.pos[0]-10,touch.pos[1]-10)
								Lline7.pos=(Lline6.pos[0]+ecart76, Lline6.pos[1])
								Lline8.pos=(Lline6.pos[0]+ecart86, Lline8.pos[1])	
								self.move_button(Lline6.pos[1])
								self.updateADSR()
							else:
								if ecart87 >= 50:
									Lline6.pos=(touch.pos[0]-10,touch.pos[1]-10)
									Lline7.pos=(Lline6.pos[0]+ecart76, Lline6.pos[1])
									Lline8.pos=(740, Lline8.pos[1])	
									self.move_button(Lline6.pos[1])
									self.updateADSR()
		elif (Lline7.pos[0] - rayon) <= touch.pos[0] <= (Lline7.pos[0] + rayon):
			if (Lline7.pos[1] - rayon) <= touch.pos[1] <= (Lline7.pos[1] + rayon):
				if Lline6.pos[0]+10 <= touch.pos[0] <= Lline8.pos[0]+10:
					if touch.pos[0] + ecart87 <= 750:
								Lline7.pos=(touch.pos[0]-10,Lline6.pos[1])	
								Lline8.pos=(Lline7.pos[0]+ecart87, Lline8.pos[1])	
								self.updateADSR()
								self.move_button(Lline7.pos[1])								
					else:
							if ecart87 >= 50:
								Lline7.pos=(touch.pos[0]-10,Lline6.pos[1])	
								Lline8.pos=(740, Lline8.pos[1])						
								self.updateADSR()
								self.move_button(Lline7.pos[1])
		elif (Lline8.pos[0] - rayon) <= touch.pos[0] <= (Lline8.pos[0] + rayon):
			if (Lline8.pos[1] - rayon) <= touch.pos[1] <= (Lline8.pos[1] + rayon):
				if Lline7.pos[0]+10 <= touch.pos[0] <= 750:
								Lline8.pos=(touch.pos[0]-10,19)	
								self.move_button(Lline7.pos[1])
								self.updateADSR()								
		#print(Lline5.pos,Lline6.pos,Lline7.pos,Lline8.pos)
		self.displaylines()	

	def displaylines(self):
		Lline1.points=[(52,30),(Lline5.pos[0]+10,Lline5.pos[1]+10)]
		Lline2.points=[(Lline6.pos[0]+10, Lline6.pos[1]+10),(Lline5.pos[0]+10,Lline5.pos[1]+10)]
		Lline3.points=[(Lline7.pos[0]+10, Lline7.pos[1]+10),(Lline6.pos[0]+10, Lline6.pos[1]+10)]
		Lline4.points=[(Lline7.pos[0]+10, Lline7.pos[1]+10),(Lline8.pos[0]+10, Lline8.pos[1]+10)]		


	def updateADSR(self):
		global ADSRPool2
		ADSRPool2[trackselected-1]=[Lline5.pos[0],Lline5.pos[1],Lline6.pos[0],Lline6.pos[1],Lline7.pos[0],Lline6.pos[1],Lline8.pos[0],Lline8.pos[1]]
		#print(ADSRPool2[trackselected-1])
		self.convert2to3()

	def convert2to3(self):
		#en fonction loopsize
		global ADSRPool3
		lps=loopsize[trackselected-1]
		p1=[0,0]
		p2=[(Lline5.pos[0]-41)/700*lps+1,(Lline5.pos[1])/330]
		p3=[(Lline6.pos[0]-52)/700*lps,(Lline6.pos[1])/330]
		p4=[(Lline7.pos[0]-52)/700*lps,(Lline7.pos[1])/330]
		p5=[(Lline8.pos[0]-52)/700*lps,(Lline8.pos[1])/330]	
		#print("P",p1,p2,p3,p4,p5)					
		i=0
		a1=self.coefs(p1,p2)
		a2=self.coefs(p2,p3)
		a3=self.coefs(p3,p4)
		a4=self.coefs(p4,p5)
		while i<lps:
			if i < p2[0]:
				r=a1*i
				if r>0:ADSRPool3[trackselected-1][i]=r
				else:ADSRPool3[trackselected-1][i]=0
				x=i
			elif p2[0] <= i <= p3[0]:
				r=a2*(i-x)+ADSRPool3[trackselected-1][x]
				if r>0: ADSRPool3[trackselected-1][i]=r
				else:ADSRPool3[trackselected-1][i]=0
				x=i
			elif p3[0] <= i <= p4[0]:
				r=a3*(i-x)+ADSRPool3[trackselected-1][x]
				if r>0: ADSRPool3[trackselected-1][i]=r
				else:ADSRPool3[trackselected-1][i]=0
				x=i
			elif p4[0] <= i <= p5[0]:
				r=a4*(i-x)+ADSRPool3[trackselected-1][x]
				if r>0: ADSRPool3[trackselected-1][i]=r
				else:ADSRPool3[trackselected-1][i]=0
				x=i	
			elif i>p5[0]:ADSRPool3[trackselected-1][i]=0

			i+=1
		#print(ADSRPool3[trackselected-1])
		q8.put(ADSRPool3[trackselected-1])



	def coefs(self,p1,p2):
		coef=(p2[1]-p1[1])/(p2[0]-p1[0])*5
		#print(coef)
		return coef


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class RandomScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.CalculateRandom, 0.002)
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))	
			Clock.unschedule(self.CalculateRandom)										
		global trackmode
		if trackmode[trackselected-1]!=4:
			clearsequence()
			deleteLFO()
			deleteADSR()
		trackmode[trackselected-1]=4
		print('trackmode',trackmode[trackselected-1])

		global randombutmode
		randombutmode=0
		self.mode(0)
		global loopsize
		loopsize[trackselected-1]=64
		q2.put(loopsize)
		print(trackselected-1)
		global points
		points=[self.ids.w_canvas.canvas.get_group('a')[0],self.ids.w_canvas.canvas.get_group('b')[0],self.ids.w_canvas.canvas.get_group('c')[0],self.ids.w_canvas.canvas.get_group('d')[0],self.ids.w_canvas.canvas.get_group('e')[0],self.ids.w_canvas.canvas.get_group('f')[0]]
		self.init()
		self.b006.text=str(trackselected)+ ": RANDOM"
		if y1.value!=0:self.b0003.pos=185,419
		else:self.b0003.pos=1185,419

	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")
		try:Clock.unschedule(self.CalculateRandom)
		except:pass



	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b013.pos= 344,900
			self.b016.pos= 496,900			
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b012.pos= 496,301
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 496,242	
			self.b015.pos= 496,183
			self.b016.pos= 496,124				
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b016.pos= 496,900

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360		
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b016.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
		else:
			self.b013.pos= 344,900			
			self.b010.pos= 1000,0	


	def mode(self,num):
		global randombutmode
		if num==0:
			self.b003.state='normal'
		if num==2:
			if randombutmode==2:
				randombutmode=0
				self.b003.state='normal'
			else:
				randombutmode=2
				self.b003.state='down'
				w2.value=0
		print(("buton mode",randombutmode))



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.delseq()
			Clock.schedule_interval(self.CalculateRandom, 0.002)
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			Clock.unschedule(self.CalculateRandom)
			playing=0
			v1.value=2


	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		Clock.unschedule(self.CalculateRandom)
		v1.value=0
		playing=0


	def listening(self,*args):
		global wheel
		global randombutmode
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if randombutmode==0: pass
		if randombutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				randombutmode=0
				self.b003.state='normal'
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			#print('launched')
			Clock.schedule_interval(self.CalculateRandom, 0.002)

		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2
			Clock.unschedule(self.CalculateRandom)


	def CalculateRandom(self,*args):
		global randomcalculated
		#global resetedrandom
		count=v2.value%64
		# if count==0 and resetedrandom==0:
		# 	resetedrandom=1
		# 	self.delseq()

		if count%4==0 and randomcalculated==0:
			randomcalculated=1
			self.randomizing(count)
		elif count%4==2 and randomcalculated==1:
			randomcalculated=0
			#resetedrandom=0
		elif count%4==1 and randomcalculated==0:
			randomcalculated=1
			self.randomizing(count)

	def delseq(self):
		global sequencepool3
		print(sequencepool3[trackselected-1])
		for l in range(65):sequencepool3[trackselected-1][l]=[]
		print("deleted seq3")
		q6.put(sequencepool3[trackselected-1])

	def randomizing(self,count):
		global sequencepool3
		global Ratchetcount
		r=random.random()
		#print(count)
		#print("Random",r*100,"Desnity",RandomDensity[trackselected-1])
		#mettre le random calcu dans le else?
		if Ratchetcount>0:
			Ratchetcount-=1
		else:
			self.delstep(count+4)

			if r*100<RandomDensity[trackselected-1]:
				ratch=RandomRatchet[trackselected-1]
				Ratchetcount=RandomRatchet[trackselected-1]
				n=random.random()*100
				note=36+int(RandomTemp[trackselected-1]*n/280)
				while ratch>=0:
					#print(ratch,"ratcheting steps")
					self.delstep(count+4+ratch*4)
					sequencepool3[trackselected-1][(count+4+ratch*4)%64].append([note,1,4])
					sequencepool3[trackselected-1][(count+8+ratch*4)%64].append([note,0,4])
					sequencepool3[trackselected-1][(count+4+ratch*4)%64]=sorted(sequencepool3[trackselected-1][(count+4+ratch*4)%64],key=operator.itemgetter(1,0))
					sequencepool3[trackselected-1][(count+8+ratch*4)%64]=sorted(sequencepool3[trackselected-1][(count+8+ratch*4)%64],key=operator.itemgetter(1,0))
					ratch-=1
			q6.put(sequencepool3[trackselected-1])
				#print(sequencepool3[trackselected-1])

	def delstep(self,step):
		global sequencepool3
		for elem in sequencepool3[trackselected-1][(step)%64]:
			if elem[1]==1:
				sequencepool3[trackselected-1][(step)%64].remove(elem)
				sequencepool3[trackselected-1][(step+4)%64].remove([elem[0],0,elem[2]])
				#print(sequencepool3[trackselected-1])
				#print("deleted the sequence#####")	
			#q6.put(sequencepool3[trackselected-1])


	def label1(self, *args):
		global RandomRatchet
		positions=[57,193,327,460,594,727]
		self.sld1.value=int(args[1])
		self.lbl1.text=str(int(self.sld1.value))
		RandomRatchet[trackselected-1]=int(args[1])
		for i in range(6):
			if i==int(args[1]):
				points[int(args[1])].pos=[1000,67]
			else: points[i].pos=[positions[i],67]

	def label2(self, *args):
		global RandomTemp
		self.sld2.value=int(args[1])
		self.lbl2.text=str(int(self.sld2.value))
		RandomTemp[trackselected-1]=int(args[1])

	def label3(self, *args):
		global RandomDensity
		self.sld3.value=int(args[1])
		self.lbl3.text=str(int(self.sld3.value))
		RandomDensity[trackselected-1]=int(args[1])

	def init(self):
		self.sld1.value=RandomRatchet[trackselected-1]
		self.sld2.value=RandomTemp[trackselected-1]
		self.sld3.value=RandomDensity[trackselected-1]
		self.lbl1.text=str(RandomRatchet[trackselected-1])
		self.lbl2.text=str(RandomTemp[trackselected-1])
		self.lbl3.text=str(RandomDensity[trackselected-1])

	def reset(self):
		global RandomTemp
		global RandomDensity
		global RandomRatchet
		RandomTemp[trackselected-1]=20
		RandomDensity[trackselected-1]=20
		RandomRatchet[trackselected-1]=0
		self.init()




##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class EuclideanScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.animate, 0.002) 
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))	
			Clock.unschedule(self.animate) 				
		l1 = self.ids.w_canvas.canvas.get_group('a')[0]
		l2 = self.ids.w_canvas.canvas.get_group('b')[0]
		l3 = self.ids.w_canvas.canvas.get_group('c')[0]				
		l4 = self.ids.w_canvas.canvas.get_group('d')[0]
		l5 = self.ids.w_canvas.canvas.get_group('e')[0]
		l6 = self.ids.w_canvas.canvas.get_group('f')[0]
		l7 = self.ids.w_canvas.canvas.get_group('g')[0]
		l8 = self.ids.w_canvas.canvas.get_group('h')[0]
		l9 = self.ids.w_canvas.canvas.get_group('i')[0]
		l10 = self.ids.w_canvas.canvas.get_group('j')[0]
		l11 = self.ids.w_canvas.canvas.get_group('k')[0]				
		l12 = self.ids.w_canvas.canvas.get_group('l')[0]
		l13 = self.ids.w_canvas.canvas.get_group('m')[0]
		l14 = self.ids.w_canvas.canvas.get_group('n')[0]
		l15 = self.ids.w_canvas.canvas.get_group('o')[0]
		l16 = self.ids.w_canvas.canvas.get_group('p')[0]
		c1 = self.ids.w_canvas.canvas.get_group('q')[0]	
		g1 = self.ids.w_canvas.canvas.get_group('r')[0]	
		g2 = self.ids.w_canvas.canvas.get_group('s')[0]	
		g3 = self.ids.w_canvas.canvas.get_group('t')[0]
		g4 = self.ids.w_canvas.canvas.get_group('u')[0]	
		g5 = self.ids.w_canvas.canvas.get_group('v')[0]	
		g6 = self.ids.w_canvas.canvas.get_group('w')[0]	
		g7 = self.ids.w_canvas.canvas.get_group('x')[0]
		g8 = self.ids.w_canvas.canvas.get_group('y')[0]
		g9 = self.ids.w_canvas.canvas.get_group('z')[0]	
		g10 = self.ids.w_canvas.canvas.get_group('z1')[0]	
		g11 = self.ids.w_canvas.canvas.get_group('z2')[0]
		g12 = self.ids.w_canvas.canvas.get_group('z3')[0]
		g13 = self.ids.w_canvas.canvas.get_group('z4')[0]	
		g14 = self.ids.w_canvas.canvas.get_group('z5')[0]	
		g15 = self.ids.w_canvas.canvas.get_group('z6')[0]
		g16 = self.ids.w_canvas.canvas.get_group('z7')[0]	
		global items
		global itemscolor
		items=[l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16]
		itemscolor=[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15,g16]		
		global trackmode
		global loopsize
		if trackmode[trackselected-1]!=5:
			clearsequence()
			deleteLFO()
			deleteADSR()
		trackmode[trackselected-1]=5
		print('trackmode',trackmode[trackselected-1])
		global euclibutmode
		euclibutmode=0
		self.mode(0)
		print(trackselected-1)
		#self.posbutton()
		self.init()
		self.b006.text=str(trackselected)+ ":EUCLIDEAN"
		if y1.value!=0:self.b0003.pos=185,419
		else:self.b0003.pos=1185,419
		
	def projectmode(self):
		if projectmode==0:self.manager.current = 'song_mode'
		else:self.manager.current = 'MixerScreen'

	def projectmdoedisplay(self):
		if projectmode==0:self.b008.text= 'SONG'
		else:self.b008.text= 'LIVE'		

	def init(self):
		#print("here")
		self.label2()
		self.label1()
		self.posbutton()
		self.LoopSdisplay()



	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


	def displayinfo(self):
		global manuelmodeeucli
		if manuelmodeeucli==0:
			manuelmodeeucli=1
			self.b016.text="MANUAL: ON"
		else:
			manuelmodeeucli=0
			self.b016.text="MANUAL: OFF"
		self.posbutton()





	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,360
			self.b009.pos= 648,301
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b016.pos= 344,900	
			self.b013.pos= 344,900	
			self.b017.pos= 496,900		
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.projectmdoedisplay()
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b011.pos= 496,360
			self.b012.pos= 496,301
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b013.pos= 344,900
			self.b014.pos= 496,242	
			self.b015.pos= 496,183	
			self.b016.pos= 344,900
			self.b017.pos= 496,124			
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
		else:
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b017.pos= 496,900

	def tools(self):
		if self.b005.state=="down":
			self.b013.pos= 344,360		
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b016.pos= 344,301
			self.b017.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
		else:
			self.b013.pos= 344,900	
			self.b016.pos= 344,900		
			self.b010.pos= 1000,0	


	def mode(self,num):
		global euclibutmode
		if num==0:
			self.b003.state='normal'
			self.b004.state='normal'
		if num==2:
			if euclibutmode==2:
				euclibutmode=0
				self.b003.state='normal'
			else:
				euclibutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if euclibutmode==3:
				euclibutmode=0
				self.b004.state='normal'
			else:
				euclibutmode=3
				self.b004.state='down'
				w2.value=0
		print(("buton mode",euclibutmode))



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()



	def listening(self,*args):
		global wheel
		global euclibutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if euclibutmode==0: pass
		if euclibutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				euclibutmode=0
				self.b003.state='normal'

		if euclibutmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<16*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)
						self.LoopSdisplay()				
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>16:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()
			if encoderpushed==1:
				euclibutmode=0
				self.b004.state='normal'

		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			Clock.schedule_interval(self.animate, 0.002) 
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2
			Clock.unschedule(self.animate)

	def LoopSdisplay(self):
		#self.l1.text=str(loopsize[trackselected-1]/16)
		self.b004.text=str(loopsize[trackselected-1]/16)



	def update1(self, *args):
		global stepeucli
		stepeucli[trackselected-1]=int(args[1])

	def update2(self, *args):
		global pulseeucli
		pulseeucli[trackselected-1]=int(args[1])
		#print(pulseeucli) 

	def label1(self):
		self.sld1.value=stepeucli[trackselected-1]
		self.lbl1.text=str(int(stepeucli[trackselected-1]))

	def label2(self):
		self.sld2.value=pulseeucli[trackselected-1]
		self.lbl2.text=str(int(pulseeucli[trackselected-1]))
		#print("lsd2",self.sld2.value)

	def posbutton(self):
		#print("pos")
		r=170
		step = stepeucli[trackselected-1]
		teta=2*pi/step
		for n in range(16):
			if n<step:
				items[n].pos=[r*sin((n)*teta)+520, r*cos((n)*teta)+200]
			else:
				items[n].pos=[1000,1000]
		self.colorbutton()

	def manueloff(self):
		global manuelmodeeucli
		manuelmodeeucli=0  
		self.b016.text="MANUAL: OFF"


	def colorbutton(self, *args):
		r=170
		step = stepeucli[trackselected-1]
		teta=2*pi/step
		if manuelmodeeucli==0:
			self.Eucli() 
			#print("Calling Eucli")
		for i in range(16):
			if EucliPool2[trackselected-1][i] == 1:
				itemscolor[i].pos=[r*sin((i)*teta)+520, r*cos((i)*teta)+200]
			else:
				itemscolor[i].pos=[1000,1000]

	def reposition(self):
		r=170
		step = stepeucli[trackselected-1]
		teta=2*pi/step
		for n in range(16):
			if n<step:
				items[n].pos=[r*sin((n)*teta)+520, r*cos((n)*teta)+200]
			else:
				items[n].pos=[1000,1000]
		for i in range(16):
			if EucliPool2[trackselected-1][i] == 1:
				itemscolor[i].pos=[r*sin((i)*teta)+520, r*cos((i)*teta)+200]
			else:
				itemscolor[i].pos=[1000,1000]



	def Eucli(self):
		global EucliPool2
		steps=stepeucli[trackselected-1]
		pulses=pulseeucli[trackselected-1]
		#print(steps, pulses)
		count=0	
		ResultOffset=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		Result=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		ResultC=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		for i in range(steps):
			count=count+pulses
			if count>=steps:
				count=count%steps
				Result[i]=1
		for j in range(steps):
			ResultC[j]=Result[(j-1)%steps]
		for i in range(steps):
			ResultOffset[i]=ResultC[(i-EucliOffset[trackselected-1])%steps]
		#print("ResultOffset",ResultOffset)
		EucliPool2[trackselected-1]=ResultOffset
		self.convert2to3()


	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.animate, 0.002) 
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			Clock.unschedule(self.animate)
			v1.value=2 


	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		Clock.unschedule(self.animate)
		v1.value=0
		playing=0


	def animate(self, *args):
		counter=(v2.value-1)%loopsize[trackselected-1]
		#while counter>=loopsize[trackselected-1]:counter-=loopsize[trackselected-1]
		if counter%4==0:
			#self.posbutton()
			self.reposition()
			button_number=int((counter/4)%stepeucli[trackselected-1])
			color_number=button_number
			anim1 = Animation(pos=[itemscolor[color_number].pos[0]-10,itemscolor[color_number].pos[1]-10],size=(40, 40),duration =0.1)+Animation(pos=[itemscolor[color_number].pos[0]+0,itemscolor[color_number].pos[1]+0],size=(20, 20),duration =0.1)
			anim2 = Animation(pos=[items[button_number].pos[0]-5,items[button_number].pos[1]-5],size=(30, 30),duration =0.1)+Animation(pos=[items[button_number].pos[0]+0,items[button_number].pos[1]+0],size=(20, 20),duration =0.1)	
			anim2.start(items[button_number])
			#print("but number", button_number, "Result", Result,(button_number-offset)%stepeucli[trackselected-1])
			if EucliPool2[trackselected-1][color_number]==1:
				#print("animating")
				anim1.start(itemscolor[color_number])

	def on_touch_move(self, touch):
		rayon=20
		global ChangedEucli
		global EucliPool2
		global EucliOffset
		for i in range(stepeucli[trackselected-1]):
				if (items[i].pos[0] - rayon) <= touch.pos[0] <= (items[i].pos[0] + rayon):
					if (items[i].pos[1] - rayon) <= touch.pos[1] <= (items[i].pos[1] + rayon):
						#print(i)
						if self.b016.text=="MANUAL: ON":
							if ChangedEucli==0:
								color_number=(i)%stepeucli[trackselected-1]
								ChangedEucli=1
								if EucliPool2[trackselected-1][color_number]==0:
									EucliPool2[trackselected-1][color_number]=1
									#itemscolor[color_number].pos=[r*sin((color_number)*teta)+520, r*cos((color_number)*teta)+200]
								else:
									EucliPool2[trackselected-1][color_number]=0
									#itemscolor[color_number].pos=[1000,1000]
								self.colorbutton()

								#print("EucliPool2",EucliPool2[trackselected-1])
						else:
							EucliOffset[trackselected-1]=(i)%stepeucli[trackselected-1]
							self.posbutton()
						self.convert2to3()
						break

		else:
			ChangedEucli=0

				
	def Reset(self):
		global pulseeucli
		global stepeucli
		global EucliOffset
		global EucliPool2
		self.manueloff()
		pulseeucli[trackselected-1]=1
		stepeucli[trackselected-1]=7
		EucliOffset[trackselected-1]=0
		self.posbutton()
		self.init()


	def convert2to3(self):
		global sequencepool3
		#print("converting")
		#print('euclippol2',EucliPool2)
		for l in range(64*4+1):sequencepool3[trackselected-1][l]=[]
		for i in range(64):
			if EucliPool2[trackselected-1][i%stepeucli[trackselected-1]]==1:
				sequencepool3[trackselected-1][i*4].append([36,1,4])
				sequencepool3[trackselected-1][i*4+4].append([36,0,4])
				sequencepool3[trackselected-1][i*4]=sorted(sequencepool3[trackselected-1][i*4],key=operator.itemgetter(1,0))
				sequencepool3[trackselected-1][i*4+4]=sorted(sequencepool3[trackselected-1][i*4+4],key=operator.itemgetter(1,0))
				
				#sequencepool3[trackselected-1][(i+stepeucli[trackselected-1])*4].append([36,1,4])
				#sequencepool3[trackselected-1][(i+8)*4+4].append([36,0,4])
				#sequencepool3[trackselected-1][(i+8)*4]=sorted(sequencepool3[trackselected-1][i*4],key=operator.itemgetter(1,0))
				#sequencepool3[trackselected-1][(i+8)*4+4]=sorted(sequencepool3[trackselected-1][i*4+4],key=operator.itemgetter(1,0))
				
		q6.put(sequencepool3[trackselected-1])

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class MixerScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))											
		global loopsize
		global livebutmode
		livebutmode=0
		self.mode(0)
		print(trackselected-1)
		self.infos()
		global loopsizeS
		self.b004.text=str(loopsizeS/64)
		global listbuttonlive
		listbuttonlive=[self.b01,self.b02,self.b03,self.b04,self.b05,self.b06,self.b07,self.b08,self.b09,self.b0100,self.b0110,self.b0120,self.b0130,self.b01400,self.b0150,self.b0160]
		if loopsizeS>32*64:
			loopsizeS=32*64
			v3.value=loopsizeS
			self.mute()
		global projectmode
		if projectmode==0:
			projectmode=1
			for i,elem in enumerate(listbuttonlive):elem.state='normal'
			self.mute()
		self.safedisplay()

	def safemode(self):
		global safemode
		if safemode==0:safemode=1
		else:safemode=0
		self.safedisplay()

	def safedisplay(self):
		if safemode==1:self.b1234.pos= 496,419
		else:self.b1234.pos= 496,919


	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule livemode")


	def menu(self):
		if self.b007.state=="down":
			self.b008.pos= 648,900
			self.b009.pos= 648,360
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b013.pos= 344,900		
			self.b006.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b0141.pos= 496,900
			self.b0142.pos= 344,900
			self.b013.pos= 496,900
		else:
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b010.pos= 1000,0


	def seqmode(self):
		if self.b006.state=="down":
			self.b008.pos= 496,360
			self.b009.pos= 648,900
			self.b013.pos= 344,900		
			self.b007.state="normal"
			self.b005.state="normal"
			self.b010.pos= 0,0
			self.b0140.pos= 344,900	
			self.b0141.pos= 496,301
			self.b0142.pos= 344,900
			self.b013.pos= 496,900
		else:
			self.b008.pos= 496,900
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b010.pos= 1000,0
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b0141.pos= 496,900


	def tools(self):
		if self.b005.state=="down":
			self.b0142.pos= 344,301
			self.b0141.pos= 496,900
			self.b0140.pos= 344,360	
			self.b013.pos=	344,242
			self.b011.pos= 496,900
			self.b012.pos= 496,900
			self.b014.pos= 496,900
			self.b015.pos= 496,900
			self.b008.pos= 648,900
			self.b009.pos= 648,900
			self.b007.state="normal"
			self.b006.state="normal"
			self.b010.pos= 0,0
		else:
			self.b0142.pos= 344,900
			self.b0140.pos= 344,900	
			self.b013.pos= 496,900		
			self.b010.pos= 1000,0	


	def mode(self,num):
		global livebutmode
		if num==2:
			if livebutmode==2:
				livebutmode=0
				self.b003.state='normal'
			else:
				livebutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if livebutmode==3:
				livebutmode=0
				self.b004.state='normal'
			else:
				livebutmode=3
				self.b004.state='down'
				w2.value=0
		if num==0:
			livebutmode=0
			self.b003.state='normal'
			self.b004.state='normal'
		print("livebutmode mode",livebutmode)



	def closemenus(self):
		if self.b007.state=="down":
			self.b007.state="normal"
			self.menu()
		if self.b006.state=="down":
			self.b006.state="normal"
			self.seqmode()
		if self.b005.state=="down":
			self.b005.state="normal"
			self.tools()

	def start(self):
		global playing
		if self.b001.state=="down":
			v1.value=1
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2


	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0


	def listening(self,*args):
		global wheel
		global livebutmode
		global loopsize
		global BPM
		global loopsizeS
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		if livebutmode==0: pass
		if livebutmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM
			if encoderpushed==1:
				livebutmode=0
				self.b003.state='normal'

		if livebutmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS<32*64:
						loopsizeS+=64
						v3.value=loopsizeS
						self.mute()
						self.b004.text=str(loopsizeS/64)
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS>64:
						loopsizeS-=64
						v3.value=loopsizeS
						self.mute()
						self.b004.text=str(loopsizeS/64)
			if encoderpushed==1:
				livebutmode=0
				self.b004.state='normal'

		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2

	def displayinfo(self):
		global displayinfolive
		if displayinfolive==0:
			displayinfolive=1
			self.b0140.text="INFOS: ON"
		else:
			displayinfolive=0
			self.b0140.text="INFOS: OFF"
		self.infos()


	def infos(self):
		listinfo=[self.lbl16,self.lbl15,self.lbl14,self.lbl13,self.lbl12,self.lbl11,self.lbl10,self.lbl9,self.lbl8,self.lbl7,self.lbl6,self.lbl5,self.lbl4,self.lbl3,self.lbl2,self.lbl1]
		if displayinfolive==1:
			self.lbl16.pos=55,288
			self.lbl15.pos=255,288
			self.lbl14.pos=455,288
			self.lbl13.pos=655,288
			self.lbl12.pos=55,183
			self.lbl11.pos=255,183
			self.lbl10.pos=455,183
			self.lbl9.pos=655,183
			self.lbl8.pos=55,78
			self.lbl7.pos=255,78
			self.lbl6.pos=455,78
			self.lbl5.pos=655,78
			self.lbl4.pos=55,-27
			self.lbl3.pos=255,-27
			self.lbl2.pos=455,-27
			self.lbl1.pos=655,-27
			for n,elem in enumerate(listinfo):
				if trackmode[n]==1: 
					elem.text="SEQUENCE"
				elif trackmode[n]==2: 
					elem.text="LFO"
				elif trackmode[n+rangeYs]==3: 
					for i,value in enumerate(ADSRtrig):
						if value==n+rangeYs+1:
							elem.text="ADSR (TRIG: " + str(i+1) +")"
							break
						else:
							elem.text="ADSR (NO TRIG)"
				elif trackmode[n]==4: 
					elem.text="RANDOM"
				elif trackmode[n]==5: 
					elem.text="EUCLIDEAN"
		else:
			for n,elem in enumerate(listinfo):
				elem.pos[0]=1000


	def displayedit(self):
		global displayeditlive
		if displayeditlive==0:
			displayeditlive=1
			self.b0142.text="EDIT: ON"
		else:
			displayeditlive=0
			self.b0142.text="EDIT: OFF"
		self.edit()

	def edit(self):
		listedit=[self.e01,self.e02,self.e03,self.e04,self.e05,self.e06,self.e07,self.e08,self.e09,self.e010,self.e011,self.e012,self.e013,self.e014,self.e015,self.e016]
		if displayeditlive==1:
			self.e01.pos=2,373
			self.e02.pos=201,373
			self.e03.pos=401,373
			self.e04.pos=601,373
			self.e05.pos=2,269
			self.e06.pos=201,269
			self.e07.pos=401,269
			self.e08.pos=601,269
			self.e09.pos=2,164
			self.e010.pos=201,164
			self.e011.pos=401,164
			self.e012.pos=601,164
			self.e013.pos=2,59
			self.e014.pos=201,59
			self.e015.pos=401,59
			self.e016.pos=601,59
		else:
			for n,elem in enumerate(listedit):
				elem.pos[0]=1000

	def mute(self,*args):
		global song
		for i in range(64):song[i]=[]
		print(song)
		for i,elem in enumerate(listbuttonlive):
			self.mutechannel(i+1,elem.state)
			#print("elem",elem.state)
		print(song)	
		q3.put(song)

	def mutechannel(self,channel,status):
		global song
		if status=='normal':
			print(channel, "muted")
		else:
			print(channel, 'playing')
			for i in range(loopsizeS/64):
				song[i].append(channel)


	def changescreen(self, channel):
		global trackselected
		trackselected=channel
		print('trackselected',trackselected)
		r2.put(trackselected)
		s2.put(trackselected)		
		v5.value=trackselected
		if trackmode[channel-1]==1: 
			self.manager.current = 'piano_roll'
		elif trackmode[channel-1]==2: 
			self.manager.current = 'LFOScreen'
		elif trackmode[channel-1]==3: 
			self.manager.current = 'ADSRScreen'
		elif trackmode[channel-1]==4: 
			self.manager.current = 'RandomScreen'
		elif trackmode[channel-1]==5: 
			self.manager.current = 'EuclideanScreen'



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

class Timing():


	def Timer(self,v1,v2,v3,v4,v5,v6,v7,v8,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12):
		nextcall=time.time()
		count=0
		MIDIstoped=0
		paused=0
		portopened=0
		dininreset=0
		while 1:
			BPM=v4.value
			interval=float(60/Decimal(BPM)/Decimal(16))
			v2.value=count
			trackselected=v5.value
			while q1.empty() is False:
					sequencepool2=q1.get()
					#print('sequencepool2', sequencepool2)
			while q2.empty() is False:
					loopsize=q2.get()
					#print(('loopsize', loopsize))
			while q3.empty() is False:
					song=q3.get()
					#print(('song', song))
			while q4.empty() is False:
					Sendinfo=q4.get()
					#print(('sendinfo', Sendinfo))
			while q5.empty() is False:
					Syncinfo=q5.get()
					#print(('Syncinfo',Syncinfo))
			while q6.empty() is False:
					update3=q6.get()
					sequencepool3[trackselected-1]=update3
					#print("track",trackselected-1,'sequencepool3queue', sequencepool3[trackselected-1])
			while q7.empty() is False:
					UpdateEnvPool3=q7.get()
					EnvPool3[trackselected-1]=UpdateEnvPool3
					#print('EnvPool3.track', EnvPool3[trackselected-1])
			while q8.empty() is False:
					UpdateADSRool3=q8.get()
					ADSRPool3[trackselected-1]=UpdateADSRool3
					#print('UpdateADSRool3.track', ADSRPool3[trackselected-1])
			while q9.empty() is False:
					ADSRtrig=q9.get()
					#print('ADSRtrig', ADSRtrig)			
			while q10.empty() is False:
					sequencepool3=q10.get()
					#print('sequencepool3queue', sequencepool3)
			while q11.empty() is False:
					EnvPool3=q11.get()
					#print('EnvPool3', EnvPool3)
			while q12.empty() is False:
					ADSRPool3=q12.get()
					#print('UpdateADSRool3', ADSRPool3)




			if rpi==1 and Syncinfo[4]==0:
				available_ports = midiout.get_ports()
				port = available_ports[0]
				if len(available_ports)>1: port = available_ports[1]
				try:port = mido.open_output(port)
				except:print("error usb out port",port)
			else:
				port=0

			if v1.value==1:
				if MIDIstoped==1 and paused==0:
					self.MIDImessage(250,Syncinfo)
					self.USBmessage("start",Syncinfo,port)
					self.jacksyncstart(Syncinfo,BPM)

				if paused==1:
					paused=0
					self.MIDImessage(251,Syncinfo)
					self.USBmessage("continue",Syncinfo,port)
					self.jacksyncstart(Syncinfo,BPM)
				MIDIstoped=0
				count+=1
				if count > v3.value:
					count=1
				nextcall = nextcall+interval
				self.send2(count,sequencepool3,loopsize,song,Sendinfo,port,Syncinfo,ADSRtrig,EnvPool3,ADSRPool3)
				
				if y1.value!=0:
					while v7.value < 1 and y1.value!=0:
						if v8.value==0 and dininreset==0:
							count=0
							dininreset=1
							v8.value=1
							print('here')
						else:dininreset=0
						#pass
					v7.value-=1

				else:
					#print("available time",(nextcall-time.time()))
					if nextcall-time.time()>0:
						if nextcall-time.time()>interval/2+0.004:
							#print("waiting:",nextcall-time.time()-interval/2)
							time.sleep(nextcall-time.time()-interval/2)
							self.midlfo(count,EnvPool3,loopsize,song,Sendinfo)
							self.midadsr(count,ADSRPool3,loopsize,song,Sendinfo)
							self.midsendCV()
							#print("sleeping",(nextcall-time.time()))
							#time.sleep(nextcall-time.time())
						if nextcall-time.time()>0: time.sleep(nextcall-time.time())
						else: nextcall=time.time()
					else:
						nextcall=time.time()





			elif v1.value==2:
				paused=1
				if MIDIstoped==0:
					self.MIDImessage(252,Syncinfo)
					self.USBmessage("stop",Syncinfo,port)
					self.jacksyncstop()
					MIDIstoped=1
					#self.stopCV()
					for i in range(0,16):
						self.noteoffUSB(i,Sendinfo,port)
						self.noteoffMIDI(i,Sendinfo)
			else:
				if MIDIstoped==0 or paused==1:
					MIDIstoped=1
					paused=0
					self.MIDImessage(252,Syncinfo)
					self.USBmessage("stop",Syncinfo,port)
					self.jacksyncstop()
					#self.stopCV()
					global ADSRcounter
					ADSRcounter=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
					for i in range(0,16):
						self.noteoffUSB(i,Sendinfo,port)
						self.noteoffMIDI(i,Sendinfo)
				count=0
			time.sleep(0.0005)



	def send2(self,count,sequencepool3,loopsize,song,Sendinfo,port,Syncinfo,ADSRtrig,EnvPool3,ADSRPool3):
		for n,track in enumerate(sequencepool3): #n is track number
			pos=count%loopsize[n]-1
			if pos==-1: pos=loopsize[n]-1
			if pos==0:
				if n+1 in song[int(count/(16*4))-1]:
					#print(("All Notes Off on track: ",n+1))
					if Sendinfo[n][6]==1: self.noteoffUSB(n,Sendinfo,port)
					if Sendinfo[n][6]==2: self.noteoffMIDI(n,Sendinfo)
				if n+1 in song[int(v3.value/(16*4))-1] and count==1:
					#print(("All Notes Off on track (looped): ",n+1))
					if Sendinfo[n][6]==1: self.noteoffUSB(n,Sendinfo,port)
					if Sendinfo[n][6]==2: self.noteoffMIDI(n,Sendinfo)
			if n+1 in song[int(count/(16*4))]:
				#print(pos)
				if EnvPool3[n][pos]!=[]:
					#print(n,EnvPool3[n][pos])
					if Sendinfo[n][9]>0:self.CVsendLFO(n,EnvPool3[n][pos],Sendinfo)
				if len(track[pos])>0:
					if ADSRtrig[n]!=0:
						for elem in track[pos]:
							if elem[1]==1:
								self.CVlaunchADSR(ADSRtrig[n])
								break
					for elem in track[pos]:
						if Sendinfo[n][6]==1: self.USBsend2(n,elem,Sendinfo,port)
						if Sendinfo[n][6]==2: self.MIDIsend2(n,elem,Sendinfo)
						if Sendinfo[n][1]>0: self.CVsendPitch2(n,elem,Sendinfo)
						if Sendinfo[n][3]>0: self.CVsendGate2(n,elem,Sendinfo)
				if ADSRcounter[n]>0:
					if Sendinfo[n][12]>0:self.CVsendADSR(n,ADSRPool3,Sendinfo,loopsize)
			#if count%64==0 and n+1 not in song[int(count/(16*4))] and n+1 in song[int(count/(16*4))-1]
			#	print("All Notes Off song mode change")
			#	if Sendinfo[n][6]==1: self.noteoffUSB(n,Sendinfo,port)
			#	if Sendinfo[n][6]==2: self.noteoffMIDI(n,Sendinfo)
		self.sendCV()

		if count%2==0:
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)
		else:
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)

	def midlfo(self,count,EnvPool3,loopsize,song,Sendinfo):
		for n,lfo in enumerate(EnvPool3):
			if n+1 in song[int(count/(16*4))]:
				pos=count%loopsize[n]-1
				if EnvPool3[n][pos]!=[] and EnvPool3[n][pos+1]!=[]:
					#print(n,EnvPool3[n][pos])
					#if Sendinfo[n][9]>0:self.CVsendLFO(n,EnvPool3[n][pos],Sendinfo)
					if Sendinfo[n][9]>0:
						elem=(EnvPool3[n][pos]+EnvPool3[n][pos+1])/2
						#print("sending LFO:", "loopsize:" , loopsize[n],"pos",pos,"value",elem)
						if elem!=[]:
							a,b=divmod(4096*(elem+5.00)/15,256)
							#print(('CV LFO',Sendinfo[n][9],Sendinfo[n][10], 'Value',elem))
							CVsends2.append([Sendinfo[n][9],Sendinfo[n][10],[int(a), int(b)],Sendinfo[n][11]])

	def midadsr(self,count,ADSRPool3,loopsize,song,Sendinfo):
		for n,adsr in enumerate(EnvPool3):
			if ADSRcounter[n]>0:
				if Sendinfo[n][12]>0:
					if 2<ADSRcounter[n]<loopsize[n]+1: 
						#elem=(ADSRPool3[n][ADSRcounter[n]-2]+ADSRPool3[n][ADSRcounter[n]-1])/4.0
						elem=(ADSRPool3[n][ADSRcounter[n]-2]+ADSRPool3[n][ADSRcounter[n]-1])/2.0
						#print("adsr",elem)
						if elem!=[] and elem!=0:
							a,b=divmod(4096*(elem+5.00)/15,256)		
							CVsends2.append([Sendinfo[n][12],Sendinfo[n][13],[int(a), int(b)],Sendinfo[n][14]])
							#print("elem added")

	def midsendCV(self):
		global CVsends2
		CVsends2=sorted(CVsends2, key = lambda x: x[3])
		dacregister2=[[],[],[]]
		for elem in CVsends2:
			if elem[0]==0x61: dacregister2[0].append([elem[0],elem[1],elem[2]])
			if elem[0]==0x62: dacregister2[1].append([elem[0],elem[1],elem[2]])
			if elem[0]==0x60: dacregister2[2].append([elem[0],elem[1],elem[2]])									
		#print("dacregisteres",dacregister2)
		#print("Sendinfo",Sendinfo)
		CVsends2=[]
		try:
			for dac in dacregister2:
				if len(dac)==1:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], dac[0][2])
					#print(dac[0][0], dac[0][1], dac[0][2])
				if len(dac)==2:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
				if len(dac)==3:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1]])
				if len(dac)==4:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1],dac[3][1], dac[3][2][0],dac[3][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1],dac[3][1], dac[3][2][0],dac[3][2][1]])
		except: print("error dac registers")




	def sendCV(self):
		global CVsends
		global CVdelayed
		CVsends=sorted(CVsends, key = lambda x: x[3])
		#print("Cv sends:",CVsends)
		#print("CV delayed", CVdelayed)
		dacregister=[[],[],[]]
		for elem in CVsends:
			if elem[0]==0x61: dacregister[0].append([elem[0],elem[1],elem[2]])
			if elem[0]==0x62: dacregister[1].append([elem[0],elem[1],elem[2]])
			if elem[0]==0x60: dacregister[2].append([elem[0],elem[1],elem[2]])									
		CVsends=CVdelayed
		CVdelayed=[]
		#print("dacregisteres",dacregister)
		#print("Sendinfo",Sendinfo)
		try:
			for dac in dacregister:
				if len(dac)==1:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], dac[0][2])
					#print(dac[0][0], dac[0][1], dac[0][2])
				if len(dac)==2:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
				if len(dac)==3:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1]])
				if len(dac)==4:
					if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1],dac[3][1], dac[3][2][0],dac[3][2][1]])
					#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1],dac[2][1], dac[2][2][0],dac[2][2][1],dac[3][1], dac[3][2][0],dac[3][2][1]])
		except: print("error dac registers")

	def stopCV(self):
		global CVsends
		CVsends=[]
		i=0
		a,b=divmod(4096*(5.00)/15,256)
		while i <12:
			CVsends.append([CVinfo[i][0],CVinfo[i][1],[int(a), int(b)],CVinfo[i][2]])
			i+=1
		#print(CVsends)
		self.sendCV()



	def CVsendLFO(self,n,elem,Sendinfo):
		if elem!=[]:
			a,b=divmod(4096*(elem+5.00)/15,256)
			#print(('CV LFO',Sendinfo[n][9],Sendinfo[n][10], 'Value',elem))
			CVsends.append([Sendinfo[n][9],Sendinfo[n][10],[int(a), int(b)],Sendinfo[n][11]])
			
	def CVlaunchADSR(self,trigering):
		global ADSRcounter
		ADSRcounter[trigering-1]=1
		#print("launch counter ADSR",trigering)
		#print(ADSRcounter)

	def CVsendADSR(self,n,ADSRPool3,Sendinfo,loopsize):
		global ADSRcounter
		if ADSRcounter[n]<loopsize[n]+1:ADSRcounter[n]+=1
		else:ADSRcounter[n]=2
		#print("adsr counter",ADSRcounter)
		#print("ADSR",ADSRPool3[n][ADSRcounter[n]-2]/2.0)
		#elem=ADSRPool3[n][ADSRcounter[n]-2]/2.0
		elem=ADSRPool3[n][ADSRcounter[n]-2]
		#print("ADSR",elem)
		if elem!=[]:
			a,b=divmod(4096*(elem+5.00)/15,256)		
			CVsends.append([Sendinfo[n][12],Sendinfo[n][13],[int(a), int(b)],Sendinfo[n][14]])
			#print(CVsends)


	def resetADSRcounter(self,n):
		global ADSRcounter
		ADSRcounter[n]=0
		#print(ADSRcounter)


	def noteoffUSB(self,n,Sendinfo,port):
		#print("note off USB")
		channel=Sendinfo[n][0]-1
		msg=mido.Message('control_change', channel=channel,control=123)
		try: port.send(msg)
		except:
			pass
			#print('(Port error note off)')

	def noteoffMIDI(self,n,Sendinfo):
		#print("note off DIN",n)
		byte1=bin(int(176+Sendinfo[n][0]-1))
		byte2=bin(int(123))
		byte3=bin(0)
		byte_chr1 = chr(int(byte1,2))
		byte_chr2 = chr(int(byte2,2))
		byte_chr3 = chr(int(byte3,2))
		if rpi==1:
			ser.write(byte_chr1)
			ser.write(byte_chr2)
			ser.write(byte_chr3)


	def MIDImessage(self,message,Syncinfo):
		#stop 252, continue 251, start 250, clock 248
		#print(message)
		if Syncinfo[0]==1:
			byte1=bin(int(message))
			#print(message)
			byte_chr1 = chr(int(byte1,2))
			if rpi==1: ser.write(byte_chr1)

	def USBmessage(self,message,Syncinfo,port):
		#stop, continue, start, clock
		if Syncinfo[1]==1:
			msg=mido.Message(message)
			#print(message)
			try:
				port.send(msg)
				#print("clock1")
				if Syncinfo[3]==2 and message=="clock":
					port.send(msg)
					#print("clock2")
			except:
				pass
				#print('(Port error message)')


	def CVsendGate2(self,n,elem,Sendinfo):
		global CVsends
		global CVdelayed
		if elem[1]==1:
			#print(('CV Gate On',Sendinfo[n][3], Sendinfo[n][4], 'Value: 8V'))
			if [Sendinfo[n][3],Sendinfo[n][4],[0x05, 0x55],Sendinfo[n][8]] in CVsends and [Sendinfo[n][3],Sendinfo[n][4],[0x0D, 0xE0],Sendinfo[n][8]] not in CVdelayed:
				CVdelayed.append([Sendinfo[n][3],Sendinfo[n][4],[0x0D, 0xE0],Sendinfo[n][8]])
			else:
				if [Sendinfo[n][3],Sendinfo[n][4],[0x0D, 0xE0],Sendinfo[n][8]] not in CVsends and [Sendinfo[n][3],Sendinfo[n][4],[0x0D, 0xE0],Sendinfo[n][8]] not in CVdelayed:
					CVsends.append([Sendinfo[n][3],Sendinfo[n][4],[0x0D, 0xE0],Sendinfo[n][8]])
		else:
			#print(('CV Gate Off',Sendinfo[n][3], Sendinfo[n][4], 'Value: 0V'))
			if [Sendinfo[n][3],Sendinfo[n][4],[0x05, 0x55],Sendinfo[n][8]] not in CVsends:		
				CVsends.append([Sendinfo[n][3],Sendinfo[n][4],[0x05, 0x55],Sendinfo[n][8]])			

	def CVsendPitch2(self,n,elem,Sendinfo):
		if elem[1]==1:
			a,b=divmod(4096*elem[0]/15/12+4096/15*Sendinfo[n][5],256)
			#print(('CV Pitch On',Sendinfo[n][1],Sendinfo[n][2], 'Value',elem[0], 'Offset' , Sendinfo[n][5]))
			if len(CVsends)>0:
				for elem in CVsends: 
					if elem [3]==Sendinfo[n][7]:break
				else: CVsends.append([Sendinfo[n][1],Sendinfo[n][2],[a, b],Sendinfo[n][7]])
			else: CVsends.append([Sendinfo[n][1],Sendinfo[n][2],[a, b],Sendinfo[n][7]])

	def MIDIsend2(self,n,elem,Sendinfo):
		if elem[1]==1:
			#print(("DIN send" , elem[0] ,"channel" , Sendinfo[n][0]))
			byte1=bin(int(128+16+Sendinfo[n][0]-1))
			byte3=bin(100)
		else:
			#print(("DIN stop" , elem[0] ,"channel" , Sendinfo[n][0]))
			byte1=bin(int(128+Sendinfo[n][0]-1))
			byte3=bin(0)
		byte2 = bin(int(24+elem[0]))
		byte_chr1 = chr(int(byte1,2))
		byte_chr3 = chr(int(byte3,2))
		byte_chr2 = chr(int(byte2,2))
		if rpi==1:
			ser.write(byte_chr1)
			ser.write(byte_chr2)
			ser.write(byte_chr3)

	def USBsend2(self,n,elem,Sendinfo,port):
		#print(port)
		channel=Sendinfo[n][0]-1
		if elem[1]==1: msg=mido.Message('note_on', note=elem[0]+24, channel=channel)
		else: msg=mido.Message('note_off', note=elem[0]+24, channel=channel)
		try: port.send(msg)
		except:
			#print('(Port error sending)')
			pass

	def jacksyncstart(self,Syncinfo,BPM):
		if rpi==1:
			GPIO.output(jackstart,GPIO.HIGH)
			pwmsync.ChangeFrequency(BPM*Syncinfo[2]/4)
			pwmsync.start(50)


	def jacksyncstop(self):
		if rpi==1:
			GPIO.output(jackstart,GPIO.LOW)
			pwmsync.stop()




##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class Listen():


	def starting(self,w1,w2):
		global clkLastState
		global swLastState
		if rpi==1:
			clkLastState = GPIO.input(clk)
			swLastState = GPIO.input(sw)
		while 1:
			self.encoder()
			time.sleep(0.001)


	def encoder(self):
		#print('listening')
		global clkLastState
		global swLastState
		if rpi==1:
			clkState = GPIO.input(clk)
			dtState = GPIO.input(dt)
			if clkState != clkLastState:
				if dtState != clkState: w1.value+=-1
				else: w1.value+=1
			clkLastState = clkState

			swstate =GPIO.input(sw)
			if swstate != swLastState:
				if swstate==0:
					if w2.value==1: w2.value=0
					else: w2.value=1
			swLastState=swstate







class Listen2():


	def starting(self,r1,r2,r3,r4,x1,y1):
		global midibyte
		global messagemidi
		global Syncmessage
		midibyte=0
		Syncmessage=0
		messagemidi = [0, 0, 0]
		#print("listen2")	
		while 1:
			while r1.empty() is False:
				Sendinfo=r1.get()
				#print(('Sendinfo', Sendinfo))
			while r2.empty() is False:
				trackselected=r2.get()
				#print(('trackselected', trackselected))
			while r3.empty() is False:
				Syncinfo=r3.get()
				#print(('Syncinfo2', Syncinfo))	
			#print("listen2")		
			self.MIDIdinIn(Sendinfo,trackselected,Syncinfo)
			time.sleep(0.001)
			


	def MIDIdinIn(self,Sendinfo,trackselected,Syncinfo):
		global midibyte
		if rpi==1:
			while midibyte < 3:
				data = ord(ser.read(1)) # read a byte
				#print(data)
				if data==250 or data==251 or data==252 or data==248:
				#	self.DINsyncout(data,Syncinfo)
					if x1.value==1 or y1.value==2:self.DINsyncin(data)
				if data >> 7 != 0:
					midibyte = 0      # status byte!   this is the beginning of a midi message!
				messagemidi[midibyte] = data
				midibyte += 1
			midibyte=0
			messagetype = messagemidi[0] >> 4
			messagechannel = (messagemidi[0] & 15) + 1
			note = messagemidi[1] if len(messagemidi) > 1 else None
			velocity = messagemidi[2] if len(messagemidi) > 2 else None
			if messagetype==8 or messagetype==9 or messagetype==11:
				#self.ThroughDin([messagetype,note,velocity],Sendinfo,trackselected)
				if x1.value==1:self.ThroughCV([messagetype,note,velocity],Sendinfo,trackselected)
			if messagetype==9:
				if x1.value==1:self.DinINRec(note)

	def DinINRec(self,note):
		#print(note)
		r4.put(note)

	def DINsyncin(self,message):
		global Syncmessage
		#print("DINSYNCIN message!!",x1.value)
		if v6.value==0 or 1:
			v6.value=2
		if message==250 and y1.value==2:
			print("PLAY")
			v2.value=0
			v1.value=1
			v8.value=0
			Syncmessage=0
			
		if message==251 and y1.value==2:
			#print("CONTINUE")
			v1.value=1
			v6.value=1
			#print("STOP")
			#v1.value=0
			#v6.value=0
		# if message==252:
		# 	#print("STOP")
		# 	#pass
		# 	if y1.value==0:
		# 		v1.value=0
		# 		v6.value=0
		if message==248 and v1.value==1:
			if y1.value==2:
				Syncmessage+=1
				if Syncmessage==1:
					v7.value+=1
				if Syncmessage==3:
					v7.value+=1
					Syncmessage=0
			else:
				Syncmessage=0


	def DINsyncout(self,message,Syncinfo):
		if Syncinfo[0]==1:
			byte1=bin(int(message))
			byte_chr1 = chr(int(byte1,2))
			if rpi==1: ser.write(byte_chr1)
		if message==250: print("PLAY")
		if message==251: print("PAUSE")
		if message==252: print("STOP")


	def ThroughDin(self,Message,Sendinfo,trackselected):
		if Message[0]==9:
			#print("send" , Message)
			byte1=bin(int(128+16+Sendinfo[trackselected-1][0]-1))
			byte3=bin(100)
		if Message[0]==8:
			#print("stop" , Message)
			byte1=bin(int(128+Sendinfo[trackselected-1][0]-1))
			byte3=bin(0)
		if Message[0]==11:
			#print("stop all notes" , Message)
			byte1=bin(int(176+Sendinfo[trackselected-1][0]-1))
			byte3=bin(0)
		byte2 = bin(int(Message[1]))
		byte_chr1 = chr(int(byte1,2))
		byte_chr3 = chr(int(byte3,2))
		byte_chr2 = chr(int(byte2,2))
		ser.write(byte_chr1)
		ser.write(byte_chr2)
		ser.write(byte_chr3)

	def ThroughCV(self,Message,Sendinfo,trackselected):
		#print(Message)
		Tosend=[]
		if Sendinfo[trackselected-1][3]>0:
			if Message[0]==0x90: Tosend.append([Sendinfo[trackselected-1][3], Sendinfo[trackselected-1][4], [0x0D, 0xE0],Sendinfo[trackselected-1][8]])
			if Message[0]==0x80: Tosend.append([Sendinfo[trackselected-1][3], Sendinfo[trackselected-1][4], [0x05, 0x55],Sendinfo[trackselected-1][8]])
		if Sendinfo[trackselected-1][1]>0:
			if Message[0]==0x90 and (Message[1]-24)>0 and (Message[1]-24)<96 :
				a,b=divmod(4096*(Message[1]-24)/15/12+4096/15*Sendinfo[trackselected-1][5],256)
				Tosend.append([Sendinfo[trackselected-1][1], Sendinfo[trackselected-1][2], [a, b],Sendinfo[trackselected-1][7]])
		if len(Tosend)>0:
			Tosend=sorted(Tosend, key = lambda x: x[3])
			#print(Tosend)
			dacregister=[[],[],[]]
			for elem in Tosend:
				if elem[0]==0x61: dacregister[0].append([elem[0],elem[1],elem[2]])
				if elem[0]==0x62: dacregister[1].append([elem[0],elem[1],elem[2]])
				if elem[0]==0x60: dacregister[2].append([elem[0],elem[1],elem[2]])	
			try:
				for dac in dacregister:
					if len(dac)==1:
						if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], dac[0][2])
						#print(dac[0][0], dac[0][1], dac[0][2])
					if len(dac)==2:
						if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
						#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
			except: print("error through CV")

class Listen3():


	def starting(self,s1,s2,s3,s4):
		portopened=0
		if rpi==1: 
			midi_in = rtmidi.MidiIn()
			midi_in.ignore_types(timing=False)
		global Syncmessage
		Syncmessage=0

		while 1:
			while s1.empty() is False:
				Sendinfo=s1.get()
				#print(('Sendinfo', Sendinfo))
			while s2.empty() is False:
				trackselected=s2.get()
				#print(('trackselected', trackselected))
			while s3.empty() is False:
				Syncinfo=s3.get()
				#print(('Syncinfo', Syncinfo))
			if rpi==1 and Syncinfo[4]==1:
				available_ports = midiout.get_ports()
				if len(available_ports)==2 and portopened==0:
					#midi_in = rtmidi.MidiIn(rtapi=3)
					midi_in = rtmidi.MidiIn()
					midi_in.ignore_types(timing=False)
					midi_in.open_port(1)

					portopened=1
					#r=rtmidi.get_compiled_api()
					#print("api",r)
				elif len(available_ports)==2 and portopened==1:
					midi_in.close_port()
					portopened=0
					del midi_in
					print('deleted port')	
			if Syncinfo[4]==0:
				try: del midi_in
				except: pass
				portopened=0		
			if rpi==1 and portopened==1: self.MIDIusbIn(Sendinfo,trackselected,midi_in,Syncinfo)
			time.sleep(0.001)


	def MIDIusbIn(self,Sendinfo,trackselected,midi_in,Syncinfo):
		if rpi==1:
			#midi_in.ignore_types(timing=False)
			#try:
			message= midi_in.get_message()
			if message:
				#print(message)
				self.ThroughCV(message[0],Sendinfo,trackselected)
				self.USBrec(message[0])
				#print(message)
				self.USBsyncin(message[0])
				# q=midi_in.get_current_api()
				# if q == rtmidi.API_UNIX_JACK:
				# 	print("Using JACK API for MIDI input.")

				#self.USBsync(message[0],Syncinfo) #pour plus tard
			#except: print("midi_in unknown")

	def USBsyncin(self,message):
		global Syncmessage
		#print("DINSYNCIN message!!",x1.value)
		if v6.value==0 or 1:
			v6.value=2
		# if message[0]==250:
		# 	#print("PLAY")
		# 	v2.value=0
		# 	v1.value=1
		# 	v8.value=0
		# 	Syncmessage=0
			
		# if message[0]==251:
		# 	#print("CONTINUE")
		# 	v1.value=1
		# 	v6.value=1
		# 	#print("STOP")
		# 	#v1.value=0
		# 	#v6.value=0
		if message[0]==252:
			#print("STOP")
			#pass
			v1.value=0
			v6.value=0
		if 	message[0]==248 and v1.value==0:	
			v2.value=0
			v1.value=1
			v8.value=0
			Syncmessage=0
		if message[0]==248 and v1.value==1:
			if y1.value==1:
				Syncmessage+=1
				if Syncmessage==1:
					v7.value+=1
				if Syncmessage==3:
					v7.value+=1
					Syncmessage=0
			else:
				Syncmessage=0


	def USBrec(self,message):
		if 144 <= message[0] <= 159: s4.put(message[1])

	def USBsync(self,message,Syncinfo):
		if Syncinfo[1]==1:
			if message[0]==250: #play
				v1.value=1
			if message[0]==252: #stop
				v1.value=2
			if message[0]==251: #continue
				v1.value=2
		#print(message)


	def ThroughCV(self,Message,Sendinfo,trackselected):
		Tosend=[]
		if Sendinfo[trackselected-1][3]>0:
			if Message[0]==144: Tosend.append([Sendinfo[trackselected-1][3], Sendinfo[trackselected-1][4], [0x0D, 0xE0],Sendinfo[trackselected-1][8]])
			if Message[0]==128: Tosend.append([Sendinfo[trackselected-1][3], Sendinfo[trackselected-1][4], [0x05, 0x55],Sendinfo[trackselected-1][8]])				
		if Sendinfo[trackselected-1][1]>0:
			if Message[0]==144 and (Message[1]-24)>0 and (Message[1]-24)<96 :
				a,b=divmod(4096*(Message[1]-24)/15/12+4096/15*Sendinfo[trackselected-1][5],256)
				Tosend.append([Sendinfo[trackselected-1][1], Sendinfo[trackselected-1][2], [a, b],Sendinfo[trackselected-1][7]])						
		if len(Tosend)>0:
			Tosend=sorted(Tosend, key = lambda x: x[3])
			#print("Tosend",Tosend)
			dacregister=[[],[],[]]
			for elem in Tosend:
				if elem[0]==0x61: dacregister[0].append([elem[0],elem[1],elem[2]])
				if elem[0]==0x62: dacregister[1].append([elem[0],elem[1],elem[2]])
				if elem[0]==0x60: dacregister[2].append([elem[0],elem[1],elem[2]])	
			try:
				for dac in dacregister:
					if len(dac)==1:
						if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], dac[0][2])
						#print(dac[0][0], dac[0][1], dac[0][2])
					if len(dac)==2:
						if rpi==1:bus.write_i2c_block_data(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
						#print(dac[0][0], dac[0][1], [dac[0][2][0],dac[0][2][1],dac[1][1], dac[1][2][0],dac[1][2][1]])
			except: print("error through CV")



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class Manager(ScreenManager):
	screen_one= ObjectProperty(None)
	screen_two= ObjectProperty(None)
	screen_three= ObjectProperty(None)
	screen_four= ObjectProperty(None)
	screen_five= ObjectProperty(None)
	screen_six= ObjectProperty(None)
	screen_seven= ObjectProperty(None)

class SequencerApp(App):

	def build(self):
		Config.set('graphics', 'KIVY_CLOCK', 'interrupt')
		Config.write()
		sm = Manager(transition=NoTransition())
		return sm

	def __init__(self, **kwargs):
		super(SequencerApp, self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		#print("keyboard, ",keycode)
		if keycode[0]==276:w1.value-=1
		elif keycode[0]==275:w1.value+=1
		elif keycode[0]==13:
			if w2.value==1: w2.value=0
			else: w2.value=1
		return True

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


keyrange=[['C0',1],['C#0',0],['D0',1],['D#0',0],['E0',1],['F0',1],['F#0',0],['G0',1],['G#0',0],['A0',1],['A#0',0],['B0',1],
		['C1',1],['C#1',0],['D1',1],['D#1',0],['E1',1],['F1',1],['F#1',0],['G1',1],['G#1',0],['A1',1],['A#1',0],['B1',1],
		['C2',1],['C#2',0],['D2',1],['D#2',0],['E2',1],['F2',1],['F#2',0],['G2',1],['G#2',0],['A2',1],['A#2',0],['B2',1],
		['C3',1],['C#3',0],['D3',1],['D#3',0],['E3',1],['F3',1],['F#3',0],['G3',1],['G#3',0],['A3',1],['A#3',0],['B3',1],
		['C4',1],['C#4',0],['D4',1],['D#4',0],['E4',1],['F4',1],['F#4',0],['G4',1],['G#4',0],['A4',1],['A#4',0],['B4',1],
		['C5',1],['C#5',0],['D5',1],['D#5',0],['E5',1],['F5',1],['F#5',0],['G5',1],['G#5',0],['A5',1],['A#5',0],['B5',1],
		['C6',1],['C#6',0],['D6',1],['D#6',0],['E6',1],['F6',1],['F#6',0],['G6',1],['G#6',0],['A6',1],['A#6',0],['B6',1],
		['C7',1],['C#7',0],['D7',1],['D#7',0],['E7',1],['F7',1],['F#7',0],['G7',1],['G#7',0],['A7',1],['A#7',0],['B7',1]]


timerange=["1","","","",".","","","",".","","","",".","","","","2","","","",".","","","",".","","","",".","","","","3","","","",".","","","",".","","","",".","","","","4","","","",".","","","",".","","","",".","","","",
"5","","","",".","","","",".","","","",".","","","","6","","","",".","","","",".","","","",".","","","","7","","","",".","","","",".","","","",".","","","","8","","","",".","","","",".","","","",".","","","",
"9","","","",".","","","",".","","","",".","","","","10","","","",".","","","",".","","","",".","","","","11","","","",".","","","",".","","","",".","","","","12","","","",".","","","",".","","","",".","","","",
"13","","","",".","","","",".","","","",".","","","","14","","","",".","","","",".","","","",".","","","","15","","","",".","","","",".","","","",".","","","","16","","","",".","","","",".","","","",".","","","",
"17","","","",".","","","",".","","","",".","","","","18","","","",".","","","",".","","","",".","","","","19","","","",".","","","",".","","","",".","","","","20","","","",".","","","",".","","","",".","","","",
"21","","","",".","","","",".","","","",".","","","","22","","","",".","","","",".","","","",".","","","","23","","","",".","","","",".","","","",".","","","","24","","","",".","","","",".","","","",".","","","",
"25","","","",".","","","",".","","","",".","","","","26","","","",".","","","",".","","","",".","","","","27","","","",".","","","",".","","","",".","","","","28","","","",".","","","",".","","","",".","","","",
"29","","","",".","","","",".","","","",".","","","","30","","","",".","","","",".","","","",".","","","","31","","","",".","","","",".","","","",".","","","","32","","","",".","","","",".","","","",".","","","",
"33","","","",".","","","",".","","","",".","","","","34","","","",".","","","",".","","","",".","","","","35","","","",".","","","",".","","","",".","","","","36","","","",".","","","",".","","","",".","","","",
"37","","","",".","","","",".","","","",".","","","","38","","","",".","","","",".","","","",".","","","","39","","","",".","","","",".","","","",".","","","","40","","","",".","","","",".","","","",".","","","",
"41","","","",".","","","",".","","","",".","","","","42","","","",".","","","",".","","","",".","","","","43","","","",".","","","",".","","","",".","","","","44","","","",".","","","",".","","","",".","","","",
"45","","","",".","","","",".","","","",".","","","","46","","","",".","","","",".","","","",".","","","","47","","","",".","","","",".","","","",".","","","","48","","","",".","","","",".","","","",".","","","",
"49","","","",".","","","",".","","","",".","","","","50","","","",".","","","",".","","","",".","","","","51","","","",".","","","",".","","","",".","","","","52","","","",".","","","",".","","","",".","","","",
"53","","","",".","","","",".","","","",".","","","","54","","","",".","","","",".","","","",".","","","","55","","","",".","","","",".","","","",".","","","","56","","","",".","","","",".","","","",".","","","",
"57","","","",".","","","",".","","","",".","","","","58","","","",".","","","",".","","","",".","","","","59","","","",".","","","",".","","","",".","","","","60","","","",".","","","",".","","","",".","","","",
"61","","","",".","","","",".","","","",".","","","","62","","","",".","","","",".","","","",".","","","","63","","","",".","","","",".","","","",".","","","","64","","","",".","","","",".","","","",".","","","",
"65","","","",".","","","",".","","","",".","","","","66","","","",".","","","",".","","","",".","","","","67","","","",".","","","",".","","","",".","","","","68","","","",".","","","",".","","","",".","","","",
"69","","","",".","","","",".","","","",".","","","","70","","","",".","","","",".","","","",".","","","","71","","","",".","","","",".","","","",".","","","","72","","","",".","","","",".","","","",".","","","",
"73","","","",".","","","",".","","","",".","","","","74","","","",".","","","",".","","","",".","","","","75","","","",".","","","",".","","","",".","","","","76","","","",".","","","",".","","","",".","","",""]

# [step number, note number, on, note length][step number + note length, note number, off, nnote length]
sequencepool2=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# [Channel 1, Channel 2..] => [[step 1],[step 2],[step 3],...  ] => [[note, status, length],[note, status, length],..]
sequencepool_0=[[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]]

sequencepool3=sequencepool_0


EnvPool2=[[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]],[[400.001,379.001]]]

EnvPool3=[[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]]

ADSRPool2=[[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0],[92.0,370.0,142.0,195.0,292.0,195.0,492.0,20.0]]

ADSRPool3=[[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]]

EucliPool2=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

EnvPool0=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#print(sequencepool3)

#print(sequencepool3[1])
# [Midi channel, Pitch Dac N, Pitch Ch N, Gate Dac N, Gate Ch N, Pitch offeset,DIN or USB,CV Num Pitch, Cv Num Gate]
Sendinfo=numpy.full((100,15),0)
Sendinfo=Sendinfo.tolist()
#print(Sendinfo)

# Indexed chronologialy ; [Track a,Track b, ...]
song=[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# [DAC Adress, Channel Adress]
#CVinfo=[[0x62,0x54,3],[0x62,0x56,4],[0x62,0x52,2],[0x62,0x50,1],[0x61,0x54,7],[0x61,0x56,8],[0x61,0x52,6],[0x61,0x50,5],[0x60,0x54,11],[0x60,0x56,12],[0x60,0x52,10],[0x60,0x50,9]]
#CVinfo=[[0x61,0x54,3],[0x61,0x56,4],[0x61,0x52,2],[0x61,0x50,1],[0x62,0x56,8],[0x62,0x54,7],[0x62,0x52,6],[0x62,0x50,5],[0x60,0x56,12],[0x60,0x54,11],[0x60,0x52,10],[0x60,0x50,9]]
CVinfo=[[0x60,0x44,3],[0x60,0x46,4],[0x60,0x42,2],[0x60,0x40,1],[0x61,0x46,8],[0x61,0x44,7],[0x61,0x42,6],[0x61,0x40,5],[0x62,0x46,12],[0x62,0x44,11],[0x62,0x42,10],[0x62,0x40,9]]

zoom=4
rangeX=0
rangeXs=0
rangeXmax=64*16-1
rangeFile=0
rangeYs=0
rangeY=36 #C0=0, 8 octaves
rangeMidi=0
rangeCV=0
rangeCVTrack=0
start=0
trackselected=1
wheel=0
loopsizeS=64*16
erased=0
trackselectedparam=1
BPM=120
interval=float(60/Decimal(BPM)/Decimal(16))
count=0
recordingON=0
DACpool=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
CVsends=[]
CVsends2=[]
CVdelayed=[]
stoplong=0
trackmode=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
Phase=[55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55]
ADSRtrig=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  #track i triggers ADSR from track x
ADSRcounter=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
displayinfo=1
stepeucli=[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
pulseeucli=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
ChangedEucli=0
EucliOffset=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
manuelmodeeucli=0
RandomDensity=[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
RandomTemp=[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
RandomRatchet=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
randomcalculated=0
resetedrandom=0
Ratchetcount=0
displayinfolive=1
displayeditlive=0
polaritylfo=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
DrawPoints=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
projectmode=0
safemode=0
dininreset=0

# size of the loops of each tracks
loopsize=numpy.full(100,64)

loopsize=loopsize.tolist()
playing=0

buttonpushed="b000"
buttonpushedsong="b000"
if rpi==1:
	with open('/home/pi/Desktop2/UIP/param.json') as f: paramcf1 = json.load(f)
	with open('/home/pi/Desktop2/UIP/savedseq.json') as s: saved = json.load(s)
	with open('/home/pi/Desktop2/UIP/savedsong.json') as s2: savedsong = json.load(s2)
	with open('/home/pi/Desktop2/UIP/savedsong2.json') as s3: savedsong2 = json.load(s3)
	with open("/home/pi/Desktop2/UIP/licence.json") as l: licence=json.load(l)
else:
	with open('param.json') as f: paramcf1 = json.load(f)
	with open('savedseq.json') as s: saved = json.load(s)
	with open('savedsong.json') as s2: savedsong = json.load(s2)
	with open('savedsong2.json') as s3: savedsong2 = json.load(s3)
	with open("licence.json") as l: licence=json.load(l)
version=licence["licence"][0]["version"]
print("CFM1 Version: " + str(version))

paramcalc=ParamScreen()
Sendinfo=paramcalc.convert()


#[din sync,usb sync,clock ppq,usb ppq,usb in (1) or out (0)]
Syncinfo=[0,0,0,0,0]
Syncinfo=paramcalc.convertsync()

midiout = rtmidi.MidiOut()
#midiout = 0

def outsmp(v1,v2,v3,v4,v5,v6,v7,v8,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12):
	ti=Timing()
	ti.Timer(v1,v2,v3,v4,v5,v6,v7,v8,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12)

#v1: playing ; v2: count ; v3: song size ; v4: BPM
#q1:sequencepool ; q2: loopsize ; q3: song ; q4: Sendinfo

v1=multiprocessing.Value('i',1)
v1.value=0
v2=multiprocessing.Value('i',1)
v3=multiprocessing.Value('i',1)
v3.value=16*4*16
v4=multiprocessing.Value('i',1)
v4.value=BPM
v5=multiprocessing.Value('i',1)
v5.value=trackselected
v6=multiprocessing.Value('i',1)
v6.value=2
v7=multiprocessing.Value('i',1)
v7.value=0
v8=multiprocessing.Value('i',1)
v8.value=1

q1=multiprocessing.Queue()
q1.put(sequencepool2)
q2=multiprocessing.Queue()
q2.put(loopsize)
q3=multiprocessing.Queue()
q3.put(song)
q4=multiprocessing.Queue()
q4.put(Sendinfo)
q5=multiprocessing.Queue()
q5.put(Syncinfo)
q6=multiprocessing.Queue()
#q6.put(sequencepool3)
q7=multiprocessing.Queue()
q8=multiprocessing.Queue()
q9=multiprocessing.Queue()
q9.put(ADSRtrig)
q10=multiprocessing.Queue()
q10.put(sequencepool3)
q11=multiprocessing.Queue()
q11.put(EnvPool3)
q12=multiprocessing.Queue()
q12.put(ADSRPool3)
#q5.put(Syncinfo)


def insmp(w1,w2):
	listen=Listen()
	listen.starting(w1,w2)

w1=multiprocessing.Value('i',1)
w1.value=0
w2=multiprocessing.Value('i',1)
w2.value=0


def insmp2(r1,r2,r3,r4,x1,y1):
	listen2=Listen2()
	listen2.starting(r1,r2,r3,r4,x1,y1)

r1=multiprocessing.Queue()
r1.put(Sendinfo)
r2=multiprocessing.Queue()
r2.put(trackselected)
r3=multiprocessing.Queue()
r3.put(Syncinfo)
r4=multiprocessing.Queue()
x1=multiprocessing.Value('i',1)
x1.value=0
y1=multiprocessing.Value('i',1)
y1.value=0

def insmp3(s1,s2,s3,s4):
	listen3=Listen3()
	listen3.starting(s1,s2,s3,s4)

s1=multiprocessing.Queue()
s1.put(Sendinfo)
s2=multiprocessing.Queue()
s2.put(trackselected)
s3=multiprocessing.Queue()
s3.put(Syncinfo)
s4=multiprocessing.Queue()

p=multiprocessing.Process(target=outsmp,args=(v1,v2,v3,v4,v5,v6,v7,v8,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12))
p.start()
pq=multiprocessing.Process(target=insmp,args=(w1,w2))
pq.start()
pq2=multiprocessing.Process(target=insmp2,args=(r1,r2,r3,r4,x1,y1))
pq2.start()
pq3=multiprocessing.Process(target=insmp3,args=(s1,s2,s3,s4))
pq3.start()



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################



def deleteLFO():
	global EnvPool2
	global EnvPool3
	global Phase
	Phase[trackselected-1]=55
	EnvPool2[trackselected-1]=[0]
	EnvPool3[trackselected-1]=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	#print("deleted",EnvPool3[trackselected-1])
	#print("EnvPool0",EnvPool0)
	q7.put(EnvPool3[trackselected-1])
	print("LFO deleted")

def deleteADSR():
	global ADSRPool2
	global ADSRPool3
	global ADSRtrig
	ADSRPool2[trackselected-1]=[0]
	ADSRPool3[trackselected-1]=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	q8.put(ADSRPool3[trackselected-1])
	for n,elem in enumerate(ADSRtrig):
		if elem == trackselected:
			ADSRtrig[n]=0
	q9.put(ADSRtrig)
	#print("adsr trig",ADSRtrig)
	print("ADSR deleted")

def clearsequence():
	global sequencepool2
	global sequencepool3
	sequencepool2[trackselected-1]=[]
	for i,elem in enumerate(sequencepool3[trackselected-1]): sequencepool3[trackselected-1][i]=[]
	q1.put(sequencepool2)
	q6.put(sequencepool3[trackselected-1])
	#print(sequencepool3[trackselected-1])
	print("Sequence deleted")
	deleteEuclidean()

def deleteRandom():
	print("Random deleted")

def deleteEuclidean():
	global EucliPool2
	EucliPool2[trackselected-1]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	print("Euclidean deleted")



try:
	seq=SequencerApp()
	seq.run()
finally:
	if rpi==1:
		GPIO.cleanup()
	print("cleaned")