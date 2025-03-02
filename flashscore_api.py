from flask import Flask, jsonify
import sqlite3
import os

# Configuração do banco de dados
db_path = "flashscore.db"
app = Flask(__name__)

def criar_tabela():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_casa TEXT,
            time_fora TEXT,
            gols_casa INTEGER,
            gols_fora INTEGER,
            over_1_5 REAL,
            over_2_5 REAL,
            btts REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estatisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            over_1_5 REAL,
            over_2_5 REAL,
            btts REAL,
            escanteios REAL,
            cartoes REAL,
            marcou_ultimos_20 INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/dados/partidas', methods=['GET'])
def obter_partidas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partidas")
    dados = cursor.fetchall()
    conn.close()
    
    colunas = ["id", "time_casa", "time_fora", "gols_casa", "gols_fora", "over_1_5", "over_2_5", "btts"]
    resultado = [dict(zip(colunas, linha)) for linha in dados]
    
    return jsonify(resultado)

@app.route('/dados/estatisticas', methods=['GET'])
def obter_estatisticas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estatisticas")
    dados = cursor.fetchall()
    conn.close()
    
    colunas = ["id", "time", "over_1_5", "over_2_5", "btts", "escanteios", "cartoes", "marcou_ultimos_20"]
    resultado = [dict(zip(colunas, linha)) for linha in dados]
    
    return jsonify(resultado)

if __name__ == "__main__":
    if not os.path.exists(db_path):
        criar_tabela()
    app.run(debug=True)
