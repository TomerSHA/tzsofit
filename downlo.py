
import urllib2
from bs4 import BeautifulSoup
import logging
import errno
import os

logging.basicConfig(filename='downloads.log',level=logging.DEBUG)
logging.info("NEW RUN@@@@@")

def downloadpage(url,path,sublink):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page).body
    downloadlink = soup.find("div", {"class":"download"})
    shortTitle = soup.find("div", {"id":"content"}).h1.get_text()
    link = downloadlink.a.get("href")
    fileName = path + '\\' + str(sublink) + '_' + shortTitle + '.mp3'
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        file_handler = os.open(fileName,flags)
    except OSError as e:
        if e.errno == errno.EEXIST:
            raise
    print 'download start ' + str(sublink)
    if len(link) <= len('http://www.tzsofit.co.il/system/skits/'):
        return False
    f = urllib2.urlopen(link)
    data = f.read()
    with os.fdopen(file_handler, "wb") as code:
        code.write(data)
    code.close()
    print 'file finished'
    return True



def main():

    category_count=0
    directory = 'tzsofit'
    page = urllib2.urlopen('http://www.tzsofit.co.il/skits')
    soup = BeautifulSoup(page).body
    linklist = soup.find_all("div",{"class":"accordion-group"})

    for link in linklist:
        if not os.path.exists(directory + str(category_count)):
            os.makedirs(directory + str(category_count))
        print 'Section ' + str(category_count) + ':'
        category_links = link.find_all("a")
        category_links.pop(0)
        sublinks = 0
        for short in  category_links:
            success = False
            shortLink = 'http://www.tzsofit.co.il' + short.get("href")
            try:
                success = downloadpage(shortLink,directory + str(category_count), sublinks)
            except IOError:
                logging.warning(str(category_count) + ' - ' + str(sublinks) + ' failed: ' + shortLink)
            except OSError:
                logging.info(str(category_count) + ' - ' + str(sublinks) + ' already exists')
            except Exception  as e:
                logging.info(str(category_count) + ' - ' + str(sublinks) + ' not expected')
                logging.warning(e)
            if not success:
                logging.info(str(category_count) + ' - ' + str(sublinks) + ' failed: ' + shortLink)
            else:
                logging.info(str(category_count) + ' - ' + str(sublinks) + ' success')
            sublinks+=1
        category_count+=1


if __name__ == '__main__':
    main()
