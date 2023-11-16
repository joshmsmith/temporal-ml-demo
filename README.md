# Temporal ML Sentiment Demo
This is Machine Learning demo using [Temporal](temporal.io) to orchestrate file processing of csv dataset and show sentiment as well as probability for user reviews using inference. Any csv that has a column called ```Reviewer_Location``` and ```Review_Text``` will work. Text should be a review of a product or service. Location should be where the reviewer was located.

The demo implements activity sticky queue in Temporal so that activities run on same worker where the csv file has been uploaded.
## Demo Info
This demo primarily demonstrates an interesting way to show the _durable integration_ features of Temporal, demonstrating developer **velocity** by integrating to an AI system - ChatGPT - and easily managing asynchronous calls.
You can also demo **visibility** by showing the work being done in the Temporal user interface.


| Primary Value Demonstration | ✅ |
|:-------------------|---|
| Velocity          | ✅ |
| Reliability       |   |
| Insight           |   |

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

# Setup & Run
See [Demo Setup & Run Instructions](./how-to-run.md).



# Walkthrough
### 1. Load CSV
![Load CSV](/static/csv.png)
### 2. Select Location
![Select Location](/static/location.png)
### 3. Review Results
![View Sentiment and Probability](/static/table.png)
