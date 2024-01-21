from gpt4all import GPT4All
import itertools
from generate import utils


class API:
    logger = utils.create_logger()

    def __init__(self, caching=True):
        # Assumes windows
        self.caching = caching
        if self.caching:
            self.previous_responses = utils.manage_dict("responses")

    def process_message(self, message: str) -> str:
        self.logger.warn(f"Message:\n{message}\n\nAnswer:\n")
        if self.caching:
            if message in self.previous_responses:
                self.logger.error(
                    "Found cached response: " + self.previous_responses[message]
                )
                return self.previous_responses[message]
        return ""

    def cache_message(self, message: str, response: str):
        self.logger.info(f"Cached: {response}")
        if self.caching:
            self.previous_responses[message] = response
            utils.manage_dict("responses", self.previous_responses)

    def process_conversation(self, conversation: list[str], system_template: str = ""):
        # This format works well enough.
        response = (
            "Context:\n"
            + "\n".join(conversation[:-1])
            + "\n\nAnswer the following:\n"
            + conversation[-1]
        )
        return self.process_message(response, system_template)

    def process(self, blurb_list, system_template: str = "") -> list[str]:
        """
        [] -> [[]] -> 0 items
        [['1']] -> [['1']] -> 1 item
        ['1', ['1', '2']] -> [['1', '1'], ['1', '2']] -> 2 items
        [['1'. '3'], ['1', '2']] -> [['1', '1'], ['1', '2'], ['3', '1'], ['3', '2']] -> 4 items
        """
        self.logger.debug("Blurb_list: " + str(blurb_list))

        def flatten_to_list_of_strings(to_flatten: list):
            def should_flatten(questionable_list):
                for item in questionable_list:
                    if isinstance(item, list):
                        return True
                return False

            def flatten(list_of_lists):
                result = []
                for item in list_of_lists:
                    if isinstance(item, list):
                        result.extend(flatten(item))
                    else:
                        result.append(item)
                return result

            flattened = []
            for item in to_flatten:
                if isinstance(item, str):
                    flattened.append([item])
                elif isinstance(item, list):
                    if should_flatten(item):
                        flattened.append(flatten(item))
                    else:
                        flattened.append(item)
            flattened = [item for item in flattened if item]
            return flattened

        converted_lists = flatten_to_list_of_strings(blurb_list)
        self.logger.debug(
            "converted_lists (list[item] to list[list[str]]): " + str(converted_lists)
        )
        product_result = list(itertools.product(*converted_lists))
        self.logger.debug("product_result: " + str(product_result))
        to_return = []
        for blurb in product_result:
            if len(blurb) == 1:
                to_return.append(self.process_message(blurb[0], system_template))
            elif len(blurb) > 1:
                to_return.append(self.process_conversation(blurb, system_template))
        return to_return


class Gpt4allAPI(API):
    def __init__(self, caching=True, use_gpu=False, reduce_threads=True):
        super().__init__(caching)
        self.gpt4all_instance = GPT4All(
            "wizardlm-13b-v1.2.Q4_0", device="gpu" if use_gpu else ""
        )
        print("using gpu")
        # if reduce_threads:
        #     self.gpt4all_instance.model.set_thread_count(1)
        # else:
        #     self.gpt4all_instance.model.set_thread_count(4)

    # override
    def process_message(self, message: str, system_template: str = ""):
        if response := super().process_message(message):
            return response
        with self.gpt4all_instance.chat_session(system_template):
            response = self.gpt4all_instance.generate(
                message,
                max_tokens=50000,
                temp=0.9,
                top_k=40,
                top_p=0.9,
                repeat_penalty=1.1,
                repeat_last_n=64,
                n_batch=9,
                # streaming=True,
            )
        super().cache_message(message, response)
        return response


