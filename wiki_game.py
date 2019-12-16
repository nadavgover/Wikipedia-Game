from data_structures import *
from WikiGameError import WikiGameError
import wikipediaapi


class WikiGame:
    def __init__(self, source, destination):
        self.wikipedia = wikipediaapi.Wikipedia()
        self.article1 = source
        self.article2 = destination
        self.path = None

    def safe_get(self, title):
        """Safely gets a Wikipedia article object for the inputted title.
        Some links within Wikipedia pages link to articles that have not been created yet.
        This is a method for ignoring those, as the wikipeida package throws an error for these articles."""
        try:
            assert isinstance(title, str)
        except AssertionError:
            raise WikiGameError("Title must be of type string. Found {} instead".format(type(title)))

        wiki_page = self.wikipedia.page(title)
        if wiki_page.exists():
            return wiki_page
        else:
            return

    def is_valid_article(self, title):
        """Determines whether a given title links to a valid Wikipedia page. Similar reasoning as in safe_get(), see
        previous docstring for more info."""
        try:
            assert isinstance(title, str)
        except AssertionError:
            raise WikiGameError("Title must be of type string. Found {} instead".format(type(title)))

        wiki_page = self.wikipedia.page(title)
        return wiki_page.exists()

    def solve(self):
        """Wikipedia solver function. Uses breadth-first search (BFS) on the links in an article."""
        try:
            assert isinstance(self.article1, str) and isinstance(self.article2, str)
        except AssertionError:
            raise WikiGameError("Both articles must be of string Type.")

        source = self.safe_get(self.article1)
        destination = self.safe_get(self.article2)

        if source is None:
            raise WikiGameError("Initial article does not exist, try another one.")
        if destination is None:
            raise WikiGameError("Goal article does not exist, try another one.")

        if source.title == destination.title:
            self.path = [self.article1]
            return

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
            links = current.links()
            for link_title in links:
                if link_title == destination.title:
                    # skips out on much extra searching.
                    return self.tree_path(current, self.article1, self.article2)
                if link_title not in used:
                    article = links[link_title]
                    if article:
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

if __name__ == '__main__':
    wiki = WikiGame("foo", "bar")
