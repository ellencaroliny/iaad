import streamlit as st
import plotly.express as px
import pandas as pd
import time
from datetime import datetime, date
from connect_db import connect_to_db
from consultas import *



def startup_crud_interface():
    st.title("Gerenciamento de Startups")

    # Inicializa estados de exibição dos formulários
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False
    if "show_delete_form" not in st.session_state:
        st.session_state.show_delete_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False

    # Botões lado a lado
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Adicionar Startup"):
            st.session_state.show_insert_form = True
            st.session_state.show_edit_form = False
            st.session_state.show_delete_form = False

    with col2:
        if st.button("Editar Startup"):
            st.session_state.show_edit_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_delete_form = False

    with col3:
        if st.button("Deletar Startup"):
            st.session_state.show_delete_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_edit_form = False

    # Obter IDs existentes para validação
    startups = get_startups()
    existing_ids = {s[0] for s in startups}  # Conjunto de IDs existentes
    cidades_existentes = get_cidades()

    # Formulário de Adicionar Startup
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Startup")

        col_id, col_nome = st.columns([1, 3])
        with col_id:
            id_startup = st.number_input("ID", min_value=1, key="add_id")
            if id_startup in existing_ids:
                st.error("❌ Este ID já está em uso. Escolha outro.")

        with col_nome:
            nome_startup = st.text_input("Nome da Startup", key="add_nome")

        usar_nova_cidade = st.checkbox("Cadastrar nova cidade", key="add_nova_cidade_check")

        if usar_nova_cidade:
            cidade_sede = st.text_input("Nova Cidade", key="add_cidade_nova")
        else:
            cidade_sede = st.selectbox("Cidade Existente", cidades_existentes, key="add_cidade_select")

        if st.button("Salvar") and id_startup not in existing_ids:
            insert_startup(id_startup, nome_startup, cidade_sede)
            st.success("✅ Startup adicionada!")
            st.session_state.show_insert_form = False
            time.sleep(1)
            st.rerun()

    # Formulário de Editar Startup
    if st.session_state.show_edit_form:
        st.subheader("Editar Startup")

        if startups:
            col_id, col_nome = st.columns([1, 3])
            with col_id:
                startup_ids = [s[0] for s in startups]
                selected_edit_id = st.selectbox("Startup para editar", startup_ids, key="edit_select")
                startup_to_edit = next((s for s in startups if s[0] == selected_edit_id), None)

            with col_nome:
                nome_startup = st.text_input("Nome da Startup", value=startup_to_edit[1], key="edit_nome")

            usar_nova_cidade = st.checkbox("Cadastrar nova cidade", key="edit_nova_cidade_check")

            if usar_nova_cidade:
                cidade_sede = st.text_input("Nova Cidade", key="edit_cidade_nova")
            else:
                cidade_index = cidades_existentes.index(startup_to_edit[2]) if startup_to_edit[2] in cidades_existentes else 0
                cidade_sede = st.selectbox("Cidade Existente", cidades_existentes, index=cidade_index, key="edit_cidade_select")

            if st.button("Salvar Alterações"):
                update_startup(selected_edit_id, nome_startup, cidade_sede)
                st.success("✅ Startup atualizada!")
                st.session_state.show_edit_form = False
                time.sleep(1)
                st.rerun()

    # Formulário de Deletar Startup
    if st.session_state.show_delete_form:
        st.subheader("Excluir Startup")

        if startups:
            startup_ids = [s[0] for s in startups]
            selected_delete_id = st.selectbox("Selecione a Startup para excluir", startup_ids, key="delete_select")

            startup_to_delete = next((s for s in startups if s[0] == selected_delete_id), None)

            if startup_to_delete:
                st.write("### Confirme a exclusão:")
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.write("**ID**")
                    st.write(startup_to_delete[0])
                with col2:
                    st.write("**Nome**")
                    st.write(startup_to_delete[1])
                with col3:
                    st.write("**Cidade**")
                    st.write(startup_to_delete[2])

            if st.button("Excluir"):
                delete_startup(selected_delete_id)
                st.success(f"✅ Startup {selected_delete_id} foi deletada!")
                st.session_state.show_delete_form = False
                time.sleep(1)
                st.rerun()

    # Exibir lista de startups (somente se não estiver na aba de deletar)
    if not st.session_state.show_delete_form:
        st.subheader("Lista de Startups")

        if startups:
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                st.write("**ID**")
            with col2:
                st.write("**Nome**")
            with col3:
                st.write("**Cidade**")

            for startup in startups:
                col1, col2, col3 = st.columns([1, 2, 2])
                with col1:
                    st.write(startup[0])
                with col2:
                    st.write(startup[1])
                with col3:
                    st.write(startup[2])


