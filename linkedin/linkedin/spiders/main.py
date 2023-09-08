import scrapy


class DataSpider(scrapy.Spider):

    name            = "main"
    allowed_domains = ["www.linkedin.com"]
    api             = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=United%20States&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start="

    def start_requests(self):
        first_request = 0
        start_url     = self.api + str(first_request)

        yield scrapy.Request(

            url       = start_url,
            callback  = self.parse_data,
            meta      = {'first_request': first_request}
        )

    def parse_data(self, response):

        first_request = response.meta['first_request']
        jobs          = response.css("li")
        count_of_jobs = len(jobs)

        print("count of returned jobs "+ str(count_of_jobs) )
        for job in jobs:
            yield {
                'job_title': job.css('h3.base-search-card__title::text').get(default='0').strip(),
                'company'  : job.css('h4.base-search-card__subtitle a::text').get(default='0').strip(),
                'location' : job.css('span.job-search-card__location::text').get(default='0').strip(),
                'info'     : job.css('div.job-search-card__benefits span.result-benefits__text::text').get(default='0').strip(),
                'posted'   : job.css('.job-search-card__listdate::text').get(default='0').strip(),
                'datetime' : job.css('time.job-search-card__listdate::attr(datetime)').get(default='0').strip(),
                'job_link' : job.css('a[class^="base-card__full-link"]::attr(href)').get(default='0').strip(),
                'comp_link': job.css('h4.base-search-card__subtitle a::attr(href)').get(default='0').strip(),
            }

        if count_of_jobs > 0:

            first_request = int(first_request) + 25
            next_url      = self.api + str(first_request)

            yield scrapy.Request(

                url       = next_url,
                callback  = self.parse_data,
                meta      = {'first_request': first_request},
            )
