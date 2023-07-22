#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import serial as ser
import time
import os
import cv2
import argparse
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mytrash_ui import Ui_MainWindow


Recyleable_waste = [7,8]
Other_waste = [3]
Harmful_waste = [1,2]
Kitchen_waste = [4,5,6]
global n,flag#检测帧照片命名
n=1042
flag=0

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
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")


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
display = jetson.utils.videoOutput()
# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)


#-----------------------------------------------------------------------------------------
#识别函数

def Detect_mine():
	global n
	time.sleep(0.2)
	img = input.Capture()
	display.Render(img)

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)
	#display.Render(img)
	#display.SetStatus(str(n)+"-Object Detection |  Network {:.0f}FPS".format(net.GetNetworkFPS()))
	jetson.utils.saveImageRGBA(str(n)+'.jpg',img)
	#cv2.imshow('.jpg',img)
	#output = jetson.utils.videoOutput("notdetection")
	#output.Render(img)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))
	if format(len(detections)) == '0' :
		se.write('O'.encode("GB2312"))
		mwin.plainTextEdit_2.appendPlainText("Other_waste：")

	for detection in detections:
		if detection.ClassID in Recyleable_waste :
			se.write('R'.encode("GB2312"))
			mwin.plainTextEdit_2.appendPlainText('Recyleable_waste：')
			print("ok")
		elif detection.ClassID in Other_waste:
			se.write('O'.encode("GB2312"))
			mwin.plainTextEdit_2.appendPlainText("Other_waste：")
			print("ok")
		elif detection.ClassID in Harmful_waste:
			se.write('H'.encode("GB2312"))
			mwin.plainTextEdit_2.appendPlainText('Harmful_waste：')
			print("ok")
		elif detection.ClassID in Kitchen_waste:
			se.write('K'.encode("GB2312"))
			mwin.plainTextEdit_2.appendPlainText('Kitchen_waste：')
			print("ok")
		#print(detection)
		print(detection.ClassID)
		break
	n+=1

	#net.PrintProfilerTimes()

#-------------------------------------------------------------------------------------------------------
#多线程
class single_detectionThread(QThread):
	def __init__(self):
		super().__init__()

	def run(self):
		global flag
		while True:
			receiving_code = se.readline().decode("GB2312")
			print(receiving_code)
			if receiving_code == 'A':
				print("detecting")
				Detect_mine()
				print("over")
			if flag == 1 :
				break


#---------------------------------------------------------------------------------------------------------
#UI界面
class MainWindow(Ui_MainWindow, QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.mythread = single_detectionThread()

		self.pushButton_5.clicked.connect(self.start_pushbutton)
		
		self.pushButton_3.clicked.connect(self.reset_pushbutton)
		self.pushButton_4.clicked.connect(self.video_start)
	def start_pushbutton(self):
		msgbox = QMessageBox.information(self,"系统提示：","开启成功！")
		self.pushButton_5.setEnabled(True)
		print('开始识别：\n')
		self.plainTextEdit_2.appendPlainText('开始识别：')
		self.mythread.start()

		self.pushButton_2.clicked.connect(self.stop_pushbutton)


	def stop_pushbutton(self):
		global flag
		reply = QMessageBox.question(self, '系统提示', '你确定要结束识别？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		# event.accept()
		if reply != QMessageBox.Yes:
			event.ignore()
		else:
			flag = 1
			self.mythread.quit()
			print('结束所有任务\n')
			self.plainTextEdit_2.appendPlainText('结束所有任务！')
		self.pushButton_2.setEnabled(False)


	def reset_pushbutton(self):
		self.pushButton_5.setEnabled(True)
		self.pushButton_2.setEnabled(True)
		self.plainTextEdit_2.appendPlainText('重新启动：')
		self.plainTextEdit_2.setPlainText("")  # 清屏
		self.mythread.start()


	def video_start(self):
		self.plainTextEdit_2.appendPlainText('视频播放中...')


if __name__ == "__main__":
	app = QApplication(sys.argv)
	mwin = MainWindow()
	mwin.show()
	sys.exit(app.exec_())

# process frames until the user exitsRecyleable
	# capture the next image



