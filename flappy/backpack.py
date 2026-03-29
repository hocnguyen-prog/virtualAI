from flask import Flask, request, jsonify

app = Flask(__name__)
scores = []

@app.route("/score", methods=["POST"])
def add():
    scores.append(request.json)
    scores.sort(key=lambda x: x["score"], reverse=True)
    return {"ok": True}

@app.route("/top")
def top():
    html = """
    <html>
    <head>
        <title>Leaderboard</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to bottom, #87CEEB, #ffffff);
                text-align: center;
            }
            h1 {
                margin-top: 40px;
            }
            table {
                margin: auto;
                border-collapse: collapse;
                width: 300px;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            th, td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #4CAF50;
                color: white;
            }
            tr:hover {
                background: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>🏆 Leaderboard</h1>
        <table>
            <tr><th>Rank</th><th>Name</th><th>Score</th></tr>
    """

    for i, s in enumerate(scores[:10]):
        html += f"<tr><td>{i+1}</td><td>{s['name']}</td><td>{s['score']}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html


app.run()