from util.wordcloud import AIPicGenerator
from api.apis import API
from analyzer.processors import PreProcesser
from tags.tags import AITagFactory
import time
import logging
import sys

def main_logic():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger("tag-generator")
    api = API()
    ai_pic_generator = AIPicGenerator()
    pre_processor = PreProcesser()
    ai_tag_factory = AITagFactory("AI Analyzed Post Tag", "Analyzed tag based on all existing posts", "0xffffffff")

    while True:
        next_profile = api.fetch_next_ai_tag_profile()
        if next_profile is not None:
            logger.info("Process next profile {}".format(next_profile['profileId']))
            profile_id = next_profile['profileId']
            id = next_profile['id']
            ai_result = api.get_all_ai_results(profile_id)
            if len(ai_result) < 10:
                logger.info("no ai result for profile {}".format(profile_id))
                api.update_profile_status(id, -1)
                continue
            logger.info("ai_result: {}".format(ai_result))
            _, existing = pre_processor.pre_format([], ai_result)
            img_path, tags = ai_pic_generator.generate_word_cloud_pic(existing, profile_id, ai_tag_factory.nftid)
            ai_tag = ai_tag_factory.generate_ai_tag_metadata(profile_id, img_path, tags)
            api.push_nft(ai_tag)
            api.update_profile_status(id, -1)
        time.sleep(1)

main_logic()