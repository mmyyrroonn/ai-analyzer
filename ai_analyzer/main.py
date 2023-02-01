from analyzer.main import AIAnalyzer
from api.apis import API
from analyzer.processors import PreProcesser, PostProcesser
import time

def main_logic():
    api = API()
    pre_processor = PreProcesser()
    ai_analyzer = AIAnalyzer()
    post_processor = PostProcesser()

    update_step = 3

    while True:
        next_profile = api.fetch_next_waiting_profile()
        if next_profile is not None:
            print("Process next profile {}".format(next_profile['profileId']))
            profile_id = next_profile['profileId']
            id = next_profile['id']
            content = api.get_all_posts(profile_id)
            print("content: {}".format(content))
            ai_result = api.get_all_ai_results(profile_id)
            print("ai_result: {}".format(ai_result))

            filtered_content = pre_processor.filter_contents(content, ai_result)
            # cutted_filtered_content = dict([(key, filtered_content[key]) for i, key in enumerate(filtered_content) if i < 100])       
            analyzer_process = ai_analyzer.query_key_words_for_content(filtered_content)

            unprocessed = len(filtered_content)
            api.update_profile_status(id, unprocessed)
            raw_results = {}
            for key, rst in analyzer_process:
                raw_results[key] = rst
                if len(raw_results) >= update_step:
                    refined_results = post_processor.refine_text_and_split(raw_results)
                    api.update_ai_results(profile_id, raw_results, refined_results)
                    unprocessed -= update_step
                    api.update_profile_status(id, unprocessed)
                    raw_results = {}
            # update remaining ai results
            refined_results = post_processor.refine_text_and_split(raw_results)
            api.update_ai_results(profile_id, raw_results, refined_results)

            # mark as finished
            api.update_profile_status(id, 0)
        time.sleep(1)

main_logic()