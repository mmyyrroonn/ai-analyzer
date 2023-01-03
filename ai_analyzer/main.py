from analyzer.main import AIAnalyzer
from util.json import load_keywords
from util.wordcloud import AITagGenerator
from api.apis import API
from analyzer.processors import PreProcesser, PostProcesser
import time

def main_logic():
    api = API()
    pre_processor = PreProcesser()
    ai_analyzer = AIAnalyzer()
    post_processor = PostProcesser()

    while True:
        next_profile = api.fetch_next_waiting_profile()
        if next_profile is not None:
            print("Process next profile {}".format(next_profile['profile']))
            profile_id = next_profile['profile']
            content = api.get_all_posts(profile_id)
            print("content: {}".format(content))
            ai_result = api.get_all_ai_results(profile_id)
            print("ai_result: {}".format(ai_result))

            filtered_content = pre_processor.filter_contents(content, ai_result)
            cutted_filtered_content = dict([(key, filtered_content[key]) for i, key in enumerate(filtered_content) if i < 5])
            
            raw_results = ai_analyzer.query_key_words_for_content(cutted_filtered_content)
            
            refined_results = post_processor.refine_text_and_split(raw_results)
            api.update_ai_results(profile_id, raw_results, refined_results)
            api.update_profile_status(next_profile['id'])
        time.sleep(1)

main_logic()