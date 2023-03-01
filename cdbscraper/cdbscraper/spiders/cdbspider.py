import json
import sys
import scrapy
import phonenumbers


class CdbspiderSpider(scrapy.Spider):
    """
    This spider will try to crawl whatever is passed in `start_urls` which
    should be a newline-separated list of website URLs.

    Example: start_urls=http://example1.com\nhttp://example2.com
    """

    name = "cdbspider"
    allowed_domains = ["www.cmsenergy.com"]
    start_urls = ["http://www.cmsenergy.com/"]

    def __init__(self, name=None, **kwargs):
        if "start_urls" in kwargs:
            self.start_urls = kwargs.pop("start_urls")
            self.start_urls = self.start_urls.replace("\n", "\\n")
            self.start_urls = f"{self.start_urls}".split(r"\n")

        super().__init__(name, **kwargs)

    def parse(self, response):
        output = {"logo": "", "phones": [], "website": ""}
        redirected = response.request.meta.get("redirect_urls")
        if redirected and len(redirected):
            output["website"] = redirected[0]
        else:
            output["website"] = response.request.url

        imgs = response.css("img")
        for img in imgs:
            img_url = img.attrib.get("src", "").lower()
            img_class = img.attrib.get("class", "").lower()
            if not img_url.startswith("http"):
                img_url = "https:" + img_url
            output["logo"] = (
                img_url
                if img_url.find("logo") != -1 or img_class.find("logo") != 1
                else ""
            )

        body = "".join(response.css("body").xpath("//body//text()").extract())
        for m in phonenumbers.PhoneNumberMatcher(body, "US"):
            f = phonenumbers.format_number(
                m.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            if f not in output["phones"]:
                output["phones"].append(f)

        sys.stdout.write(json.dumps(output) + "\n")
