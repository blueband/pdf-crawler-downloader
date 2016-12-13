import requests
import threading
from queue import Queue
from gui_link_finder import *
from gui_BookScrapie import *



class Spider(object):
    # define Class Variable that is shared by all Spiderbot
    project_directory_name = ''
    search_terms = ''
    google_search_base_url = ''
    queue_file = ''
    crawled_file = ''
    queue_pdf_url_file = ''
    crawled_pdf_url_file = ''
    queue = set()
    crawled = set()
    queue_pdf_url = set()
    crawled_pdf_url = set()
    NUMBER_OF_THREADS = 4

    thread_queue = Queue()
    headers = {
        'user_agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-Us; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

    def __init__(self,keyword):  # The user supply the keyword that needs to be search for
        Spider.search_terms = Spider.search_keyword(keyword)
        Spider.project_directory_name = Spider.search_terms
        Spider.crawled_file = Spider.project_directory_name + '/google_crawled.txt'
        Spider.crawled_pdf_url_file = Spider.project_directory_name + '/crawled_pdf_url.txt'
        Spider.queue_file = Spider.project_directory_name + '/google_search_queue.txt'
        Spider.queue_pdf_url_file = Spider.project_directory_name + '/queue_pdf.txt'

        self.boot()
        self.crawled_page('First Spider Crawling', Spider.google_search_base_url)
        Spider.main()       # calling The Thread Bot

    # each Book keyword we search for, the app create a folder for each projects()
    def search_keyword(keyword):
        # keyword = input('Please enter name of book or topic you are searching for :').lower()
        keyword = keyword.strip().lower()
        return keyword

    @staticmethod
    def boot():
        Spider.project_directory_name = (create_project_dir(Spider.search_terms))
        Spider.search_terms = Spider.search_terms + ' ' + 'pdf'
        Spider.google_search_base_url = 'http://www.google.com/search?q=%s' % Spider.search_terms
        create_data_files(Spider.project_directory_name, Spider.google_search_base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.queue_pdf_url = file_to_set(Spider.queue_pdf_url_file)
        Spider.crawled_pdf_url = file_to_set(Spider.crawled_pdf_url_file)

    @staticmethod
    def crawled_page(Thread_name, page_url):
        if page_url not in (Spider.crawled and Spider.crawled_pdf_url):
            print(Thread_name + ' now crawlling ' + page_url)
            print('Queue' + str(len(Spider.queue)) + '  | crawled' + str(len(Spider.crawled)))
            # gather_links method  return two variable
            google_url_links, pdf_url_links = Spider.gather_links(page_url)
            Spider.add_links_to_queue(google_url_links, pdf_url_links)
            Spider.crawled.add(page_url)
            Spider.queue.remove(page_url)

            Spider.update_google_files()
            Spider.PdfDownloader()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        response = requests.get(page_url, headers=Spider.headers)

        html_string = str(response.content, 'cp437')
        finder = LinkFinder(html_string, Spider.google_search_base_url, page_url)
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(google_url_links, pdf_url_links):

        for link in google_url_links:
            if link in Spider.queue:
                continue
            if link in Spider.crawled:
                continue
            else:
                Spider.queue.add(link)
        for link2 in pdf_url_links:
            if link2 in Spider.queue_pdf_url:
                continue
            if link2 in Spider.crawled_pdf_url:
                continue
            else:
                Spider.queue_pdf_url.add(link2)

    @staticmethod
    def update_google_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def update_pdf_files():
        set_to_file(Spider.queue_pdf_url, Spider.queue_pdf_url_file)
        set_to_file(Spider.crawled_pdf_url, Spider.crawled_pdf_url_file)

    # A pdf URL is accept from a set, bot then go ahead to download the file to specific sub-directory
    @staticmethod
    def PdfDownloader():
        list_links = file_to_set(Spider.queue_pdf_url_file)
        LINK_COUNTER = 1
        pdf_dir = Spider.project_directory_name + '/' + create_project_dir('pdfdownload')
        for link in list_links:
            print('These are the link to download', link, 'debug point')
            if LINK_COUNTER <= 3:
                print('I am now downloading the file at ', link)
                pdf_file_name = Spider.file_name(link)

                response = requests.get(link, stream=True)
                pdf_file = open(pdf_file_name, 'wb')
                for chunk in response.iter_content(chunk_size=1000000):
                    if chunk:  # Keep Alive until file is download
                        pdf_file.write(chunk)

                Spider.crawled_pdf_url.add(link)
                Spider.queue_pdf_url.remove(link)
                print('I had download this number of file', LINK_COUNTER)
                LINK_COUNTER += 1

        # print(link, 'This is print debug inside PdfDownloader()')
        Spider.update_pdf_files()

    def file_name(link):
        file_name = link.split('.')
        filename = file_name[-2]
        if '/' not in filename:
            pass
        else:
            real_file_name = filename.split('/')
            real_file_name = real_file_name[-1]
        full_file_name = real_file_name + '.' + file_name[-1]

        return full_file_name

    # gui_main file was copy to this location



    # Spider(keyword)

    # Create workers thread (will die when main exit)
    @staticmethod
    def create_workers():
        for _ in range(Spider.NUMBER_OF_THREADS):
            t = threading.Thread(target=Spider.work)
            t.demon = True
            t.start()

    # do the next job in the queue
    @staticmethod
    def work():
        while True:
            url = Spider.thread_queue.get()
            Spider.crawled_page(threading.current_thread().name, url)
            Spider.thread_queue.task_done()

    # Each queue link is a new job
    @staticmethod
    def create_jobs():
        for link in file_to_set(Spider.queue_file):
            Spider.thread_queue.put(link)
        Spider.thread_queue.join()
        Spider.crawl()

    # Checking if items is queue, then crawl the availabe links
    @staticmethod
    def crawl():
        queued_links = file_to_set(Spider.queue_file)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + 'links in the queue')
            Spider.create_jobs()

    @staticmethod
    def main():
        Spider.create_workers()
        Spider.crawl()


