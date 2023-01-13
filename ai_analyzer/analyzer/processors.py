class PreProcesser:
    def __init__(self) -> None:
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

class PostProcesser:
    def __init__(self) -> None:
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
                print(e)
        return refined_results
        