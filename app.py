import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# --- Função para extrair UF pelo DDD ---
DDD_UF = {
    "11":"SP","12":"SP","13":"SP","14":"SP","15":"SP","16":"SP","17":"SP","18":"SP","19":"SP",
    "21":"RJ","22":"RJ","24":"RJ",
    "27":"ES","28":"ES",
    "31":"MG","32":"MG","33":"MG","34":"MG","35":"MG","37":"MG","38":"MG",
    "41":"PR","42":"PR","43":"PR","44":"PR","45":"PR","46":"PR",
    "47":"SC","48":"SC","49":"SC",
    "51":"RS","53":"RS","54":"RS","55":"RS",
    "61":"DF","62":"GO","63":"TO","64":"GO","65":"MT","66":"MT","67":"MS",
    "68":"AC","69":"RO",
    "71":"BA","73":"BA","74":"BA","75":"BA","77":"BA",
    "79":"SE",
    "81":"PE","82":"AL","83":"PB","84":"RN","85":"CE","86":"PI","87":"PE","88":"CE","89":"AL",
    "91":"PA","92":"AM","93":"PA","94":"PA","95":"RR","96":"AP","97":"AM","98":"MA","99":"MA"
}

def extrair_uf(telefone):
    if pd.isna(telefone) or len(str(telefone)) < 2:
        return ""
    ddd = str(telefone).replace("(","").replace(")","").replace(" ","").replace("-","")[:2]
    return DDD_UF.get(ddd, "")

# --- Lista de certificações válidas ---
CERTIFICACOES_VALIDAS = [
    "Aneps - Certificação Completa",
    "Aneps - Certificação Completa + Lgpd (Conforme Res 4935/21)",
    "Aneps - Certificação Crédito Consignado",
    "Aneps - Certificação Crédito Consignado + Lgpd (Conforme Res 4935/21)",
    "Aneps - Certificação Lgpd - Lei Geral De Proteção De Dados",
    "Aneps - Certificação Plus",
    "Aneps - Certificação Plus + Lgpd (Conforme Res 4935/21)",
    "ANEPS Certificacao Completa",
    "ANEPS Certificacao Completa LGPD Conforme Res 4935 21",
    "ANEPS Certificacao Credito Consignado",
    "ANEPS Certificacao Credito Consignado LGPD Conforme Res 4935 21",
    "ANEPS Certificacao LGPD Lei Geral de Protecao de Dados",
    "ANEPS Certificacao PLDFT Correspondente Bancarios e Cambiais",
    "ANEPS Certificacao Plus",
    "ANEPS Certificacao Plus LGPD Conforme Res 4935 21",
    "Certificação ANEC Completa + LGPD",
    "Certificação ANEC em Crédito Consignado + LGPD",
    "Certificação ANEC em Crédito Consignado PLUS + LGPD",
    "Certificação Completa De Correspondente - Res. 3.954/2011",
    "Certificação Completa De Correspondente - Res. 4.935 Bacen",
    "Certificacao Completa de Correspondente Res 3 954 2011",
    "Certificacao Completa de Correspondente Res 4 935 Bacen",
    "Certificação Completa Lgpd - Lei Geral De Proteção De Dados",
    "Certificacao Completa LGPD Lei Geral de Protecao de Dados",
    "Certificação Correspondente Bancário – Modalidade Transacional",
    "Certificacao Correspondente Bancario Modalidade Transacional",
    "CERTIFICAÇÃO CORRESPONDENTE NO PAÍS - MODALIDADE COMPLETA + LGPD - RES. CMN Nº 4.935/2021",
    "Certificacao PLDFT Prevencao a Lavagem de Dinheiro e ao Financiamento do Terrorismo",
    "Certificacao Transacional Instituto Totum",
    "Certificação Transacional Instituto Totum",
    "Fbb100 Correspondente Completa",
    "Fbb100 Correspondente Completo",
    "Fbb100 Correspondente Completo + Lgpd",
    "FBB100 Correspondente Completo LGPD",
    "Fbb110 Correspondente Consignado",
    "Fbb110 Correspondente Consignado + Lgpd",
    "FBB110 Correspondente Consignado LGPD"
]

# --- Mapeamento banco selecionado -> INF. ADICIONAL ---
BANCO_INF = {
    "AMIGOZ": "AMIGOZ",
    "PARANA CRIAÇÃO": "PARANA BANCO",
    "PARANA RESET": "PARANA BANCO",
    "EMPRESTEI CARD CRIAÇÃO": "EMPRESTEI CARD",
    "EMPRESTEI CARD RESET": "EMPRESTEI CARD",
    "TOTALCASH CRIAÇÃO": "TOTALCASH",
    "TOTALCASH RESET": "TOTALCASH",
    "NEO CREDITO CRIAÇÃO": "NEO CREDITO",
    "NEO CREDITO RESET": "NEO CREDITO",
    "BRB - INCONTA CRIAÇÃO": "BRB - INCONTA",
    "BRB - INCONTA RESET": "BRB - INCONTA",
    "CAIXA": "CAIXA",
    "EURO CRIAÇÃO": "EURO",
    "EURO RESET": "EURO"
}

