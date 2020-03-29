#!/usr/bin/python

import httplib2
import os
import sys
import csv

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client-secrets-2.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

OUTPUT_FILENAME = "comments_{0}.csv"

def get_authenticated_service(args):
    print("thing")
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)
    print("thing2")

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    with open("youtube-v3-discoverydocument.json", "r") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

def get_comment_threads(youtube, video_id, comments=[], token=""):
    results = youtube.commentThreads().list(
        part="snippet",
        pageToken=token,
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    if "nextPageToken" in results:
        return get_comment_threads(youtube, video_id, comments, results["nextPageToken"])
    else:
        return comments


# TODO: make --videoid= just --vid= or --id= or something
def main():
    argparser.add_argument("--videoid", help="Required; ID for video for which the comment will be inserted.")
    args = argparser.parse_args()

    if not args.videoid:
        exit("Please specify videoid using the --videoid= parameter.")

    youtube = get_authenticated_service(args)
    csv_filename = OUTPUT_FILENAME.format(args.videoid)
    try:
        video_comment_threads = get_comment_threads(youtube, args.videoid)

        with open(csv_filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for comment in video_comment_threads:
                writer.writerow([comment])

        print("Downloaded {0} comments to {1}}".format(len(video_comment_threads)))
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    main()
