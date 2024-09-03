import sqlite3

conn = sqlite3.connect('banco_teste8.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS protocolos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rota TEXT,
        motorista TEXT,
        transportadora TEXT,
        pedido TEXT,
        remessa TEXT,
        nota_fiscal TEXT,
        motivo TEXT,
        data_registro DATE
    )
''')

conn.commit()
conn.close()