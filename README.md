## IR System - TFIDF Implementation to search relevant covid19 clinical trails

### Running the application
- Python >3
- Create a folder meta in the application root directory, This is where the indexes cached for quick queries!
- Run app.py
       - python3 app.py <path-to-data-file-dir>
- On querying, Application attempts to return top 10 relevant documents with their titles, filename, similarity score
       
### Data set files and index construction
Since the actual data is huge. I created a medium size version which contain 500 files. along with indexes cached. 
Files in meta folder can be removed to reconstruct the indexes. If you attempt to create a new index with much bigger clinical trails data.
Use the link below to download the original dataset and delete the index files in meta/, so the index is re created.

1. Meta folder is already present in the folder. You could use the already constructed index of original set or recreate by not 
using the meta folder.
1. Original dataset (3095 files) - https://drive.google.com/drive/folders/1UaO7pIfw8eSMYnussKsNpG6yeT9UmCva?usp=sharing

### Additional Libraries Dependencies
- nltk
    - punkt
    - wordnet
    - stopwords
- pandas

### Overview
#### Step 1
- Tokenization
    - tags extracted from XML
        1.	brief_title 
        2.	official_title
        3.	brief_summary
        4.	location_countries/country
        5.	detailed_description
        6.	Phase
        7.	intervention/description
        8.	intervention/intervention_type
        9.	Condition
        10.	Keyword
- Remove stop words
- Perform normalization (covid -- covid19)

#### Step 2
- inverted index 
- Document id to document name index

#### step 3
- Save index for future use

#### Step 4
- Ranked retrieval using tfidf for terms

### Resources
https://clinicaltrials.gov/ct2/about-studies/glossary
https://clinicaltrials.gov/ct2/html/images/info/public.xsd
https://clinicaltrials.gov/ct2/results/map?cond=COVID-19&map=
http://www.trec-cds.org/2019.html#documents
