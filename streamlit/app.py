import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from connect_db import connect_to_db
from consultas import *

def startup_crud_interface():
    st.title("Gerenciamento de Startups")
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    if st.button("Adicionar Nova Startup"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Startup")
        id_startup = st.number_input("ID da Startup", min_value=1, key="add_id")
        nome_startup = st.text_input("Nome da Startup", key="add_nome")
        cidade_sede = st.text_input("Cidade Sede", key="add_cidade")
        if st.button("Salvar"):
            insert_startup(id_startup, nome_startup, cidade_sede)
            st.success("Startup adicionada com sucesso!")
            st.rerun()  

    st.subheader("Lista de Startups")
    startups = get_startups()

    if startups:
        # Cabeçalho da tabela
        col1, col2, col3, col4 = st.columns([1, 2, 2, 4])
        with col1:
            st.write("**ID**")
        with col2:
            st.write("**Nome**")
        with col3:
            st.write("**Cidade**")
        with col4:
            st.write("**Ações**")
        # Corpo da tabela
        for startup in startups:
            col1, col2, col3, col4 = st.columns([1, 2, 2, 4])
            with col1:
                st.write(startup[0]) 
            with col2:
                st.write(startup[1]) 
            with col3:
                st.write(startup[2]) 
            with col4:
                col_edit, col_delete = st.columns([1, 1])
                with col_edit:
                    if st.button("Editar", key=f"edit_{startup[0]}"):
                        st.session_state.edit_id = startup[0]
                with col_delete:
                    # Deletar
                    if st.button("Deletar", key=f"delete_{startup[0]}"):
                        delete_startup(startup[0])
                        st.success(f"Startup {startup[0]} deletada com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Startup")
        startup_to_edit = next((s for s in startups if s[0] == st.session_state.edit_id), None)
        if startup_to_edit:
            id_startup = st.number_input("ID da Startup", value=startup_to_edit[0], key="edit_id")
            nome_startup = st.text_input("Nome da Startup", value=startup_to_edit[1], key="edit_nome")
            cidade_sede = st.text_input("Cidade Sede", value=startup_to_edit[2], key="edit_cidade")
            if st.button("Salvar Alterações"):
                update_startup(id_startup, nome_startup, cidade_sede)
                st.success("Startup atualizada com sucesso!")
                del st.session_state.edit_id  
                st.rerun() 

def programadores_crud_interface():
    st.title("Gerenciamento de Programadores")
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    # Obter a lista de startups para o selectbox
    startups = get_startups()
    startup_options = {startup[1]: startup[0] for startup in startups}  # Mapeia nome_startup para id_startup

    if st.button("Adicionar programador"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar programador")
        id_programador = st.number_input("ID do programador", min_value=1, key="add_id_programador")
        nome_programador = st.text_input("Nome do programador", key="add_nome")
        
        # Gênero como opção
        genero = st.selectbox(
            "Gênero",
            options=["Masculino (M)", "Feminino (F)"],
            key="add_genero"
        )
        genero = genero[-2]  # Extrai "M" ou "F" da string selecionada

        # Data de Nascimento sem limite
        data_nasc = st.date_input("Data de Nascimento", key="add_data_nasc")

        # ID da Startup como lista de opções
        startup_selecionada = st.selectbox(
            "Startup",
            options=list(startup_options.keys()),  # Exibe os nomes das startups
            key="add_startup"
        )
        id_startup = startup_options[startup_selecionada]  # Obtém o ID da startup selecionada
        
        if st.button("Salvar"):
            insert_programador(id_programador, nome_programador, genero, data_nasc, id_startup)
            st.success("Programador adicionado com sucesso!")
            st.rerun()  

    st.subheader("Lista de Programadores")
    programadores = get_programadores()

    if programadores:
        # Cabeçalho da tabela
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 2, 4])
        with col1:
            st.write("**Id_programador**")
        with col2:
            st.write("**Nome**")
        with col3:
            st.write("**Genero**")
        with col4:
            st.write("**Data_Nascimento**")
        with col5:
            st.write("**Id_startup**") 
        with col6:
            st.write("**Ações**")
        # Corpo da tabela
        for programador in programadores:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 2, 2, 4])
            with col1:
                st.write(programador[0])
            with col2:
                st.write(programador[1])
            with col3:
                st.write(programador[2])
            with col4:
                st.write(programador[3])
            with col5:
                st.write(programador[4]) 
            with col6:
                col_edit, col_delete = st.columns([1, 1])
                with col_edit:
                    if st.button("Editar", key=f"edit_{programador[0]}"):
                        st.session_state.edit_id = programador[0]
                with col_delete:
                    # Deletar
                    if st.button("Deletar", key=f"delete_{programador[0]}"):
                        delete_programador(programador[0])
                        st.success(f"Programador {programador[0]} deletado com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Programador")
        programador_to_edit = next((s for s in programadores if s[0] == st.session_state.edit_id), None)
        if programador_to_edit:
            id_programador = st.number_input("ID do programador", value=programador_to_edit[0], key="edit_id")
            nome_programador = st.text_input("Nome do programador", value=programador_to_edit[1], key="edit_nome")
            
            # Gênero como opção
            genero = st.selectbox(
                "Gênero",
                options=["Masculino (M)", "Feminino (F)"],
                index=0 if programador_to_edit[2] == "M" else 1,  # Seleciona a opção correta
                key="edit_genero"
            )
            genero = genero[-2]  # Extrai "M" ou "F" da string selecionada

            # Data de Nascimento sem limite
            data_nasc = st.date_input("Data de Nascimento", value=programador_to_edit[3], key="edit_data_nasc")

            # ID da Startup como lista de opções
            startup_selecionada = st.selectbox(
                "Startup",
                options=list(startup_options.keys()),  # Exibe os nomes das startups
                index=list(startup_options.values()).index(programador_to_edit[4]),  # Seleciona a startup correta
                key="edit_startup"
            )
            id_startup = startup_options[startup_selecionada]  # Obtém o ID da startup selecionada

            if st.button("Salvar Alterações"):
                update_programador(id_programador, nome_programador, genero, data_nasc, id_startup)
                st.success("Programador atualizado com sucesso!")
                del st.session_state.edit_id  
                st.rerun()

