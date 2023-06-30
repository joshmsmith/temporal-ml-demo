from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
async def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        df = pd.read_csv(file)
        return render_template('table.html', table=df.to_html(index=False))
    else:
        return "No file selected."    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)    
