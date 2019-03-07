# -*- coding: utf-8 -*-
import requests
import os
import argparse
from tqdm import tqdm
#Open file with train/test files
# For each filename in file, download

def download_file(filename, mode='trainval', base_dir=""):
  url = 'https://s3.amazonaws.com/ava-dataset/{}/{}'.format(mode, filename)
  file_path = "{}/{}".format(base_dir, filename)
  if check_file(filename, base_dir):
    print("File {} already exists. Skipping.".format(filename))
  else:
    print("\tDownloading file {} from url: {}".format(filename, url))
    r = requests.get(url, allow_redirects=True)
    print("Writing file {} to disk.".format(filename))
    open(file_path, 'wb').write(r.content)

def read_url_file(path):
  filenames = [line.rstrip('\n') for line in open(path)]
  return filenames

def check_file(filename, base_dir):
  url = "{}/{}".format(base_dir, filename)
  return os.path.isfile(url)


def parse_arguments():
  description = 'Helper script for downloading AVA dataset videos'
  p = argparse.ArgumentParser(description=description)
  p.add_argument('input', type=str, help='CSV file containing filenames to download')
  p.add_argument('-v', '--video_dir', type=str, help='Directory where videos will be stored', default='.')
  p.add_argument('-m', '--mode', type=str, help='trainval or test', default="trainval")

  return p.parse_args()

#Just parsing arguments 
args = parse_arguments()


input_filename = args.input
video_dir = args.video_dir
mode = args.mode

videos = read_url_file(input_filename)

for filename in tqdm(videos):
  download_file(filename, mode, video_dir)