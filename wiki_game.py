from data_structures import *
from WikiGameError import WikiGameError
import wikipediaapi
import pickle

class WikiGame:
    def __init__(self, source, destination):
        self.wikipedia = wikipediaapi.Wikipedia()
        self.article1 = source
        self.article2 = destination
        self.path = None
        # self.used_once_before = self.get_titles_to_articles_dict()

    def safe_get(self, title):
        """Safely gets a Wikipedia article object for the inputted title. Some links within Wikipedia pages link to articles
        that have not been created yet. This is a method for ignoring those, as the wikipeida package throws an error for
        these articles."""
        try:
            assert isinstance(title, str)
        except AssertionError:
            raise WikiGameError("Title must be of type string. Found {} instead".format(type(title)))

        wiki_page = self.wikipedia.page(title)
        if wiki_page.exists():
            return wiki_page
        else:
            return
        # try:
        #     return self.wikipedia.page(title)
        # except:  # Article does not exist or can refer for more than one thing
        #     return

    def is_valid_article(self, title):
        """Determines whether a given title links to a valid Wikipedia page. Similar reasoning as in safe_get(), see
        previous docstring for more info."""
        try:
            assert isinstance(title, str)
        except AssertionError:
            raise WikiGameError("Title must be of type string. Found {} instead".format(type(title)))

        wiki_page = self.wikipedia.page(title)
        return wiki_page.exists()
        # try:
        #     wikipedia.page(title)
        #     return True
        # except wikipedia.PageError:
        #     return False

    def solve(self):
        """Wikipedia solver function. Uses breadth-first search (BFS) on the links in an article."""
        try:
            assert isinstance(self.article1, str) and isinstance(self.article2, str)
        except AssertionError:
            raise WikiGameError("Both articles must be of string Type.")
        # if not self.is_valid_article(self.article2):
        #     raise WikiGameError("Goal article does not exist, try another one.")
        # if not self.is_valid_article(self.article1):
        #     raise WikiGameError("Initial article does not exist, try another one.")

        # source = self.wikipedia.page(self.article1)
        source = self.safe_get(self.article1)
        # destination = self.wikipedia.page(self.article2)
        destination = self.safe_get(self.article2)

        if source is None:
            raise WikiGameError("Initial article does not exist, try another one.")
        if destination is None:
            raise WikiGameError("Goal article does not exist, try another one.")

        # if source.title not in self.used_once_before:  # For running this code next time. potentially faster
        #     self.add_instance_to_file(source)

        if source.title == destination.title:
            self.path = [self.article1]
            return
        # if self.article1 == self.article2:
        #     return [self.article1]

        # BFS
        q = Queue()
        tree = Tree(source)
        used = set()
        q.enqueue(tree)
        while not q.is_empty():
            current = q.dequeue()
            if current.visited:
                # This node has already been processed.
                continue
            current.visited = True
            # if current.title() not in self.used_once_before:
            #     self.add_instance_to_file(current)
            links = current.links()  # The problem is here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! the links are not good
            for link_title in links:
                if link_title == destination.title:
                    # skips out on much extra searching.
                    return self.tree_path(current, self.article1, self.article2)
                if link_title not in used:
                    # The child is not in the queue.
                    # if link_title in self.used_once_before:  # potentially faster loading
                    #     article = self.used_once_before[link_title]
                    # else:
                    #     article = self.safe_get(link_title)
                    article = links[link_title]
                    if article:
                        # safe_get() returns None if the article is invalid; None is False in Python.
                        # This block continues tree construction.
                        # if article.title not in self.used_once_before:  # For running this code next time
                        #     self.add_instance_to_file(article)
                        used.add(link_title)
                        branch = Tree(article, current)
                        current.add_children(branch)
                        q.enqueue(branch)

    def tree_path(self, node, article1, article2):
        """Returns the trace from article1 to article2 (arguments to solve)."""
        """Goes up the tree until it finds the root, which is article1"""
        try:
            assert isinstance(node, Tree)
        except AssertionError:
            raise WikiGameError("Node must be of Tree type. Found {} instead".format(type(node)))

        path = [article2]
        while node.parent is not None:
            # node.parent is None iff Node is the root of the tree ie. article1
            path.append(node.title())
            node = node.parent
        path.append(article1)
        path.reverse()
        self.path = path
        # return path

    def print_path(self):
        for c, link in enumerate(self.path, start=1):
            print(c, link)

    # def add_instance_to_file(self, wiki_page, filename="instances.pkl"):
    #     with open(filename, "ab") as instances:
    #         pickle.dump(wiki_page, instances, pickle.HIGHEST_PROTOCOL)

    # def unpickle_articles(self, filename="instances.pkl"):
    #     """Unpickle a file of pickled data."""
    #     with open(filename, "rb") as f:
    #         while True:
    #             try:
    #                 yield pickle.load(f)
    #             except EOFError:
    #                 break

    # def get_titles_to_articles_dict(self, filename="instances.pkl"):
    #     """Reads a file full with pre-loaded articles.
    #     Returns d{<title>: <article>}"""
    #     d = {}
    #     for wiki_page in self.unpickle_articles(filename):
    #         title = wiki_page.title
    #         d[title] = wiki_page
    #     return d

# Testing if your page exists
if __name__ == '__main__':
    wiki = WikiGame("foo", "bar")
    page = wiki.safe_get("mosfet")
    print(page.fullurl)


