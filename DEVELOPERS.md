# Developers instructions #

## Running the tests locally ##

1. Retrieve your **craft ai** _owner_ and _token_.
2. On your dev machine, at the root of your clone, create a file named `.env` with the following content

  ```
  CRAFT_TOKEN=<retrieved_token>
  ```

3. Run `pip3 install -r requirements.txt` to install dependencies
4. You can run the following script:

  ```console
  $ ./run-tests.sh
  ```

## Releasing a new version (needs administrator rights) ##

1. Make sure the build of the master branch is passing  
  [![Build](https://img.shields.io/travis/craft-ai/craft-ai-client-python/master.svg?style=flat-square)](https://travis-ci.org/craft-ai/craft-ai-client-python)

2. Checkout the master branch locally

  ```console
  $ git fetch
  $ git checkout master
  $ git reset --hard origin/master
  ```

3. Updade the readme

  ```console
  $ ./scripts/update_readme.sh
  $ git add README.* && git commit -m "Updated README files"
  ```

4. Update to the new version vX.Y.Z (this should follow [semver](http://semver.org) guidelines)

  ```console
  $ edit ./craftai/__init__.py
  $ git add ./craftai/__init__.py && git commit -m "Bumping to version vX.Y.Z"
  $ git tag -a vX.Y.Z
  ```

5. Push!

  ```console
  $ git push -f origin master
  $ git push --tags
  ```
