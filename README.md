# temporal-ml-demo
Machine Learning demo using temporal to orchestrate decision making based on model inference using chatgpt

# Setup
```bash
$ mkdir .venv
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
```

# Run App
```bash
$ poetry run python starter.py
```

# Run Worker
```bash
$ export CHATGPT_API_KEY=mykey
```

```bash
$ poetry run python worker.py
```
