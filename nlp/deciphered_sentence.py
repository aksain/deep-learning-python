import networkx as nx


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


class LinkedNode:
    def __init__(self, data):
        self.prev_node = None
        self.next_node = None
        self.data = data
    
    def __repr__(self):
        return str(self.data)


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def insert_first(self, data):
        linked_node = LinkedNode(data)
        if self.__head is None:
            self.__head = linked_node
            self.__tail = linked_node
        else:
            linked_node.next_node = self.__head
            self.__head.prev_node = linked_node

            self.__head = linked_node
        return linked_node

    def insert(self, data):
        linked_node = LinkedNode(data)
        if self.__head is None:
            self.__head = linked_node
            self.__tail = linked_node
        else:
            linked_node.prev_node = self.__tail
            self.__tail.next_node = linked_node
            self.__tail = linked_node
        
        return linked_node

    def delete_first(self):
        deleted_node = None
        if self.__head is not None:
            deleted_node = self.__head
            self.__head = self.__head.next_node
            if self.__head is not None:
                self.__head.prev_node = None

        return deleted_node

    def delete(self):
        deleted_node = None
        if self.__tail is not None:
            deleted_node = self.__tail
            self.__tail = self.__tail.prev_node
            if self.__tail is not None:
                self.__tail.next_node = None

        return deleted_node

    def is_empty(self):
        return self.__head is None

    def get_first(self):
        return self.__head.data if not self.is_empty() else None

    def get_last(self):
        return self.__tail.data if not self.is_empty() else None
    
    def __repr__(self):
        tmp = self.__head
        response = "["
        while tmp is not None:
            response = response + "|" + str(tmp)
            tmp = tmp.next_node
            
        return response + "]"


class Stack:
    def __init__(self):
        self.__items = []

    def isEmpty(self):
        return self.size() == 0

#     def push(self, item):
#         if self.isEmpty() or self.peek().text != item.text:
#             self.__items.append(item)
            
    def push(self, item):
        self.__items.append(item)
        
    def pop(self):
        return self.__items.pop()

    def peek(self):
        return None if self.isEmpty() else self.__items[len(self.__items) - 1]

    def size(self):
        return len(self.__items)

    def contains(self, item):
        return item in self.__items

    def clear(self):
        del self.__items[:]
        
    def __repr__(self):
        return self.__items.__repr__()
    
    
class SimpleGraph:
    def __init__(self):
        self.__items
    

class DecipheredSentence:
    def __init__(self):
        self.graph_tokens = nx.DiGraph()
        self.list_tokens = LinkedList()
        self.noun_chunks = Stack()
        self.propn_chunks = Stack()
        self.verbs = Stack()
        self.neg_advs = Stack()
        
    def __repr__(self):
        return "Token List: " + str(self.list_tokens) + "\nNoun Chunks: " + str(self.noun_chunks) + "\nProper Noun Chunks: " + str(self.propn_chunks) + "\nVerbs: " + str(self.verbs) + "\nNeg Adv: " +  str(self.neg_advs)