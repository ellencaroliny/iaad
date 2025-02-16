
import mysql.connector
import streamlit as st

def connect_to_db():
    """Conecta ao banco de dados e retorna a conexão"""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            user='root',
            password='141201',
            database='startup'
        )
        if connection.is_connected():
            print("✅ Conectado ao banco de dados com sucesso!")
            return connection
    except mysql.connector.Error as err:
        st.error(f"❌ Erro ao conectar ao banco: {err}")
        return None

def inserir_programador(nome, genero, data_nasc, id_startup):
    """Insere um programador no banco de dados"""
    conn = connect_to_db()  #

    if conn is None:
        return  # 

    try:
        cursor = conn.cursor()
        query = "INSERT INTO Programadores (nome_programador, genero, data_nasc, id_startup) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nome, genero, data_nasc, id_startup))
        conn.commit()
        st.success("✅ Programador cadastrado com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"❌ Erro ao inserir programador: {err.msg}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 Conexão fechada.")

if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        db_connection.close()
