from connect_db import connect_to_db

def insert_startup(id_startup, nome_startup, cidade_sede):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO Startups (id_startup, nome_startup, cidade_sede) VALUES (%s, %s, %s)"
    cursor.execute(query, (id_startup, nome_startup, cidade_sede))
    db.commit()
    cursor.close()
    db.close()

def buscar_relacionamento(id_programador, id_linguagem):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        SELECT * FROM programador_linguagem
        WHERE id_programador = %s AND id_linguagem = %s
    """
    cursor.execute(query, (id_programador, id_linguagem))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()

    return resultado

def get_programadores_por_cidade(cidade):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
    SELECT p.nome_programador, p.genero, p.data_nasc, s.nome_startup
    FROM Programadores p
    LEFT JOIN Startups s ON p.id_startup = s.id_startup
    WHERE s.cidade_sede = %s
    """
    cursor.execute(query, (cidade,))
    programadores = cursor.fetchall()
    cursor.close()
    db.close()
    return programadores

def get_todos_programadores():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT id_programador, nome_programador FROM Programadores")
    programadores = cursor.fetchall()
    cursor.close()
    db.close()
    return programadores

def get_programadores_com_dependentes():
    db = connect_to_db()
    cursor = db.cursor()
    query = """
    SELECT p.nome_programador, COUNT(d.nome_dependente) AS num_dependentes
    FROM Programadores p
    LEFT JOIN Dependentes d ON p.id_programador = d.id_programador
    GROUP BY p.id_programador
    """
    cursor.execute(query)
    programadores = cursor.fetchall()
    cursor.close()
    db.close()
    return programadores

def calcular_idade(data_nasc):
    hoje = date.today()
    idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    return idade

def eh_maior_de_idade(data_nasc):
    return calcular_idade(data_nasc) >= 18

def get_programadores_por_data_nasc(data_inicio, data_fim):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
    SELECT nome_programador, data_nasc
    FROM Programadores
    WHERE data_nasc BETWEEN %s AND %s
    """
    cursor.execute(query, (data_inicio, data_fim))
    programadores = cursor.fetchall()
    cursor.close()
    db.close()
    return programadores

def get_cidades():
    db=connect_to_db()

    cursor = db.cursor()
    
    cursor.execute("SELECT DISTINCT cidade_sede FROM startups")  
    cidades = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    db.close()
    return cidades


def get_dependentes_por_programador(id_programador):
    db = connect_to_db()
    
    cursor = db.cursor()
    
    query = """
    SELECT id_dependente, nome_dependente, parentesco, data_nasc, id_programador
    FROM dependentes
    WHERE id_programador = %s
    """
    cursor.execute(query, (id_programador,))
    
    dependentes = cursor.fetchall()

    cursor.close()
    db.close()
    
    return dependentes

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

def get_linguagens_por_programador(id_programador):
    db = connect_to_db()
    cursor = db.cursor()
    
    query = """
    SELECT L.nome_linguagem
    FROM Programador_Linguagem PL
    JOIN Linguagens L ON PL.id_linguagem = L.id_linguagem
    WHERE PL.id_programador = %s
    """
    
    cursor.execute(query, (id_programador,))
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