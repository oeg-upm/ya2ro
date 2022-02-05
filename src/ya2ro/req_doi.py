from bs4 import BeautifulSoup
import requests as req
import json

class dataset(object):

    def __init__(self, doi_link):
        try:
            bib_json = req.get(doi_link, headers={"Accept":"application/ld+json"}).text
        except:
            bib_json = req.get("https://doi.org/"+doi_link, headers={"Accept":"application/ld+json"}).text
            
        self.doi_link = doi_link
        self.json = json.loads(bib_json)

    def get_name(self):
        try:
            return self.json["name"]
        except:
            return None    
    
    def get_author(self):
        try:
            return self.json["author"]["name"]
        except:
            return None

    def get_description(self):
        try:
            return self.json["description"]
        except:
            return None

    def get_license(self):
        try:
            if isinstance(self.json["license"], list):
                license = " and ".join([f"'{l}'" for l in self.json["license"]])
            else:
                license = self.json["license"]

            return license
        except:
            return None


class bib(object):

    def __init__(self, doi_link):

        bib_json = req.get(doi_link, headers={"Accept":"application/citeproc+json"}).text
        bib_html = req.get(doi_link).text
        
        self.citation = req.get(doi_link, headers={"Accept":"text/x-bibliography"}).text
        self.bibtext = req.get(doi_link, headers={"Accept":"application/x-bibtex"}).text
        self.doi_link = doi_link
        self.html = BeautifulSoup(bib_html, 'html.parser')
        self.json = json.loads(bib_json)

    def get_title(self):
        try:
            return self.json["title"]
        except:
            print(f"ERROR: fetching title from {self.doi_link}.")
            return None
    
    def get_authors(self):
        try:
            authors = []
            for entry in self.json["author"]:
                authors.append(entry["given"] + " " + entry["family"])
            return authors
        except:
            print(f"ERROR: fetching authors from {self.doi_link}.")
            return None

    def get_summary(self):
        try:
            return self.html.find("meta", property="og:description").get("content", None)
        except:
            print(f"ERROR: Unable to retrieve the summary, check if {self.doi_link} is up.")
            return None

    def get_citation(self):
        try:
            return self.citation
        except:
            print(f"ERROR: Unable to retrieve citation, check if {self.doi_link} is up.")
            return None
    
    def get_bibtext(self):
        try:
            return self.bibtext
        except:
            print(f"ERROR: Unable to retrieve bibtext, check if {self.doi_link} is up.")
            return None

