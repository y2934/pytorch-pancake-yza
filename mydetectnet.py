#!/usr/bin/python3
""""""
#最终程序，识别检测和测溢满同步进行


import jetson.inference
import serial as ser #串口通信
import time
import numpy as np
import cv2 as cv
import os
import argparse
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mytrash_ui import Ui_MainWindow #ui文件
#import RPi.GPIO as GPIO  # 树莓派GPIO
import VL53L0X  # 激光测距 可以测量两米的绝对距离


Recyclable_waste = [7,8]
Other_waste = [3]
Harmful_waste = [1,2]
Kitchen_waste = [4,5,6]
global n,flag, STR, num_all, num_harmful, num_kitchen, num_other, num_recyclable,STR2

#n=151  #保存照片序号
flag=0  #检测结束标志位
num_all = 0  # 垃圾总数
num_harmful = 0
num_recyclable = 0
num_other = 0
num_kitchen = 0  # 各种垃圾独自的数量
STR = ''  # 垃圾显示文本
STR2=''#溢满提示文本


#-----------------------------------------------------------------------------------------
#重新赋值


def fuchuzhi():
	global n,flag, STR,STR2, num_all, num_harmful, num_kitchen, num_other, num_recyclable
	flag=0
	num_all = 0  # 垃圾总数
	num_harmful = 0
	num_recyclable = 0
	num_other = 0
	num_kitchen = 0  # 各种垃圾独自的数量
	STR = ''  # 垃圾显示文本
	STR2 =''  # 溢满提示文本
	FLAG_A=0
	FLAG_B=0

#-----------------------------------------------------------------------------------------
#TOF初始化

#
tof1 = VL53L0X.VL53L0X(tca9548a_num=0, tca9548a_addr=0x70)
tof2 = VL53L0X.VL53L0X(tca9548a_num=6, tca9548a_addr=0x70)
tof3 = VL53L0X.VL53L0X(tca9548a_num=3, tca9548a_addr=0x70)
tof4 = VL53L0X.VL53L0X(tca9548a_num=5, tca9548a_addr=0x70)
#
tof1.open()
tof2.open()
tof3.open()
tof4.open()
#
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)
tof3.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)
tof4.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)
#
timing = tof2.get_timing()
if timing < 20000:
	timing = 20000
print("Timing %d s" % (timing / 1000))
# #-----------------------------------------------------------------------------------------
# #测距函数
def Get_distance():
	distance1 = 0
	distance2 = 0
	distance3 = 0
	distance4 = 0
	global FLAG_A, FLAG_B, FLAG_C, FLAG_D,flag_A_previous, flag_B_previous, flag_C_previous, flag_D_previous, STR2
#
	m = 5
	for i in range(m):
		count = i+1
		# Get distance from VL53L0X  on TCA9548A bus 1
		distance1 += tof1.get_distance()   # 投放口下
		print("1: %d mm, %d cm, %d" % ((distance1/count), (distance1/count/10), count))

# 		# Get distance from VL53L0X  on TCA9548A bus 2
		distance2 += tof2.get_distance() 
		print("2: %d mm, %d cm, %d" % ((distance2/count), (distance2/count/10), count))

		# Get distance from VL53L0X  on TCA9548A bus 1
		distance3 += tof3.get_distance()  # 投放口下
		print("3: %d mm, %d cm, %d" % ((distance3 / count), (distance3 / count / 10), count))

		# 		# Get distance from VL53L0X  on TCA9548A bus 2
		distance4 += tof4.get_distance()
		print("4: %d mm, %d cm, %d" % ((distance4 / count), (distance4 / count / 10), count))
#
		time.sleep(timing / 1000000.00)
#
	print("1: %d mm, %d cm" % ((distance1/m), (distance1/m/10)))
	print("2: %d mm, %d cm" % ((distance2/m), (distance2/m/10)))
	print("3: %d mm, %d cm" % ((distance3 / m), (distance3 / m / 10)))
	print("4: %d mm, %d cm" % ((distance4 / m), (distance4 / m / 10)))
	if distance1 <= 400 * m:
		print('1号口溢满')
		FLAG_A = 1
	else:
		FLAG_A = 0
	if distance2 <= 400 * m:
		print('2号口溢满')
		FLAG_B = 1
	else:
		FLAG_B = 0
	if distance3 <= 400 * m:
		print('3号口溢满')
		FLAG_C = 1
	else:
		FLAG_C = 0
	if distance4 <= 400 * m:
		print('4号口溢满')
		FLAG_D = 1
	else:
		FLAG_D = 0

	if FLAG_A and not flag_A_previous:
		STR2 += '可回收垃圾 溢满提醒!\n'
		tof1.stop_ranging()
		flag_A_previous = True

	if FLAG_B and not flag_B_previous:
		STR2 += '其他垃圾 溢满提醒!\n'
		tof2.stop_ranging()
		flag_B_previous = True

	if FLAG_C and not flag_C_previous:
		STR2 += '有害垃圾 溢满提醒!\n'
		tof3.stop_ranging()
		flag_C_previous = True

	if FLAG_D and not flag_D_previous:
		STR2 += '厨余垃圾 溢满提醒!\n'
		tof4.stop_ranging()
		flag_D_previous = True


