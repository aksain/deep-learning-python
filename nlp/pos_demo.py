import networkx as nx
import re
import spacy
from spacy import displacy

nlp = spacy.load('en')

# clean_regs = [re.compile('.<.*?>'), re.compile('<.*?>'), re.compile(' \(.*?\)')]
clean_regs = [re.compile('<.*?>'), re.compile(' \(.*?\)')]

# def process_token(token, visited):
#     token_key = token.text + token.dep_
#     if token_key in visited:
#         return False
#
#     # if token.tag_ in ['NNP', 'NNPS']:
#     if token.pos_ in ['NOUN', 'PROPN']:
#         print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#               token.shape_, token.is_alpha, token.is_stop, token.head)
#         visited.append(token_key)
#
#         if token.dep_ in ['compound']:
#             print token.text + " " + token.head.text
#
#             # print(token.head, token.head.dep_)
#             process_token(token.head, visited)

class Token:
    def __init__(self, text, pos, dep, root):
        self.text = text
        self.pos = pos
        self.dep = dep
        self.root = root

    def __repr__(self):
        return self.text

    def prepend_text(self, text):
        self.text = text + "" + self.text

    def append_text(self, text):
        self.text += " " + text


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.size() == 0

    def push(self, item):
        if self.isEmpty() or self.peek().text != item.text:
            self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return None if self.isEmpty() else self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def contains(self, item):
        return item in self.items

    def clear(self):
        del self.items[:]


def execute_noun_rules(noun_chunk, token_stack, token, visited):
    if noun_chunk is None or token in visited:
        return

    if noun_chunk.text in ['two specific conditions']:
        print('Ignoring noise noun: ' + noun_chunk.text)
        return

    token_stack.push(Token(noun_chunk.text, noun_chunk.root.pos_, noun_chunk.root.dep_, noun_chunk.root))


def execute_verb_rules(noun_chunk, token_stack, verb, visited):
    if noun_chunk is not None or verb in visited:
        return

    # if verb.text == 'will':
    #     print("Clearing stack, Reason: " + verb.text)
    #     token_stack.clear()
    #     return

    # if isinstance(verb, spacy.tokens.token.Token) and token_stack.contains(verb):
    #     return

    # stack_item = token_stack.peek()
    # if isinstance(stack_item, spacy.tokens.token.Token) and stack_item.pos_ in ['VERB']:
    #     print("Poping Stack value: " + str(stack_item) + ", Reason: Continuous verbs")
    #     token_stack.pop()

    token_stack.push(Token(verb.text, verb.pos_, verb.dep_, verb.head))
    if verb.dep_ in ['auxpass']:
        vhead = verb.head
        print [child for child in vhead.lefts]
        token_stack.peek().append_text(vhead.text)
        visited.append(vhead)
        # token_stack.push(Token(vhead.text, vhead.pos_, vhead.dep_, vhead.head))

    # if verb.dep_ in['ROOT']:
    #     token_stack.push(verb)


def get_matching_noun_chunk(sentence_span, noun):
    final_noun_chunk = None
    for noun_chunk in sentence_span.noun_chunks:
        if noun.text in noun_chunk.text:
            # finding exact match as a noun can be part of multiple noun chunks due to multiple occurences
            if noun_chunk.start <= noun.i < noun_chunk.end:
                final_noun_chunk = noun_chunk

    return final_noun_chunk


def get_matching_noun_chunk_for_verb(sentence_span, verb):
    final_noun_chunk = None
    for noun_chunk in sentence_span.noun_chunks:
        if verb.text + " " in noun_chunk.text or " " + verb.text in noun_chunk.text:
            # finding exact match as a verb can be part of multiple noun chunks due to multiple occurences
            if noun_chunk.start <= verb.i < noun_chunk.end:
                final_noun_chunk = noun_chunk

    return final_noun_chunk


with open("../data/diseases_conditions/A_Hemophilia_(Hemophilia)") as f:
    DG = nx.DiGraph()
    for line in f.readlines():

        clean_text = line
        for clean_reg in clean_regs:
            clean_text = re.sub(clean_reg, '', clean_text)

        print clean_text

        doc = nlp(unicode(clean_text, 'utf-8'))
        sentence_spans = list(doc.sents)

        visited = list('')
        for sentence_span in sentence_spans[:3]:
            print sentence_span

            for noun_chunk in sentence_span.noun_chunks:
                print noun_chunk
                DG.add_node(noun_chunk.text)

            for token in sentence_span:
                print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)

            token_stack = Stack()
            # for token in reversed(sentence_span):
            for token in sentence_span:
                if token in visited:
                    continue

                if token.pos_ in ['PROPN', 'NOUN']:
                    noun_chunk = get_matching_noun_chunk(sentence_span, token)
                    execute_noun_rules(noun_chunk, token_stack, token, visited)

                elif token.pos_ in ['VERB']:
                    noun_chunk = get_matching_noun_chunk_for_verb(sentence_span, token)
                    # print("process stack: " + str(token_stack.items))
                    execute_verb_rules(noun_chunk, token_stack, token, visited)

                # elif token.pos_ in ['ADV'] and token.dep_ in ['neg']:
                #     print "Removed from stack: " + str(token_stack.pop()) + ", Reason: " + token.text

                visited.append(token)

            print("process stack:" + str(token_stack.items))
