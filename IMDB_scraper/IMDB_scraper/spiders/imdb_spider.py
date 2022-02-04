# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/title/tt3783958/']

    def parse(self, response):
        url = response.css("div.SubNav__SubNavContainer-sc-11106ua-1.hDUKxp").\
            css("li.ipc-inline-list__item")[0].css("a").attrib["href"]
        url = response.urljoin(url)
        yield scrapy.Request(url, callback = self.parse_full_credits)


    def parse_full_credits(self,response):
        #list of actors url
        actor_urls = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        #call in each url the actor page method
        for url in actor_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback = self.parse_actor_page)


    def parse_actor_page(self, response):
        '''
        This method assumes that we start on the page of an actor.
        It should yield a dictionary with two key- value pairs.
        The whole method takes no more than 15 lines of code.
        '''
        actor_name = response.xpath('//h1[@class="header"]/span/text()').extract_first()

        #filmo = response.css("div.filmo-row")
        #text = filmo.xpath("//b/a/text()").extract()
        #ids =filmo.css("::attr(id)").extract()
        #ids = response.css("div.filmo-row").css("::attr(id)").extract()
        #movie_or_TV_name = []
        #for i in ids:
          #  if i[0:5] == "actor":
          #      movie_name.append(response.css('div.filmo-row[id=i] b a::text'))

        movie_name = response.css('div.filmo-row[id^="actor"] b a::text').extract()
        for name in movie_name:
            yield {
            "actor": actor_name,
            "movie_or_TV_name": name
            }
