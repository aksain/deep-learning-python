class LinkedNode:
    def __init__(self, data):
        self.prev_node = None
        self.next_node = None
        self.data = data


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

class DecipheredSentence:
    def __init__(self):
        self.list_tokens =