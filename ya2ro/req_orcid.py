import requests as req
import json

class orcid(object):

    def __init__(self, orcid_link):
        self.json = json.loads(req.get(orcid_link, headers={"Accept":"application/ld+json"}).text)
        self.json_bio = json.loads(req.get(orcid_link, headers={"Accept":"application/orcid+json"}).text)
        self.orcid_link = orcid_link
    def get_full_name(self):
        try:
            return self.json["givenName"] + " " + self.json["familyName"]
        except:
            print(f"ERROR: Unable to retrieve the author´s full name, check if {self.orcid_link} is up.")
            return None

    def get_webs(self):
        """Get all webs separated in a list"""
        try:
            if self.json["url"] is None:
                return None
            else:
                if isinstance(self.json['url'], str):
                    return list([self.json['url']])
                else :
                    return list(self.json['url'])
        except:
            print(f"ERROR: Unable to retrieve the author´s web, check if {self.orcid_link} is up.")
            return None

    def get_affiliation(self):
        """Gets all the non repeated names afiliation in a list '"""
        try:
            affiliations = set()

            if self.json["affiliation"] is None:
                return None

            if isinstance(self.json["affiliation"], dict):
                affiliations.add(self.json["affiliation"]['name'])

            if isinstance(self.json["affiliation"], list):
                for aff in self.json["affiliation"]:
                    affiliations.add(aff['name'])
            
            return list(affiliations)

        except:
            print(f"ERROR: Unable to retrieve the affiliations, check if {self.orcid_link} is up.")
            return None
        
    def get_bio(self):
        try:
            return self.json_bio['person']['biography']['content']
        except:
            print(f"ERROR: Unable to retrieve the biography, check if {self.orcid_link} is up.")
            return None        