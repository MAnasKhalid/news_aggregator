import time

import requests

from mod_api.helpers import aggregator_map
from mod_api.reddit import authenticate, get_data


class Source:
    def __init__(self, name, base_url, **extra_args):
        self.name = name
        self.base_url = base_url
        self.reddit = None
        if name == 'REDDIT':
            self.reddit = authenticate()

    def get_url(self):
        return self.base_url

    def get_data(self,query):
        if self.reddit:
            return get_data(query=query,reddit=self.reddit)
        else:
            # 1. implement general get_generic_api_data here in future
            # 2. find a way to get few field otherwise looping it the last option
            # 3. Store the results back in queryset
            data = requests.get(f"https://newsapi.org/v2/top-headlines?q={query}&apiKey=1e1d0182b7994878b37709fdaebcf877").json()
            all_data = []
            for article in data['articles']:
                all_data.append(aggregator_map(article['url'],article['title'],source=self.name))
            return all_data