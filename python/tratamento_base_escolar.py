from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

PASTA_BRUTOS = BASE_DIR / "dados" / "brutos"
PASTA_TRATADOS = BASE_DIR / "dados" / "tratados"

PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)


# ============================================================
# FUNÇÃO PARA CARREGAR CSV
# ============================================================

def carregar_csv(nome):

    caminho = PASTA_BRUTOS / f"{nome}.csv"

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    df = pd.read_csv(
        caminho,
        encoding="utf-8-sig"
    )

    print(
        f"Carregado: {nome}.csv "
        f"→ {len(df):,} registros"
    )

    return df


# ============================================================
# CARREGAMENTO
# ============================================================

print("=" * 70)
print("ETL — COLÉGIO HORIZONTE")
print("=" * 70)

alunos = carregar_csv("alunos")
professores = carregar_csv("professores")
funcionarios = carregar_csv("funcionarios")
turmas = carregar_csv("turmas")
matriculas = carregar_csv("matriculas")
mensalidades = carregar_csv("mensalidades")
despesas = carregar_csv("despesas")
notas = carregar_csv("notas")
frequencia = carregar_csv("frequencia")


# ============================================================
# PADRONIZAÇÃO DE TEXTOS
# ============================================================

def limpar_texto(df):

    colunas_texto = df.select_dtypes(
        include=["str"]
    ).columns

    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
        )

    return df


alunos = limpar_texto(alunos)
professores = limpar_texto(professores)
funcionarios = limpar_texto(funcionarios)
turmas = limpar_texto(turmas)
matriculas = limpar_texto(matriculas)
mensalidades = limpar_texto(mensalidades)
despesas = limpar_texto(despesas)
notas = limpar_texto(notas)
frequencia = limpar_texto(frequencia)


# ============================================================
# PADRONIZAÇÃO DE DATAS
# ============================================================

colunas_datas = {
    "alunos": [
        "data_nascimento"
    ],

    "matriculas": [
        "data_matricula"
    ],

    "mensalidades": [
        "competencia",
        "data_vencimento",
        "data_pagamento"
    ],

    "despesas": [
        "competencia"
    ],

    "frequencia": [
        "competencia"
    ]
}


datasets = {
    "alunos": alunos,
    "matriculas": matriculas,
    "mensalidades": mensalidades,
    "despesas": despesas,
    "frequencia": frequencia
}


for nome, colunas in colunas_datas.items():

    df = datasets[nome]

    for coluna in colunas:

        if coluna in df.columns:

            df[coluna] = pd.to_datetime(
                df[coluna],
                errors="coerce"
            )


# ============================================================
# PADRONIZAÇÃO NUMÉRICA
# ============================================================

colunas_numericas = {
    "turmas": [
        "capacidade",
        "ano_letivo"
    ],

    "mensalidades": [
        "valor"
    ],

    "despesas": [
        "valor"
    ],

    "notas": [
        "nota"
    ],

    "frequencia": [
        "percentual_frequencia"
    ],

    "matriculas": [
        "valor_matricula"
    ]
}


datasets_numericos = {
    "turmas": turmas,
    "mensalidades": mensalidades,
    "despesas": despesas,
    "notas": notas,
    "frequencia": frequencia,
    "matriculas": matriculas
}


for nome, colunas in colunas_numericas.items():

    df = datasets_numericos[nome]

    for coluna in colunas:

        if coluna in df.columns:

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )


# ============================================================
# PADRONIZAÇÃO DE VALORES MONETÁRIOS
# ============================================================

mensalidades["valor"] = mensalidades[
    "valor"
].round(2)

despesas["valor"] = despesas[
    "valor"
].round(2)

matriculas["valor_matricula"] = matriculas[
    "valor_matricula"
].round(2)


# ============================================================
# PADRONIZAÇÃO DE CATEGORIAS
# ============================================================

