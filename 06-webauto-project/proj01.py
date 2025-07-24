# proj01.py

import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# 유튜브 Data API 키와 채널 ID 입력
# https://brunch.co.kr/@mystoryg/156
API_KEY = 'AIzaSyCzjIQzoNKQbUNfpgRzYm-cMQwuQ0F4AR0'  # 여기에 본인의 API 키 입력
CHANNEL_ID = 'UCRuSxVu4iqTK5kCh90ntAgA'  # 여기에 분석할 채널 ID 입력

# 1. 채널의 업로드 플레이리스트 ID 가져오기
url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}'
res = requests.get(url)
playlist_id = res.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# 2. 플레이리스트에서 영상 정보 반복 수집
videos = []
next_page = ''
while True:
    playlist_url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&pageToken={next_page}&key={API_KEY}'
    res = requests.get(playlist_url).json()
    for item in res['items']:
        video_id = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        published = item['snippet']['publishedAt']
        videos.append({'video_id': video_id, 'title': title, 'published': published})
        print(video_id)
    next_page = res.get('nextPageToken', '')
    print(playlist_url)
    if not next_page:
        break

# 3. 각 영상의 상세 정보(조회수, 좋아요, 싫어요 등) 추가 수집
for v in videos:
    video_url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={v["video_id"]}&key={API_KEY}'
    res = requests.get(video_url).json()
    stats = res['items'][0]['statistics']
    snippet = res['items'][0]['snippet']
    v['viewCount'] = int(stats.get('viewCount', 0))
    v['likeCount'] = int(stats.get('likeCount', 0))
    v['dislikeCount'] = int(stats.get('dislikeCount', 0))  # 일부 채널은 제공 안될 수 있음
    v['published'] = snippet['publishedAt'][:10]
    print(res)

# 4. 데이터프레임으로 변환 및 저장
videos_df = pd.DataFrame(videos)
videos_df['published'] = pd.to_datetime(videos_df['published'])
videos_df = videos_df.sort_values(by='published', ascending=False)
videos_df.to_csv('youtube_channel_videos.csv', index=False, encoding='utf-8-sig')


plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 5. 인기 동영상 TOP 10 시각화
top10 = videos_df.sort_values(by='viewCount', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.barh(top10['title'][::-1], top10['viewCount'][::-1], color='tomato')
plt.title('유튜브 인기 동영상 TOP 10')
plt.xlabel('조회수')
plt.tight_layout()
plt.savefig('youtube_top10.png')
plt.show()

# 6. 월별 업로드 패턴 분석
videos_df['year_month'] = videos_df['published'].dt.to_period('M')
monthly = videos_df.groupby('year_month').size()
plt.figure(figsize=(10,5))
monthly.plot(marker='o')
plt.title('월별 영상 업로드 수')
plt.xlabel('업로드 월')
plt.ylabel('업로드 수')
plt.tight_layout()
plt.savefig('youtube_upload_pattern.png')
plt.show()

print('분석 완료! youtube_channel_videos.csv, youtube_top10.png, youtube_upload_pattern.png 파일이 생성되었습니다.')