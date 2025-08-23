from flask import Flask, render_template, request, jsonify
from sentiment_utils import analyze_all_youtube_comments
import os
from dotenv import load_dotenv
import time
from threading import Thread
import json  
import uuid

load_dotenv()

app = Flask(__name__)
app.config['RESULTS_FOLDER'] = 'static/results'
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

analysis_status = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('video_url', '').strip()
        
        if not video_url:
            return render_template('index.html', error="Please enter a YouTube URL")
        
        if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
            return render_template('index.html', error="Please enter a valid YouTube URL")
        
        analysis_id = str(uuid.uuid4())
        analysis_status[analysis_id] = {
            'status': 'processing',
            'video_url': video_url,
            'progress': 0,
            'start_time': time.time()
        }
        
        Thread(target=run_analysis, args=(analysis_id, video_url)).start()
        
        return render_template('progress.html', analysis_id=analysis_id)
    
    return render_template('index.html')

def run_analysis(analysis_id, video_url):
    try:
        results = analyze_all_youtube_comments(
            video_url,
            progress_callback=lambda p: update_progress(analysis_id, p)
        )
        
        filename = f"{analysis_id}.json"
        filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f)
        
        analysis_status[analysis_id] = {
            'status': 'complete',
            'results_file': filename,
            'total_comments': len(results['comments']),
            'processing_time': round(time.time() - analysis_status[analysis_id]['start_time'], 2)
        }
        
    except Exception as e:
        analysis_status[analysis_id] = {
            'status': 'error',
            'error': str(e)
        }

def update_progress(analysis_id, progress):
    if analysis_id in analysis_status:
        analysis_status[analysis_id]['progress'] = progress

@app.route('/check_status/<analysis_id>')
def check_status(analysis_id):
    return jsonify(analysis_status.get(analysis_id, {'status': 'unknown'}))

@app.route('/results/<analysis_id>')
def show_results(analysis_id):
    status = analysis_status.get(analysis_id, {})
    if status.get('status') != 'complete':
        return render_template('error.html', error="Analysis not complete or not found")
    
    with open(os.path.join(app.config['RESULTS_FOLDER'], status['results_file'])) as f:
        results = json.load(f)
    
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)