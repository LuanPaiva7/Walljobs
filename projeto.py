import streamlit as st
import pandas as pd
import os

# Funções para manipulação da planilha
def carregar_planilha():
    if os.path.exists('produtos.xlsx'):
        return pd.read_excel('produtos.xlsx', engine='openpyxl')
    else:
        return pd.DataFrame(columns=['nomeproduto', 'codigoproduto', 'preco', 'descricao'])

def salvar_planilha(df):
    df.to_excel('produtos.xlsx', index=False, engine='openpyxl')
    
def adicionar_produto(nomeproduto, codigoproduto, preco, descricao):
    df = carregar_planilha()
    novo_produto = pd.DataFrame([{
        'nomeproduto': nomeproduto,
        'codigoproduto': codigoproduto,
        'preco': preco,
        'descricao': descricao
    }])
    df = pd.concat([df, novo_produto], ignore_index=True)
    salvar_planilha(df)

def editar_produto(index, nomeproduto, codigoproduto, preco, descricao):
    df = carregar_planilha()
    df.at[index, 'nomeproduto'] = nomeproduto
    df.at[index, 'codigoproduto'] = codigoproduto
    df.at[index, 'preco'] = preco
    df.at[index, 'descricao'] = descricao
    salvar_planilha(df)

def deletar_produto(index):
    df = carregar_planilha()
    df = df.drop(index)
    salvar_planilha(df)

# Interface do usuário
st.title('Cadastro de Produtos')

with st.form(key="inclui_produto"):
    input_nomeproduto = st.text_input("Insira o nome do produto")
    input_codigoproduto = st.text_input("Insira o código do produto")
    input_preco = st.number_input("Insira o preço do produto")
    input_descricao = st.selectbox("Insira a descrição", ['Novo', 'Velho', 'Usado', 'Reforma'])
    input_button_submit = st.form_submit_button("Gravar")

if input_button_submit:
    adicionar_produto(input_nomeproduto, input_codigoproduto, input_preco, input_descricao)
    st.success("Produto gravado")

st.subheader("Produtos Cadastrados") 

df = carregar_planilha()
if not df.empty:
    st.dataframe(df)

    indices = df.index.tolist()
    produto_selecionado = st.selectbox('Selecione o produto para editar ou deletar', options=indices, format_func=lambda x: df.at[x, 'nomeproduto'])

    if produto_selecionado is not None:
        with st.form(key="edit_delete_form"):
            novo_nomeproduto = st.text_input("Editar nome do produto:", value=df.at[produto_selecionado, 'nomeproduto'])
            novo_codigoproduto = st.text_input("Editar código do produto:", value=df.at[produto_selecionado, 'codigoproduto'])
            novo_preco = st.number_input("Editar preço do produto:", value=df.at[produto_selecionado, 'preco'])
            nova_descricao = st.selectbox("Editar descrição", ['Novo', 'Velho', 'Usado', 'Reforma'], index=['Novo', 'Velho', 'Usado', 'Reforma'].index(df.at[produto_selecionado, 'descricao']))

            editar_button_submit = st.form_submit_button("Salvar Edição")
            deletar_button_submit = st.form_submit_button("Deletar Produto")

        if editar_button_submit:
            editar_produto(produto_selecionado, novo_nomeproduto, novo_codigoproduto, novo_preco, nova_descricao)
            st.success("Produto editado")
            st.experimental_rerun()

        if deletar_button_submit:
            deletar_produto(produto_selecionado)
            st.success("Produto deletado")
            st.experimental_rerun()

else:
    st.write("Nenhum produto cadastrado ainda")
