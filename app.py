import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuração da página do Streamlit para layout expandido (wide)
st.set_page_config(layout="wide", page_title="Dashboard de Gráficos - Atividade 06")

# Configurações visuais dos gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]

# --- SIDEBAR (Informações do Aluno) ---
with st.sidebar:
    st.header("👤 Informações do Aluno")
    # Substitua as strings vazias pelos seus dados reais
    nome_aluno = st.text_input("Nome:", value="Seu Nome Completo")
    num_chamada = st.text_input("Número da Chamada:", value="00")
    turma_aluno = st.text_input("Turma:", value="Sua Turma (Ex: 3º DSA)")
    
    st.markdown("---")
    st.caption("Recolha este menu na seta acima para expandir a visão dos gráficos.")

# --- TÍTULO PRINCIPAL ---
st.title("📊 Dashboard Analítico - Atividade 06")
st.markdown("Visualização integrada e análise automatizada dos conjuntos de dados mapeados.")

# Caminho da pasta que contém os CSVs
pasta_dados = "dados"

# Validação da pasta de dados
if not os.path.exists(pasta_dados):
    st.error(f"Erro: A pasta '{pasta_dados}' não foi encontrada no diretório atual.")
    st.stop()

# Listar e ordenar todos os arquivos CSV na pasta
arquivos = sorted([f for f in os.listdir(pasta_dados) if f.endswith('.csv')])

if not arquivos:
    st.warning("Nenhum arquivo .csv encontrado na pasta 'dados'.")
    st.stop()

# Lista para armazenar as funções de plotagem geradas dinamicamente
plots_para_exibir = []

