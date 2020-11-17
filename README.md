http://qwone.com/~jason/20Newsgroups/

http://www.trec-cds.org/2019.html

https://clinicaltrials.gov/ct2/about-studies/glossary
https://clinicaltrials.gov/ct2/html/images/info/public.xsd
https://clinicaltrials.gov/ct2/results/map?cond=COVID-19&map=
http://www.trec-cds.org/2019.html#documents
### clinical trails
- Phase
- intervention
- location
- Primary outcome
- keyword

### Implementation
- Precision and recall
- TF-IDF
- No need of ordering
- no stemming
- noun groups?
- normalization (covid -- covid19, phase 2 -- phase-2, case sensitive)


### Phases
## Step 1
- tokenization
    - tags
        - keyword
        - condition
        - brief_title
        - official_title
        - brief_summary
        - detailed_description
        - location_countries
        - study_design_info (not so important)
- stop words
- normalization (covid -- covid19)

## Step 2
- inverted index 

        

## Step 3
- boolean retrieval
- filters(phases, intervention)
https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
## Step 4
- Ranked retrieval - tfidf for terms


### Libraries
- nltk
    - punkt
    - wordnet
    - stopwords
- pandas
