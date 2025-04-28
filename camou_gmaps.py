from camoufox.sync_api import Camoufox
from scrapling.parser import Adaptor
import json
import random


def make_request(searchTexts):
    with Camoufox(headless=False, humanize=True, block_images=True,
                  timeout=0,
                  # set_viewport_size={'width': 1280, 'height': 1024},
                  i_know_what_im_doing=True) as browser:

        # page = StealthyFetcher.fetch(url=url, block_images=True,
        #                              humanize=True,
        #                              timeout=60000,
        #                              page_action=tinker_page, wait=3000,
        #                              )
        # context = browser.new_context()
        url = 'https://www.google.com/maps'
        page = browser.new_page()
        page.set_default_timeout(timeout=0)
        page.set_viewport_size({'width': 1280, 'height': 1024})
        # page.set_viewport_size({"width": 1280, "height": 1024})
        page.goto(url)
        # search_texts = ['The Westin Copley Place (New Opening)',
        #                 'BayCare Urgent Care (New Tampa)']
        for search_text in searchTexts:
            print('+' * 30)
            print('Searching for: ', search_text)
            html_text = tinker_page(page, search_text)
            page.locator('[aria-label="Close"]').first.click()
    # print(page.status)
            extract_data(html_text)
        # url2 = 'BayCare Urgent Care (New Tampa)'
    # title = page.css('title').get()
    # print(title)


def tinker_page(page, search_text):
    search_box = page.locator('#searchboxinput')
    search_box.click()
    search_box.type(
        search_text,
        delay=0.34)

    search_box.press(key='Enter')
    page.wait_for_timeout(2750)
    # time.sleep(0.3)
    # page.get_by_role('button', name='Search').click()
    page.wait_for_timeout(2030)
    page.locator('h1').first.click()
    # time.sleep(0.3)
    # time.sleep(7)
    # page.get_by_role('tab').filter(has_text='Reviews').click()
    # page.wait_for_timeout(2500)
    random_scroll(page)
    # page.mouse.wheel(0, 5000)
    # page.mouse.wheel(0, 5000)
    # page.mouse.wheel(0, 5000)
    page.wait_for_timeout(3500)
    # page.locator('[aria-label="Close"]').first.click()
    # time.sleep(10)
    return page.content()
    # html = page.content()


def random_scroll(page):
    random_number = random.randint(50, 1150)
    page.mouse.wheel(0, random_number)


def extract_data(html_text):
    page = Adaptor(html_text)
    title = page.css('h1 ::text').get()
    details = page.css('.rogA2c ::text').extract()
    print(len(details))
    print('*' * 30)
    print(*details)
    print()
    print('title: ', title)

    address_bu = page.css('[data-tooltip="Copy address"]')
    address = address_bu.css('.rogA2c ::text').get_all()
    print('address: ', address[0] if len(address) > 0 else '')
    # if len(address) > 1:
    located_in = address[1] if len(address) > 1 else ''
    print('located_in: ', located_in)

    website_bu = page.css('[data-tooltip="Open website"]')
    website = website_bu.css('.rogA2c ::text').get()
    print('website: ', website)

    phone_bu = page.css('[data-tooltip="Copy phone number"]')
    phone = phone_bu.css('.rogA2c ::text').get()
    print('phone: ', phone)

    plus_code_bu = page.css('[data-tooltip="Copy plus code"]')
    maps_plus_code = plus_code_bu.css('.rogA2c ::text').get()
    print('plus code: ', maps_plus_code)

    try:
        rating_bar = page.css('.F7nice')
        rating = rating_bar.css(' ::text').extract()
        reviews = rating[-1].replace('(', '').replace(')', '').replace(',', '')
        print('rating: ', rating[0])
        print('no. of reviews: ', reviews)
        place_type = page.css('.DkEaL ::text').get()
        print('type:', place_type)
    except Exception as e:
        print(e)

    place_data = {
        'title': title,
        'address': address[0] if len(address) > 0 else '',
        'phone': phone,
        'website': website,
        'google maps plus code': maps_plus_code,
        'rating': rating,
        'reviews': reviews,
        'place type': place_type,
    }
    final_data.append(place_data)


def main():
    with open('searchTextMaps.json', 'r+') as file:
        searchTexts = json.load(file)
    make_request(searchTexts[21:26])


final_data = []
main()
print(len(final_data))
with open('./output/mapsData.json', 'w+') as file:
    json.dump(final_data, file)
