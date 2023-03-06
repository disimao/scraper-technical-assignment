"""\
This script powers the Scrapy project that, 
given a list of website URLs as input, visits them
and finds, extracts and outputs the websites’ logo image URLs 
and all phone numbers present on the websites.
"""
import json
import sys
import re

import phonenumbers
import scrapy
import tldextract


class CdbspiderSpider(scrapy.Spider):
    """
    This spider will try to crawl whatever is passed in `start_urls` which
    should be a newline-separated list of website URLs.

    Example: start_urls=http://example1.com\nhttp://example2.com
    """

    name = "cdbspider"
    allowed_domains = ["www.placeholder1.com"]
    start_urls = ["https://www.placeholder1.com"]

    def __init__(self, name=None, **kwargs):
        if "start_urls" in kwargs:
            kwargs["start_urls"] = kwargs["start_urls"].replace("\n", "\\n")
            kwargs["start_urls"] = kwargs["start_urls"].split(r"\n")
        super().__init__(name, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse_website(self, response):
        redirected = response.request.meta.get("redirect_urls")
        if redirected and len(redirected):
            return redirected[0]
        return response.request.url

    def parse_logo(
        self, response, fqdn, domain_match, logo_pattern="header img"
    ):
        imgs = response.css(logo_pattern)
        url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        for img in imgs:
            link_parent = img.xpath(
                f"parent::a/@href[contains(.,'{domain_match}')]"
            )
            if len(link_parent):
                img_urls = [
                    value
                    for key, value in img.attrib.items()
                    if "src" in key.lower() and domain_match in value
                ]
                img_class = img.attrib.get("class", "").lower()
                if len(img_urls) or img_class.find("logo") != -1:
                    img_logos = [
                        img_url
                        for img_url in img_urls
                        if "logo" in img_url.lower()
                    ]
                    img_logo = img_logos[0] if len(img_logos) else img_urls[0]
                    url_match = re.findall(url_regex, img_logo)
                    img_logo = url_match[0] if len(url_match) else img_logo
                    if not img_logo.startswith("http"):
                        tld_ext = tldextract.extract(img_logo)
                        if not tld_ext.fqdn:
                            if not img_logo.startswith("/"):
                                img_logo = f"/{img_logo}"
                            img_logo = f"https://{fqdn}{img_logo}"
                        else:
                            fqdn_pos = img_logo.find(tld_ext.fqdn)
                            img_logo = f"https://{img_logo[fqdn_pos:]}"
                    return img_logo
        return ""

    def parse_phonenaumbers(self, response, country_code="US"):
        country_code = country_code.upper()
        if country_code not in phonenumbers.SUPPORTED_SHORT_REGIONS:
            country_code = "US"
        body = "".join(response.css("body").xpath("//body//text()").extract())
        phonenumbers_list = []
        for m in phonenumbers.PhoneNumberMatcher(body, country_code):
            phone_str = "".join(
                [
                    digit
                    if digit in [" ", "+", "(", ")"] or digit.isdigit()
                    else " "
                    for digit in m.raw_string
                ]
            )
            if phone_str not in phonenumbers_list:
                phonenumbers_list.append(phone_str)
        return phonenumbers_list

    def parse(self, response):
        output = {"logo": "", "phones": [], "website": ""}
        output["website"] = self.parse_website(response)
        tld_ext = tldextract.extract(output["website"])
        url_logo = self.parse_logo(response, tld_ext.fqdn, tld_ext.domain)
        if not url_logo:
            url_logo = self.parse_logo(
                response,
                tld_ext.fqdn,
                domain_match="",
                logo_pattern="body img",
            )
        output["logo"] = url_logo
        url_suffix = tld_ext.suffix.split(".")
        country_code = url_suffix[-1] if len(url_suffix) > 1 else "US"
        output["phones"] = self.parse_phonenaumbers(response, country_code)

        sys.stdout.write(json.dumps(output) + "\n")
