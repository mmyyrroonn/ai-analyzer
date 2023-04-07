import tiktoken
import logging

class PreProcesser:
    def __init__(self) -> None:
        self.token_limit = 1024
        self.content_limit = 10
        pass

    def pre_format(self, contents_list, existing_results):
        contents_dict = {}
        existing_dict = {}
        for item in contents_list:
            contents_dict[item['id']] = item['content']
        for item in existing_results:
            existing_dict[item['id']] = item['refined']
        return contents_dict, existing_dict

    def filter_contents(self, contents_list, existing_results):
        contents, existing = self.pre_format(contents_list, existing_results)
        filtered_contents_with_enough_length = dict(filter(lambda item: len(item[1]) >= 30 if item[1] is not None else False, contents.items()))
        existing_keys = existing.keys()
        filtered_contents = dict(filter(lambda item: item[0] not in existing_keys, filtered_contents_with_enough_length.items()))
        return filtered_contents

    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def group_contents(self, filtered_contents):
        group_contents = {}
        ids = []
        contents = []
        token_counts = 0
        index = 0
        for key, value in list(filtered_contents.items()):
            token_count = self.num_tokens_from_string(value)
            if token_counts + token_count > self.token_limit or len(contents) >= self.content_limit:
                group_contents[index] = {"ids": ids, "contents": contents}
                index += 1
                ids = []
                contents = []
                token_counts = 0
            ids.append(key)
            contents.append(value)
            token_counts += token_count
        group_contents[index] = {"ids": ids, "contents": contents}
        return group_contents

class PostProcesser:
    def __init__(self) -> None:
        self.logger = logging.getLogger("post-processor")
        pass

    def refine_text_and_split(self, raw_results):
        refined_results = {}
        for key, data in raw_results.items():
            try:
                striped_data = data.strip().strip('"').strip('!').strip('').lstrip('Keywords:').strip()
                splited_data = striped_data.split(',')
                refined_data = [ item.strip() for item in splited_data ]
                refined_results[key] = refined_data
            except Exception as e:
                self.logger.error(e)
        return refined_results
        