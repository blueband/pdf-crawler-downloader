import bs4
from gui_BookScrapie import search_queue_url, url_cleanup


class LinkFinder(bs4.BeautifulSoup):
    def __init__(self, m, google_search_base_url, page_url):
         self.google_search_base_url = google_search_base_url
         self.page_url = page_url
         self.pdf_url_links = set()
         self.google_url_links = set()
         super().__init__(m, 'html.parser')
       
        

    def handle_starttag(self, name, namespace, nsprefix, attrs):
        if name == 'a':
            for (attributes, value) in attrs.items():
                if ('&start=') not in value:pass
                else:
                    list_of_links = search_queue_url(value)
                    self.google_url_links.add(list_of_links)
                    
                                    
                if ('.pdf&') not in value: pass
                else:
                    list_pdf_url = url_cleanup(value)
                    self.pdf_url_links.add(list_pdf_url)  # test point 2

    def page_links(self):
        return self.google_url_links, self.pdf_url_links

    def error(self, message):
        pass