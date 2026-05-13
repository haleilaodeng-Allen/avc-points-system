from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_excel("AVC_Master_Points_Database.xlsx.xlsx")

    html = df.to_html(index=False)

    return f"""
    <html>
    <head>
        <title>AVC Database</title>
        <style>
            body {{
                font-family: Arial;
                padding: 30px;
                background-color: #f5f5f5;
            }}

            h1 {{
                color: #333;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
                background: white;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}

            th {{
                background-color: #333;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>AVC Points Database</h1>
        {html}
    </body>
    </html>
    """

app.run(debug=True)