def programadores_crud_interface():
    st.title("Gerenciamento de Programadores")
    
    # Inicializa estados de exibição dos formulários
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False
    if "show_delete_form" not in st.session_state:
        st.session_state.show_delete_form = False

    # Obter a lista de startups para o selectbox
    startups = get_startups()
    startup_options = {startup[1]: startup[0] for startup in startups}  # Mapeia nome_startup para id_startup
    
    # Botões lado a lado
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Adicionar Programador"):
            st.session_state.show_insert_form = True
            st.session_state.show_edit_form = False
            st.session_state.show_delete_form = False

    with col2:
        if st.button("Editar Programador"):
            st.session_state.show_edit_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_delete_form = False

    with col3:
        if st.button("Deletar Programador"):
            st.session_state.show_delete_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_edit_form = False


    # Formulário de Adicionar Programador
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Programador")

        # Obtém IDs de programadores existentes para validar
        programadores = get_programadores()
        existing_ids = {p[0] for p in programadores}  # Conjunto de IDs existentes
        
        # Colunas para inserir o ID e nome
        col_id, col_nome = st.columns([1, 3])
        with col_id:
            id_programador = st.number_input("ID do Programador", min_value=1, key="add_id_programador")
            if id_programador in existing_ids:
                st.error("❌ Este ID já está em uso. Escolha outro.")

        with col_nome:
            nome_programador = st.text_input("Nome do Programador", key="add_nome")

        # Gênero como opção
        genero = st.selectbox(
            "Gênero",
            options=["Masculino (M)", "Feminino (F)"],
            key="add_genero"
        )
        genero = genero[-2]  # Extrai "M" ou "F" da string selecionada

        # Data de Nascimento com validação de idade
        data_nasc = st.date_input("Data de Nascimento", key="add_data_nasc")
        if data_nasc:
            if not eh_maior_de_idade(data_nasc):
                st.error("❌ O programador deve ter pelo menos 18 anos.")

        # ID da Startup como lista de opções
        startups = get_startups()  # Função que recupera as startups
        startup_options = {s[1]: s[0] for s in startups}  # Mapeamento de nome da startup para ID
        startup_options['NENHUMA STARTUP'] = 'NULL'
        print(startup_options)
        startup_selecionada = st.selectbox(
            "Startup",
            options=list(startup_options.keys()),  # Exibe os nomes das startups
            key="add_startup"
        )
        id_startup = startup_options[startup_selecionada]  # Obtém o ID da startup selecionada

        if st.button("Salvar") and id_programador not in existing_ids:
            if data_nasc and eh_maior_de_idade(data_nasc):
                try:
                    insert_programador(id_programador, nome_programador, genero, data_nasc, id_startup)
                    st.success("✅ Programador adicionado!")
                except Exception as e:
                    st.error(f'Cada programador deve estar vinculado a uma startup!')


    # Formulário de Editar Programador
    if st.session_state.show_edit_form:
        st.subheader("Editar Programador")

        programadores = get_programadores()
        if programadores:
            col_id, col_nome = st.columns([1, 3])  # Coluna do ID menor e Nome maior
            with col_id:
                programador_ids = [p[0] for p in programadores]
                selected_edit_id = st.selectbox("Programador para editar", programador_ids, key="edit_select")
                programador_to_edit = next((p for p in programadores if p[0] == selected_edit_id), None)

            with col_nome:
                nome_programador = st.text_input("Nome do Programador", value=programador_to_edit[1], key="edit_nome")

            # Gênero como opção
            genero = st.selectbox(
                "Gênero",
                options=["Masculino (M)", "Feminino (F)"],
                index=0 if programador_to_edit[2] == "M" else 1,  # Seleciona a opção correta
                key="edit_genero"
            )
            genero = genero[-2]  # Extrai "M" ou "F" da string selecionada

            # Data de Nascimento com validação de idade
            data_nasc = st.date_input("Data de Nascimento", value=programador_to_edit[3], key="edit_data_nasc")
            if data_nasc:
                if not eh_maior_de_idade(data_nasc):
                    st.error("❌ O programador deve ter pelo menos 18 anos.")

            # ID da Startup como lista de opções
            startup_selecionada = st.selectbox(
                "Startup",
                options=list(startup_options.keys()),  # Exibe os nomes das startups
                index=list(startup_options.values()).index(programador_to_edit[4]),  # Seleciona a startup correta
                key="edit_startup"
            )
            id_startup = startup_options[startup_selecionada]  # Obtém o ID da startup selecionada

            if st.button("Salvar Alterações"):
                if data_nasc and eh_maior_de_idade(data_nasc):
                    update_programador(selected_edit_id, nome_programador, genero, data_nasc, id_startup)
                    st.success("✅ Programador atualizado!")
                    st.session_state.show_edit_form = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Não foi possível atualizar o programador. Verifique a data de nascimento.")



    # Formulário de Deletar Programador
    if st.session_state.show_delete_form:
        st.subheader("Excluir Programador")

        programadores = get_programadores()
        if programadores:
            # Se a lista de programadores estiver vazia, exibe uma mensagem e interrompe o código
            programador_ids = [p[0] for p in programadores]
            if len(programador_ids) == 0:
                st.warning("Não há programadores disponíveis para exclusão.")
            else:
                # Selecione um único programador para exclusão (não mostra a lista completa)
                selected_delete_id = st.selectbox("Selecione o Programador para excluir", programador_ids, key="delete_select")

                # Localiza o programador selecionado
                programador_to_delete = next((p for p in programadores if p[0] == selected_delete_id), None)

                if programador_to_delete:
                    st.write("### Confirme a exclusão:")
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                    with col1:
                        st.write("**ID**")
                        st.write(programador_to_delete[0])
                    with col2:
                        st.write("**Nome**")
                        st.write(programador_to_delete[1])
                    with col3:
                        st.write("**Gênero**")
                        st.write("Masculino" if programador_to_delete[2] == "M" else "Feminino")
                    with col4:
                        # Exibe a startup associada ao programador
                        startup_id = programador_to_delete[4]  # ID da startup
                        startup_nome = next((s[1] for s in startups if s[0] == startup_id), "Startup não encontrada")
                        st.write("**Startup**")
                        st.write(startup_nome)

                # Botão para confirmar a exclusão
                if st.button("Excluir"):
                    delete_programador(selected_delete_id)
                    st.success(f"✅ Programador {selected_delete_id} deletado!")
                    st.session_state.show_delete_form = False
                    time.sleep(1)
                    st.rerun()



    if not st.session_state.show_delete_form:
        # Exibir lista de programadores sem botões de editar ou deletar
        st.subheader("Lista de Programadores")
        programadores = get_programadores()

        if programadores:
            # Cabeçalho da tabela
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])
            with col1:
                st.write("**Id_programador**")
            with col2:
                st.write("**Nome**")
            with col3:
                st.write("**Genero**")
            with col4:
                st.write("**Data_Nascimento**")
            with col5:
                st.write("**Startup**") 
            # Corpo da tabela
            for programador in programadores:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])
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



