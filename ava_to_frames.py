#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import video
import os
import random
import argparse
from tqdm import tqdm
import math


def make_dir(root, filename):
	sep = "."
	filename = filename.split(sep, 1)[0]
	path = os.path.join(root,filename)
	if not os.path.exists(path):
		print("Directory for video {} doesn't exist. Creating...".format(filename))
		os.makedirs(path)
	else:
		print("Directory for video {} already exists. Skipping...".format(filename))
	return path

def read_url_file(path):
	filenames = [line.rstrip('\n') for line in open(path)]
	return filenames

def process_and_check_video(video_id, video_path, output_path, progress, resize_min_size=400, fps=25):
	process_video(video_path, output_path, video_id, fps=fps, resize_min_size=resize_min_size)
	progress = register_video(video_id, output_path, progress)
	return progress
	
def process_frame(frame, output_folder, video_id, frame_number, current_second, resize_min_size=400, jpg_quality=85):
	# Compute output dimensions
	height, width, _ = frame.shape
	ratio = float(height)/float(width)
	if ratio > 1.0:
		W = resize_min_size
		H = int(ratio * float(W))
	else:
		H = resize_min_size
		W = int(float(H) / ratio)

	# Resize frame
	resized_frame = cv.resize(frame,(W,H))

	# Generate destination path
	frame_number = str(frame_number)
	current_second = '0'*(4-len(str(current_second)))+ str(current_second)
	frame_number = '0'*(2-len(frame_number))+frame_number
	dst_filename = "{}_{}_{}.jpg".format(video_id, current_second,frame_number)
	dst_filename = os.path.join(output_folder, dst_filename)

	# Save frame
	cv.imwrite(dst_filename, resized_frame, [cv.IMWRITE_JPEG_QUALITY, jpg_quality])

def process_video(video_path, output_folder, video_id, resize_min_size=400, fps=25):
	print(video_path)
	cam = video.create_capture(video_path)
	video_fps = cam.get(cv.CAP_PROP_FPS) #cam.get(cv.cv.CV_CAP_PROP_FPS) #
	frameCount = int(cam.get(cv.CAP_PROP_FRAME_COUNT))
	duration = frameCount/video_fps
	frame_time_step = 1/float(frameCount)
	print("FPS: {}".format(video_fps))
	print("frameCount: {}".format(frameCount))
	print("frame_time_step: {}".format(frame_time_step))
	intervals = np.arange(0,1,1/(fps*duration))

	current_second = 0
	if video_fps > 29:
		lin = np.linspace(0,math.floor(video_fps),fps)
	else:
		lin = np.linspace(0,math.floor(video_fps)-1,fps)
	while(cam.isOpened()):
		f = 0
		frame_number = 0
		total_frame = 0
		for i,elem in enumerate(lin):
			ret, frame = cam.read()
			total_frame += 1
			if ret==True:
				process_frame(frame, output_folder, video_id, frame_number, current_second, resize_min_size=resize_min_size)
				frame_number += 1

				if i != 0:
					f = int(elem) - int(lin[i-1])
				else:
					f = int(lin[i+1]) - int(elem)

				for _ in range(f-1):
					ret, frame = cam.read()
					total_frame += 1

					if total_frame >= video_fps:
						break
			else:
				break

			if total_frame >= video_fps:
				break

		ret, frame = cam.retrieve()
		if not ret:
			break

		current_second += 1

	#current_second = 0
	# frame_number = 0
	# ret, frame = cam.read()
	# for fr, interval in enumerate(tqdm(intervals)):
	# 	if frame_number >= fps:
	# 		frame_number = 0
	# 	current_second = fr//fps
	# 	#Set next frame to closest to interval
	# 	#cam.set(cv.CAP_PROP_POS_FRAMES,interval)
	# 	#capture frame
	# 	ret, frame = cam.read()
	# 	process_frame(frame, output_folder, video_id, frame_number, current_second, resize_min_size=resize_min_size)
	# 	frame_number += 1

def load_progress(output_dir):
	path = os.path.join(output_dir,'progress.txt')

	filenames = list()
	if os.path.exists(path):
		filenames = [line.rstrip('\n') for line in open(path)]
	return filenames

def check_video(video_id, progress):
	video_id = video_id.split(".",1)[0]
	if video_id in progress:
		print("File processed.")
		return True
	else:
		print("File not processed.")
		return False
def register_video(video_id, output_dir, progress):
	#Add filename to list
	progress.append(video_id)
	#Write file
	print("Registering completed video")
	path = os.path.join(output_dir,"..",'progress.txt')
	with open(path, 'w') as f:
		for id in progress:
			f.write("%s\n" % id)
	
	return progress

if __name__ == '__main__':

	description = 'Helper script for converting AVA dataset videos to JPG frames'
	p = argparse.ArgumentParser(description=description)

	p.add_argument('input_csv', type=str, help='CSV file containing the following format:')
	p.add_argument('video_dir', type=str,
	help='Directory where unprocessed videos are stored')
	p.add_argument('output_dir', type=str,
	help='Output directory where videos will be saved.')
	p.add_argument('-f', '--fps', type=int, default=25,
	help='Number of Frames Per Second to sample the video at')
	p.add_argument('-s', '--size', type=int, default=400,
	help='Minimum size in pixels to resize the video')

	#Just parsing arguments 
	args = p.parse_args()

	input_filename = args.input_csv
	video_dir = args.video_dir
	output_dir = args.output_dir
	fps = args.fps
	min_size = args.size
	filenames = read_url_file(input_filename)

	progress = load_progress(output_dir)
	#Main loop
	for f in tqdm(filenames):
		video_id = f.split('.', 1)[0]
		f = "{}_900_1800.mp4".format(f)
		if not check_video(f, progress):
			output_path = make_dir(output_dir, f)
			video_path = os.path.join(video_dir,f)
			progress = process_and_check_video(video_id, video_path, output_path, progress, resize_min_size=min_size, fps=fps)
			
		else:
			print("Video already processed. Skipping video {}".format(f))