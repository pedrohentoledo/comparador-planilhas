import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Comparador de Planilhas Online",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Comparador de Planilhas Online")
st.markdown("Faça upload de duas planilhas e compare colunas! 🔍")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    ignorar_case = st.checkbox(
        "Ignorar maiúsculas/minúsculas", 
        value=True,
        help="Considera 'PEDRO' e 'pedro' como iguais"
    )
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Como usar:
    1. Faça upload de 2 planilhas
    2. Selecione as colunas  
    3. Clique em **Comparar Colunas**
    4. Veja os resultados!
    
    ### 📋 Formatos suportados:
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    """)
    
    st.markdown("---")
    st.markdown("🛠️ Desenvolvido com Streamlit")
    st.markdown("🔒 Seus dados não são salvos em servidores")

# Função melhorada para ler arquivos
def ler_arquivo(arquivo):
    try:
        if arquivo.name.lower().endswith('.csv'):
            # Tenta diferentes encodings para CSV
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    return pd.read_csv(arquivo, encoding=encoding, on_bad_lines='skip')
                except UnicodeDecodeError:
                    continue
            return pd.read_csv(arquivo, on_bad_lines='skip')  # Última tentativa
        else:
            return pd.read_excel(arquivo, engine='openpyxl')
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {str(e)}")
        return None

# Upload das planilhas
st.subheader("📁 Faça upload das planilhas")
col1, col2 = st.columns(2)

with col1:
    arquivo1 = st.file_uploader(
        "Selecione a primeira planilha",
        type=["xlsx", "xls", "csv"],
        key="file1"
    )

with col2:
    arquivo2 = st.file_uploader(
        "Selecione a segunda planilha", 
        type=["xlsx", "xls", "csv"],
        key="file2"
    )

# Processamento principal
if arquivo1 and arquivo2:
    with st.spinner("Processando arquivos..."):
        try:
            # Ler arquivos
            df1 = ler_arquivo(arquivo1)
            df2 = ler_arquivo(arquivo2)
            
            if df1 is not None and df2 is not None:
                st.success("✅ Arquivos carregados com sucesso!")
                
                # Visualização rápida
                exp_col1, exp_col2 = st.columns(2)
                with exp_col1:
                    with st.expander(f"📋 Visualizar {arquivo1.name}"):
                        st.dataframe(df1.head(3))
                with exp_col2:
                    with st.expander(f"📋 Visualizar {arquivo2.name}"):
                        st.dataframe(df2.head(3))
                
                # Seleção de colunas
                st.subheader("🎯 Selecione as colunas para comparar")
                col3, col4 = st.columns(2)
                
                with col3:
                    coluna1 = st.selectbox("Coluna da Planilha 1:", df1.columns, key="col1")
                
                with col4:
                    coluna2 = st.selectbox("Coluna da Planilha 2:", df2.columns, key="col2")
                
                # Botão de comparação
                if st.button("🔍 Comparar Colunas", type="primary", use_container_width=True):
                    with st.spinner("Comparando colunas..."):
                        # Processar valores
                        if ignorar_case:
                            valores1 = set(df1[coluna1].dropna().astype(str).str.strip().str.upper())
                            valores2 = set(df2[coluna2].dropna().astype(str).str.strip().str.upper())
                        else:
                            valores1 = set(df1[coluna1].dropna().astype(str).str.strip())
                            valores2 = set(df2[coluna2].dropna().astype(str).str.strip())
                        
                        # Calcular resultados
                        iguais = valores1.intersection(valores2)
                        apenas1 = valores1 - valores2
                        apenas2 = valores2 - valores1
                        
                        # Mostrar resultados
                        st.subheader("📈 Resultados da Comparação")
                        
                        # Métricas
                        col_met1, col_met2, col_met3 = st.columns(3)
                        with col_met1:
                            st.metric("✅ Em Comum", len(iguais))
                        with col_met2:
                            st.metric("❌ Só Planilha 1", len(apenas1))
                        with col_met3:
                            st.metric("❌ Só Planilha 2", len(apenas2))
                        
                        # Abas com detalhes
                        tab1, tab2, tab3 = st.tabs([
                            f"Valores em Comum ({len(iguais)})",
                            f"Só Planilha 1 ({len(apenas1)})", 
                            f"Só Planilha 2 ({len(apenas2)})"
                        ])
                        
                        with tab1:
                            if iguais:
                                st.write("**Valores encontrados em ambas as planilhas:**")
                                for valor in sorted(iguais):
                                    st.write(f"• {valor}")
                            else:
                                st.info("Nenhum valor em comum entre as colunas selecionadas.")
                        
                        with tab2:
                            if apenas1:
                                st.write("**Valores presentes apenas na Planilha 1:**")
                                for valor in sorted(apenas1):
                                    st.write(f"• {valor}")
                            else:
                                st.info("Nenhum valor exclusivo da Planilha 1.")
                        
                        with tab3:
                            if apenas2:
                                st.write("🔍 **Valores presentes apenas na Planilha 2:**")
                                for valor in sorted(apenas2):
                                    st.write(f"• {valor}")
                            else:
                                st.info("Nenhum valor exclusivo da Planilha 2.")
                        
                        # Estatísticas
                        with st.expander("📊 Estatísticas Detalhadas"):
                            st.write(f"**Configuração:** {'Ignorar maiúsculas/minúsculas' if ignorar_case else 'Diferenciar maiúsculas/minúsculas'}")
                            st.write(f"**Coluna da Planilha 1:** {coluna1}")
                            st.write(f"**Coluna da Planilha 2:** {coluna2}")
                            st.write(f"**Total de valores únicos na Planilha 1:** {len(valores1)}")
                            st.write(f"**Total de valores únicos na Planilha 2:** {len(valores2)}")
                            st.write(f"**Taxa de correspondência:** {len(iguais)/max(len(valores1), 1):.1%}")
            
            else:
                st.error("❌ Não foi possível ler os arquivos. Verifique se estão nos formatos suportados.")
                
        except Exception as e:
            st.error(f"❌ Ocorreu um erro durante o processamento: {str(e)}")

else:
    st.info("📝 Aguardando upload de duas planilhas para começar...")
    
    # Exemplo de uso
    with st.expander("🧪 Ver exemplo de uso"):
        st.markdown("""
        **Exemplo:**
        - Planilha 1: `clientes_janeiro.xlsx` com coluna **"Nome"**
        - Planilha 2: `clientes_fevereiro.csv` com coluna **"Cliente"**
        
        **Resultado:**
        - ✅ **Valores em comum:** Clientes que aparecem em ambas as planilhas
        - ❌ **Apenas Planilha 1:** Clientes que só estão na primeira planilha  
        - ❌ **Apenas Planilha 2:** Clientes que só estão na segunda planilha
        """)