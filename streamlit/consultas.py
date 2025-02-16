from connect_db import connect_to_db

def insert_startup(id_startup, nome_startup, cidade_sede):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Startups (id_startup, nome_startup, cidade_sede) VALUES (%s, %s, %s)"
    cursor.execute(query, (id_startup, nome_startup, cidade_sede))
    db.commit()
    cursor.close()
    db.close()

def get_startups():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Startups")
    startups = cursor.fetchall()
    cursor.close()
    db.close()
    return startups

def update_startup(id_startup, nome_startup, cidade_sede):
    db = connect_to_db()
    cursor = db.cursor()
    query = "UPDATE Startups SET nome_startup = %s, cidade_sede = %s WHERE id_startup = %s"
    cursor.execute(query, (nome_startup, cidade_sede, id_startup))
    db.commit()
    cursor.close()
    db.close()

def delete_startup(id_startup):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM Startups WHERE id_startup = %s"
    cursor.execute(query, (id_startup,))
    db.commit()
    cursor.close()
    db.close()


def insert_programador(id_programador, nome_programador, genero, data_nasc, id_startup):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Programadores (id_programador, nome_programador, genero, data_nasc, id_startup) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (id_programador, nome_programador, genero, data_nasc, id_startup))
    db.commit()
    cursor.close()
    db.close()

def get_programadores():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Programadores")
    programadores = cursor.fetchall()
    cursor.close()
    db.close()
    return programadores

def update_programador(id_programador, nome_programador, genero, data_nasc, id_startup):
    db = connect_to_db()
    cursor = db.cursor()
    query = "UPDATE Programadores SET nome_programador = %s, genero = %s, data_nasc = %s, id_startup = %s WHERE id_programador = %s"
    cursor.execute(query, (nome_programador, genero, data_nasc, id_startup, id_programador))
    db.commit()
    cursor.close()
    db.close()

def delete_programador(id_programador):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM Programadores WHERE id_programador = %s"
    cursor.execute(query, (id_programador,))
    db.commit()
    cursor.close()
    db.close()


def insert_dependente(nome_dependente, parentesco, data_nasc, id_programador):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Dependentes (nome_dependente, parentesco, data_nasc, id_programador) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nome_dependente, parentesco, data_nasc, id_programador))
    db.commit()
    cursor.close()
    db.close()

def get_dependentes():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Dependentes")
    dependentes = cursor.fetchall()
    cursor.close()
    db.close()
    return dependentes

def update_dependente(id_dependente, nome_dependente, parentesco, data_nasc, id_programador):
    db = connect_to_db()
    cursor = db.cursor()
    query = "UPDATE Dependentes SET nome_dependente = %s, parentesco = %s, data_nasc = %s, id_programador = %s WHERE id_dependente = %s"
    cursor.execute(query, (nome_dependente, parentesco, data_nasc, id_programador, id_dependente))
    db.commit()
    cursor.close()
    db.close()

def delete_dependente(id_dependente):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM Dependentes WHERE id_dependente = %s"
    cursor.execute(query, (id_dependente,))
    db.commit()
    cursor.close()
    db.close()


def insert_linguagem(id_linguagem, nome_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Linguagens (id_linguagem, nome_linguagem) VALUES (%s, %s)"
    cursor.execute(query, (id_linguagem, nome_linguagem))
    db.commit()
    cursor.close()
    db.close()

def get_linguagens():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Linguagens")
    linguagens = cursor.fetchall()
    cursor.close()
    db.close()
    return linguagens

def update_linguagem(id_linguagem, nome_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = "UPDATE Linguagens SET nome_linguagem = %s WHERE id_linguagem = %s"
    cursor.execute(query, (nome_linguagem, id_linguagem))
    db.commit()
    cursor.close()
    db.close()

def delete_linguagem(id_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM Linguagens WHERE id_linguagem = %s"
    cursor.execute(query, (id_linguagem,))
    db.commit()
    cursor.close()
    db.close()

def insert_programador_linguagem(id_programador, id_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Programador_Linguagem (id_programador, id_linguagem) VALUES (%s, %s)"
    cursor.execute(query, (id_programador, id_linguagem))
    db.commit()
    cursor.close()
    db.close()

def get_programador_linguagens():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Programador_Linguagem")
    programador_linguagens = cursor.fetchall()
    cursor.close()
    db.close()
    return programador_linguagens

def delete_programador_linguagem(id_programador, id_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = "DELETE FROM Programador_Linguagem WHERE id_programador = %s AND id_linguagem = %s"
    cursor.execute(query, (id_programador, id_linguagem))
    db.commit()
    cursor.close()
    db.close()