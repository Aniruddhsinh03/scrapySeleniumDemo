# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from scrapy.loader import ItemLoader
from scrapySeleniumDemo.items import ScrapyseleniumdemoItem


class ScrapyseleniumdataextractionSpider(Spider):
    name = 'scrapySeleniumDataExtractionAndActionDemo'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        # initialise chromedriver for selenium
        self.driver = webdriver.Chrome('E:\SELENIUM DRIVER\chromedriver')
        # get webpage from get request
        self.driver.get('http://books.toscrape.com')
        # parse source in selector
        sel = Selector(text=self.driver.page_source)
        # fetching all books details urls
        books = sel.xpath('//h3/a/@href').extract()
        # extract all urls using for loop
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book_page)

        while True:
            # all next page url call logic in try-catch because if not found any url
            # (suppose last page have not next page url)
            # at that time handle NoSuchElementException and close driver
            try:
                # extracting next page url
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                # wait for element (taking time to load in browser)
                sleep(3)
                self.logger.info('Sleeping for 3 seconds.')
                # click for next page
                next_page.click()
                # parse next page for data
                sel = Selector(text=self.driver.page_source)
                # again extract same data for book list page
                books = sel.xpath('//h3/a/@href').extract()
                # extract books url from list page
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    # extract all urls one by one
                    yield Request(url, callback=self.parse_book_page)
            # handle if element not found
            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

    def parse_book_page(self, response):
        # extract all books data with details
        l = ItemLoader(item=ScrapyseleniumdemoItem(), response=response)
        image_urls = response.xpath('//img/@src').extract_first()
        image_urls = image_urls.replace('../..', 'http://books.toscrape.com/')
        title = response.xpath('//*[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        # extract data using selenium driver because this element data load by javascript
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
        l.add_value('image_urls', image_urls)
        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('instock_availability', instock_availability)
        l.add_value('rating', rating)
        l.add_value('description', description)
        l.add_value('upc', upc)
        l.add_value('product_type', product_type)
        l.add_value('price__excl_tax', price__excl_tax)
        l.add_value('price_incl_tax', price_incl_tax)
        l.add_value('tax', tax)
        l.add_value('availability', availability)
        l.add_value('number_of_reviews', number_of_reviews)
        return l.load_item()
