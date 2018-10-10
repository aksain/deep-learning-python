# import SpaCy module
import spacy

# load English language model
nlp = spacy.load('en')

# Text needs to be in unicode string
doc = nlp(u'The US and China\'s escalation of trade tariffs is expected to hit growth in both countries in 2019'
    u', when the boost from President Trump\'s sweeping tax cuts will also start to wane. '
    u''
    u'Mr Obstfeld said the world would become a "poorer and more dangerous place" unless world leaders worked together '
    u'to raise living standards, improve education and reduce inequality.')

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
print "%-15s %-15s %-15s %-15s" % ("Token", "Token POS Tag", "Token Lemma", "Token Dependency")
print "-----------------------------------------------------------------"
for token in doc:
    print "%-15s %-15s %-15s %-15s" % (token, token.pos_, token.lemma_, token.dep_)
