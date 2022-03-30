# Documentation - ya2ro

## Fields supported

### Paper

Documentation for all supported fields for type paper.

`type:`This field is required and is used to indicate the type of the work.

```yaml
type: "paper"
```

`doi_paper:`All the relevant information of the paper will be retrieved. Such as:

* Title
* Summary
* Bibtext
* Citation/Bibliography
* Authors

```yaml
doi_paper: https://doi.org/xxxxxxxxx
```

`title:`Title of the paper.

```yaml
title: "Paper - Template"
```

`summary:`A brief summary of the paper, also known as an abstract.

```yaml
summary: "This is a summary of the paper."
```

`datasets:` All the datasets used and created during the paper. This tool supports to define each dataset manually specifying all fields or to use a DOI and ya2ro will try to automatically fetch the data.

```yaml
datasets:
  - 
    doi: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
    license: "MIT-License"
    author: "Author name"
-
    path: templates/datasets
    name: "Dataset name"
    author: "Author name"
    description: "Description of a local dataset"
- https://doi.org/xx.xxxx/xxxxxxxxxx # Or just a link and ya2ro will guess the type
```

`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided ya2ro will use SOMEF to automatically fetch relevant data.

```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
  - https://sofware.web.com # Or just a link and ya2ro will guess the type
```

`bibliography:`In this field is where the bibliography can be added. Also a doi can be used and the bibliography entry will be fetch automatically.

```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
  - https://doi.org/XXXXXXXXX
```

`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is provided, ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.

```yaml
authors:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```

---

### Project

Documentation for all supported fields for type project.

`type:`This field is required and is used to indicate the type of the work.

```yaml
type: "project"
```

`title:`Title of the project.

```yaml
title: "Project - Template"
```

`goal:`In this field you should inlcude the goal for the project.

```yaml
goal: "Here is where a description of what is this project trying to achieve."
```

`social_motivation:`In this field you should include why this project will help in a social way.

```yaml
social_motivation: "This is the social motivation behind this project."
```

`sketch:`Path to an image where a visual description/workflow is shown.

```yaml
sketch: "images/sketch_ya2ro.jpg"
```

`areas:`All the areas involucrated inside this project.

```yaml
areas: 
  - "Area 1: Some description."
  - "Area 2: Some description."
```

`activities:`All the individual subtasks of the project.

```yaml
activities:
  - "Subtask 1: Some description."
  - "Subtask 2: Some description."
```

`demo:`Link or links to demos of the project.

```yaml
demo: 
  -
    link: http://demo.com
    description: "This is a description for a demo."
  -
    name: "Demo name"
    link: http://demo.com
    description: "This is a description for a demo with name."
```

`datasets:` All the datasets used and created during the paper. This tool supports to define each dataset manually specifying all fields or to use a DOI and ya2ro will try to automatically fetch the data.

```yaml
datasets:
  - 
    doi: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
    license: "MIT-License"
    author: "Author name"
  -
    path: templates/datasets
    name: "Dataset name"
    author: "Author name"
    description: "Description of a local dataset"
  - https://doi.org/xx.xxxx/xxxxxxxxxx # Or just a link and ya2ro will guess the type
```

`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided, ya2ro will use SOMEF to automatically fetch relevant data.

```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
  - https://sofware.web.com # Or just a link and ya2ro will guess the type
```

`bibliography:`In this field is where the bibliography can be added. Also a doi can be used and the bibliography entry will be fetch automatically.

```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
  - https://doi.org/XXXXXXXXX
```

`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is provided ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.

```yaml
participants:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```

`contact:`In this field you can add some contact information.

```yaml
contact:
  email: contact@projectmail.com
  phone: +34 999 999 999
```
