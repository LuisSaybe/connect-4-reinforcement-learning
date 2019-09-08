## grid world with tensorflow 2

#### build

build

```sh
docker build --rm -t tf-gridworld .
```

#### run

```sh
docker run -it -p 8000:8000  --rm tf-gridworld
```

#### make code changes and run

```sh
docker build --rm -t tf-gridworld . && docker run -it --rm -p 8000:8000 tf-gridworld
```
