import requests
import os

from argparse import ArgumentParser


def update_readme():
    url = "http://beta.craft.ai/content/api/python.md"
    r = requests.get(url)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(os.sep, dir_path, "README.md")

    if r.status_code == 200:
        with open(file_path, 'w') as f:
            for line in r.text:
                f.write(line)
            print("Successfully updated README.md")


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--update_readme",
        action="store_true",
        help="Updates the README.md file from craft.ai official documentation")

    args = parser.parse_args()
    if args.update_readme:
        update_readme()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
