import streamlit as st
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

    if st.button("Adicionar programador"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar programador")
        id_programador = st.number_input("ID do programador", min_value=1, key="add_id_programador")
        nome_programador = st.text_input("Nome do programador", key="add_nome")
        genero=st.text_input("Nome do programador", key="add_genero")
        data_nasc=st.text_input("Nome do programador", key="add_data_nasc")
        id_startup=st.text_input("Nome do programador", key="add_id_startup")
        
        if st.button("Salvar"):
            insert_startup(id_programador, nome_programador, genero, data_nasc, id_startup)
            st.success("Programador adicionado com sucesso!")
            st.rerun()  

    st.subheader("Lista de Startups")
    programadores = get_programadores()

    if programadores:
        # Cabeçalho da tabela
        col1, col2, col3, col4, col5, col6= st.columns([2, 2, 1, 2, 2, 4])
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
        for programador in  programadores:
            col1, col2, col3, col4, col5, col6= st.columns([2, 2, 1, 2, 2, 4])
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
                        st.success(f"Programador {programador[0]} deletada com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Programador")
        programador_to_edit = next((s for s in programadores if s[0] == st.session_state.edit_id), None)
        if programador_to_edit:
            id_programador = st.number_input("ID do programador", value=programador_to_edit[0], key="edit_id")
            nome_programador = st.text_input("Nome do programador",value=programador_to_edit[1], key="edit_nome")
            genero=st.text_input("Nome do programador",value=programador_to_edit[2], key="edit_genero")
            data_nasc=st.text_input("Nome do programador",value=programador_to_edit[3], key="edit_data_nasc")
            id_startup=st.text_input("Nome do programador",value=programador_to_edit[4], key="edit_id_startup")

            if st.button("Salvar Alterações"):
                update_programador(id_programador, nome_programador, genero, data_nasc, id_startup)
                st.success("Programador atualizado com sucesso!")
                del st.session_state.edit_id  
                st.rerun()

def dependentes_crud_interface():
    st.title("Gerenciamento de Dependentes")

    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    if st.button("Adicionar novo dependente"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar dependente")
        nome_dependente = st.text_input("Nome", key="add_dependente")
        parentesco = st.text_input("Parentesco", key="add_parentesco")
        data_nasc = st.text_input("Data_nascimento", key="add_data")
        id_programador = st.number_input("id_programador", key="add_id")
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
            st.write("**Data_Nacimento**")
        with col4:
            st.write("**Id_programador**")
        with col5:
            st.write("**Ações**")
        # Corpo da tabela
        for dependente in dependentes:
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 4])
            with col1:
                st.write(dependente[1]) # Por que a coluna[0] é o id do dependente
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
                        st.success(f"dependente {dependente[0]} deletada com sucesso!")
                        st.rerun()
    # Editar
    if "edit_id" in st.session_state:
        st.subheader("Editar Dependente")
        dependente_to_edit = next((s for s in dependentes if s[0] == st.session_state.edit_id), None)
        if dependente_to_edit:
            nome_dependente = st.text_input("Nome", value=dependente_to_edit[0], key="edit_dependente")
            parentesco = st.text_input("Parentesco", value=dependente_to_edit[1], key="edit_parentesco")
            data_nasc = st.text_input("Data_nascimento", value=dependente_to_edit[2], key="edit_data")
            id_programador = st.number_input("id_programador", value=dependente_to_edit[3], key="edit_id")
            if st.button("Salvar Alterações"):
                update_dependente(nome_dependente, parentesco, data_nasc, id_programador)
                st.success("Startup atualizada com sucesso!")
                del st.session_state.edit_id  
                st.experimental_rerun() 


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
            insert_dependente(id_linguagem, nome_linguagem)
            st.success("Linguagem adicionada com sucesso!")
            st.experimental_rerun()  

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
                        st.experimental_rerun()
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
    st.title("Gerenciamento de Linguagens por programador")

    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False

    if st.button("Adicionar nova Linguagem por programador"):
        st.session_state.show_insert_form = True
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Linguagem por programador")
        id_programador=st.number_input("ID do programador",  key="add_id_programador", step=1)
        id_linguagem=st.number_input("ID da linguagem",  key="add_id+linguagem", step=1)
        
        if st.button("Salvar"):
            insert_programador_linguagem(id_programador, id_linguagem)
            st.success("Linguagem adicionada a um programador com sucesso!")
            st.rerun()

    st.subheader("Lista de linguagens por programador")
    programador_linguagem = get_programador_linguagens()

    if programador_linguagem:
        # Cabeçalho da tabela
        col1, col2, col3, = st.columns([1, 2, 2])
        with col1:
            st.write("**ID_programador**")
        with col2:
            st.write("**ID_linguagem**")
        with col3:
            st.write("**Ações**")
        # Corpo da tabela
        for lp in programador_linguagem:
            col1, col2, col3, = st.columns([1, 2, 2])
            with col1:
                st.write(lp[0])
            with col2:
                st.write(lp[1]) 
            with col3:
                if st.button("Deletar", key=f"delete_{lp[0]}_{lp[1]}"):
                    delete_programador_linguagem(lp[0], lp[1])
                    st.success(f"Relação {lp[0]}-{lp[1]} deletada com sucesso!")
    



# Rodar no stremlit
def main():

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

if __name__ == "__main__":
    main()