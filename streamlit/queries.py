import streamlit as st
import pandas as pd
from connect_db import connect_to_db

def run_query(query):
    db = connect_to_db()
    if db:
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        db.close()
        return pd.DataFrame(data, columns=columns)
    return pd.DataFrame()

st.set_page_config(page_title="Dashboard de Startups", layout="wide")
st.title("📊 Dashboard de Startups e Programadores")

st.sidebar.header("Navegação")
selecao = st.sidebar.selectbox("Escolha a análise", [
    "Número de Programadores por Startup",
    "Média de Idade dos Programadores",
    "Número de Dependentes por Programador",
    "Programador Mais Velho e Mais Novo",
    "Número de Programadores por Gênero",
    "Startups Mais Diversas",
    "Idade Mínima e Máxima dos Programadores por Startup",
    "Visualizar Programadores e Startups"
])

queries = {
    "Número de Programadores por Startup": """
        SELECT s.nome_startup, COUNT(p.id_programador) AS total_programadores
        FROM Startups s
        LEFT JOIN Programadores p ON s.id_startup = p.id_startup
        GROUP BY s.nome_startup
        ORDER BY total_programadores DESC;
    """,
    "Média de Idade dos Programadores": """
        SELECT s.nome_startup, 
               ROUND(AVG(YEAR(CURDATE()) - YEAR(p.data_nasc)), 1) AS media_idade
        FROM Startups s
        LEFT JOIN Programadores p ON s.id_startup = p.id_startup
        GROUP BY s.nome_startup
        ORDER BY media_idade DESC;
    """,
    "Número de Dependentes por Programador": """
        SELECT p.nome_programador, COUNT(d.id_dependente) AS total_dependentes
        FROM Programadores p
        LEFT JOIN Dependentes d ON p.id_programador = d.id_programador
        GROUP BY p.nome_programador
        ORDER BY total_dependentes DESC;
    """,
    "Programador Mais Velho e Mais Novo": """
        SELECT nome_programador, data_nasc, YEAR(CURDATE()) - YEAR(data_nasc) AS idade
        FROM Programadores
        WHERE data_nasc = (SELECT MIN(data_nasc) FROM Programadores)
           OR data_nasc = (SELECT MAX(data_nasc) FROM Programadores);
    """,
    "Número de Programadores por Gênero": """
        SELECT CASE 
            WHEN genero = 'M' THEN 'Masculino' 
            WHEN genero = 'F' THEN 'Feminino' 
            ELSE 'Outro' 
        END AS genero,
        COUNT(*) AS total
        FROM Programadores
        GROUP BY genero;
    """,
    "Startups Mais Diversas": """
        SELECT s.nome_startup,
               SUM(CASE WHEN p.genero = 'M' THEN 1 ELSE 0 END) AS total_homens,
               SUM(CASE WHEN p.genero = 'F' THEN 1 ELSE 0 END) AS total_mulheres,
               ABS(SUM(CASE WHEN p.genero = 'M' THEN 1 ELSE 0 END) - 
                   SUM(CASE WHEN p.genero = 'F' THEN 1 ELSE 0 END)) AS score_diversidade
        FROM Startups s
        LEFT JOIN Programadores p ON s.id_startup = p.id_startup
        GROUP BY s.nome_startup
        ORDER BY score_diversidade ASC;
    """,
    "Idade Mínima e Máxima dos Programadores por Startup": """
        SELECT s.nome_startup, 
               MIN(YEAR(CURDATE()) - YEAR(p.data_nasc)) AS idade_minima,
               MAX(YEAR(CURDATE()) - YEAR(p.data_nasc)) AS idade_maxima
        FROM Startups s
        JOIN Programadores p ON s.id_startup = p.id_startup
        GROUP BY s.nome_startup
        ORDER BY idade_minima ASC;
    """,
    "Visualizar Programadores e Startups": "SELECT * FROM vw_programadores_info;"
}

df = run_query(queries[selecao])

if not df.empty:
    st.dataframe(df)
else:
    st.error("Nenhum dado encontrado.")