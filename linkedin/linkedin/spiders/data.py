import scrapy


class DataSpider(scrapy.Spider):
    name = "data"
    allowed_domains = ["www.linkedin.com"]
    start_urls = [
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=United%20States&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=100"]

    def parse(self, response):
        yield {
            'job_title': response.css('h3.base-search-card__title::text').get().strip(),
            'company': response.css('h4.base-search-card__subtitle a::text').get().strip(),
            'location': response.css('span.job-search-card__location::text').get().strip(),
            'info': response.css('div.job-search-card__benefits span.result-benefits__text::text').get().strip(),
            'date': response.css('.job-search-card__listdate::text').get().strip(),

        }
