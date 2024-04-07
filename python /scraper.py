import scrapy
from datetime import datetime

class BrickSetScraper(scrapy.Spider):
    name = 'brickset_spider'
    start_urls = []
    CURRENT_YEAR = datetime.date(datetime.now()).year
    START_YEAR = CURRENT_YEAR - 1
    END_YEAR = CURRENT_YEAR

    for year in range(START_YEAR, END_YEAR+1):
        start_urls.append("https://brickset.com/sets/year-"+str(year))

    def parse(self, response):
        SET_SELECTOR = '.set'
        NAME_SELECTOR = 'h1 ::text'
        PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
        MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
        THEME_SELECTOR = '.tags a::text'
        SET_NUMBER_SELECTOR = '.tags a::text'
        YEAR_SELECTOR = '.tags a.year::text'

        output_file = 'brickset_data.txt'
        with open(output_file, 'a', encoding='utf-8') as f:
            for brickset in response.css(SET_SELECTOR):
                name = brickset.css(NAME_SELECTOR).extract_first()
                pieces = brickset.xpath(PIECES_SELECTOR).extract_first()
                minifigs = brickset.xpath(MINIFIGS_SELECTOR).extract_first()

                # Extract the theme, set number, and year
                theme = brickset.css(THEME_SELECTOR)[1].extract()
                set_number = brickset.css(SET_NUMBER_SELECTOR)[0].extract()
                year = brickset.css(YEAR_SELECTOR).extract_first()
                f.write(f"Name: {name}\n")
                f.write(f"Pieces: {pieces}\n")
                f.write(f"Minifigs: {minifigs}\n")
                f.write(f"Theme: {theme}\n")
                f.write(f"Set Number: {set_number}\n")
                f.write(f"Year: {year}\n")
                f.write("=" * 50 + "\n")

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )