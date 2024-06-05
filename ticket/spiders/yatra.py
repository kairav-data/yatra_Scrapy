import re
import scrapy

class YatraSpider(scrapy.Spider):
    name = "yatra"

    def __init__(self, origin=None, travel_date=None, destination=None, *args, **kwargs):
        super(YatraSpider, self).__init__(*args, **kwargs)
        self.origin = origin
        self.travel_date = travel_date
        self.destination = destination

        match = re.search(r"(\d{2})/(\d{2})/(\d{4})", self.travel_date)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            date = f"{day}%2F{month}%2F{year}"
        else:
            date = self.travel_date  # Fallback if the date format is not matched

        self.start_urls = [self.construct_url(date, destination, origin)]

    def construct_url(self, travel_date, destination, origin):
        base_url = 'https://www.yatra.com/'
        return (f"{base_url}air-search-ui/dom2/trigger?"
                f"ADT=1&CHD=0&INF=0&class=Economy&destination={destination}"
                f"&destinationCountry=IN&flexi=0&flight_depart_date={travel_date}"
                f"&hb=&noOfSegments=1&origin={origin}&originCountry=IN")

    def parse(self, response):
        # Implement parsing logic here
        tickets=response.xpath("//div[@class='flightItem border-shadow pr']")


