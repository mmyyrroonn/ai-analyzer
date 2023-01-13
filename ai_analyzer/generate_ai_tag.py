from util.wordcloud import AIPicGenerator
from api.apis import API
from analyzer.processors import PreProcesser
from tags.tags import AITagFactory
import time

def main_logic():
    api = API()
    ai_pic_generator = AIPicGenerator()
    pre_processor = PreProcesser()
    ai_tag_factory = AITagFactory("AI Analyzed Post Tag", "Analyzed tag based on all existing posts", "0xffffffff")

    while True:
        next_profile = api.fetch_next_ai_tag_profile()
        if next_profile is not None:
            print("Process next profile {}".format(next_profile['profile']))
            profile_id = next_profile['profile']
            ai_result = api.get_all_ai_results(profile_id)
            if len(ai_result) == 0:
                print("no ai result for profile {}".format(profile_id))
                continue
            print("ai_result: {}".format(ai_result))
            _, existing = pre_processor.pre_format([], ai_result)
            img_path = ai_pic_generator.generate_word_cloud_pic(existing, profile_id, ai_tag_factory.nftid)
            ai_tag = ai_tag_factory.generate_ai_tag_metadata(profile_id, img_path)
            api.push_nft(ai_tag)
        time.sleep(5)

main_logic()