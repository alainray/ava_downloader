# Ava Downloader Script

This script downloads all videos associated with the AVA (Atomic Visual Actions) dataset available from https://github.com/cvdfoundation/ava-dataset. 

You must download the files with the filenames from that repository.

# Requirements:
* tqdm

Input to the script is:

* Input file: either 
* Mode: whether you are downloading train/validation videos or test videos. Possible values: 'trainval', 'test'
* Video Directory: where you want to store the videos.

Script is run with:

`python ava_downloader.py <file> -m <mode> -v <dir>`

So if you want to download the train and validation videos to the *'download'* directory then you would use:

`python ava_downloader.py ava_file_names_test_v2.1.txt -m trainval -v download`

#TODO:
* Add script that cuts videos to the appropriate 900-1800s range.
* Add script to turn videos into frames.
