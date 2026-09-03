from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PASTA_DADOS = BASE_DIR / "dados" / "brutos"


def carregar(nome):
    caminho = PASTA_DADOS / f"{nome}.csv"

    if not caminho.exists():
        print(f"❌ Não encontrado: {caminho}")
        return None

    df = pd.read_csv(caminho)

    print(f"✅ {nome}.csv → {len(df):,} registros")

    return df


print("=" * 60)
print("VALIDAÇÃO — COLÉGIO HORIZONTE")
print("=" * 60)


alunos = carregar("alunos")
professores = carregar("professores")
funcionarios = carregar("funcionarios")
turmas = carregar("turmas")
matriculas = carregar("matriculas")
mensalidades = carregar("mensalidades")
despesas = carregar("despesas")
notas = carregar("notas")
frequencia = carregar("frequencia")


print("\n" + "=" * 60)
print("VALIDAÇÕES DE INTEGRIDADE")
print("=" * 60)


# ------------------------------------------------------------
# ALUNOS → TURMAS
# ------------------------------------------------------------

ids_turmas = set(turmas["id_turma"])

alunos_sem_turma = alunos[
    ~alunos["id_turma"].isin(ids_turmas)
]

print(
    f"\nAlunos sem turma válida: "
    f"{len(alunos_sem_turma)}"
)


# ------------------------------------------------------------
# MATRÍCULAS → ALUNOS
# ------------------------------------------------------------

ids_alunos = set(alunos["id_aluno"])

matriculas_sem_aluno = matriculas[
    ~matriculas["id_aluno"].isin(ids_alunos)
]

print(
    f"Matrículas sem aluno válido: "
    f"{len(matriculas_sem_aluno)}"
)


# ------------------------------------------------------------
# MATRÍCULAS → TURMAS
# ------------------------------------------------------------

matriculas_sem_turma = matriculas[
    ~matriculas["id_turma"].isin(ids_turmas)
]

print(
    f"Matrículas sem turma válida: "
    f"{len(matriculas_sem_turma)}"
)


# ------------------------------------------------------------
# MENSALIDADES → ALUNOS
# ------------------------------------------------------------

mensalidades_sem_aluno = mensalidades[
    ~mensalidades["id_aluno"].isin(ids_alunos)
]

print(
    f"Mensalidades sem aluno válido: "
    f"{len(mensalidades_sem_aluno)}"
)


# ------------------------------------------------------------
# NOTAS → ALUNOS
# ------------------------------------------------------------

notas_sem_aluno = notas[
    ~notas["id_aluno"].isin(ids_alunos)
]

print(
    f"Notas sem aluno válido: "
    f"{len(notas_sem_aluno)}"
)


# ------------------------------------------------------------
# FREQUÊNCIA → ALUNOS
# ------------------------------------------------------------

frequencia_sem_aluno = frequencia[
    ~frequencia["id_aluno"].isin(ids_alunos)
]

print(
    f"Frequências sem aluno válido: "
    f"{len(frequencia_sem_aluno)}"
)


# ------------------------------------------------------------
# TURMAS → PROFESSORES
# ------------------------------------------------------------

ids_professores = set(
    professores["id_professor"]
)

turmas_sem_professor = turmas[
    ~turmas["id_professor"].isin(ids_professores)
]

print(
    f"Turmas sem professor válido: "
    f"{len(turmas_sem_professor)}"
)


# ------------------------------------------------------------
# DUPLICIDADES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDAÇÃO DE CHAVES")
print("=" * 60)


print(
    "IDs de alunos duplicados:",
    alunos["id_aluno"].duplicated().sum()
)

print(
    "IDs de turmas duplicados:",
    turmas["id_turma"].duplicated().sum()
)

print(
    "IDs de professores duplicados:",
    professores["id_professor"].duplicated().sum()
)

print(
    "IDs de matrículas duplicados:",
    matriculas["id_matricula"].duplicated().sum()
)

print(
    "IDs de mensalidades duplicados:",
    mensalidades["id_mensalidade"].duplicated().sum()
)


# ------------------------------------------------------------
# RESUMO FINANCEIRO
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("RESUMO FINANCEIRO")
print("=" * 60)


receita_total = mensalidades["valor"].sum()

receita_paga = mensalidades.loc[
    mensalidades["status"] == "Pago",
    "valor"
].sum()

receita_vencida = mensalidades.loc[
    mensalidades["status"] == "Vencido",
    "valor"
].sum()

despesas_total = despesas["valor"].sum()


print(
    f"Receita prevista: "
    f"R$ {receita_total:,.2f}"
)

print(
    f"Receita recebida: "
    f"R$ {receita_paga:,.2f}"
)

print(
    f"Inadimplência: "
    f"R$ {receita_vencida:,.2f}"
)

print(
    f"Despesas: "
    f"R$ {despesas_total:,.2f}"
)


# ------------------------------------------------------------
# OCUPAÇÃO
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("OCUPAÇÃO")
print("=" * 60)


ocupacao = (
    alunos.groupby("id_turma")
    .size()
    .reset_index(name="alunos")
)

ocupacao = ocupacao.merge(
    turmas[
        [
            "id_turma",
            "capacidade"
        ]
    ],
    on="id_turma",
    how="left"
)

ocupacao["taxa_ocupacao"] = (
    ocupacao["alunos"]
    / ocupacao["capacidade"]
)

print(
    f"Capacidade total: "
    f"{ocupacao['capacidade'].sum():,}"
)

print(
    f"Alunos matriculados: "
    f"{ocupacao['alunos'].sum():,}"
)

print(
    f"Ocupação média: "
    f"{ocupacao['taxa_ocupacao'].mean() * 100:.2f}%"
)


# ------------------------------------------------------------
# RESULTADO
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDAÇÃO CONCLUÍDA")
print("=" * 60)