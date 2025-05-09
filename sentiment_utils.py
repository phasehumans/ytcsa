from models.load_model import load_model
from googleapiclient.discovery import build
import re
import os
from dotenv import load_dotenv
from collections import defaultdict
import time

load_dotenv()

model, vectorizer = load_model()

def extract_video_id(url):
    """Extract YouTube video ID from URL with comprehensive pattern matching"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/live\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*[&?]v=([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    
    for pattern in patterns:
        try:
            match = re.search(pattern, url)
            if match and match.group(1):
                return match.group(1)
        except re.error:
            continue
            
    return None

def clean_text(text):
    text = str(text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.strip().lower()

def predict_sentiment(comment):
    clean_comment = clean_text(comment)
    vectorized_comment = vectorizer.transform([clean_comment])
    return model.predict(vectorized_comment)[0]

def get_all_youtube_comments(video_url, progress_callback=None):
    """Fetch all available comments from YouTube video"""
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL - could not extract video ID")
    
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
    comments = []
    next_page_token = None
    total_comments = 0
    processed_comments = 0
    
    try:
        video_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()
        total_comments = int(video_response['items'][0]['statistics']['commentCount'])
    except:
        total_comments = 0
    
    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                order="relevance",
                pageToken=next_page_token
            )
            response = request.execute()
            
            if 'items' not in response:
                break
                
            batch = [
                item['snippet']['topLevelComment']['snippet']['textDisplay']
                for item in response['items']
            ]
            comments.extend(batch)
            processed_comments += len(batch)
            
            if progress_callback and total_comments > 0:
                progress = min(100, int((processed_comments / total_comments) * 100))
                progress_callback(progress)
            
            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
                time.sleep(1)
            else:
                break
                
        except Exception as e:
            if 'quotaExceeded' in str(e):
                raise ValueError("YouTube API quota exceeded - try again later")
            break
    
    return comments

def analyze_all_youtube_comments(video_url, progress_callback=None):
    """Analyze all comments with progress reporting"""
    comments = get_all_youtube_comments(video_url, progress_callback)
    
    results = {
        'video_id': extract_video_id(video_url),
        'comments': [],
        'counts': {'positive': 0, 'neutral': 0, 'negative': 0},
        'examples': {'positive': [], 'neutral': [], 'negative': []},
        'total_comments': len(comments),
        'processed_comments': 0
    }
    
    for i, comment in enumerate(comments):
        sentiment = predict_sentiment(comment)
        results['comments'].append({
            'text': comment,
            'sentiment': sentiment,
            'id': i
        })
        results['counts'][sentiment] += 1
        
        if len(results['examples'][sentiment]) < 3:
            results['examples'][sentiment].append(comment)
        
        results['processed_comments'] = i + 1
        if progress_callback and results['total_comments'] > 0:
            progress = min(100, int((i + 1) / results['total_comments'] * 100))
            progress_callback(progress)
    
    results['percentages'] = {
        'positive': round(results['counts']['positive'] / results['total_comments'] * 100, 1),
        'neutral': round(results['counts']['neutral'] / results['total_comments'] * 100, 1),
        'negative': round(results['counts']['negative'] / results['total_comments'] * 100, 1)
    }
    
    return results