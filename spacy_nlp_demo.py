import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en')
# Process whole documents
text = (u"An alteration in mental status refers to general changes in brain function, such as confusion, amnesia (memory loss), loss of alertness, disorientation (not cognizant of self, time, or place), defects in judgment or thought, unusual or strange behavior, poor regulation of emotions, and disruptions in perception, psychomotor skills, and behavior. I have got 20Rs. Net income was $9.4 million compared to the prior year of $2.7 million.")
# text = (u"An alteration in mental status is neither a general change nor a specific one")
doc = nlp(text)

for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)

# Find Nouns
for noun in doc.noun_chunks:
    print(noun)

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
