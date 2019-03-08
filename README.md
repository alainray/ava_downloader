# AVA Dataset Downloader Script

This script downloads all videos associated with the AVA (Atomic Visual Actions) dataset available from https://github.com/cvdfoundation/ava-dataset. 

You must download the files with the filenames from that repository.

## Requirements:
* tqdm
* subprocess
* ffmpeg (for cutting videos)
* OpenCV2 (for turning video into frames)
* Tested on Ubuntu 16.04.

## HOW TO
There are 2 scripts available on the repository:
* **ava_dataset.py:** this script will download and/or cut videos to the appropriate 900-1800s range where AVA labels reside. 
* **ava_to_frames.py:** Script was modified from an original script by @caspillaga. This script will turn videos downloaded by the prior script and turn them into frames. Pixel size for the minimum dimension is set by default to 400 pixels. FPS to sample at is 25. JPG quality is set at 85%. The video.py and tst_scene_render.py files must reside in the same folder as the script.

### ava_dataset.py
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

Or if you want to download the train and validation videos and cut them in the *'processed'* directory, then you would do use:

`python ava_dataset.py ava_file_names_trainval_v2.1.txt -m trainval -v download -o processed -f dc`

### ava_to_frames.py
Input to the script is:

* **Input file:** either ava_file_names_trainval_v2.1.txt or ava_file_names_test_v2.1.txt.
* **Video Directory:** directory where videos are stored.
* **Output Folder:** where you want to store the processed frames. 
* **FPS:** at how many frames per second you want to sample the videos. Default: 25.
* **Min size:** the minimum size you want to resize the video in pixels. Default: 400 pixels.

This script will create one directory for every video with all frames included. The output frames filenames will follow this pattern:

`<video_id>_<second>_<number of frame>.jpg`

Thus if you saved the frames in the 'frames' folder, for video id '053oq2xB3oU' then you would find the files under:

`../frames/053oq2xB3oU/053oq2xB3oU_0001_000000.jpg
../frames/053oq2xB3oU/053oq2xB3oU_0001_000001.jpg
../frames/053oq2xB3oU/053oq2xB3oU_0001_000002.jpg
../frames/053oq2xB3oU/053oq2xB3oU_0001_000003.jpg
../frames/053oq2xB3oU/053oq2xB3oU_0001_000004.jpg`

Script is run with:

`python ava_to_frames.py <file> -v <video_dir> -o <output_dir> -f <fps> -s <min_size>`

So if you want to get frames from videos stored in the *'videos'* directory and save them to the *'frames'* directory, at 25 fps and with 400 pixels as the minimum size to resize the video to, then you would do:

`python ava_to_frames.py ava_file_names_trainval_v2.1.txt  -v videos -o frames -f 25 -s 400`

## TODO:
* Enable threading functionality.
