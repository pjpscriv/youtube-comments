# youtube-comments

A python script for downloading youtube comments based on [senticomment](https://github.com/johnafish/senticomment).

## Install Dependencies

The script uses these python libraries:
- `httplib2`
- `csv`
- `oauth2client`
- `google-api-python-client`

You can install them by running:
```
pip3 install -r requirements.txt
```

## Set Up Google Cloud
1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a new project. 
2. Enable the YouTube Data API v3.
3. Add an email address and product name to the 'OAuth consent screen' tab.
4. Create credentials (OAuth client ID, Application Type: Other).
5. Go into the options for the new credentials and click *Download JSON* 
6. Download this file and rename it `client_secrets.json`.

## Running the Code
```
python3 youtube-comments.py --videoid={your video ID here}
```
This will run the script and generate a CSV of the video's comments.
