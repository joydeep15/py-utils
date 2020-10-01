import re
import requests
from bs4 import BeautifulSoup

def main():

    lastid = 21640

    while lastid > 0 :
        site = 'http://handmadeexpo.com/client/loadmore21.php?lastid='+str(lastid)
        response = requests.get(site)

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        urls = [img['src'] for img in img_tags]

        urls = set(urls)
        urls = sorted(urls)
        lastid = int(re.search(r'/([\w_-]+[.](jpg|gif|png))$', urls[0]).group(1).split('.')[0])

        for url in urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            # image = requests.get(url).content

            if not filename:
                 print("Regex didn't match with the url: {}".format(url))
                 continue
            with open('images\\' + filename.group(1), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative
                    # if it is provide the base url which also happens
                    # to be the site variable atm.
                    url = '{}{}'.format(site, url)
                response = requests.get(url)
                print('processed: ' +str(filename.group(1)))
                f.write(response.content)

if __name__ == '__main__':
    main()