#-----------------------------------------------------------------------------------------
#serial port initialization
se = ser.Serial("/dev/ttyUSB0",115200,timeout=0.01)
if se.isOpen():
	print("Serial port initialization Success")
	print(se.name)
else:
	print("Serial port initialization Failed")
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.",
								 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
								 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.4, help="minimum detection threshold to use")


is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
#display output detects
#display = jetson.utils.videoOutput()
#实时显示图片

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)


#-----------------------------------------------------------------------------------------
#识别函数

def Detect_mine():
	global n,flag, STR, num_all, num_harmful, num_kitchen, num_other, num_recyclable
	STR = ''
	if num_all == 0:   #第一个垃圾不用延时
		pass
	else:
		time.sleep(0.4)     
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)
	#display.Render(img)  #渲染图片
	#display.SetStatus(str(n)+"-Object Detection |  Network {:.0f}FPS".format(net.GetNetworkFPS()))
	#jetson.utils.saveImageRGBA(str(n)+'.jpg',img)  #保存图片以查看，影响识别速度
	#output = jetson.utils.videoOutput("notdetection")
	#output.Render(img)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))
	if format(len(detections)) == '0' :        #未识别到的情况
		se.write('O'.encode("GB2312"))
		print("other")
		num_all += 1
		num_other += 1
		STR = "%d nothing %d ok! \n" % (num_all, num_other)

	for detection in detections:
		if detection.ClassID in Recyclable_waste :
			se.write('R'.encode("GB2312"))
			print("recyclable")
			num_all += 1
			num_recyclable += 1
			STR = "%d 可回收垃圾 %d ok! \n" % (num_all, num_recyclable)
			#mwin.plainTextEdit_2.appendPlainText(STR)
		elif detection.ClassID in Other_waste:
			se.write('O'.encode("GB2312"))
			print("other")
			num_all += 1
			num_other += 1
			STR = "%d 其他垃圾 %d ok! \n" % (num_all, num_other)
			#mwin.plainTextEdit_2.appendPlainText(STR)
		elif detection.ClassID in Harmful_waste:
			se.write('H'.encode("GB2312"))
			print("Harmful")
			num_all += 1
			num_harmful += 1
			STR = "%d 有害垃圾 %d ok! \n" % (num_all, num_harmful)
			#mwin.plainTextEdit_2.appendPlainText(STR)
		elif detection.ClassID in Kitchen_waste:
			se.write('K'.encode("GB2312"))
			print("kitchen")
			num_all += 1
			num_kitchen += 1
			STR = "%d 厨余垃圾 %d ok! \n" % (num_all, num_kitchen)
			#mwin.plainTextEdit_2.appendPlainText(STR)
		#print(detection)

		print(detection.ClassID)
		break
	#n+=1

	#net.PrintProfilerTimes()

#-------------------------------------------------------------------------------------------------------
#多线程
#识别线程
class single_detectionThread(QThread,QObject):
	mysignal = pyqtSignal(str)  # 定义检测信号

	def __init__(self):
		super(single_detectionThread, self).__init__()		
		fuchuzhi()
	def run(self):
		global num_all
		while (flag==0):
			receiving_code = se.readline().decode("GB2312")
			print(receiving_code)
			if receiving_code == 'A':
				print("detecting")
				Detect_mine()
				self.mysignal.emit(STR)  #发射信号
				print("over")
			if num_all == 10:
				break

	def thread_exit(self):
		print("detect stop!")
		self.quit()
		self.wait()
		
		#self.terminate()    #强制退出，避免使用

