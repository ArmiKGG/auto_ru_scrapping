import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import lxml
from json import JSONDecoder
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

head = Headers(headers=True)


def extract_json_objects(text, decoder=JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1


def soup_it(link):
    res = requests.get(link, headers=head.generate(), verify=False)
    soup = BeautifulSoup(res.content, 'lxml')
    return soup, str(res.content)


class AutoRu:
    def __init__(self, soup, data):
        self.soup = soup
        self.data = data

    def get_comment(self):
        data = self.soup.find(class_='CardDescriptionHTML')
        if data:
            return data.text
        return None

    def get_images(self):
        data = self.soup.find_all(class_='ImageGalleryDesktop__thumb')
        data = ['https://' + i['src'].replace('//', '').replace('small', '1200x900n') for i in data]
        if data:
            return data
        return None

    def get_tag(self):
        data = self.soup.find(class_='OfferPriceBadge')
        if data:
            return data.text
        return None

    def get_params(self):
        data = self.soup.select('ul.CardInfo li')
        all_jsonned = []
        for dat in data:
            dexter = dat.find_all('span')
            app_json = {
                dexter[0].text: dexter[1].text
            }
            all_jsonned.append(app_json)

        return all_jsonned

    def get_specs(self):
        data_clt = {}
        prices = []
        services = []

        for result in extract_json_objects(self.data):
            if result.get('owners_number'):
                data_clt['owners_number'] = result
            if result.get('transport_tax'):
                data_clt['transport_tax'] = result
            if result.get('health'):
                data_clt['health'] = result
            if result.get('service'):
                services.append(result)
            if result.get('is_on_moderation'):
                data_clt['is_on_moderation'] = result
            if result.get('abbr'):
                data_clt['abbr'] = result
            if result.get('mileage'):
                data_clt['mileage'] = result
            if result.get('aux'):
                data_clt['additional_options'] = result
            if result.get('create_timestamp') and result.get('RUR'):
                prices.append(result)

            if result.get('latitude') and result.get('longitude'):
                data_clt['lat_long'] = result
        for img in data_clt['mileage']['image_urls']:
            img['url'] = img['sizes']['1200x900n'].replace('//', '')
            del img['sizes']

        data_clt['prices'] = prices
        data_clt['services'] = services
        return data_clt


