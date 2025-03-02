import sqlite3
import time
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

db_name = "flashscore.db"
app = Flask(__name__)

def criar_tabela():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estatisticas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time TEXT,
                        over_1_5 REAL,
                        over_2_5 REAL,
                        btts REAL,
                        escanteios REAL,
                        cartoes REAL,
                        marcou_ultimos_20 INTEGER
                    )''')
    conn.commit()
    conn.close()

def coletar_dados_flashscore():
    print("Iniciando coleta de dados...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.flashscore.com/")
    time.sleep(5)
    
    # Exemplo: Simulação de coleta de dados (substituir pelo scraping real)
    estatisticas = {
        "time": "Time Exemplo",
        "over_1_5": 75.0,
        "over_2_5": 55.0,
        "btts": 60.0,
        "escanteios": 4.2,
        "cartoes": 2.3,
        "marcou_ultimos_20": 18
    }
    
    salvar_dados(estatisticas)
    driver.quit()

def salvar_dados(dados):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO estatisticas (time, over_1_5, over_2_5, btts, escanteios, cartoes, marcou_ultimos_20)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (dados["time"], dados["over_1_5"], dados["over_2_5"], dados["btts"], dados["escanteios"], dados["cartoes"], dados["marcou_ultimos_20"]))
    conn.commit()
    conn.close()

@app.route('/dados', methods=['GET'])
def obter_dados():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estatisticas")
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados)

if __name__ == "__main__":
    criar_tabela()
    coletar_dados_flashscore()
    app.run(debug=True)
