from bs4 import BeautifulSoup
import requests as req
import json

class bib(object):

    def __init__(self, doi_link):

        bib_json = req.get(doi_link, headers={"Accept":"application/citeproc+json"}).text
        bib_html = req.get(doi_link).text

        self.doi_link = doi_link
        self.html = BeautifulSoup(bib_html, 'html.parser')
        self.bib = json.loads(bib_json)

    def get_title(self):
        try:
            return self.bib["title"]
        except:
            print(f"Error: fetching title from {self.doi_link}.")
    
    def get_authors(self):
        try:
            authors = []
            for entry in self.bib["author"]:
                authors.append(entry["given"] + " " + entry["family"])
            return authors
        except:
            print(f"Error: fetching authors from {self.doi_link}.") 

    def get_summary(self):
        try:
            return self.html.find("meta", property="og:description").get("content", None)
        except:
            print(f"Error: Unable to retrieve the summary, check if {self.doi_link} is up.")