status_padrao = {
    "Pago": "Pago",
    "Em aberto": "Em Aberto",
    "Vencido": "Vencido",
    "Cancelado": "Cancelado",
    "Ativa": "Ativo",
    "Ativo": "Ativo"
}


for df in [
    alunos,
    professores,
    funcionarios,
    turmas,
    matriculas,
    mensalidades,
    despesas
]:

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .replace(status_padrao)
        )


# ============================================================
# CRIAÇÃO DE CHAVES
# ============================================================

# Chave da competência mensal
mensalidades["chave_competencia"] = (
    mensalidades["competencia"]
    .dt.strftime("%Y%m")
)

despesas["chave_competencia"] = (
    despesas["competencia"]
    .dt.strftime("%Y%m")
)

frequencia["chave_competencia"] = (
    frequencia["competencia"]
    .dt.strftime("%Y%m")
)


# ============================================================
# DIMENSÃO CALENDÁRIO
# ============================================================

data_inicio = pd.Timestamp("2026-01-01")
data_fim = pd.Timestamp("2026-12-31")

datas = pd.date_range(
    start=data_inicio,
    end=data_fim,
    freq="D"
)

calendario = pd.DataFrame({
    "data": datas
})

calendario["ano"] = calendario[
    "data"
].dt.year

calendario["mes_numero"] = calendario[
    "data"
].dt.month

calendario["mes"] = calendario[
    "data"
].dt.month_name(
    locale="pt_BR"
)

calendario["mes_ano"] = (
    calendario["data"]
    .dt.strftime("%m/%Y")
)

calendario["trimestre"] = (
    calendario["data"]
    .dt.quarter
)

calendario["dia"] = calendario[
    "data"
].dt.day

calendario["dia_semana_numero"] = (
    calendario["data"]
    .dt.dayofweek + 1
)

calendario["dia_semana"] = (
    calendario["data"]
    .dt.day_name(
        locale="pt_BR"
    )
)

calendario["eh_fim_de_semana"] = (
    calendario["dia_semana_numero"]
    .isin([6, 7])
)


# ============================================================
# ORDENAÇÃO DO MÊS
# ============================================================

meses = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

calendario["mes_numero"] = (
    calendario["data"].dt.month
)


# ============================================================
# VALIDAÇÕES
# ============================================================

print("\n" + "=" * 70)
print("VALIDAÇÕES")
print("=" * 70)


def validar_nulos(df, nome):

    total_nulos = df.isna().sum().sum()

    print(
        f"{nome}: "
        f"{total_nulos} células nulas"
    )


validar_nulos(alunos, "Alunos")
validar_nulos(professores, "Professores")
validar_nulos(funcionarios, "Funcionários")
validar_nulos(turmas, "Turmas")
validar_nulos(matriculas, "Matrículas")
validar_nulos(mensalidades, "Mensalidades")
validar_nulos(despesas, "Despesas")
validar_nulos(notas, "Notas")
validar_nulos(frequencia, "Frequência")


# ============================================================
# EXPORTAÇÃO
# ============================================================

bases_tratadas = {

    "dim_alunos": alunos,
    "dim_professores": professores,
    "dim_funcionarios": funcionarios,
    "dim_turmas": turmas,

    "fato_matriculas": matriculas,
    "fato_mensalidades": mensalidades,
    "fato_despesas": despesas,
    "fato_notas": notas,
    "fato_frequencia": frequencia,

    "dim_calendario": calendario
}


print("\n" + "=" * 70)
print("EXPORTAÇÃO")
print("=" * 70)


for nome, df in bases_tratadas.items():

    caminho = (
        PASTA_TRATADOS
        / f"{nome}.csv"
    )

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"OK: {nome}.csv "
        f"→ {len(df):,} registros"
    )


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("ETL CONCLUÍDO")
print("=" * 70)

print(
    f"\nArquivos tratados salvos em:\n"
    f"{PASTA_TRATADOS}"
)