def dependentes_crud_interface():
    st.title("Gerenciamento de Dependentes")

    # Inicializa estados de exibição dos formulários
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False
    if "show_delete_form" not in st.session_state:
        st.session_state.show_delete_form = False

    # Obter a lista de programadores para o selectbox
    programadores = get_programadores()
    programador_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in programadores}  # Mapeia nome_programador para id_programador

    # Botões lado a lado
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Adicionar Dependente"):
            st.session_state.show_insert_form = True
            st.session_state.show_edit_form = False
            st.session_state.show_delete_form = False

    with col2:
        if st.button("Editar Dependente"):
            st.session_state.show_edit_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_delete_form = False

    with col3:
        if st.button("Deletar Dependente"):
            st.session_state.show_delete_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_edit_form = False

    # Formulário de Adicionar Dependente
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Dependente")
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
            st.success("Dependente adicionado!")
            st.session_state.show_insert_form = False
            time.sleep(1)
            st.rerun()

    # Formulário de Editar Dependente
    if st.session_state.show_edit_form:
        st.subheader("Editar Dependente")

        # Seleção de Programador para listar seus dependentes
        programador_selecionado = st.selectbox(
            "Selecione um Programador",
            options=list(programador_options.keys()),
            key="edit_programador"
        )
        id_programador = programador_options[programador_selecionado]

        # Obter dependentes do programador selecionado
        dependentes = get_dependentes_por_programador(id_programador)
        if dependentes:
            # Criar uma lista de opções com os nomes dos dependentes
            dependente_options = [f"{d[1]} (ID: {d[0]})" for d in dependentes]
            selected_edit_option = st.selectbox("Dependente para editar", dependente_options, key="edit_select")

            # Extrair o ID do dependente selecionado a partir da opção escolhida
            selected_edit_id = int(selected_edit_option.split(" (ID: ")[1].replace(")", ""))

            dependente_to_edit = next((d for d in dependentes if d[0] == selected_edit_id), None)

            if dependente_to_edit:
                nome_dependente = st.text_input("Nome", value=dependente_to_edit[1], key="edit_nome")
                parentesco = st.text_input("Parentesco", value=dependente_to_edit[2], key="edit_parentesco")
                data_nasc = st.date_input("Data de Nascimento", value=dependente_to_edit[3], key="edit_data")

                if st.button("Salvar Alterações"):
                    update_dependente(dependente_to_edit[0], nome_dependente, parentesco, data_nasc, id_programador)
                    st.success("Dependente atualizado!")
                    st.session_state.show_edit_form = False
                    time.sleep(1)
                    st.rerun()


    # Formulário de Deletar Dependente
    if st.session_state.show_delete_form:
        st.subheader("Excluir Dependente")

        # Seleção de Programador para listar seus dependentes
        programador_selecionado = st.selectbox(
            "Selecione um Programador",
            options=list(programador_options.keys()),
            key="delete_programador"
        )
        id_programador = programador_options[programador_selecionado]

        # Obter dependentes do programador selecionado
        dependentes = get_dependentes_por_programador(id_programador)
        if dependentes:
            # Criar uma lista de opções com os nomes dos dependentes
            dependente_options = [f"{d[1]} (ID: {d[0]})" for d in dependentes]
            selected_delete_option = st.selectbox("Dependente para excluir", dependente_options, key="delete_select")

            # Extrair o ID do dependente selecionado a partir da opção escolhida
            selected_delete_id = int(selected_delete_option.split(" (ID: ")[1].replace(")", ""))

            dependente_to_delete = next((d for d in dependentes if d[0] == selected_delete_id), None)

            if dependente_to_delete:
                st.write(f"**Nome**: {dependente_to_delete[1]}")
                st.write(f"**Parentesco**: {dependente_to_delete[2]}")
                st.write(f"**Data de Nascimento**: {dependente_to_delete[3]}")

                if st.button("Excluir"):
                    delete_dependente(dependente_to_delete[0])
                    st.success(f"Dependente {dependente_to_delete[1]} excluído!")
                    st.session_state.show_delete_form = False
                    time.sleep(1)
                    st.rerun()


    # Exibir lista de dependentes (somente se não estiver na aba de deletar)
    if not st.session_state.show_delete_form and not st.session_state.show_edit_form:
        st.subheader("Lista de Dependentes")
        dependentes = get_dependentes()

        if dependentes:
            # Cabeçalho da tabela
            col1, col2, col3, col4= st.columns([1, 2, 2, 2])
            with col1:
                st.write("**Nome**")
            with col2:
                st.write("**Parentesco**")
            with col3:
                st.write("**Data Nascimento**")
            with col4:
                st.write("**Id Programador**")
            
            # Corpo da tabela
            for dependente in dependentes:
                col1, col2, col3, col4= st.columns([1, 2, 2, 2])
                with col1:
                    st.write(dependente[1])  # Nome do dependente
                with col2:
                    st.write(dependente[2])  # Parentesco
                with col3:
                    st.write(dependente[3])  # Data de Nascimento
                with col4:
                    st.write(dependente[4])  # ID do programador

    



