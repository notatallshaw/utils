"""
Script to check validity of anchor tag links in an HTML file.
"""

from html.parser import HTMLParser
import argparse
import urllib.request as req

ARG_ERROR = 1  # type: int
PARSE_ERROR = 2  # type: int
IO_ERROR = 3   # type: int

class OurHTMLParser(HTMLParser):
    """
    Our descendant of base HTMLParser class: we override just the methods we
    need to.
    """
    def __init__(self):  # type: () -> None
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs):  # type: (str, object) -> None
        """
        This is a callback function that is used by HTMLParser for start tags:
            it is called!
        """
    def handle_data(self, data):  # type: (str) -> None
        """
        Here we can look for long lines or other such problems.
        """
        
def is_accessible(link):  # type: (str) -> bool
    """
    Function that accesses a url string and returns response status code.
    """
    if link.startswith('http') or link.startswith('https'):
        req.urlopen(link)
    elif link.startswith('/'):
        rel_link = "http://www.thedevopscourse.com" + link
        req.urlopen(rel_link)
    else:
        rel_link_two = "http://www.thedevopscourse.com/" + link
        req.urlopen(rel_link_two)
    return True  # this needs to return false if not accesible!


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url_inp_file",
                            help="text url input file to be parsed")
    args = arg_parser.parse_args()
    url_inp_file = args.url_inp_file

    url_list = []

    try:
        # get all the url links
        with open(url_inp_file, 'r') as urls:
            for url_link in urls:
                url_link = url_link.strip()
                url_list.append(url_link)
    except IOError:
        print("Couldn't read " + url_inp_file)
        exit(IO_ERROR)

    for url in url_list:
        try:
            is_accessible(url)
        except req.HTTPError as http_e:
            print(str(http_e.getcode()) + " for file "
                  + url_inp_file + " at url " + url)
        except req.URLError:
            print(req.URLError.reason + " for file "
                  + url_inp_file + " at url " + url)

    exit(0)
