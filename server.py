
# app.py
from flask import Flask, request, abort, make_response

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
    pw = data.get('password', '')
    if pw == EXPECTED_PASSWORD:
        # exemplo: devolver ok; aqui poderias devolver um token JWT, cookie de sessão, etc.
        return "Autenticado", 200
    else:
        return "Password inválida", 401

if __name__ == '__main__':
    # Executa localmente: em produção usa gunicorn/uwsgi atrás de HTTPS
    app.run(host='127.0.0.1', port=5000)
