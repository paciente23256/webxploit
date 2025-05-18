#!/usr/bin/python
# @paciente23256

"""
webxploit 2.0.2025
web interface with flask
"""

from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from pathlib import Path
import time
import webxploit  # Deve estar no mesmo diretório
import json

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / 'logs'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_scan():
    target = request.form['target']
    threads = int(request.form.get('threads', 10))
    project = request.form.get('project') or str(int(time.time()))

    logs_folder = LOGS_DIR
    config = webxploit.load_config(BASE_DIR / 'config')

    Path(logs_folder / project).mkdir(parents=True, exist_ok=True)
    targets = [target]

    webxploit.generate_rcs(targets, threads, project, config, BASE_DIR, logs_folder)
    webxploit.run_rcs(project, logs_folder)
    webxploit.get_successful(project, logs_folder)
    webxploit.generate_report(project, logs_folder)

    return redirect(url_for('report', project=project))

@app.route('/report/<project>')
def report(project):
    project_dir = LOGS_DIR / project
    return render_template('report.html', project=project, files=list(project_dir.iterdir()))

@app.route('/download/<project>/<filename>')
def download_file(project, filename):
    return send_from_directory(LOGS_DIR / project, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
