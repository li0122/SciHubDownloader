import requests
from bs4 import BeautifulSoup
import sys, getopt
from tqdm import tqdm
def download(url: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(url.split('/')[-1], 'wb') as file, tqdm(
        desc=url.split('/')[-1],
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

def main(arg):
    loc = str(arg)
    soup = BeautifulSoup(requests.post("https://sci-hub.se/", data = {'request':loc}).text,"html.parser")
    sel = soup.select("div embed")
    lore = BeautifulSoup((str(soup.find_all("div", {"id": "citation"})[0])), "html.parser")
    print(lore.text+'\n')
    for s in sel: 
        fileRoute = "https://sci-hub.se/"+str(s["src"]).split("#")[0]
        download(fileRoute)

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:",["serial="])
except getopt.GetoptError:
    print("scihub.py -s <paper ID>")
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print("scihub.py -s <paper ID>")
        sys.exit()
    elif opt == "-s":
        main(arg)
