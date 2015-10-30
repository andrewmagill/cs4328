class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

class Singly(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def insert_at_head(self, data):
        temp = Node(data)
        if self.head:
            temp.next = self.head
        self.head = temp
        #self.current = temp

    def insert_at_tail(self, data):
        temp = Node(data)
        if self.tail:
            cursor = self.head
            while cursor.next:
                if cursor.next == self.current:
                    break
                else:
                    cursor = cursor.next
            cursor.next = self.tail
        self.tail = temp
        #self.current = temp

    def insert(self, data):
        temp = Node(data)
        if not self.current:
            self.current = temp
            self.head = temp
            self.tail = temp
        else:
            if self.tail == self.current:
                self.tail = temp
            temp.next = self.current.next
            self.current.next = temp
            self.advance()

    def remove(self):
        if not self.current:
            return False

        if self.tail == self.head:
            self.head = None
            self.tail = None
            self.current = None
        elif self.current == self.head:
            self.head = self.current.next
            self.current = self.current.next
        else:
            cursor = self.head
            while cursor.next:
                if cursor.next == self.current:
                    break
                else:
                    cursor = cursor.next
            temp = self.current.next
            cursor.next = temp
            if self.current == self.tail:
                self.tail = cursor
            self.current = cursor

    def advance(self):
        if not self.current:
            return False

        if not self.current.next:
            return False

        self.current = self.current.next
        return True

    def reset(self):
        self.current = self.head
