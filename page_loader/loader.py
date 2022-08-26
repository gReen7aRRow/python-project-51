import os
import re
import requests

FORMATS = ('.3dm', '.asp', '.aspx', '.cer', '.cmf',
           '.chm', '.crdownload', '.csr', '.css',
           '.dll', '.download', '.eml', '.flv',
           '.htaccess', '.htm', '.html', '.jnlp',
           '.js', '.jsp', '.magnet', '.mht', '.mhtm',
           '.mhtml', '.msg', '.mso', '.php', '.prf',
           '.rss', '.srt', '.stl', '.swf', '.torrent',
           '.url', '.vcf', '.webarchive', '.webloc',
           '.xhtml', '.xul')


def get_full_path(url, path):
    url = url.replace('.html', '')
    for i, v in enumerate(url):
        if v == '/':
            url = url[i+2:]
            break
    full_domen = re.sub(r'\W', '-', url)
    full_path = os.path.join(path, full_domen) + '.html'
    return full_path


def download(url, path=os.getcwd()):
    full_path = get_full_path(url, path)
    page = requests.get(url)
    html = page.text
    f = open(full_path, 'w')
    f.write(html)
    f.close()
    return full_path
