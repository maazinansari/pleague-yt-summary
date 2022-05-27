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

def get_video_details(video_id_list):
    comma = ','
    video_list_str = comma.join(video_id_list)
    video_request = yt_service.videos().list(part="snippet,contentDetails,statistics",
                                             id=video_list_str)
    video_response = video_request.execute()
    n_response = video_response['pageInfo']['totalResults']
    
    for vid in video_response['items']:
        # views
        views = vid['statistics']['viewCount']
        # duration
        duration = vid['contentDetails']['duration']
        # comments
        comments = vid['statistics']['commentCount']
        # localized title?

    return(None)
    
# returns a dictionary of dictionaries. Easier to create than a dictionary of lists
# {id_1: {}, id_2: {}, ... }
def playlist_to_table(playlist_items):
    total_videos = playlist_items['total_video_count']
    
    out_dict = dict()
    for vid in playlist_items['video_list']:
        new_id = vid['snippet']['resourceId']['videoId']
        out_dict[new_id] = {
            'publish_time' : vid['snippet']['publishedAt'],
            'index'        : total_videos - int(vid['snippet']['position']),
            'id'           : vid['snippet']['resourceId']['videoId'], #redundant
            'title'        : vid['snippet']['title'],
            #'description'  : vid['snippet']['description'],
            'thumbnail'    : vid['snippet']['thumbnails']['default']['url']
            }
    
    return(out_dict)
    
# print(yt_response)



x = get_playlist_id('UC0v-pxTo1XamIDE-f__Ad0Q') #(パーソル パ・リーグTV公式)PacificLeagueTV = UC0v-pxTo1XamIDE-f__Ad0Q
print(x)
y = get_playlist_items(x,107, 50)
z = playlist_to_table(y)
for j in z:
    print(z[j]['index'], z[j]['id'], z[j]['publish_time'])
    
# most videos posted between 0700 UTC and 1400 UTC


# vid_list = [x[][] for x in vid_listjson]