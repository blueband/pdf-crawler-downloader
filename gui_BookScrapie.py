import os
import sys
from urllib import parse


    
# We are creating Directory/Folder based on Enter Keywords
def create_project_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


# Create queue and crawled list file (if not create before)
def create_data_files(project_directory_name, google_search_base_url):
    queue = project_directory_name + '/google_search_queue.txt'
    crawled = project_directory_name + '/google_crawled.txt'
    queue_pdf_url = project_directory_name + '/queue_pdf.txt'
    crawled_pdf_url = project_directory_name + '/crawled_pdf_url.txt'
    if not os.path.isfile(queue):
        write_file(queue, google_search_base_url)

    if not os.path.isfile(crawled):
        write_file(crawled, '')

    if not os.path.isfile(queue_pdf_url):
        write_file(queue_pdf_url, '')
    if not os.path.isfile(crawled_pdf_url):
        write_file(crawled_pdf_url, '')


# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()



# Add data on to the existing files
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the content of file
def delete_file_content(path):
    with open(path, 'w'):
        pass


# Reading file and converts each line  to a set item
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n',''))
    return results

    

# iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_content(file)
    for link in sorted(links):
        append_to_file(file,link)
    



# This function take uncleaning Url and return all url with pdf at the end of it
def url_cleanup(page_url):
    new_url_begining = page_url.find('=')
    new_url_ending = page_url.find('.pdf',new_url_begining)
    full_url = (page_url[new_url_begining+1:new_url_ending+4])
    if ('.pdf') not in full_url:pass
    elif full_url.startswith('http://webcache'):pass
    elif full_url.startswith('related'):pass
      
    else:
        return full_url
        #add_url(full_url)
            
# Extract all google result page 
def search_queue_url(page_url):
    base_url = 'https://google.com'
    new_url_begining = page_url.find('=')
    new_url_ending = page_url.find('sa=',new_url_begining)

    # Creating Full Google URL to navigate to NEXT page
    search_queue_url_list = parse.urljoin(base_url, (page_url[new_url_begining-9:new_url_ending+5]))
    if ('start=') not in search_queue_url_list:pass
    elif search_queue_url_list == 'None': pass
    else:
        return search_queue_url_list