# --- Layouts simplificados (exemplo, adapte conforme seu layout real) ---
LAYOUTS = {
    "AMIGOZ": {
        "ID LEV": ("workflow", "ID"),
        "CORBAN": "WL CASAQUI",
        "NOME": ("workflow", "Nome"),
        "TELEFONE": ("workflow", "Telefone"),
        "NASCIMENTO": ("workflow", "Nascimento"),
        "CPF": ("workflow", "CPF"),
        "PERFIL DE ACESSO": "CONSULTOR",
        "EMAIL": ("workflow", "E-Mail"),
        "UF": "UF",
        "CERTIFICAÇÃO": "Certificação",
        "DATA EMISSÃO": "Data Emissao",
        "DATA DE VALIDADE": "Data Validade",
        "TIPO DE ACESSO": "CONSULTOR",
        "DATA DO ENVIO": "data_atual"
    },
"BRB - INCONTA CRIAÇÃO": {
    "ID LEV": ("workflow", "ID"),
    "NOME": ("workflow", "Nome"),
    "TELEFONE": ("workflow", "Telefone"),
    "CPF": ("workflow", "CPF"),
    "EMAIL": ("workflow", "E-Mail"),
    "CERTIFICAÇÃO": "Certificação",
    "DATA EMISSÃO": "Data Emissao",
    "DATA DE VALIDADE": "Data Validade",
    "UF": "UF",
    "DATA DO ENVIO": "data_atual"
},

    "BRB - INCONTA RESET": {
        "ID LEV": ("workflow", "ID"),
        "NOME": ("workflow", "Nome"),
        "CPF": ("workflow", "CPF"),
        "LOGIN": ("workflow", "Usuário Banco"),
        "UF": "UF",
        "DATA DO ENVIO": "data_atual"
    },

    "CAIXA": {
        "ID LEV": ("workflow", "ID"),
        "CORBAN": "PLUS",
        "NOME": ("workflow", "Nome"),
        "TELEFONE": ("workflow", "Telefone"),
        "UF": "UF",
        "NASCIMENTO": ("workflow", "Nascimento"),
        "CPF": ("workflow", "CPF"),
        "PERFIL DE ACESSO": "CONSULTOR",
        "EMAIL": ("workflow", "E-Mail"),
        "CERTIFICAÇÃO": "Certificação",
        "DATA EMISSÃO": "Aprovacao",
        "DATA DE VALIDADE": "Validade",
        "TIPO DE ACESSO": "CONSULTOR",
        "DATA DO ENVIO": "data_atual"
    },

    "PARANA CRIAÇÃO": {
        "ID": ("workflow", "ID"),
        "DATA": "data_atual",
        "NOME": ("workflow", "Nome"),
        "NUMERO CERTIFICAÇÃO": "Certificação",
        "DATA EXAME": "Data Emissao",
        "CPF": ("workflow", "CPF"),
        "UF": "UF"
    },

    "PARANA RESET": {
        "ID": ("workflow", "ID"),
        "CPF": ("workflow", "CPF"),
        "UF": "UF"
    },

    "EMPRESTEI CARD CRIAÇÃO": {
        "ID": ("workflow", "ID"),
        "NOME": ("workflow", "Nome"),
        "CPF": ("workflow", "CPF"),
        "E-MAIL": ("workflow", "E-Mail"),
        "Telefone": ("workflow", "Telefone"),
        "UF": "UF",
        "CERTIFICAÇÃO": "Certificação",
        "DATA EMISSÃO": "Data Emissao",
        "DATA DE VALIDADE": "Data Validade",
        "DATA DO ENVIO": "data_atual"
    },

    "EMPRESTEI CARD RESET": {
        "ID": ("workflow", "ID"),
        "CPF": ("workflow", "CPF"),
        "E-MAIL": ("workflow", "Usuário Banco"),
        "UF": "UF",
        "DATA DO ENVIO": "data_atual"
    },

    "TOTALCASH CRIAÇÃO": {
        "Promotora": "LEV",
        "CPF": ("workflow", "CPF"),
        "Nome": ("workflow", "Nome"),
        "Email": ("workflow", "E-Mail"),
        "Telefone": ("workflow", "Telefone"),
        "UF": "UF",
        "Perfil": "CONSULTOR",
        "CERTIFICAÇÃO": "Certificação"
    },

    "TOTALCASH RESET": {
        "Promotora": "LEV",
        "CPF": ("workflow", "CPF"),
        "Nome": ("workflow", "Nome"),
        "Email": ("workflow", "E-Mail"),
        "UF": "UF"
    },

    "NEOCREDITO CRIAÇÃO": {
        "NOME": ("workflow", "Nome"),
        "CPF": ("workflow", "CPF"),
        "E-MAIL": ("workflow", "E-Mail"),
        "UF": "UF",
        "CERTIFICAÇÃO": "Certificação"
    },

    "NEOCREDITO RESET": {
        "NOME": ("workflow", "Nome"),
        "CPF": ("workflow", "CPF"),
        "E-MAIL": ("workflow", "E-Mail"),
        "UF": "UF"
    }
}

