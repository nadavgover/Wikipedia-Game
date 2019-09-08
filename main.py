from wiki_game import WikiGame
from WikiGameError import WikiGameError
import time

def get_user_input():
    print("For best results and avoiding disambiguation,\n"
          "it's better to go to Wikipedia and copy the exact name of the article.\n")
    source = input("Enter source article:")
    destination = input("Enter destination article: ")
    return source, destination


def main():
    try:
        source, destination = get_user_input()
        wiki = WikiGame(source=source, destination=destination)
        print("Solving, this might take a few seconds\n")
        start_time = time.time()
        wiki.solve()
        elapsed_time = time.time() - start_time
        print("The shortest path is:")
        wiki.print_path()
        print("")
        print("Found a path in {} seconds, which are {} minutes".format(elapsed_time, elapsed_time / 60.0))

    except WikiGameError as e:
        print(e)


if __name__ == '__main__':
    main()
