from bs4 import BeautifulSoup
import requests as req
import json

class bib(object):

    def __init__(self, doi_link):

        bib_json = req.get(doi_link, headers={"Accept":"application/citeproc+json"}).text
        bib_html = req.get(doi_link).text

        self.html = BeautifulSoup(bib_html, 'html.parser')
        self.bib = json.loads(bib_json)

    def get_title(self):
        return self.bib["title"]
    
    def get_authors(self):
        authors = []
        for entry in self.bib["author"]:
            authors.append(entry["given"] + " " + entry["family"])
        return authors

    def get_summary(self):
        return self.html.find("meta", property="og:description").get("content", None)

#doi = bib("https://doi.org/10.1109/WI.2018.00-93")
#print(doi.get_title())
#print(doi.get_authors())
#print(doi.get_summary())