# Processamento dos arquivos em memória
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_dados, arquivo)
    
    try:
        df = pd.read_csv(caminho_arquivo, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(caminho_arquivo, encoding='latin1')
        
    colunas = list(df.columns)
    
    # Dicionário para encapsular o gráfico e seu texto de análise padrão correspondente
    plot_info = {"titulo": arquivo, "render_func": None, "analise": ""}

    # 1. Gráfico de Vendas por Categoria e Região
    if 'categoria' in colunas and 'regiao' in colunas:
        def plot_1(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.barplot(data=data, x='categoria', y='vendas_medias', hue='regiao', palette='tab10', ax=ax)
            ax.set_title(f'Vendas Médias por Categoria e Região\n({arq})')
            ax.set_xlabel('Categoria')
            ax.set_ylabel('Vendas Médias')
            return fig
        plot_info["render_func"] = plot_1
        plot_info["analise"] = "**Análise:** Este gráfico de barras segmentado permite identificar quais categorias performam melhor em regiões específicas, destacando disparidades regionais de consumo."

    # 2. Distribuição de Salários por Departamento
    elif 'departamento' in colunas and 'salario' in colunas:
        def plot_2(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.boxplot(data=data, x='departamento', y='salario', palette='Set2', ax=ax)
            ax.set_title(f'Distribuição Salarial por Departamento\n({arq})')
            ax.set_xlabel('Departamento')
            ax.set_ylabel('Salário')
            return fig
        plot_info["render_func"] = plot_2
        plot_info["analise"] = "**Análise:** O diagrama de caixa (boxplot) evidencia a dispersão salarial, assimetrias e a presença de potenciais *outliers* (salários muito discrepantes) entre os setores."

    # 3. Dispersão de Altura vs Peso por Sexo
    elif 'altura_cm' in colunas and 'peso_kg' in colunas:
        def plot_3(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x='altura_cm', y='peso_kg', hue='sexo', alpha=0.7, palette='Set1', ax=ax)
            ax.set_title(f'Relação de Altura vs Peso\n({arq})')
            ax.set_xlabel('Altura (cm)')
            ax.set_ylabel('Peso (kg)')
            return fig
        plot_info["render_func"] = plot_3
        plot_info["analise"] = "**Análise:** O gráfico de dispersão demonstra graficamente a correlação positiva esperada entre altura e peso, segregada por agrupamento biológico."

    # 4. Distribuição de Idades (Histograma)
    elif 'idade' in colunas:
        def plot_4(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.histplot(data=data, x='idade', bins=15, kde=True, color='purple', ax=ax)
            ax.set_title(f'Distribuição de Idade\n({arq})')
            ax.set_xlabel('Idade')
            ax.set_ylabel('Frequência')
            return fig
        plot_info["render_func"] = plot_4
        plot_info["analise"] = "**Análise:** O histograma acompanhado da curva de densidade (KDE) revela a faixa etária predominante da amostra e a concentração dos dados amostrais."

    # 5. Volume de Chamados por Tipo de Atendimento
    elif 'tipo_atendimento' in colunas:
        def plot_5(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.countplot(data=data, y='tipo_atendimento', order=data['tipo_atendimento'].value_counts().index, palette='viridis', ax=ax)
            ax.set_title(f'Volume por Tipo de Atendimento\n({arq})')
            ax.set_xlabel('Quantidade')
            ax.set_ylabel('Tipo de Atendimento')
            return fig
        plot_info["render_func"] = plot_5
        plot_info["analise"] = "**Análise:** A visualização em barras horizontais ordena de forma decrescente as demandas mais recorrentes na central de atendimento, ideal para priorizar melhorias."

    # 6. Heatmap de Movimento por Dia e Horário
    elif 'dia_semana' in colunas and 'horario' in colunas:
        def plot_6(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            pivot_df = data.pivot(index='dia_semana', columns='horario', values='movimento_clientes')
            dias_ordem = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            pivot_df = pivot_df.reindex([d for d in dias_ordem if d in pivot_df.index])
            sns.heatmap(pivot_df, annot=True, fmt="g", cmap="YlGnBu", ax=ax)
            ax.set_title(f'Mapa de Calor de Movimento\n({arq})')
            ax.set_xlabel('Horário')
            ax.set_ylabel('Dia da Semana')
            return fig
        plot_info["render_func"] = plot_6
        plot_info["analise"] = "**Análise:** O mapa de calor aponta visualmente os horários e dias de pico ('ponto quente'). É um recurso crítico para planejamento de escala de equipes e recursos."

    # 7. Série Temporal de Vendas por Loja
    elif 'data' in colunas and 'vendas' in colunas:
        def plot_7(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            data['data'] = pd.to_datetime(data['data'])
            sns.lineplot(data=data, x='data', y='vendas', hue='loja', marker='o', ax=ax)
            ax.set_title(f'Evolução de Vendas por Loja\n({arq})')
            ax.set_xlabel('Data')
            ax.set_ylabel('Vendas')
            plt.xticks(rotation=45)
            return fig
        plot_info["render_func"] = plot_7
        plot_info["analise"] = "**Análise:** O gráfico de linhas temporal traça a tendência histórica do faturamento, auxiliando na identificação de sazonalidades ou padrões de crescimento entre filiais."

    # 8. Faturamento por Canal de Venda
    elif 'canal_venda' in colunas and 'faturamento' in colunas:
        def plot_8(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            df_sorted = data.sort_values('faturamento', ascending=False)
            sns.barplot(data=df_sorted, x='faturamento', y='canal_venda', palette='Blues_r', ax=ax)
            ax.set_title(f'Faturamento Total por Canal\n({arq})')
            ax.set_xlabel('Faturamento')
            ax.set_ylabel('Canal de Venda')
            return fig
        plot_info["render_func"] = plot_8
        plot_info["analise"] = "**Análise:** Apresenta a relevância financeira de cada canal de venda no faturamento total bruto, explicitando quais meios geram maior receita para a organização."

    # 9. Tendência de Renda vs Gasto Mensal
    elif 'renda_mensal' in colunas and 'gasto_mensal' in colunas:
        def plot_9(data=df, arq=arquivo):
            fig, ax = plt.subplots()
            sns.regplot(data=data, x='renda_mensal', y='gasto_mensal', scatter_kws={'alpha':0.6}, line_kws={'color':'red'}, ax=ax)
            ax.set_title(f'Correlação Renda vs Gasto Mensal\n({arq})')
            ax.set_xlabel('Renda Mensal')
            ax.set_ylabel('Gasto Mensal')
            return fig
        plot_info["render_func"] = plot_9
        plot_info["analise"] = "**Análise:** A linha de regressão linear vermelha explicita o comportamento de consumo à medida que a renda se eleva, validando teorias econômicas básicas de comportamento do consumidor."

    if plot_info["render_func"] is not None:
        plots_para_exibir.append(plot_info)

# --- REQUISITO: EXIBIÇÃO TRÊS A TRÊS COM ANÁLISE ABAIXO ---
# Loop que avança de 3 em 3 elementos
for i in range(0, len(plots_para_exibir), 3):
    bloco_atual = plots_para_exibir[i:i+3]
    
    # Cria dinamicamente 3 colunas lado a lado
    cols = st.columns(3)
    
    # Loop interno para renderizar os gráficos nas respectivas colunas
    for idx, item in enumerate(bloco_atual):
        with cols[idx]:
            figura = item["render_func"]()
            st.pyplot(figura)
            plt.close(figura) # Libera memória do backend do matplotlib

    # Cria uma linha abaixo das figuras para apresentar os textos explicativos integrados
    cols_analise = st.columns(3)
    for idx, item in enumerate(bloco_atual):
        with cols_analise[idx]:
            st.markdown(item["analise"])
            
    st.markdown("---")  # Divisor visual entre as linhas do Dashboard