def dependentes_crud_interface():
    st.title("Gerenciamento de Dependentes")

    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    # Obter a lista de programadores para o selectbox
    programadores = get_programadores()
    programador_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in programadores}  # Mapeia nome_programador para id_programador

    if st.button("Adicionar novo dependente"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar dependente")
        nome_dependente = st.text_input("Nome", key="add_dependente")
        parentesco = st.text_input("Parentesco", key="add_parentesco")
        
        # Usar st.date_input para a data de nascimento
        data_nasc = st.date_input("Data de Nascimento", key="add_data")
        
        # ID do Programador como lista de opções
        programador_selecionado = st.selectbox(
            "Programador",
            options=list(programador_options.keys()),  # Exibe os nomes dos programadores
            key="add_programador"
        )
        id_programador = programador_options[programador_selecionado]  # Obtém o ID do programador selecionado
        
        if st.button("Salvar"):
            insert_dependente(nome_dependente, parentesco, data_nasc, id_programador)
            st.success("Dependente adicionado com sucesso!")
            st.rerun()  

    st.subheader("Lista de dependentes")
    dependentes = get_dependentes()

    if dependentes:
        # Cabeçalho da tabela
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 4])
        with col1:
            st.write("**Nome**")
        with col2:
            st.write("**Parentesco**")
        with col3:
            st.write("**Data_Nascimento**")
        with col4:
            st.write("**Id_programador**")
        with col5:
            st.write("**Ações**")
        # Corpo da tabela
        for dependente in dependentes:
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 4])
            with col1:
                st.write(dependente[1])  # Por que a coluna[0] é o id do dependente
            with col2:
                st.write(dependente[2]) 
            with col3:
                st.write(dependente[3]) 
            with col4:
                st.write(dependente[4]) 
            with col5:
                col_edit, col_delete = st.columns([1, 1])
                with col_edit:
                    if st.button("Editar", key=f"edit_{dependente[0]}"):
                        st.session_state.edit_id = dependente[0]
                with col_delete:
                    # Deletar
                    if st.button("Deletar", key=f"delete_{dependente[0]}"):
                        delete_dependente(dependente[0])
                        st.success(f"Dependente {dependente[0]} deletado com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Dependente")
        dependente_to_edit = next((s for s in dependentes if s[0] == st.session_state.edit_id), None)
        if dependente_to_edit:
            nome_dependente = st.text_input("Nome", value=dependente_to_edit[1], key="edit_dependente")
            parentesco = st.text_input("Parentesco", value=dependente_to_edit[2], key="edit_parentesco")
            
            # Usar st.date_input para a data de nascimento
            data_nasc = st.date_input("Data de Nascimento", value=dependente_to_edit[3], key="edit_data")
            
            # ID do Programador como lista de opções
            programador_selecionado = st.selectbox(
                "Programador",
                options=list(programador_options.keys()),  # Exibe os nomes dos programadores
                index=list(programador_options.values()).index(dependente_to_edit[4]),  # Seleciona o programador correto
                key="edit_programador"
            )
            id_programador = programador_options[programador_selecionado]  # Obtém o ID do programador selecionado

            if st.button("Salvar Alterações"):
                update_dependente(dependente_to_edit[0], nome_dependente, parentesco, data_nasc, id_programador)
                st.success("Dependente atualizado com sucesso!")
                del st.session_state.edit_id  
                st.rerun()


