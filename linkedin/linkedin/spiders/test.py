import scrapy


class DataSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.linkedin.com"]
    start_urls = [
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=United%20States&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=0"]

    def parse(self, response):
        jobs = response.css("li")
        for job in jobs:
            yield {
                'job_title': job.css('h3.base-search-card__title::text').get(default='0').strip(),
                'company': job.css('h4.base-search-card__subtitle a::text').get(default='0').strip(),
                'location': job.css('span.job-search-card__location::text').get(default='0').strip(),
                'info': job.css('div.job-search-card__benefits span.result-benefits__text::text').get(default='0').strip(),
                'date': job.css('.job-search-card__listdate::text').get(default='0').strip(),
            }

        # # Handle pagination
        # next_page = response.css('a.pagination__link[aria-label="Next"]').attrib['href']
        # if next_page:
        #     yield response.follow(next_page, self.parse)
