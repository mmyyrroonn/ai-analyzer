"""Main module."""

from flask import Flask, request
from .analyzer.main import AIAnalyzer
from .util.json import load_keywords
from .util.wordcloud import AITagGenerator
from .api.apis import API
from .analyzer.processors import PreProcesser, PostProcesser

app = Flask(__name__)
ai_tag_generator = AITagGenerator()
api = API()

@app.route('/')
def hello():
    return "Hello, NoSocial!"

@app.route('/test', methods=['POST'])
def three_key_words():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the 'prompt' field from the JSON data
    prompt = data['prompt']
    ai_analyzer = AIAnalyzer()
    results = ai_analyzer.query_key_words_for_post(prompt)
    return results

@app.route('/analyzeProfile', methods=['POST'])
def analyze_profile():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the 'prompt' field from the JSON data
    profile_id = data['profileId']
    content = api.get_all_posts(profile_id)
    ai_result = api.get_all_ai_results(profile_id)
    pre_processor = PreProcesser()
    filtered_content = pre_processor.filter_contents(content, ai_result)
    cutted_filtered_content = dict([(key, filtered_content[key]) for i, key in enumerate(filtered_content) if i < 5])
    ai_analyzer = AIAnalyzer()
    raw_results = ai_analyzer.query_key_words_for_content(cutted_filtered_content)
    post_processor = PostProcesser()
    refined_results = post_processor.refine_text_and_split(raw_results)
    update_results = api.update_ai_results(profile_id, raw_results, refined_results)
    return update_results

@app.route('/fetchAllKeywords', methods=['POST'])
def fetch_all_keywords():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the 'prompt' field from the JSON data
    profile_id = data['profileId']
    keywords = load_keywords(profile_id)
    filtered_keywords = [ item for item in keywords if (not item.startswith('000')) and len(item)!=0]
    refined_keywords = [ item.strip().strip('\\n').strip("Keywords:").strip() for item in filtered_keywords]
    splited_keywords = []
    for data in refined_keywords:
        splited_keywords.extend(data.split(','))
    refined_splited_keywords = [ item.strip().strip('\\n').strip() for item in splited_keywords]
    ai_tag_generator.generate_word_cloud_pic(' '.join(refined_splited_keywords))
    return refined_splited_keywords
    

