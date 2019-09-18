from wiki_game import WikiGame
from WikiGameError import WikiGameError
import time


def main():
    try:
        wiki = WikiGame(source="Breadth-first search", destination="computer science")
        start_time = time.time()
        wiki.solve()
        elapsed_time = time.time() - start_time
        print("The shortest path is:")
        wiki.print_path()
        print("")
        print("Found a path in {:.3f} seconds, which are {:.3f} minutes".format(elapsed_time, elapsed_time / 60.0))

    except WikiGameError as e:
        print(e)


if __name__ == '__main__':
    main()
