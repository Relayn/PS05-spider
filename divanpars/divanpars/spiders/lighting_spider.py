import scrapy

class LightingSpider(scrapy.Spider):
    name = "lighting_spider"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svetilniki"]

    def parse(self, response):
        product_urls = response.css('a[href^="/product/"]::attr(href)').getall()
        for url in product_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_product)

        next_page = response.css('.next-page a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = response.css('h1::text').get()
        price_element = response.css('span[itemprop="price"]')
        price = price_element.attrib['content'] if price_element else None
        url = response.url

        yield {
            'name': name,
            'price': price,
            'url': url
        }