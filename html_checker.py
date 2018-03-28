"""
Script to check proper nesting and matching of html tags.
Right now, this only cheecks tags that stand alone on a line.
More checks will be added later.
"""

import sys
import urllib.request as req
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
import re
import argparse

ARG_ERROR = 1
PARSE_ERROR = 2
MAX_LINE = 80

tag_stack = []
line_no = 0
saw_error = False

void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link",
             "meta", "param"}


def line_msg():
    return " at line number " + str(line_no)

class OurHTMLParser(HTMLParser):
    def __init__(self):
        self.is_in_script_tag = False
        self.links = []
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.is_in_script_tag = True

        if tag == "a":
            attr = dict(attrs)
            self.links.append(attr['href'])

        if tag not in void_tags:
            tag_stack.append(tag)

    def handle_endtag(self, close_tag):
        global saw_error
        if len(tag_stack) == 0:
            print("ERROR: unmatched close tag "
                  + close_tag + "'" + line_msg())
            saw_error = True
        elif close_tag not in void_tags:
            open_tag = tag_stack.pop()
            if close_tag != open_tag:
                print("ERROR: " +
                      "Close tag '" + close_tag +
                      "' does not match open tag '"
                      + open_tag + "'" + line_msg())
                saw_error = True
        if close_tag is "script":
            self.is_in_script_tag = True

    def handle_data(self, data):
        """
        Here we can look for long lines or other such problems.
        """
        global saw_error
        # print(data)
        if len(data) > MAX_LINE:
            print("WARNING: long line found" + line_msg())
        if re.search('\x09', data):
            print("WARNING: tab character found" + line_msg()
                  + "; please uses spaces instead of tabs.")
        if re.search('[<>]', data) and not self.is_in_script_tag:
            print("ERROR: Use &gt; or &lt; instead of < or >"
                  + line_msg())
            saw_error = True

    def is_accessible(self, link):
        '''
        Here we check if the web page is accessible.
        '''
        mock_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for i in range(3):
            try:
                request = req.Request(link, headers = mock_header)
                response = req.urlopen(request)
                return True
            except:
                pass
        return False

    def check_urls_accessibility(self, links):
        print("Checking accessibility of urls...")
        for link in parser.links:
            if not self.is_accessible(link):
                link = urljoin("https://gcallah.github.io/DevOps/", link)
                if not self.is_accessible(link):
                    print("WARNING: url not accessible" + line_msg()
                    + "; " + link)
                    saw_error = True

if __name__ == '__main__':
    # if you want url checking invoke program with --u flag
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_filename")
    arg_parser.add_argument("--u", action = "store_true")
    args = arg_parser.parse_args()
    url_check = args.u

    parser = OurHTMLParser()
    file_nm = args.html_filename

    file = open(file_nm, "r")
    for line in file:
        line_no += 1
        parser.feed(line)

    if url_check:
        parser.check_urls_accessibility(parser.links)

    if saw_error:
        exit(PARSE_ERROR)
    else:
        exit(0)