def linguagens_crud_interface():
    st.title("Gerenciamento de Linguagens")

    # Inicializa estados de exibição dos formulários
    if "show_insert_form" not in st.session_state:
        st.session_state.show_insert_form = False
    if "show_delete_form" not in st.session_state:
        st.session_state.show_delete_form = False
    if "show_edit_form" not in st.session_state:
        st.session_state.show_edit_form = False

    # Botões lado a lado para Adicionar, Editar e Deletar
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Adicionar"):
            st.session_state.show_insert_form = True
            st.session_state.show_edit_form = False
            st.session_state.show_delete_form = False

    with col2:
        if st.button("Editar"):
            st.session_state.show_edit_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_delete_form = False

    with col3:
        if st.button("Deletar"):
            st.session_state.show_delete_form = True
            st.session_state.show_insert_form = False
            st.session_state.show_edit_form = False

    # Obter linguagens e validar IDs existentes
    linguagens = get_linguagens()
    existing_ids = {l[0] for l in linguagens}  # Conjunto de IDs existentes

    # Formulário de Adicionar Linguagem
    if st.session_state.show_insert_form:
        st.subheader("Adicionar Linguagem")

        col_id, col_nome = st.columns([1, 3])
        with col_id:
            id_linguagem = st.number_input("ID da Linguagem", min_value=1, key="add_id")
            if id_linguagem in existing_ids:
                st.error("❌ Este ID já está em uso. Escolha outro.")

        with col_nome:
            nome_linguagem = st.text_input("Nome", key="nome_linguagem")

        if st.button("Salvar") and id_linguagem not in existing_ids:
            insert_linguagem(id_linguagem, nome_linguagem)
            st.success("✅ Linguagem adicionada!")
            st.session_state.show_insert_form = False
            time.sleep(1)
            st.rerun()

    # Formulário de Editar Linguagem
    if st.session_state.show_edit_form:
        st.subheader("Editar Linguagem")

        if linguagens:
            col_id, col_nome = st.columns([1, 3])
            with col_id:
                linguagem_ids = [l[0] for l in linguagens]
                selected_edit_id = st.selectbox("Selecione a Linguagem", linguagem_ids, key="edit_select")
                linguagem_to_edit = next((l for l in linguagens if l[0] == selected_edit_id), None)

            with col_nome:
                nome_linguagem = st.text_input("Nome", value=linguagem_to_edit[1], key="edit_nome_linguagem")

            if st.button("Salvar Alterações"):
                update_linguagem(selected_edit_id, nome_linguagem)
                st.success("✅ Linguagem atualizada!")
                st.session_state.show_edit_form = False
                time.sleep(1)
                st.rerun()

    # Formulário de Deletar Linguagem
    if st.session_state.show_delete_form:
        st.subheader("Excluir Linguagem")

        if linguagens:
            linguagem_ids = [l[0] for l in linguagens]
            selected_delete_id = st.selectbox("Selecione a Linguagem", linguagem_ids, key="delete_select")

            linguagem_to_delete = next((l for l in linguagens if l[0] == selected_delete_id), None)

            if linguagem_to_delete:
                st.write("### Confirme a exclusão:")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write("**ID**")
                    st.write(linguagem_to_delete[0])
                with col2:
                    st.write("**Nome**")
                    st.write(linguagem_to_delete[1])

            if st.button("Excluir"):
                delete_linguagem(selected_delete_id)
                st.success(f"✅ Linguagem {selected_delete_id} deletada!")
                st.session_state.show_delete_form = False
                time.sleep(1)
                st.rerun()

    # Exibir lista de linguagens (somente se não estiver na aba de deletar)
    if not st.session_state.show_delete_form:
        st.subheader("Lista de Linguagens")

        if linguagens:
            col1, col2 = st.columns([2, 2])
            with col1:
                st.write("**ID**")
            with col2:
                st.write("**Nome**")

            for linguagem in linguagens:
                col1, col2 = st.columns([2, 2])
                with col1:
                    st.write(linguagem[0])
                with col2:
                    st.write(linguagem[1])



