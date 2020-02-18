import scrapy
from scrapy.crawler import CrawlerProcess
import json

# paste this code before spider class definition to enable logging
import logging
logging.basicConfig(filename='background.log',level=logging.DEBUG)

class Views(scrapy.Spider):
    name = 'views'
    start_urls = ['https://free-proxy-list.net']
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'CONSENT=YES+UA.en+; VISITOR_INFO1_LIVE=7woZWjMqhVc; _ga=GA1.2.309153073.1579374852; endscreen-gh=true; LOGIN_INFO=AFmmF2swRAIgFIayDoYF3kfp-7bTpN-P6yJhJi5t3Ze1R5LSxZZobPgCIDL02ytlRy0-sYgFNNys8riGkzj0yZy6H3vM0AJL78m6:QUQ3MjNmelZGZjFPSDQ1X0oyd1d2MWRBR2YtVnE2Y0NyTHJ4WGlxTUZEQTVDV3hSQkFOU1BsaHZ5U2pSbW91dy10bXNJbFFMYTEwMGozNGhwSFlkalk2UllmUlA3RzBWZU1hNlFOVEI3R2hCcUNtZEg1SUluLVl5aFdydGY2WjVZcTNmWWpYSnQ2VnFRakNWTzZxanJISnd1Z1NXRUdMNWNVMXMxR1dDSzk3c0tfRVl5NmxEWGNENnd2blFoM0dwbG9JNUNwaTBfTXN5; SID=tQd3UMX__-JBh21ggvPrm0ieZEIsHFK2JKa9ZpZkxtu34SMWdUJpiPRvIzHkFkNY2UYvSg.; __Secure-3PSID=tQd3UMX__-JBh21ggvPrm0ieZEIsHFK2JKa9ZpZkxtu34SMWBwgcJXiZNemGkh6QqMdtXw.; HSID=AuTpyVP56bcmNUc98; SSID=AhEjxf-UdRF8iDxyG; APISID=Ldjz1ogvjgtip72f/AxXApI-7pppAvz-A1; SAPISID=a-Mi48PHKTvsLcTU/A0E7y0fhZox6pSbKQ; __Secure-HSID=AuTpyVP56bcmNUc98; __Secure-SSID=AhEjxf-UdRF8iDxyG; __Secure-APISID=Ldjz1ogvjgtip72f/AxXApI-7pppAvz-A1; __Secure-3PAPISID=a-Mi48PHKTvsLcTU/A0E7y0fhZox6pSbKQ; PREF=al=ru&f5=30&hl=en; _gid=GA1.2.274668459.1581758680; YSC=_ieg6bWQ2nY; SIDCC=AN0-TYt6S9EpxlP7-RWM2TgfMPte97mp0wubDjp80YgitYbYNyDVlRTluLbK3ierJ91mJCb8adLm',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    def parse(self, response):
        table = response.css('table')
        rows = table.css('tr')
        cols = [row.css('td::text').getall() for row in rows]
        
        proxies = []
        
        for col in cols:
            if col and col[4] == 'elite proxy' and col[6] == 'yes':
                proxies.append('https://' + col[0] + ':' + col[1])
            
        self.log(proxies)
        
        for proxy in proxies:
            test_url = 'https://scrapingkungfu.herokuapp.com/api/request'
            
            # use your video url here
            video_url = 'https://www.youtube.com/watch?v=PZYHR64117Q'
            
            yield scrapy.Request(video_url, dont_filter=True, headers=self.headers, meta={'proxy': proxy}, callback=self.check_response)
         
    def check_response(self, response):
        self.log('response status is ' + str(response.status))
            
    

# run spider
process = CrawlerProcess()
process.crawl(Views)
process.start()