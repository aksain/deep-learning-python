# import SpaCy module
import spacy

# load English language model
nlp = spacy.load('en')

# Text needs to be in unicode string
doc = nlp(u'Hemophilia is not one disease but also one of a group of inherited bleeding disorders')

print "\n\nSentences in the analysed text..."
for sentence_span in doc.sents:
    print sentence_span

print "\n\nNoun chunks in the analysed text..."
# Noun chunks are helpful where many tokens together make a composite noun
for noun_chunk in doc.noun_chunks:
    print noun_chunk

print "\n\nName entities in the analysed text..."
print "%-15s %-15s" % ("Entity Name", "Entity Label")
print "-----------------------------"
for entity in doc.ents:
    print "%-15s %-15s" % (entity, entity.label_)

print "\n\nTokens and their POS tags in the analysed text..."
print "%-15s %-15s %-15s %-15s %-15s" % ("Token", "Token POS Tag", "Token Lemma", "Token Dependency", "Head")
print "-----------------------------------------------------------------"
for token in doc:
    # print type(token)
    print "%-15s %-15s %-15s %-15s %-15s" % (token, token.pos_, token.lemma_, token.dep_, token.head)
