# Video Frames View and Save Tool

## Overview
This tool allow you to input video file and display single frame on window. Also you can save the frame by this tool.


## Prerequisites
* Python>=3.7

## How to Install
After installing Python>=3.7, please run command below in your venv.
```bash
pip install -U pip setuptools build
python -m build
pip install dist/video_frame_viewer-1.0.0-py3-none-any.whl
```

## Usage
[Sample code](./sample.py) is available.
```python
from frame_viewer.app import run_app

run_app(VIDEO_PATH)
```