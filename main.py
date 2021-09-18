# import pyyaml module
import yaml
from yaml.loader import SafeLoader

# open the file and load the file
with open('input.yaml') as file:
    data = yaml.load(file, Loader=SafeLoader)

# code to modify the file
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('template.html'), 'html.parser')

# modify the title
soup.find(id = "showcase").h1.string = data["title"]

# modify the summary
summary_content = soup.find(id = "summary-content").string = "Summary: " + data["summary"]

# modify the datasets
datasets_list = soup.find(id="datasets-list")

for link in data["datasets"]:
    li_new_tag = soup.new_tag('li')
    a_new_tag = soup.new_tag('a')
    a_new_tag['href'] = link
    a_new_tag.string = link
    li_new_tag.append(a_new_tag)
    li_new_tag.a.insert_after(": TODO Dataset description")
    datasets_list.append(li_new_tag)

# modify software
software_list = soup.find(id="software-list")

for link in data["software"]:
    li_new_tag = soup.new_tag('li')
    a_new_tag = soup.new_tag('a')
    a_new_tag['href'] = link
    a_new_tag.string = "TODO software name"
    li_new_tag.append(a_new_tag)
    li_new_tag.a.insert_after(": TODO Software description")
    software_list.append(li_new_tag)

#modify bibliography
bibliography_list = soup.find(id="bibliography-list")

for entry in data["bibliography"]:
    li_new_tag = soup.new_tag('li')
    li_new_tag.string = entry
    bibliography_list.append(li_new_tag)
    
# to save the changes
with open("index.html", "w") as file:
    file.write(str(soup))