# --- Interface Streamlit ---
st.title("Gerador automático de layouts por banco - Usuários 📊")
st.write("Faça upload das bases workflow.xlsx e certificações.csv")

workflow_file = st.file_uploader("📂 Upload da Base Workflow", type=["xlsx"])
cert_file = st.file_uploader("📂 Upload da Base Certificações (CRCP)", type=["csv"])

if workflow_file and cert_file:
    workflow_df = pd.read_excel(workflow_file).dropna(how="all")
    
    certificacoes = pd.read_csv(cert_file, sep=";", encoding="latin1", on_bad_lines='skip').dropna(how="all")
    
    # Corrigir colunas
    certificacoes.columns = [c.encode('latin1').decode('utf-8', errors='ignore').strip() for c in certificacoes.columns]
    certificacoes.rename(columns={
        "Nº Certificado": "Numero Certificado",
        "Certificação": "Certificação",
        "Aprovacao": "Data Emissao",
        "Validade": "Data Validade"
    }, inplace=True)

    # UF pelo telefone
    workflow_df["UF"] = workflow_df["Telefone"].apply(extrair_uf) if "Telefone" in workflow_df.columns else ""

    banco_selecionado = st.selectbox("Selecione o banco", list(LAYOUTS.keys()))

    if banco_selecionado:
        layout = LAYOUTS[banco_selecionado]
        df_saida = pd.DataFrame()
        data_atual = datetime.now().strftime("%d/%m/%Y")
        data_atual_dt = datetime.now()

        # Filtrar workflow pelo banco correto
        nome_inf = BANCO_INF.get(banco_selecionado, banco_selecionado)
        workflow_banco = workflow_df[workflow_df.get("INF. ADICIONAL", "").str.contains(nome_inf, case=False, na=False)].copy()

        # Criar mapeamentos de certificados
        if not certificacoes.empty:
            certs_validas = certificacoes[certificacoes["Certificação"].isin(CERTIFICACOES_VALIDAS)].copy()
            certs_validas = certs_validas.sort_values("Data Validade", ascending=False).drop_duplicates("CPF")
            mapa_num = dict(zip(certs_validas["CPF"], certs_validas["Numero Certificado"]))
            mapa_data_emissao = dict(zip(certs_validas["CPF"], certs_validas["Data Emissao"]))
            mapa_data_validade = dict(zip(certs_validas["CPF"], certs_validas["Data Validade"]))
        else:
            mapa_num = {}
            mapa_data_emissao = {}
            mapa_data_validade = {}

        # Preencher planilha de saída
        for col_layout, fonte in layout.items():
            try:
                if fonte == "data_atual":
                    df_saida[col_layout] = data_atual
                elif fonte == "UF":
                    df_saida[col_layout] = workflow_banco["UF"]
                elif fonte == "Certificação":
                    df_saida[col_layout] = workflow_banco["CPF"].map(lambda x: mapa_num.get(x, "NÃO CERTIFICADO"))
                elif fonte == "Data Emissao":
                    df_saida[col_layout] = workflow_banco["CPF"].map(lambda x: mapa_data_emissao.get(x, ""))
                elif fonte == "Data Validade":
                    def checar_validade(x):
                        val = mapa_data_validade.get(x,"")
                        if val == "":
                            return "NÃO CERTIFICADO"
                        try:
                            return "VENCIDO" if pd.to_datetime(val, dayfirst=True) < data_atual_dt else val
                        except:
                            return val
                    df_saida[col_layout] = workflow_banco["CPF"].map(checar_validade)
                elif isinstance(fonte, tuple):
                    origem, campo = fonte
                    df_saida[col_layout] = workflow_banco.get(campo, "") if origem=="workflow" else ""
                else:
                    df_saida[col_layout] = fonte
            except:
                df_saida[col_layout] = ""

        # Exportar para Excel
        output = BytesIO()
        df_saida.to_excel(output, index=False)
        output.seek(0)
        st.download_button(
            label="📥 Baixar Planilha Gerada",
            data=output,
            file_name=f"{banco_selecionado}_{data_atual.replace('/','-')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Planilha gerada com sucesso!")
