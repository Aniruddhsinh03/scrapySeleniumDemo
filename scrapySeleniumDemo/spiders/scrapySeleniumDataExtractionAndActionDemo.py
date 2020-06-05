# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class ScrapyseleniumdataextractionSpider(Spider):
    name = 'scrapySeleniumDataExtractionAndActionDemo'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('E:\SELENIUM DRIVER\chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds.')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book(self, response):

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')
        title = response.xpath('//*[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        instock_availability = self.driver.find_element_by_xpath('//*[@class="instock availability"]').text
        rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        table = response.xpath('//table')[0]
        trs = table.xpath('.//tr')
        upc = trs[0].xpath('.//td//text()').extract_first()
        product_type = trs[1].xpath('.//td//text()').extract_first()
        price__excl_tax = trs[2].xpath('.//td//text()').extract_first()
        price_incl_tax = trs[3].xpath('.//td//text()').extract_first()
        tax = trs[4].xpath('.//td//text()').extract_first()
        availability = trs[5].xpath('.//td//text()').extract_first()
        number_of_reviews = trs[6].xpath('.//td//text()').extract_first()
        yield {'Image URL': image_url,
               'Title': title,
               'Price': price, 'Stock Availability': instock_availability,
               'Rating': rating,
               'Description': description, 'Upc': upc,
               'Product Type': product_type,
               'Price Excl Tax': price__excl_tax, 'Price Incl Tax': price_incl_tax,
               'Tax': tax,
               'Availability': availability, 'Number Of Reviews': number_of_reviews}