def linguagens_crud_interface():
    st.title("Gerenciamento de Linguagens")
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False
    if st.button("Adicionar nova Linguagem"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Linguagens")
        id_linguagem=st.number_input("ID da Startup", min_value=1, key="add_id")
        nome_linguagem=st.text_input("Nome", key="nome_linguagem")
        
        if st.button("Salvar"):
            insert_linguagem(id_linguagem, nome_linguagem)
            st.success("Linguagem adicionada com sucesso!")
            st.rerun()  
    st.subheader("Lista de linguagens")
    linguagens = get_linguagens()
    if linguagens:
        # Cabeçalho da tabela
        col1, col2, col3, = st.columns([1, 2, 4])
        with col1:
            st.write("**ID**")
        with col2:
            st.write("**Nome**")
        with col3:
            st.write("**Ações**")
        # Corpo da tabela
        for linguagem in linguagens:
            col1, col2, col3, = st.columns([1, 2, 4])
            with col1:
                st.write(linguagem[0])
            with col2:
                st.write(linguagem[1]) 
            with col3:
                col_edit, col_delete = st.columns([1, 1])
                with col_edit:
                    if st.button("Editar", key=f"edit_{linguagem[0]}"):
                        st.session_state.edit_id = linguagem[0]
                with col_delete:
                    # Deletar
                    if st.button("Deletar", key=f"delete_{linguagem[0]}"):
                        delete_linguagem(linguagem[0])
                        st.success(f"Linguagem {linguagem[0]} deletada com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Linguagem")
        linguagem_to_edit = next((s for s in linguagens if s[0] == st.session_state.edit_id), None)
        if linguagem_to_edit:
            id_linguagem = st.number_input("ID", value=linguagem_to_edit[0], key="edit_linguagen")
            nome_linguagem = st.text_input("Linguagem", value=linguagem_to_edit[1], key="edit_parentesco")
    
            if st.button("Salvar Alterações"):
                update_linguagem(id_linguagem, nome_linguagem)
                st.success("Linguagem atualizada com sucesso!")
                del st.session_state.edit_id  
                st.rerun()


def programador_linguagem_crud_interface():
    st.title("Gerenciamento de Linguagens por Programador")

    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    if st.button("Adicionar nova Linguagem por Programador"):
        st.session_state.show_insert_form = True

    if st.session_state.show_insert_form:
        st.subheader("Adicionar Linguagem por Programador")

        # Obtendo programadores e linguagens
        programadores = get_programadores()  # Supondo que retorna uma lista de (id, nome)
        linguagens = get_linguagens()  # Supondo que retorna uma lista de (id, nome)

        # Criando opções de seleção
        programador_options = {f"{p[0]} - {p[1]}": p[0] for p in programadores}
        linguagem_options = {f"{l[0]} - {l[1]}": l[0] for l in linguagens}

        # Selectbox para escolher programador e linguagem
        programador_choice = st.selectbox("Programador", list(programador_options.keys()), key="select_programador")
        id_programador = programador_options[programador_choice]  # Obtém o ID real

        linguagem_choice = st.selectbox("Linguagem", list(linguagem_options.keys()), key="select_linguagem")
        id_linguagem = linguagem_options[linguagem_choice]  # Obtém o ID real

        if st.button("Salvar"):
            insert_programador_linguagem(id_programador, id_linguagem)
            st.success("Linguagem adicionada a um programador com sucesso!")
            st.rerun()

    st.subheader("Lista de Linguagens por Programador")
    programador_linguagem = get_programador_linguagens()

    if programador_linguagem:
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.write("**ID Programador**")
        with col2:
            st.write("**ID Linguagem**")
        with col3:
            st.write("**Ações**")

        for lp in programador_linguagem:
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(lp[0])
            with col2:
                st.write(lp[1]) 
            with col3:
                if st.button("Deletar", key=f"delete_{lp[0]}_{lp[1]}"):
                    delete_programador_linguagem(lp[0], lp[1])
                    st.success(f"Relação {lp[0]}-{lp[1]} deletada com sucesso!")
                    st.rerun()


# Função para calcular a idade a partir da data de nascimento
def calcular_idade(data_nasc):
    hoje = datetime.today()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

# Função para a interface de gráficos dinâmicos
def graficos_interface():
    st.title("Gráficos Dinâmicos")

    # Dados dos programadores
    programadores = get_programadores()
    df_programadores = pd.DataFrame(programadores, columns=["id_programador", "nome_programador", "genero", "data_nasc", "id_startup"])
    
    # Calcular a idade dos programadores
    df_programadores['data_nasc'] = pd.to_datetime(df_programadores['data_nasc'])
    df_programadores['idade'] = df_programadores['data_nasc'].apply(calcular_idade)
    
    # Dados das linguagens
    programador_linguagens = get_programador_linguagens()
    df_programador_linguagens = pd.DataFrame(programador_linguagens, columns=["id_programador", "id_linguagem"])
    linguagens = get_linguagens()
    df_linguagens = pd.DataFrame(linguagens, columns=["id_linguagem", "nome_linguagem"])
    df_merged = pd.merge(df_programador_linguagens, df_linguagens, on="id_linguagem")
    
    # Dados das startups
    startups = get_startups()
    df_startups = pd.DataFrame(startups, columns=["id_startup", "nome_startup", "cidade_sede"])
    df_programadores_startup = pd.merge(df_programadores, df_startups, on="id_startup")

    # Gráfico 1: Distribuição de Programadores por Gênero (Gráfico de Barras)
    st.subheader("Distribuição de Programadores por Gênero")
    genero_count = df_programadores['genero'].value_counts().reset_index()
    genero_count.columns = ['Genero', 'Quantidade']
    fig1 = px.bar(genero_count, x='Genero', y='Quantidade', title="Distribuição de Programadores por Gênero")
    st.plotly_chart(fig1)

    # Gráfico 2: Linguagens mais utilizadas pelos Programadores (Gráfico de Pizza)
    st.subheader("Linguagens mais utilizadas pelos Programadores")
    linguagem_count = df_merged['nome_linguagem'].value_counts().reset_index()
    linguagem_count.columns = ['Linguagem', 'Quantidade']
    fig2 = px.pie(linguagem_count, values='Quantidade', names='Linguagem', title="Linguagens mais utilizadas pelos Programadores")
    st.plotly_chart(fig2)

    # Gráfico 3: Distribuição de Programadores por Startup (Gráfico de Barras)
    st.subheader("Distribuição de Programadores por Startup")
    startup_count = df_programadores_startup['nome_startup'].value_counts().reset_index()
    startup_count.columns = ['Startup', 'Quantidade']
    fig3 = px.bar(startup_count, x='Startup', y='Quantidade', title="Distribuição de Programadores por Startup")
    st.plotly_chart(fig3)

    # Gráfico 4: Idade dos Programadores (Histograma)
    st.subheader("Distribuição de Idade dos Programadores")
    fig4 = px.histogram(df_programadores, x='idade', nbins=10, title="Distribuição de Idade dos Programadores")
    st.plotly_chart(fig4)

    # Gráfico 5: Relação entre Idade e Linguagem (Gráfico de Dispersão)
    st.subheader("Relação entre Idade e Linguagem")
    df_programadores_linguagens = pd.merge(df_programadores, df_merged, on="id_programador")
    fig5 = px.scatter(df_programadores_linguagens, x='idade', y='nome_linguagem', color='genero', title="Relação entre Idade e Linguagem")
    st.plotly_chart(fig5)

    # Gráfico 6: Mapa de Calor de Programadores por Cidade e Linguagem
    st.subheader("Mapa de Calor: Programadores por Cidade e Linguagem")
    df_cidade_linguagem = df_programadores_startup.merge(df_programadores_linguagens, on="id_programador")
    heatmap_data = df_cidade_linguagem.groupby(['cidade_sede', 'nome_linguagem']).size().unstack().fillna(0)
    fig6 = px.imshow(heatmap_data, labels=dict(x="Linguagem", y="Cidade", color="Quantidade"), title="Programadores por Cidade e Linguagem")
    st.plotly_chart(fig6)

    # Gráfico 7: Quantidade de Dependentes por Programador (Gráfico de Barras)
    st.subheader("Quantidade de Dependentes por Programador")
    dependentes = get_dependentes()
    df_dependentes = pd.DataFrame(dependentes, columns=["id_dependente", "nome_dependente", "parentesco", "data_nasc", "id_programador"])
    dependentes_count = df_dependentes.groupby('id_programador').size().reset_index(name='Quantidade')
    dependentes_count = dependentes_count.merge(df_programadores[['id_programador', 'nome_programador']], on="id_programador")
    fig7 = px.bar(dependentes_count, x='nome_programador', y='Quantidade', title="Quantidade de Dependentes por Programador")
    st.plotly_chart(fig7)

# Função principal
def main():
    # Menu Lateral
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio(
        "Escolha uma opção",
        ["Gerenciamento de Tabelas", "Gráficos"]
    )

    if menu_option == "Gerenciamento de Tabelas":
        # Menu Tabelas do banco
        option = st.sidebar.selectbox("Escolha a tabela", ["Startups", "Programadores", "Dependentes", "Linguagens", "Programador_Linguagem"])
        
        if option == "Startups":
            startup_crud_interface()
        elif option == "Programadores":
            programadores_crud_interface()
        elif option == "Dependentes":
            dependentes_crud_interface()
        elif option == "Linguagens":
            linguagens_crud_interface()
        elif option == "Programador_Linguagem":
            programador_linguagem_crud_interface()
    elif menu_option == "Gráficos":
        graficos_interface()

if __name__ == "__main__":
    main()