import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render

# Create your views here.
def index(request):
	videos = []
	
	if request.method == 'POST':
		search_url = 'https://www.googleapis.com/youtube/v3/search'
		video_url = 'https://www.googleapis.com/youtube/v3/videos'
		
		p1 = request.POST.get('m_player1', '')
		p2 = request.POST.get('m_player2', '')
		t = request.POST.get('m_tourn', '')
		
		if request.POST.get('m_player1', '') == 'N/A':
			p1 = ''
		
		if request.POST.get('m_player2', '') == 'N/A':
			p2 = ''
		
		if request.POST.get('m_tourn', '') == 'N/A':
			t = ''
		
		#parameters for the search
		search_params = {
			'part' : 'snippet',
			'q' : request.POST.get('m_char1', '') + ' ' +  request.POST.get('m_char2', '') +' '+ t + ' ' + p1 + ' ' + p2 + ' Melee',
			'key' : settings.YOUTUBE_DATA_API_KEY,
			'maxResults' : 9,
			'type' : 'video'
		}
		
		video_ids = []
		r = requests.get(search_url, params = search_params)
		
		#store JSON results 
		results = r.json()['items']
		
		#add all results id and video id to the video_id list
		for result in results:
			video_ids.append(result['id']['videoId'])
		
		#parameters for the videos
		video_params = {
			'key' : settings.YOUTUBE_DATA_API_KEY,
			'part' : 'snippet,contentDetails',
			'id' : ','.join(video_ids),
			'maxResults' : 9
		}
		
		r = requests.get(video_url, params=video_params)
		
		#store JSON results
		results = r.json()['items']
		
		
		for result in results:
			
			video_data = {
				'title' : result['snippet']['title'],
				'id' : result['id'],
				'url' : f'https://www.youtube.com/watch?v={result["id"]}',
				'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
				'thumbnail' : result['snippet']['thumbnails']['high']['url']
			}
			#adding each video to videos list
			videos.append(video_data)
			
	context = {
		'videos' : videos
	}
	
	return render(request, 'search/index.html', context)
