# Developers instructions #

## Running the tests locally ##

1. Retrieve your **craft ai** _owner_ and _token_.
2. On your dev machine, at the root of your clone, create a file named `.env` with the following content

    ```
    CRAFT_OWNER=<retrieved_owner>
    CRAFT_TOKEN=<retrieved_token>
    ```

3. Run `pip3 install -r requirements.txt` to install dependencies
4. You can run the following script:

    ```console
    sh run-tests.sh # this runs all tests via nosetests
    ```

## Releasing a new version (needs administrator rights) ##

> Before merging a pull request back to master, update the README and push it to the branch you're working on.

    ```console
    $ ./scripts/update_readme.sh
    $ git add README.* && git commit -m "Updated README files"
    ```

1. Make sure the build of the master branch is passing
    [![Build](https://img.shields.io/travis/craft-ai/craft-ai-client-python/master.svg?style=flat-square)](https://travis-ci.org/craft-ai/craft-ai-client-python)

2. Checkout the master branch locally
    ````sh
    git fetch
    git checkout master
    git reset --hard origin/master
    ````

3. Tag the new version, writing the major changes, and push
    ```sh
    git tag -a <bumped_semantic_version>
    git push -f origin master
    git push --tags
    ````
