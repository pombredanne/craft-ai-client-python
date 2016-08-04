import requests
import os


def update_readme():
    url = "http://beta.craft.ai/content/api/python.md"
    r = requests.get(url)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(os.sep, dir_path, "README.md")

    if r.status_code == 200:
        with open(file_path, 'w') as f:
            for line in r.text:
                f.write(line)
