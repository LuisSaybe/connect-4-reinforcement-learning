## grid world with tensorflow 2

#### build

build

```sh
docker build --rm -t tf-gridworld .
```

#### run

```sh
docker run -it -w /tmp/tf-gridworld/src -v $(pwd):/tmp/tf-gridworld --rm tf-gridworld python index.py
```
