from __future__ import unicode_literals, print_function

import plac
import spacy


TEXTS = [
    'I do not have 100 euros',
    'Net income was $9.4 million compared to the prior year of $2.7 million.',
    'Revenue exceeded twelve billion dollars, with a loss of $1b.',
]


@plac.annotations(
    model=("Mode    l to load (needs parser and NER)", "positional", None, str))
def main(model='en'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_currency_relations(doc)
        for r1, r2 in relations:
            print('{:<10}\t{}\t{}'.format(r1.text, r2.ent_type_, r2.text))


def extract_currency_relations(doc):
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for money in filter(lambda w: w.ent_type_ == 'MONEY', doc):
        if money.dep_ in ('attr', 'dobj'):
            subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, money))
        elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
            relations.append((money.head.head, money))
    return relations


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b