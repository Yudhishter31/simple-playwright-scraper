import requests
from scrapling.fetchers import PlayWrightFetcher, StealthyFetcher
from playwright.sync_api import Page
import time
API_KEY = '555QNLYNBHIRANWUM4'


def send_captcha(sitekey):
    # API_URL = 'https://9kw.eu/index.cgi'
    API_URL = 'https://www.9kw.eu/'
    data = {
        'action': 'usercaptchaupload',
        'apikey': API_KEY,
        'file-upload-01': sitekey,
        'base64': '1',
        'selfsolve': '1',
        'maxtimeout': '120',
        'json': '1',
    }
    response = requests.post(API_URL, data)
    return response.json()


def get_captcha_text(captcha_id):
    API_URL = 'https://9kw.eu/index.cgi'
    data = {
        'action': 'usercaptchacorrectdata',
        'id': captcha_id,
        'apikey': API_KEY,
        'info': 1,
        'json': '1',
    }
    response = requests.get(API_URL, data)
    return response.json()


def solve_captcha(sitekey):
    timeout = 120
    captcha_id = send_captcha(sitekey)
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            resp = get_captcha_text(captcha_id)
        except CaptchaError:
            pass
        else:
            if resp.get('answer') != 'NO DATA':
                if resp.get('answer') == 'ERROR NO USER':
                    raise CaptchaError(
                        'Error: No user available to solve captcha'
                    )
                else:
                    print('captcha solved!')
                    return captcha_id, resp.get('answer')
        print('Waiting for CAPTCHA ...')
        time.sleep(1)
        raise CaptchaError('Error: API timeout')


class CaptchaError(Exception):
    pass


def make_request(url):
    page = StealthyFetcher.fetch(url=url, block_images=True,
                                 humanize=True,
                                 timeout=60000,
                                 page_action=tinker_page, wait=3000,
                                 )
    print(page.status)
    extract_data(page)
    # title = page.css('title').get()
    # print(title)


def tinker_page(page: Page):
    page.locator('#searchboxinput').fill(
        'The Westin Copley Place (New Opening)')
    page.wait_for_timeout(3000)
    # time.sleep(0.3)
    page.get_by_role('button', name='Search').click()
    page.wait_for_timeout(7000)
    # time.sleep(0.3)
    # time.sleep(7)
    # page.get_by_role('tab').filter(has_text='Reviews').click()
    # page.wait_for_timeout(2500)
    page.mouse.wheel(3, 5000)
    page.mouse.wheel(0, 5000)
    page.mouse.wheel(0, 5000)
    page.mouse.wheel(0, 5000)
    page.wait_for_timeout(3500)
    # time.sleep(10)
    sitekey = ''
    if sitekey:
        captcha_result = solve_captcha(sitekey)
        print(captcha_result)
    page.screenshot(full_page=True, path='gm2.jpg')
    return page
    # html = page.content()


def extract_data(page):
    title = page.css('title').get()
    details = page.css('.rogA2c ::text').extract()
    print(len(details))
    print('*' * 30)
    print(*details)
    print()
    print(title)

    address_bu = page.css('[data-tooltip="Copy address"]')
    address = address_bu.css('.rogA2c ::text').get()
    print('address: ', address)

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
        place_type = page.css('.fjHK4 ::text').get()
        print('type:', place_type)
    except Exception as e:
        print(e)


def main():
    url = 'https://www.google.com/maps'
    make_request(url=url)


main()
