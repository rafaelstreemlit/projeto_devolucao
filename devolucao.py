import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect('banco_teste8.db', check_same_thread=False)
cursor = conn.cursor()

def formCreation():
    st.write('Por Favor Preencha o Protocolo')
    
    with st.form(key="Registration Form", clear_on_submit=True):
        rota = st.text_input('Digite o numero da Rota :')
        motorista = st.text_input('Digite o nome da Motorista : ')
        transportadora = st.text_input('Digite o nome da Transportadora : ')
        pedido = st.text_input('Digite o numero do Pedido : ')
        remessa = st.text_input('Digite o numero da Remessa : ')
        nota_fiscal = st.text_input('Digite o numero da nota fiscal : ')
        motivo = st.text_input('Digite o motivo da Devolução : ')
        data_registro = st.date_input('Digite a Data : ')
        submit = st.form_submit_button(label='Registro')


        if submit == True:
            st.success('o registro foi efetuado com sucesso')
            addInfo(rota,motorista,transportadora,pedido,remessa,nota_fiscal,motivo,data_registro)

def addInfo(rota, motorista, transportadora, pedido, remessa,nota_fiscal, motivo, data_registro):
    # Conecte ao banco de dados
    conn = sqlite3.connect('banco_teste8.db')
    cursor = conn.cursor()

    # Insira os dados na tabela 'protocolo'
    cursor.execute('''
        INSERT INTO protocolos (rota, motorista, transportadora, pedido, remessa,nota_fiscal, motivo, data_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (rota, motorista, transportadora, pedido, remessa,nota_fiscal, motivo, data_registro))
    
    # Confirme a transação e obtenha o ID do último registro inserido
    conn.commit()
    last_id = cursor.lastrowid
    
    # Feche a conexão
    conn.close()

    # Exiba uma mensagem de sucesso com o ID do registro
    st.success(f'Devolução cadastrada com sucesso. ID do Registro: {last_id}')

# Função para buscar e exibir informações com base no ID
def viewInfo(id):
    cursor.execute("SELECT * FROM protocolos WHERE id=?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result

def viewAllRecords():
    cursor.execute("SELECT * FROM protocolos")
    records = cursor.fetchall()
    return records
    
# Função para exportar os dados para Excel
def export_to_excel(data):
    df = pd.DataFrame(data, columns=['ID', 'Rota', 'Motorista', 'Transportadora', 'Pedido', 'Remessa','Nota Fiscal', 'Motivo', 'Data'])
    return df.to_csv(index=False, sep=';').encode('latin1')


# Função principal para a interface do Streamlit
def main():
    st.title("Protocolo de Devolução/Reentrega ")

    # Seção de registro
    st.header("Registro de Protocolo")
    formCreation()

    # Seção de consulta
    st.header("Consultar Protocolo por ID")
    id_input = st.text_input("Digite o ID do protocolo:")

    if st.button("Consultar"):
        if id_input:
            try:
                id_value = int(id_input)
                result = viewInfo(id_value)
                if result:
                    st.write(f"ID: {result[0]}")
                    st.write(f"Rota: {result[1]}")
                    st.write(f"Motorista: {result[2]}")
                    st.write(f"Transportadora: {result[3]}")
                    st.write(f"Pedido: {result[4]}")
                    st.write(f"Remessa: {result[5]}")
                    st.write(f"Nota Fiscal: {result[6]}")
                    st.write(f"Motivo: {result[7]}")
                    st.write(f"Data: {result[8]}")
                    
                    csv = export_to_excel([result])
                    
                    st.download_button(
                        label="Exportar registro para CSV",
                        data=csv,
                        file_name="file.csv",
                        mime="text/csv",
                    )           
              
                else:
                    st.write("Nenhum registro encontrado para o ID fornecido.")
            except ValueError:
                st.write("Por favor, insira um ID válido.")
        else:
            st.write("Digite um ID para consultar.")

    # Seção para mostrar todos os registros
    st.header("Mostrar Todos os Registros ")
    if st.button("Mostrar Todos"):
        records = viewAllRecords()
        print(records)
        if records:
            for record in records:
                st.write(f"ID: {record[0]}, Rota: {record[1]}, Motorista: {record[2]}, Transportadora: {record[3]}, Pedido: {record[4]}, Remessa: {record[5]}, Nota Fiscal: {record[6]}, Motivo: {record[7]}, Data: {record[8]}")
            
            csv = export_to_excel(records)
                    
            st.download_button(
                label="Exportar Todos para CSV",
                data=csv,
                file_name="file.csv",
                mime="text/csv",
            )    
                  
        else:
            st.write("Nenhum registro encontrado no banco de dados.")

if __name__ == "__main__":
    main()