#测距线程
class Getdistance_thread(QThread,QObject):
	mysignal2 = pyqtSignal(str)  # 定义测距信号
	def __init__(self):
		super(Getdistance_thread,self).__init__()

	def run(self):
		global STR2, flag_A_previous, flag_B_previous, flag_C_previous, flag_D_previous
		STR2 = ''
		flag_A_previous = False
		flag_B_previous = False
		flag_C_previous = False
		flag_D_previous = False
		while True:
			Get_distance()
			self.mysignal2.emit(STR2)  # 发射信号

	def thread_exit(self):
		print("getdistance stop!")
		self.quit()
		self.wait()
		
		#self.terminate()    #强制退出，避免使用


#使用系统的mplayer命令行工具来播放视频文件
#视频线程
class video_Thread(QThread):
	def __init__(self):
		super().__init__()

#添加-input file=/dev/null参数来禁用mplayer的标准输入（stdin）
	def run(self):
		os.system('mplayer /home/m217/Videos/jay_video.mp4 -loop 0 -input file=/dev/null &')

#发送一个“quit”命令到一个名为/tmp/mplayer-control的文件中，然后使用killall命令停止所有正在运行的mplayer进程
	def thread_exit(self):
		print("video stop!")
		os.system('sleep 1 && echo "quit" > /tmp/mplayer-control && killall mplayer')
		#self.quit()
		#self.wait()
		#self.terminate()    #强制退出，避免使用


#----------------------------------------------------------------------mythread.mysignal.connect(lambda:self.signalcall)-----------------------------------
#UI界面 主线程
class MainWindow(Ui_MainWindow, QMainWindow,QMessageBox):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.detectionThread = single_detectionThread()
		self.videoThread = video_Thread()
		self.GetdistanceThread = Getdistance_thread()
		self.detectionThread.mysignal.connect(self.signalcall)
		self.GetdistanceThread.mysignal2.connect(self.signalcall2)

		self.resize(1000, 800)

		self.pushButton_5.clicked.connect(self.start_pushbutton)
		self.pushButton_3.clicked.connect(self.reset_pushbutton)
		self.pushButton_4.clicked.connect(self.video_start)
	def start_pushbutton(self):
		reply= QMessageBox.about(self,"系统提示：","开启成功！")
		self.pushButton_5.setEnabled(True)
		print('开始识别：\n')
		self.plainTextEdit_2.appendPlainText('开始识别：')
		self.plainTextEdit_3.appendPlainText('开始测溢满：')
		self.detectionThread.start()
		self.GetdistanceThread.start()


		self.pushButton_2.clicked.connect(self.stop_pushbutton)
	def stop_pushbutton(self):
		global flag
		reply = QMessageBox.question(self, '系统提示', '你确定要结束识别？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		reply.setStyleSheet("QLabel{min-width: 300px; font-size: 16px; color: white;}")
		# event.accept()
		if reply != QMessageBox.Yes:
			#event.ignore()
			pass 
		else:
			flag = 1
			print('结束所有任务\n')
			self.plainTextEdit_2.appendPlainText('结束所有任务！')
			self.videoThread.thread_exit()
			self.GetdistanceThread.thread_exit()
			self.detectionThread.thread_exit()
			self.pushButton_2.setEnabled(False)


	def reset_pushbutton(self):
		self.pushButton_5.setEnabled(True)
		self.pushButton_2.setEnabled(True)
		self.plainTextEdit_2.appendPlainText('重新启动：')
		self.plainTextEdit_2.setPlainText("")  # 清屏
		self.plainTextEdit_3.setPlainText("")
		fuchuzhi()
		reply= QMessageBox.about(self,"系统提示：","开启成功！")
		reply.setStyleSheet("QLabel{min-width: 300px; font-size: 16px; color: white;}")
		self.pushButton_5.setEnabled(True)
		print('开始识别：\n')
		self.plainTextEdit_2.appendPlainText('开始识别：')
		self.plainTextEdit_3.appendPlainText('开始测溢满：')
		self.detectionThread.start()
		self.GetdistanceThread.start()


	def video_start(self):
		self.plainTextEdit_2.appendPlainText('视频播放中...')
		self.videoThread.start()

	def signalcall(self,text):    #检测文本显示信号槽函数
		self.plainTextEdit_2.appendPlainText(text)

	def signalcall2(self,text):    #溢满文本显示信号槽函数
		self.plainTextEdit_3.appendPlainText(text)

	


if __name__ == "__main__":
	app = QApplication(sys.argv)
	mwin = MainWindow()
	mwin.show()
	sys.exit(app.exec_())

# process frames until the user exits



