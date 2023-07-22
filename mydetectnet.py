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
import argparse
import sys


#bottle,cans,stone
#pills,battery,carrot,white
Recyleable_waste = [1,2]
Other_waste = [3]
Harmful_waste = [4,5]
Kitchen_waste = [6,7]

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
display = jetson.utils.videoOutput()
	
# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)



def Detect_mine():
	time.sleep(0.4)
	img = input.Capture()
	
	
	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)
	output = jetson.utils.videoOutput("notdetection")
	display.Render(img)
	#output.Render(img)
	display.SetStatus("Object Detection |  Network {:.0f}FPS".format(net.GetNetworkFPS()))
	
	
		
	
	# print the detections
	print("detected {:d} objects in image".format(len(detections)))
	if format(len(detections)) == '0' :
		se.write('O'.encode("GB2312"))
		
	for detection in detections:
		if detection.ClassID in Recyleable_waste :
			se.write('R'.encode("GB2312"))
		elif detection.ClassID in Other_waste:
			se.write('O'.encode("GB2312"))
		elif detection.ClassID in Harmful_waste:
			se.write('H'.encode("GB2312"))
		elif detection.ClassID in Kitchen_waste:
			se.write('K'.encode("GB2312"))
		
		#print(detection)
		print(detection.ClassID)
		break
	
	#net.PrintProfilerTimes()
		

	
# process frames until the user exitsRecyleable
while True:
	
	Receiving_code = se.readline().decode("GB2312")
	print(Receiving_code)
	if Receiving_code == 'A' :
		print("detecting")
		Detect_mine()
		print("over")
	# capture the next image
	


