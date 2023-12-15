from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["auto.ria.com"]
    start_urls = [
        f"https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=-1&page={page}&size=100"
        for page in range(11)
    ]
    rules = (
        Rule(LinkExtractor(allow=".*uk.*"), callback="parse_item"),
    )

    def parse_item(self, response):
        car_items = response.css('div[data-mark-name]')
        car_items = response.xpath(
            '//section[contains(@class, "ticket-item")]')

        for item in car_items:
            mark_name = item.attrib.get('data-mark-name', '')
            model_name = item.attrib.get('data-model-name', '')
            price = item.xpath(
                './/div[contains(@class, "price-ticket")]/@data-main-price').get()
            yield {
                "mark_name": mark_name,
                "model_name": model_name,
                "price": price,
            }
