# Temporal ML Sentiment Demo
Machine Learning demo using [Temporal](temporal.io) to orchestrate file processing of csv dataset and show sentiment as well as probability for user reviews using inference. Any csv that has a column called ```Reviewer_Location``` and ```Review_Text``` will work. Text should be a review of a product or service. Location should be where the reviewer was located.

The demo implements activity sticky queue in Temporal so that activities run on same worker where the csv file has been uploaded.
## Demo Info
This demo primarily demonstrates an interesting way to show the _durable integration_ features of Temporal, demonstrating developer **velocity** by integrating to 



| Value Demonstration | ✅ |
|:-------------------|---|
| Velocity          | ✅ |
| Reliability       |  |
| Insight           |  |

### Deployment
| Deployment          | ✅ |
|:-------------------|---|
| Local              | ✅ |
| Disconnected       | 🚫 |
| Kubernetes         | ✅ |

### Prerequisites
| Prerequisite       | ✅ |
|:-------------------|---|
| Network Connection | ✅ |
| Python             | ✅|
| Temporal CLI (local)| ✅ |

### Features
| Feature            | ✅ | 
|:-------------------|---|
| Schedule       |   |
| Local Activity |   |
| Signal         | ✅ |
| Query          | ✅ |
| Update         |   |
| Heartbeat      |   |
| Timer          | ✅ |
| Activity Retry |   |
| Cron           |   |   
| Data Converter |   |

### Patterns
| Pattern            | ✅ |
|:-------------------|---|
| Entity              |   |
| Fanout              |   |
| Long-polling        |   |
| Continue As New     |   |
| Long-running        |   |
| Manual Intervention | ✅ |
| Saga                |   |

### Production Grade Features
| Feature            | ✅ |
|:-------------------|---|
| User Interface   | ✅ |

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

You will find two csv datasets one of Disneyland reviews and other Amazon product reviews under the datasets directory. Simply upload one to begin the demo.

# Walkthrough
![Load CSV](/static/csv.png)
![Select Location](/static/location.png)
![View Sentiment and Probability](/static/table.png)
