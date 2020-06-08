# scrapySeleniumDemo

This is a Scrapy project to scrape online book store from http://books.toscrape.com/.

This project is only meant for educational purposes.


## Extracted data

This project extracts availability,description,image_urls,images(download with rename),url,instock_availability,number_of_reviews,price,price__excl_tax,price_incl_tax,product_type,rating,tax,title,upc.
The extracted data looks like this sample:

     {'availability': ['In stock (1 available)'],
      'description': ['England, 1921. Three years after her husband, Alex, '
                 'disappeared, shot down over Germany, Jo Manders still mourns '
                 "his loss. Working as a paid companion to Alex's wealthy, "
                 'condescending aunt, Dottie Forsyth, Jo travels to the '
                 'family’s estate in the Sussex countryside. But there is much '
                 'she never knew about her husband’s origins…and the '
                 'revelation of a mysterious death in the England, 1921. Three '
                 'years after her husband, Alex, disappeared, shot down over '
                 'Germany, Jo Manders still mourns his loss. Working as a paid '
                 "companion to Alex's wealthy, condescending aunt, Dottie "
                 'Forsyth, Jo travels to the family’s estate in the Sussex '
                 'countryside. But there is much she never knew about her '
                 'husband’s origins…and the revelation of a mysterious death '
                 'in the Forsyths’ past is just the beginning…All is not well '
                 "at Wych Elm House. Dottie's husband is distant, and her son "
                 'was grievously injured in the war. Footsteps follow Jo down '
                 'empty halls, and items in her bedroom are eerily rearranged. '
                 'The locals say the family is cursed, and that a ghost in the '
                 'woods has never rested. And when Jo discovers her husband’s '
                 'darkest secrets, she wonders if she ever really knew him. '
                 'Isolated in a place of deception and grief, she must find '
                 'the truth or lose herself forever.And then a familiar '
                 'stranger arrives at Wych Elm House… ...more'],
                 'image_urls': ['http://books.toscrape.com//media/cache/5f/03/5f0345cd81aaad65bb9f6a34ec0f6b9b.jpg'],
                 'images': [{'checksum': '8e0647d2399c6153ab1b6422562f9795',
                 'path': 'full/593c0d0742349f5958da52629084d5b537a731d9.jpg',
                 'url': 'http://books.toscrape.com//media/cache/5f/03/5f0345cd81aaad65bb9f6a34ec0f6b9b.jpg'}],
                 'instock_availability': ['In stock'],
                 'number_of_reviews': ['0'],
                 'price': ['£27.70'],
                 'price__excl_tax': ['£27.70'],
                 'price_incl_tax': ['£27.70'],
                 'product_type': ['Books'],
                 'rating': [' Four'],
                 'tax': ['£0.00'],
                 'title': ['Lost Among the Living'],
                 'upc': ['d510567580c8be52']}

## Configuration

in settings.py set pipeline for download image and store location.
command:
        
        TEM_PIPELINES = {
        'scrapy.pipelines.images.ImagesPipeline': 1,
        'scrapySeleniumDemo.pipelines.ScrapyseleniumdemoPipeline': 2
                         }
        IMAGES_STORE = 'E:\IMAGE STORE'
        
        
 pipeline for rename images with title
            
            def process_item(self, item, spider):
            os.chdir('E:\IMAGE STORE')
            if item['images'][0]['path']:
            new_image_name = item['title'][0] + '.jpg'
            new_image_path = 'full/' + new_image_name
              os.rename(item['images'][0]['path'], new_image_path)

## Spiders

This project contains one spider and you can list them using the `list`
command:

    $ scrapy list
    scrapySeleniumDataExtractionAndActionDemo

Spider extract the data from book store.




## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl scrapySeleniumDataExtractionAndActionDemo


