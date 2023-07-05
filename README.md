# temporal-ml-demo
Machine Learning demo using temporal to orchestrate file processing of csv dataset and show sentiment as well as probability for user reviews using inference. Any csv that has a column called ```Reviewer_Location``` and ```Review_Text``` will work. Text should be a review of a product or service. Location should be where the reviewer was located.

The demo implements activity sticky queue in Temporal so that activities run on same worker where the csv file has been uploaded.

# Setup
```bash
$ mkdir .venv
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
```

# Run App
```bash
$ poetry run python app.py
```

# Run Worker
```bash
$ export CHATGPT_API_KEY=mykey
```

```bash
$ poetry run python worker.py
```

# Connect to app
[http://localhost:5000](http://localhost:5000)

You will find two csv datasets one of Disneyland reviews and other Amazon product reviews under the datasets directory. Simply upload one to being the demo.

# Walkthrough
![Load CSV](/static/csv.png)
![Select Location](/static/location.png)
![View Sentiment and Probability](/static/table.png)
