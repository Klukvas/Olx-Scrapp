from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from models import DataBaseClient, ModelRecord

from settings import path_to_driver, start_url
from Logging import Logger
from  re import search
from selenium.common import exceptions

class ScrappOlx:
    def __init__(self):
        self.log = Logger().custom_logger()
        self.db_client = DataBaseClient()
        opts = Options()
        opts.log.level = "fatal"
        self.driver = webdriver.Firefox(executable_path=path_to_driver, options=opts)
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
            self.log.info(f'Getting info from category {item}')
            self.max_page = self.driver.find_elements(
                By.XPATH, '//span[contains(@class, "item fleft")][last()]'
                )[0].text
            for number in range(1, int(self.max_page)+1):
                if not self.first_page:
                    self.new_url = item+f'?page={number}'
                    self.driver.get(self.new_url)
                all_records_on_page = self.driver.find_elements(
                    By.XPATH, '//tr[contains(@class, "wrap")]//a[contains(@class, "linkWithHash detailsLink")]'
                    )
                href_to_records = [
                    item.get_attribute('href') for item in all_records_on_page
                ]
                self.first_page = False
                href_to_records = list(set(href_to_records))
                self.get_info_record(href_to_records)

    def get_phone_number(self):
        try:
            self.driver.find_element(
                By.XPATH, '//div[contains(@id, "cookiesBar")]/button[contains(@class, "cookiesBarClose")]'
            ).click()
        except Exception as err:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//div[contains(@class, "contact-button link-phone")]/strong[contains(@class, "xx-large")]'
            ))).click()
            phone = self.driver.find_element(
                By.XPATH, '//div[contains(@class, "contact-button link-phone")]/strong[contains(@class, "xx-large")]'
                ).text
            test = search(r'\d+', phone)
        except (exceptions.TimeoutException, exceptions.NoSuchElementException) as no_element:
            test = 1
            self.log.warning(f'No phone on record: {self.driver.current_url}')
            phone = ' '
        except exceptions.StaleElementReferenceException as err:
            self.driver.refresh()
            try:
                self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, '//div[contains(@class, "contact-button link-phone")]/strong[contains(@class, "xx-large")]'
                ))).click()
                phone = self.driver.find_element(
                    By.XPATH, '//div[contains(@class, "contact-button link-phone")]/strong[contains(@class, "xx-large")]'
                    ).text
                test = search(r'\d+', phone)
            except (exceptions.TimeoutException, exceptions.NoSuchElementException) as no_element:
                test = 1
                self.log.warning(f'No phone on record: {self.driver.current_url}')
                phone = ' '
        while not test:
            if phone == 'Показать телефон':
                self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, '//div[contains(@class, "contact-button link-phone")]/strong[contains(@class, "xx-large")]'
                ))).click()
            phone = self.driver.find_element(
                By.XPATH, '//strong[contains(@class, "xx-large")]'
            ).text
            test = search(r'\d+', phone)
        return phone

    def get_info_record(self, hrefs):
        for item in hrefs:
            self.log.info(f'Start parse record\n{item}')
            self.driver.get(item)
            self.wait.until(EC.element_to_be_clickable((
                By.XPATH, '//span[contains(@class, "link inlblk")]'
            )))
            try:
                no_active = driver.find_element(
                    By.XPATH, '//h3/strong'
                ).text
                is_record_active = False
            except:
                is_record_active = True
            if is_record_active:
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
                phone = self.get_phone_number()
                try:
                    image_href = self.driver.find_element(
                        By.XPATH, '//div[contains(@id, "descImage")]/img'
                    ).get_attribute('src')
                except Exception as err:
                    self.log.warning(f'Can not get image href: {err.args}')
                record_url = self.driver.current_url
                try:
                    record = ModelRecord(
                        number_record = number_record,
                        record_categoty = record_categoty,
                        title = title,
                        price = price,
                        description = description,
                        date_publish = date_publish,
                        views = views,
                        name_user = name_user,
                        phone = phone,
                        image_href = image_href,
                        record_url = record_url
                    ) 
                    self.db_client.session.merge(record)
                    self.db_client.session.commit()
                    self.log.info(f'Record {number_record} added to DB')
                except Exception as err:
                    self.log.error('Record {number_record} nont added to DB {err.args}')
    def __del__(self):
        self.driver.clsoe()
        self.log.info('Scrapping end')
t = ScrappOlx().get_info_category()