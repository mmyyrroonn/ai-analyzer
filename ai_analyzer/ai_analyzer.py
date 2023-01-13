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
    pre_processor = PreProcesser()
    next_profile = api.fetch_next_ai_tag_profile()
    if next_profile is not None:
        print("Process next profile {}".format(next_profile['profile']))
        profile_id = next_profile['profile']
        ai_result = api.get_all_ai_results(profile_id)
        print("ai_result: {}".format(ai_result))
        _, existing = pre_processor.pre_format([], ai_result)
        ai_tag_generator.generate_word_cloud_pic(existing, profile_id)
    return "success"
