import scrapy
import json

from scrapy.exceptions import CloseSpider


class ClimbersSpider(scrapy.Spider):
    count = 0
    name = 'climbers'
    allowed_domains = ['haexpeditions.com']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
    url = 'https://haexpeditions.com/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=1084&target_action=get-all-data&default_sorting=old_first&ninja_table_public_nonce=15f426c6cd&chunk_number=0'

    def start_requests(self):
        yield scrapy.Request(url = self.url, headers={"User-Agent": self.user_agent})

    def parse(self, response):
        resp = json.loads(response.body)

        for climbers in resp:
            try:

                yield {
                    "Number": climbers['value']['number'],
                    "Name": climbers['value']['name'],
                    "Nationality": climbers['value']['nationality'],
                    "Gender": climbers['value']['gender'],
                    "Age": climbers['value']['age'],
                    "Date": climbers['value']['date'],
                    "Route": climbers['value']['route'],
                    "Occupation": climbers['value']['occupation']
                }
            except Exception as e:
                print("number-3889 entry does not exist")
    
        self.count += 1
    
        if self.count == 1:
            yield scrapy.Request(url = 'https://haexpeditions.com/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=1084&target_action=get-all-data&default_sorting=old_first&skip_rows=0&limit_rows=0&chunk_number=1&ninja_table_public_nonce=dd4296071d',callback=self.parse, headers={"User-Agent": self.user_agent})

        if self.count == 2:
            yield scrapy.Request(url = 'https://haexpeditions.com/wp-admin/admin-ajax.php?action=wp_ajax_ninja_tables_public_action&table_id=1084&target_action=get-all-data&default_sorting=old_first&skip_rows=0&limit_rows=0&chunk_number=2&ninja_table_public_nonce=dd4296071d',callback=self.parse, headers={"User-Agent": self.user_agent})
