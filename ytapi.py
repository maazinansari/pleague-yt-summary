import os
from googleapiclient.discovery import build

api_key = os.environ.get('API_KEY_YT')
print(api_key)

yt_service = build(serviceName='youtube', version='v3',  developerKey=api_key)

def get_playlist_id(channel_id):
    channel_request = yt_service.channels().list(part='contentDetails',
                                                 id=channel_id
                                                )
    channel_response = channel_request.execute()
    #UCE8v6FYyQvDszL1SqMd4dNw is Maazin5
    #print(yt_response)
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    
    return(playlist_id)

# returns a dictionary with two items: 
# 1. an integer count of total videos in the playlist
# 2. a list of dictionaries 
def get_playlist_items(playlist_id, n=20, resultsPerPage=20):
    playlist_request = yt_service.playlistItems().list(part="snippet",
                                                       playlistId=playlist_id,
                                                       maxResults=resultsPerPage)
    
    playlist_response = playlist_request.execute()
    video_list = playlist_response['items']
    print(f"Got items 1-{len(video_list)} of {n}")
    
    # loop through as many pages as necessary
    next_page_tkn = playlist_response['nextPageToken']
    while len(video_list) < n:
        prev_len = len(video_list)
        print(prev_len+resultsPerPage, n-prev_len)
        next_request = yt_service.playlistItems().list(part="snippet",
                                                       playlistId=playlist_id,
                                                       maxResults=min(resultsPerPage,n-prev_len),
                                                       pageToken=next_page_tkn)
        next_response = next_request.execute()
        next_video_list = next_response['items']
        video_list += next_video_list
        print(f"Got items {prev_len+1}-{len(video_list)} of {n}")
    
    
    out_dict = dict(total_video_count = playlist_response['pageInfo']['totalResults'],
                    video_list = video_list)
    return(out_dict)

def get_video_details(video_list):
    # views
    # duration
    # comments
    # localized title?
    # 
    return(None)
    
# returns a list of dictionaries. Easier to create than a dictionary of lists
def playlist_to_table(playlist_items):
    total_videos = playlist_items['total_video_count']
    out_list = list()
    for vid in playlist_items['video_list']:
        new_row = {
            'publish_time' : vid['snippet']['publishedAt'],
            'index'        : total_videos - int(vid['snippet']['position']),
            'id'           : vid['snippet']['resourceId']['videoId'],
            'title'        : vid['snippet']['title'],
            #'description'  : vid['snippet']['description'],
            'thumbnail'    : vid['snippet']['thumbnails']['default']['url']
            }
        out_list.append(new_row)
    
    return(out_list)
    
# print(yt_response)



x = get_playlist_id('UC0v-pxTo1XamIDE-f__Ad0Q') #(パーソル パ・リーグTV公式)PacificLeagueTV = UC0v-pxTo1XamIDE-f__Ad0Q
print(x)
y = get_playlist_items(x,107, 50)
z = playlist_to_table(y)
for j in z:
    print(j['index'], j['id'], j['publish_time'])
    
# most videos posted between 0700 UTC and 1400 UTC