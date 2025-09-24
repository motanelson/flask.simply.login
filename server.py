
# app.py
from flask import Flask, request, abort, make_response
import os
import subprocess
app = Flask(__name__)

# password "fácil" para exemplo — NÃO USES assim em produção
EXPECTED_PASSWORD = "hello"

@app.route('/')
def index():
    # serve o ficheiro HTML do cliente (assume index.html no mesmo directório)
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json(silent=True) or {}
    print(data)
    pw = data.get('password', '')
    cmd = data.get('cmds', '')
    print(cmd)
    cmds=cmd.split(" ")
    if pw == EXPECTED_PASSWORD:
        try:
        
            result = subprocess.run(
                 cmds,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE,
                 text=True,
                 cwd=os.getcwd()
            )
       
            if result.stdout.find("err")<0 and result.stderr.find("err")<0:
                s=result.stdout.replace("\n","<br>")
                return s
            else:
                return "error:"
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Script execution failed', 'details': str(e)}), 500

        
    else:
        return "Password inválida", 401

if __name__ == '__main__':
    # Executa localmente: em produção usa gunicorn/uwsgi atrás de HTTPS
    app.run(host='127.0.0.1', port=5000)
