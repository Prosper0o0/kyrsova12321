from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):

    name = "mycrawler2"

    allowed_domains = ["auto.ria.com"]

    start_urls = [

        "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&year[0].gte=2000&year[0].lte=2018&categories.main.id=1&country.import.usa.not=-1&price.USD.gte=2000&price.USD.lte=40000&price.currency=1&abroad.not=0&custom.not=-1&page=0&size=100"
    
    ]

    rules = (

        Rule(LinkExtractor(allow=".*indexName=auto.*"), callback="parse_item"),
        
    )

    def parse_item(self, response):
        # Отримання марок автомобілів
        mark_names = response.css(
            "*[data-mark-name]::attr(data-mark-name)").getall()
        # Отримання цін
        prices = response.css(
            "*[data-main-price]::attr(data-main-price)").getall()
        # Отримання моделей автомобілів
        model_names = response.css(
            "*[data-model-name]::attr(data-model-name)").getall()
        # Отримання покоління автомобілів
        generation_names = response.css(
            "*[data-generation-name]::attr(data-generation-name)").getall()
        # Отримання назви обладнання
        equipment_names = response.css(
            "*[data-equipment-name]::attr(data-equipment-name)").getall()
        # Отримання року випуску
        years = response.css("*[data-year]::attr(data-year)").getall()

        combined_data = []
        for mark_name, model_name, generation_name, equipment_name, year, price in zip(mark_names, model_names, generation_names, equipment_names, years, prices):
            combined_data.append({
                "mark_name": mark_name,
                "model_name": model_name,
                "generation_name": generation_name,
                "equipment_name": equipment_name,
                "year": year,
                "price": price
            })

        # Обробка або збереження combined_data
        for item in combined_data:
            yield item
