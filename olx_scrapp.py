from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import path_to_driver, start_url
from Logging import Logger

class ScrappOlx:
    def __init__(self):
        self.log = Logger().custom_logger()
        
        self.driver = webdriver.Firefox(executable_path=path_to_driver)
        self.driver.implicitly_wait(60)
        self.wait = WebDriverWait(self.driver, 60)

        self.start_url = start_url
    def parse(self):
        self.driver.get(start_url)
        self.log.start('Pareser started ad {}'.format(start_url))
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="homeShowAllAds"]')))
        self.all_caregories = self.driver.find_elements(By.XPATH,
            '//div[contains(@class, "subcategories-list")]/div/a[contains(@class, "inlblk")]'
            )
        self.hrefs_to_categorys = (no_blank for no_blank in 
            (item.get_attribute('href') for item in self.all_caregories)
                if len(no_blank)>2)
        #возвращаем ссылки на все категории
        return self.hrefs_to_categorys
    
    def get_info_category(self):
        hrefs = self.parse()
        for item in hrefs:
            self.first_page = True
            self.driver.get(item)
            self.max_page = self.driver.find_elements(
                By.XPATH, '//span[contains(@class, "item fleft")][last()]'
                )[0].text
            for number in range(1, int(self.max_page)+1):
                if not self.first_page:
                    self.new_url = item+f'?page={number}'
                    print(f'self.new_url: {self.new_url}')
                    self.driver.get(self.new_url)
                all_records_on_page = self.driver.find_elements(
                    By.XPATH, '//a[contains(@class, "detailsLink")]'
                    )
                href_to_records = [
                    item.get_attribute('href') for item in all_records_on_page
                ]
                self.first_page = False
                self.get_info_record(href_to_records)

    def get_info_record(self, hrefs):
        for item in hrefs:
            self.driver.get(item)
            info = self.driver.find_elements(
                By.XPATH, '//a[contains(@class, "link nowrap")]/span'
                )
            city = info[0].text.split(' ')[-1]
            try:
                record_categoty = f'{info[1].text.replace(city, "")} --> {info[2].text.replace(city, "")}'
            except:
                record_categoty = f'{info[1].text.replace(city, "")}'
            title = self.driver.find_element(
                By.XPATH, '//div[contains(@class, "offer-titlebox")]/h1'
                ).text
            price = self.driver.find_element(
                By.XPATH, '//div[contains(@class, "pricelabel")]'
                ).text
            description = self.driver.find_element(
                By.XPATH, '//div[contains(@id, "textContent")]'
                ).text
            bottombar_items = self.driver.find_elements(
                By.XPATH, '//div[contains(@id, "offerbottombar")]/ul/li//strong'
                )
            date_publish = bottombar_items[0].text.replace('в', '')
            views = bottombar_items[1].text
            number_record = bottombar_items[2].text
            name_user = self.driver.find_element(
                By.XPATH, '//div[contains(@class, "offer-user__actions")]/h4'
                ).text
            try:
                self.driver.find_element(
                    By.XPATH, '//div[contains(@id, "cookiesBar")]/button[contains(@class, "cookiesBarClose")]'
                ).click()
            except Exception as err:
                print('ERROR: {}'.format(err.args))
            try:
                self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, '//div[contains(@class, "contact-button")]'
                ))).click()
                phone = self.driver.find_element(
                    By.XPATH, '//strong[contains(@class, "xx-large")]'
                    ).text
            except Exception as err:
                phone=''
                print(f'Error getting phone: {err.args}')
            image_href = self.driver.find_element(
                By.XPATH, '//div[contains(@id, "descImage")]/img'
            ).get_attribute('src')
            print(
                f'{city}\n{record_categoty}\n{title}\n{price}\n{description}\n{date_publish}\n{views}\n{number_record}\n{name_user}\n{phone}\n{image_href}'
            )
t = ScrappOlx().get_info_category()