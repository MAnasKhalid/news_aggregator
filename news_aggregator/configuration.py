from configparser import ConfigParser
import logging

from mod_api.Source import Source


class NewsAggregatorConfigParser(ConfigParser):
    '''
        Extend config parser to allow for lists
        see: http://stackoverflow.com/questions/335695/lists-in-configparser
    '''

    def getlist(self, section, option):
        ''' Get List of strings '''
        value = str(self.get(section, option))
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def getlistint(self, section, option):
        ''' Get list of integers '''
        return [int(x) for x in self.getlist(section, option)]


api_config = NewsAggregatorConfigParser()
api_config.read('news_aggregator/config.ini')
SECTIONS = api_config.sections()

NEWS_SOURCES = {}
for section in api_config.getlist('SOURCE', 'name'):
    try:
        api_config[section]
    except KeyError:
        logging.warning(f'Section : {section} is listed, but not defined.')
        continue
    source_params = dict(api_config[section])
    base_url = source_params.pop('base_url')
    NEWS_SOURCES[section] = Source(name=section,
                                   base_url=base_url,
                                   **source_params
                                   )
