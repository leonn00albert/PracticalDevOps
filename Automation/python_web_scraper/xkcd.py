""" Loads the XKCD home page.

Saves the comic image on that page.

Follows the Previous Comic link.

Repeats until it reaches the first comic.
This means your code will need to do the following:

Download pages with the requests module.

Find the URL of the comic image for a page using Beautiful Soup.

Download and save the comic image to the hard drive with iter_content().

Find the URL of the Previous Comic link, and repeat.

Open a new file editor window and save it as downloadXkcd.py.

"""


#! python3
# downloadXkcd.py - Downloads every single XKCD comic.

import requests, os, bs4

url = 'http://xkcd.com'              # starting url
os.makedirs('xkcd', exist_ok=True)   # store comics in ./xkcd
while not url.endswith('#'):
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    comicElem = soup.select('#comic img')

    if comicElem == []:
         
         print('Could not find comic image.')
    else:
        comicUrl = 'http:' + comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()
        imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print("done")