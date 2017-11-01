import spacy

nlp = spacy.load('en')

# print(random_article)

def sanitize_ent(ents):
    result = set()
    for ent in ents:
        if not any([x for x in ent if len(x) > len(ent) and ent in x ]):
            result.add(ent)

    return result



def retrieve_entities(article_text):
    organizations, persons = set(), set()
    doc = nlp(article_text)
    for ent in doc.ents:
        if (ent.label_ == 'ORG'):
            organizations.add(ent.text)
        if (ent.label_ == 'PERSON'):
            persons.add(ent.text)
    organizations, persons = sanitize_ent(organizations), sanitize_ent(persons)
    return organizations, persons
