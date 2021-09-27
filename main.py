from Ro_jsonld import Ro_jsonld
from Ro_html import Ro_html

if __name__ == "__main__":

    ro_html = Ro_html()
    ro_html.createHTML_file()

    ro_jsonld = Ro_jsonld()
    ro_jsonld.createJSONLD_file()

