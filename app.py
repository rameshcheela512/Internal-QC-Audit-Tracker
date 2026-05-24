from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite డేటాబేస్ కనెక్షన్ మరియు టేబుల్ క్రియేషన్
def init_db():
    conn = sqlite3.connect('qc_audit_db.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            auditor_name TEXT NOT NULL,
            error_type TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # శాంపిల్ డేటా (టేబుల్ ఖాళీగా ఉంటేనే ఇన్సర్ట్ అవుతుంది)
    cursor.execute("SELECT COUNT(*) FROM audit_logs")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO audit_logs (team_name, auditor_name, error_type, status) VALUES ('Team cl', 'Suresh', 'Data Entry Error', 'Resolved')")
        cursor.execute("INSERT INTO audit_logs (team_name, auditor_name, error_type, status) VALUES ('Team Gatekeeping', 'Ramesh', 'Compliance Miss', 'Pending')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/log_error', methods=['POST'])
def log_error():
    data = request.json
    try:
        conn = sqlite3.connect('qc_audit_db.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (team_name, auditor_name, error_type, status)
            VALUES (?, ?, ?, ?)
        """, (data['team_name'], data['auditor_name'], data['error_type'], data['status']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Audit log saved successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/dashboard_data', methods=['GET'])
def dashboard_data():
    try:
        conn = sqlite3.connect('qc_audit_db.db')
        conn.row_factory = sqlite3.Row  # డిక్షనరీ ఫార్మాట్ కోసం
        cursor = conn.cursor()
        
        cursor.execute("SELECT team_name, COUNT(*) as count FROM audit_logs GROUP BY team_name")
        team_data = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT error_type, COUNT(*) as count FROM audit_logs GROUP BY error_type")
        error_data = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify({"teams": team_data, "errors": error_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()  # యాప్ స్టార్ట్ అవ్వగానే డేటాబేస్ ఆటోమేటిక్‌గా క్రియేట్ అవుతుంది
    app.run(debug=True)