import requests as req
import json

class orcid_req(object):

    def __init__(self, orcid_link):
        self.json = json.loads(req.get(orcid_link, headers={"Accept":"application/ld+json"}).text)

    def get_full_name(self)-> str:
        return self.json["givenName"]+" "+self.json["familyName"]
    
    def get_webs(self):
        """Get all webs separated in a list'"""
        if self.json["url"] is None:
            return None
        else:
            return list(self.json["url"])
    

    def get_affiliation(self):
        """Gets all the non repeated names afiliation in a list '"""
        affiliations = set()

        if self.json["affiliation"] is None:
            return None

        for aff in self.json["affiliation"]:
            affiliations.add(aff["name"])
        
        return list(affiliations)