def programador_linguagem_crud_interface():
    st.title("Gerenciamento de Linguagens por Programador")

    # Obtendo programadores e linguagens
    programadores = get_programadores()  # Supondo que retorna uma lista de (id, nome)
    linguagens = get_linguagens()  # Supondo que retorna uma lista de (id, nome)

    if not programadores or not linguagens:
        st.warning("⚠️ Nenhum programador ou linguagem cadastrada!")
        return

    # Criando opções de seleção
    programador_options = {f"{p[0]} - {p[1]}": p[0] for p in programadores}
    linguagem_options = {f"{l[0]} - {l[1]}": l[0] for l in linguagens}

    # Selectbox para escolher programador e linguagem
    programador_choice = st.selectbox("Programador", list(programador_options.keys()), key="select_programador")
    id_programador = programador_options[programador_choice]

    linguagem_choice = st.selectbox("Linguagem", list(linguagem_options.keys()), key="select_linguagem")
    id_linguagem = linguagem_options[linguagem_choice]

    # Verificando se a relação já existe no banco de dados
    if verificar_relacionamento(id_programador, id_linguagem):
        st.error(f"⚠️ A relação entre  {programador_choice} e {linguagem_choice} já existe!")
    else:
        if st.button("Salvar"):
            insert_programador_linguagem(id_programador, id_linguagem)
            st.success(f"✅ Linguagem '{linguagem_choice}' adicionada ao programador '{programador_choice}'!")
            time.sleep(2)
            st.rerun()

    # Exibição da lista com as relações existentes
    st.subheader("Lista de Linguagens por Programador")
    programador_linguagem = get_programador_linguagens()

    if not programador_linguagem:
        st.info("📌 Nenhuma relação cadastrada.")
    else:
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
                if st.button("❌ Deletar", key=f"delete_{lp[0]}_{lp[1]}"):
                    delete_programador_linguagem(lp[0], lp[1])
                    st.success(f"✅ Relação {lp[0]}-{lp[1]} deletada!")
                    time.sleep(1)
                    st.rerun()

