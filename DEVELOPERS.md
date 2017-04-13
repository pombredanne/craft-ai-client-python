# Developers instructions #

## Running the tests locally ##

1. Retrieve your **craft ai** _owner_ and _token_.
2. On your dev machine, at the root of your clone, create a file named `.env` with the following content

  ```
  CRAFT_TOKEN=<retrieved_token>
  ```

3. To run the tests, run the following:

  ```console
  $ make init
  ```

4. To run the tests, run the following:

  ```console
  $ make test
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

3. Updade the readme (this creates a git commit for you)

  ```console
  $ make update-readme
  ```

4. Increment the version

  ```console
  $ make version-increment-patch
  ```

  `version-increment-minor` and `version-increment-major` are also available.

5. Push!

  ```console
  $ git push -f origin master
  $ git push --tags
  ```
