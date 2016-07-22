# Developers instructions #

## Running the tests locally ##

1. Retrieve your **craft ai** _owner_ and _token_.
2. On your dev machine, at the root of your clone, create a file named `.env` with the following content
````
CRAFT_OWNER=<retrieved_owner>
CRAFT_TOKEN=<retrieved_token>
````
3. Run `pip3 install -r requirements.txt` to install dependencies
4. You can run the following script:
```sh
sh run_tests.sh # this runs all tests via nosetests
```

<!-- ## Releasing a new version (needs administrator rights) ##

1. Make sure the build of the master branch is passing
[![Build](https://img.shields.io/travis/craft-ai/craft-ai-client-js/master.svg?style=flat-square)](https://travis-ci.org/craft-ai/craft-ai-client-js)
2. Checkout the master branch locally
````sh
git fetch
git checkout master
git reset --hard origin/master
````
3. Bump the version and push
````sh
npm version patch
git push origin master
git push --tags
```` -->