def verificar_relacionamento(id_programador, id_linguagem):
    # Função que verifica se a relação entre o programador e a linguagem já existe no banco de dados
    # Retorne True se a relação existir, False caso contrário
    relacionamento = buscar_relacionamento(id_programador, id_linguagem)
    return bool(relacionamento)

# Função para calcular a idade a partir da data de nascimento
def calcular_idade(data_nasc):
    hoje = datetime.today()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

def calcular_idade(data_nasc):
    hoje = date.today()
    idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    return idade

def eh_maior_de_idade(data_nasc):
    return calcular_idade(data_nasc) >= 18

# Tela de filtragem startups_cidades e programadores
def filtragem_interface():
    # Título da página
    st.title("Filtragem Personalizada no Banco de Dados")

    # Lista de opções
    opcoes = ["Startups", "Programadores"]

    # Exibir selectbox para seleção da tabela
    col1, col2 = st.columns([1, 1])
    
    with col1:
        opcao_selecionada = st.selectbox("Selecione uma opção", opcoes)

    # Se "Startups" for selecionado, exibir selectbox com as cidades e programadores
    if opcao_selecionada == "Startups":
        cidades = get_cidades()  # Função que retorna as cidades disponíveis
        
        with col2:
            cidade_selecionada = st.selectbox("Selecione uma cidade", cidades)

        # Buscar programadores da cidade selecionada
        programadores = get_programadores_por_cidade(cidade_selecionada)
        
        st.write(f"Programadores na cidade de {cidade_selecionada} e suas startups:")
        
        # Exibir dados dos programadores e suas startups
        if programadores:
            # Transformar os dados para DataFrame para visualização
            df_programadores = pd.DataFrame(programadores, columns=["Nome do Programador", "Gênero", "Data de Nascimento", "Nome da Startup"])
            st.dataframe(df_programadores)
        else:
            st.write("Nenhum programador encontrado nesta cidade.")

    # Se "Programadores" for selecionado, exibir todos os programadores e suas startups
    if opcao_selecionada == "Programadores":
        programadores = get_programadores()  # Função que retorna todos os programadores
        
        st.write("Programadores disponíveis:")

        if programadores:
            # Calcular idade para cada programador
            programadores_com_idade = []
            for p in programadores:
                idade = calcular_idade(p[3])  # p[3] é a data de nascimento
                programadores_com_idade.append((*p, idade))  # Adiciona a idade ao tuple

            # Converter para DataFrame
            df_programadores = pd.DataFrame(programadores_com_idade, columns=["ID", "Nome", "Gênero", "Data de Nascimento", "ID Startup", "Idade"])

            # Filtros de idade
            idade_min, idade_max = st.slider("Filtrar por idade", 18, 100, (18, 100))

            # Filtragem
            df_programadores_filtrado = df_programadores[(df_programadores['Idade'] >= idade_min) & (df_programadores['Idade'] <= idade_max)]

            st.dataframe(df_programadores_filtrado)
        else:
            st.write("Nenhum programador encontrado.")
            
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
        ["Gerenciamento de Tabelas", "Gráficos", "Filtragem"]
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
    elif menu_option == "Filtragem":
        filtragem_interface()

if __name__ == "__main__":
    main()