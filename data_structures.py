from WikiGameError import WikiGameError
import wikipediaapi as wikipedia


class Link:
    def __init__(self, val, next_link, prev_link):
        self.val = val
        self.next_link = next_link
        self.prev_link = prev_link


class Linked_List:

    def __init__(self):
        self.head, self.last = None, None
        self.size = 0

    def insert_last(self, x):
        """Adds x as the last link of the linked list"""
        new_link = Link(x, None, self.last)  # Make a new link
        if self.size == 0:
            self.head = new_link
        else:
            self.last.next_link = new_link

        self.last = new_link
        self.size += 1

    def insert_first(self, x):
        """Adds x at the front of the linked list"""
        new_link = Link(x, self.head, None)  # Make a new link
        if self.size == 0:
            self.last = new_link
        else:
            self.head.prev_link = new_link

        self.head = new_link
        self.size += 1

    def remove_first(self):
        """Removes the first link and returns it"""
        if self.size == 0:
            return None

        head = self.head.val
        if self.size == 1:  # only one element in the list, so after removal the list is empty
            self.head = None
            self.last = None
        else:  # more than one element, than update the first link
            self.head = self.head.next_link
            self.head.prev_link = None

        self.size -= 1
        return head

    def remove_last(self):
        """Removes the last link and returns it"""
        if self.size == 0:
            return None

        last = self.last.val
        if self.size == 1:  # only one element in the list, so after removal the list is empty
            self.head = None
            self.last = None
        else:  # more than one element, than update the last link
            self.last = self.last.prev_link
            self.last.next_link = None

        self.size -= 1
        return last

    def __len__(self):
        return self.size

    def __str__(self):
        output = ""
        if self.head is None:  # if the list is empty
            return output

        output += str(self.head.val)
        current_link = self.head.next_link
        while current_link is not None:
            output += ", " + str(current_link.val)
            current_link = current_link.next_link
        return output


class Queue:
    def __init__(self):
        self.linked_list = Linked_List()

    def enqueue(self, x):
        self.linked_list.insert_last(x)

    def dequeue(self):
        return self.linked_list.remove_first()

    def is_empty(self):
        return len(self.linked_list) == 0

    def front(self):
        """Returns the first item and does not dequeue it"""
        if len(self.linked_list) > 0:
            return self.linked_list.head.val

    def __len__(self):
        return len(self.linked_list)

    def __str__(self):
        return self.linked_list.__str__()


class Tree:
    """Assumes all items will be Wikipedia page types."""
    def __init__(self, x, parent=None):
        if not self.is_valid(x):
            raise WikiGameError("Each item in the Tree must be of type WikipediaPage. found {} instead".format(type(x)))
        self.item = x
        self.parent = parent
        self.children = []
        self.visited = False

    def is_valid(self, x):
        if not isinstance(x, wikipedia.WikipediaPage):
            return False
        return True

    def add_children(self, *children):
        for i in children:
            try:
                assert isinstance(i, Tree)
            except AssertionError:
                raise WikiGameError("All children must be of type Tree. Found {} instead".format(type(i)))

            # self.children.append(Tree(i, self))  # Each node is a sub Tree
            self.children.append(i)

    def links(self):
        """Returns a list of all links from the page.
        In Wikipedia the links are bi-directional, meaning that it has a reference of what is pages are linked to
        a current page.
        So this function is filtering the links that are going out from this page and not into this page"""
        # links = []
        # content = self.item.content.encode('utf8').lower()
        # for link in self.item.links:
        #     link = link.encode('utf8')
        #     if link not in links:  # Do not add the same link twice
        #         if link.lower() in content:  # if link is actually in the page. This is the filtering discussed in the docstring
        #             links.append(link)

        # return links

        # output = []  # output is like this [(<page title>, <WikipediaPage>)] list of tuples
        # links = self.item.links
        # for title in sorted(links.keys()):
        #     output.append((title, links[title]))
        #     print("%s: %s" % (title, links[title]))
        # return output

        links = {}
        content = self.item.text.lower()
        for title, page in self.item.links.items():
            if title not in links:  # Do not add the same link twice
                if title.lower() in content:  # if link is actually in the page. This is the filtering discussed in the docstring
                    links[title] = page

        return links
        # return self.item.links

    def title(self):
        return self.item.title

    def num_children(self):
        return len(self.children)

    def __str__(self):
        return str(self.item)









