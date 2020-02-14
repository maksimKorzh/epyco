from scrapy.crawler import CrawlerProcess
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    results = []
    
    def parse(self, response):
        for quote in response.css("div.quote"):
            self.results.append({
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            })

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        
        import json
        print(json.dumps(self.results, indent=2))
            
            
# run spider
process = CrawlerProcess()
process.crawl(ToScrapeCSSSpider)
process.start()