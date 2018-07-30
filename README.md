# youtube-comments

A script for downloading youtube comments based on [senticomment](https://github.com/johnafish/senticomment).

## Install Dependencies

Use python3 g.


It's recommended that you use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) so that existing packages aren't tempered with.
You'll need Python 3 installed with pip3. Run:

```
pip3 install -r requirements.txt 
```

## Set Up Google Cloud
1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a new project. 
2. Enable the YouTube Data API v3.
3. Create credentials (OAuth client ID, Application Type: Other) and download them to `client_secrets.json`.

## Running the Code
Run `python3 youtube-comments.py --videoid={your video ID here}` to run the script and generate a CSV file.
