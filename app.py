from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import asyncio
import uuid
import os
from temporalio.exceptions import FailureError
from temporalio.client import WorkflowFailureError
from client import get_client
from activities import UserSentimentInput
from workflow import ReviewProcessingWorkflow
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET'])
async def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
async def upload():
    file = request.files['file']
    labels = request.form.getlist('labels[]')
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Start booking workflow
        client = await get_client()

        id = str(uuid.uuid4().int)[:6]

        input = UserSentimentInput(
            filepath = filepath,
            labels = labels
        ) 

        try:
            result = await client.execute_workflow(
                ReviewProcessingWorkflow.run,
                input,
                id=f'inference-{id}',
                task_queue="activity_sticky_queue-distribution-queue",
            )
        except WorkflowFailureError:
            return render_template('table.html', table=df.to_html(index=False), error_message="Invalid Credit Card.")
        except FailureError:        
            return render_template('table.html', table=df.to_html(index=False), error_message="Invalid Credit Card.")
        
        df = pd.read_csv(filepath)
        df['Sentiment'] = result['sentiment']
        return render_template('table.html', table=df.to_html(index=False))
    else:
        return "No file selected."    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)    
