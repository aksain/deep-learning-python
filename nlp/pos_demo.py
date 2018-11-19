import matplotlib.pyplot as plt
import networkx as nx
import re
import spacy
import string
from spacy import displacy
from deciphered_sentence import DecipheredSentence, Token, Stack
from operator import pos

nlp = spacy.load('en')

# clean_regs = [re.compile('.<.*?>'), re.compile('<.*?>'), re.compile(' \(.*?\)')]
clean_regs = [re.compile('<.*?>'), re.compile(' \(.*?\)')]

knowldege_graph = nx.DiGraph()


def execute_noun_rules(noun_chunk, deciphered_sentence, token, visited, propn = False):
    if noun_chunk is None or token in visited:
        return

    if noun_chunk.text in ['two specific conditions']:
        print('Ignoring noise noun: ' + noun_chunk.text)
        return
    
    if deciphered_sentence.neg_advs.peek() is not None:
        return

    token_node = Token(noun_chunk.text, noun_chunk.root.pos_, noun_chunk.root.dep_, noun_chunk.root)

    for tmp_token_node in knowldege_graph.nodes:
        if tmp_token_node.is_more_concrete_version_of(token_node):
            token_node = tmp_token_node

    deciphered_noun_chunks = deciphered_sentence.noun_chunks
    if deciphered_noun_chunks.isEmpty() or deciphered_noun_chunks.peek().text != noun_chunk.text:
        if deciphered_sentence.verbs.peek() is not None and deciphered_sentence.propn_chunks.peek() is not None:
            l_vertx = deciphered_sentence.propn_chunks.peek()
            edge = deciphered_sentence.verbs.peek()
            r_vertx = token_node
            deciphered_sentence.graph_tokens.add_edge(l_vertx, r_vertx, relation=edge)
        else:
            deciphered_sentence.graph_tokens.add_node(token_node)

        deciphered_noun_chunks.push(token_node)
        if propn:
            deciphered_sentence.propn_chunks.push(token_node)


def execute_verb_rules(noun_chunk, deciphered_sentence, verb, visited):
    if noun_chunk is not None or verb in visited:
        return

    # if verb.text == 'will':
    #     print("Clearing stack, Reason: " + verb.text)
    #     deciphered_sentence.clear()
    #     return

    # stack_item = deciphered_sentence.peek()
    # if isinstance(stack_item, spacy.tokens.token.Token) and stack_item.pos_ in ['VERB']:
    #     print("Poping Stack value: " + str(stack_item) + ", Reason: Continuous verbs")
    #     deciphered_sentence.pop()

#     token_node = deciphered_sentence.list_tokens.insert(Token(verb.text, verb.pos_, verb.dep_, verb.head))
    token_node = Token(verb.text, verb.pos_, verb.dep_, verb.head)
    deciphered_sentence.verbs.push(token_node)                                                    
    if verb.dep_ in ['auxpass']:
        vhead = verb.head
        print [child for child in vhead.lefts]
#         deciphered_sentence.verbs.peek().append_text(vhead.text)
        visited.append(vhead)
        # deciphered_sentence.push(Token(vhead.text, vhead.pos_, vhead.dep_, vhead.head))

    # if verb.dep_ in['ROOT']:
    #     deciphered_sentence.push(verb)


def get_matching_noun_chunk(sentence_span, noun):
    final_noun_chunk = None
    for noun_chunk in sentence_span.noun_chunks:
        if noun.text + " " in noun_chunk.text or " " + noun.text in noun_chunk.text or noun.text == noun_chunk.text:
            # finding exact match as a noun can be part of multiple noun chunks due to multiple occurrences
            if noun_chunk.start <= noun.i < noun_chunk.end:
                final_noun_chunk = noun_chunk

    return final_noun_chunk


with open("../data/diseases_conditions/A_Hemophilia_(Hemophilia)") as f:
    for line in f.readlines():

        clean_text = line
        for clean_reg in clean_regs:
            clean_text = re.sub(clean_reg, '', clean_text)

        print clean_text

        doc = nlp(unicode(clean_text, 'utf-8'))
        sentence_spans = list(doc.sents)

        visited = list('')
        prop_nouns = Stack()
        for sentence_span in sentence_spans[:3]:
            print sentence_span

            for token in sentence_span:
                print(token.text, token.lemma_, token.pos_, token.dep_, token.head.text)

            deciphered_sentence = DecipheredSentence()
            deciphered_sentence.propn_chunks = prop_nouns
            # for token in reversed(sentence_span):
            for token in sentence_span:
                if token in visited:
                    continue

                if token.pos_ in ['PROPN'] and token.dep_ in ['nsubj', 'compound']:
                    noun_chunk = get_matching_noun_chunk(sentence_span, token)
                    execute_noun_rules(noun_chunk, deciphered_sentence, token, visited, True)
                    
                elif token.pos_ in ['NOUN']:
                    noun_chunk = get_matching_noun_chunk(sentence_span, token)
                    execute_noun_rules(noun_chunk, deciphered_sentence, token, visited)
                    
                elif token.pos_ in ['VERB']:
                    noun_chunk = get_matching_noun_chunk(sentence_span, token)
                    # print("process stack: " + str(deciphered_sentence.items))
                    execute_verb_rules(noun_chunk, deciphered_sentence, token, visited)

                elif token.pos_ in ['ADV'] and token.dep_ in ['neg']:
                    deciphered_sentence.neg_advs.push(Token(token.text, token.pos_, token.dep_, token.head))
#                 elif token.pos_ in ['ADJ'] and token.dep_ in ['nsubj']:
#                     deciphered_sentence.neg_advs.push(Token(token.text, token.pos_, token.dep_, token.head))
                elif token.pos_ in ['CCONJ'] and token.dep_ in ['cc']:
                    deciphered_sentence.conjuctions.push(Token(token.text, token.pos_, token.dep_, token.head))
                elif token.lemma_ in ['but']:
                    deciphered_sentence.neg_advs.pop()

                visited.append(token)
                
            print deciphered_sentence
            prop_nouns = deciphered_sentence.propn_chunks
            knowldege_graph.add_nodes_from(deciphered_sentence.graph_tokens)
            knowldege_graph.add_edges_from(deciphered_sentence.graph_tokens.edges.data())

    pos = nx.spring_layout(knowldege_graph)
    nx.draw(knowldege_graph, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(knowldege_graph, pos)
    plt.show()
