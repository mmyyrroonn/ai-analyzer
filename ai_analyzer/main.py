from analyzer.main import AIAnalyzer
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
            # cutted_filtered_content = dict([(key, filtered_content[key]) for i, key in enumerate(filtered_content) if i < 100])       
            analyzer_process = ai_analyzer.query_key_words_for_content(filtered_content)

            raw_results = {}
            for key, rst in analyzer_process:
                raw_results[key] = rst
                if len(raw_results) >= 10:
                    refined_results = post_processor.refine_text_and_split(raw_results)
                    api.update_ai_results(profile_id, raw_results, refined_results)
                    raw_results = {}
            # update remaining ai results
            refined_results = post_processor.refine_text_and_split(raw_results)
            api.update_ai_results(profile_id, raw_results, refined_results)

            # mark as finished
            api.update_profile_status(next_profile['id'])

            # quite simple achievement system
            # valid content larger than 60 will try to generate ai tag
            # right now, the ai tag won't update and it's only generated once
            if len(filtered_content) + len(ai_result) >= 60:
                api.push_ai_tag_generator(profile_id)
        time.sleep(5)

main_logic()