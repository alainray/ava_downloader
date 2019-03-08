# Ava Downloader Script

This script downloads all videos associated with the AVA (Atomic Visual Actions) dataset available from https://github.com/cvdfoundation/ava-dataset. 

You must download the files with the filenames from that repository.

# Requirements:
* tqdm
* subprocess
* ffmpeg

Input to the script is:

* **Input file:** either ava_file_names_trainval_v2.1.txt or ava_file_names_test_v2.1.txt.
* **Mode:** whether you are working with train/validation videos or test videos. Possible values: 'trainval', 'test'
* **Video Directory:** where you want to store the videos and/or access the videos from.
* **Function:** whether you want to download, cut or both download and cut videos. Cut videos will cut the videos to the 900-1800s range, which is where all AVA labels are. Downloading files is relatively fast, while processing may take a few days. Values accepted are 'd' for just download, 'c' for just cutting videos and 'dc' if you want to do both.
* **Output Folder:** where you want to store the processed videos.

Script is run with:

`python ava_dataset.py <file> -m <mode> -v <video_dir> -o <output_dir> -f <d/c/dc>`

So if you just want to download the train and validation videos to the *'download'* directory then you would use:

`python ava_dataset.py ava_file_names_trainval_v2.1.txt -m trainval -v download -f d`

# TODO:
* Add script to turn videos into frames.
