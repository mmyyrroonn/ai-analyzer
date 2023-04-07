from analyzer.main import AIAnalyzer
from api.apis import API
from analyzer.processors import PreProcesser, PostProcesser
import time
import multiprocessing
import logging
import sys

def processor(thread_num, queue):
    logger = logging.getLogger("ai-processor")
    logger.info("Thread {} started".format(thread_num))
    api = API()
    pre_processor = PreProcesser()
    ai_analyzer = AIAnalyzer()
    post_processor = PostProcesser()
    update_step = 3
    while True:
        next_profile = queue.get()
        if next_profile is not None:
            profile_id = next_profile['profileId']
            id = next_profile['id']
            logger.info("Thread {} processing profile {}".format(thread_num, profile_id))
            content = api.get_all_posts(profile_id)
            ai_result = api.get_all_ai_results(profile_id)
            logger.info("Thread {} ai_result content: {}".format(thread_num, ai_result))
            logger.info("Thread {} raw contents: {}".format(thread_num, content))
    
            filtered_content = pre_processor.filter_contents(content, ai_result)
            group_contents = pre_processor.group_contents(filtered_content)
            logger.info("Thread {} grouped contents: {}".format(thread_num, group_contents))
            analyzer_process = ai_analyzer.query_key_words_for_content(group_contents)
    
            unprocessed = len(filtered_content)
            api.update_profile_status(id, unprocessed)
            raw_results = {}
            for index, keys, rst in analyzer_process:
                raw_results.update({k: v for k, v in zip(keys, rst)})
                if len(raw_results) >= update_step:
                    logger.info("Thread {} raw_results contents: {}".format(thread_num, raw_results))
                    refined_results = post_processor.refine_text_and_split(raw_results)
                    api.update_ai_results(profile_id, raw_results, refined_results)
                    unprocessed -= len(raw_results)
                    api.update_profile_status(id, unprocessed)
                    raw_results = {}
            refined_results = post_processor.refine_text_and_split(raw_results)
            api.update_ai_results(profile_id, raw_results, refined_results)
    
            api.update_profile_status(id, 0)

def main_logic():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    api = API()
    queue = multiprocessing.Queue()
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=processor, args=(i, queue))
        p.start()
        processes.append(p)
    try:
        while True:
            # Retrieve IDs and add them to the queue
            next_profile = api.fetch_next_waiting_profile()
            if next_profile is not None:
                queue.put(next_profile)
            time.sleep(0.2)
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
    for p in processes:
        p.join()

if __name__ == '__main__':
    main_logic()