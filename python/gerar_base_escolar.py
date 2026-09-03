from pathlib import Path
import random
from datetime import date, timedelta

import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SEMENTE = 2026
random.seed(SEMENTE)

ANO = 2026

BASE_DIR = Path(__file__).resolve().parents[1]
PASTA_SAIDA = BASE_DIR / "dados" / "brutos"

PASTA_SAIDA.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURAÇÃO DA ESCOLA
# ============================================================

ESCOLA = "Colégio Horizonte"

SEGMENTOS = {
    "EI": {
        "nome": "Educação Infantil",
        "series": ["Infantil 1", "Infantil 2", "Infantil 3"],
        "turmas": 12,
        "capacidade": 25,
    },
    "FI": {
        "nome": "Ensino Fundamental I",
        "series": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
        "turmas": 16,
        "capacidade": 28,
    },
    "FII": {
        "nome": "Ensino Fundamental II",
        "series": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"],
        "turmas": 12,
        "capacidade": 30,
    },
    "EM": {
        "nome": "Ensino Médio",
        "series": ["1ª Série", "2ª Série", "3ª Série"],
        "turmas": 8,
        "capacidade": 32,
    },
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def gerar_nome():
    nomes = [
        "Ana", "Beatriz", "Bruno", "Carlos", "Camila",
        "Daniel", "Eduardo", "Fernanda", "Gabriel",
        "Helena", "Isabela", "João", "Julia", "Larissa",
        "Lucas", "Mariana", "Mateus", "Miguel", "Rafael",
        "Sofia", "Thiago", "Valentina", "Vinicius"
    ]

    sobrenomes = [
        "Almeida", "Barbosa", "Carvalho", "Costa", "Dias",
        "Fernandes", "Gomes", "Lima", "Martins", "Mendes",
        "Moreira", "Nascimento", "Oliveira", "Pereira",
        "Ramos", "Rocha", "Santos", "Silva", "Souza"
    ]

    return (
        f"{random.choice(nomes)} "
        f"{random.choice(sobrenomes)} "
        f"{random.choice(sobrenomes)}"
    )


def gerar_data_nascimento(idade_min, idade_max):
    hoje = date(ANO, 1, 1)

    idade = random.randint(idade_min, idade_max)

    inicio = hoje - timedelta(days=(idade + 1) * 365)
    fim = hoje - timedelta(days=idade * 365)

    return inicio + timedelta(
        days=random.randint(0, max(1, (fim - inicio).days))
    )


def gerar_cpf_ficticio(numero):
    return f"000.{numero:03d}.{(numero * 7) % 1000:03d}-00"


# ============================================================
# 1. PROFESSORES
# ============================================================

professores = []

for i in range(1, 121):

    professores.append({
        "id_professor": f"PROF{i:04d}",
        "nome": gerar_nome(),
        "segmento_principal": random.choice(
            list(SEGMENTOS.keys())
        ),
        "tipo_contrato": random.choice([
            "CLT",
            "CLT",
            "CLT",
            "PJ"
        ]),
        "carga_horaria": random.choice([
            20, 30, 40
        ]),
        "status": "Ativo"
    })

df_professores = pd.DataFrame(professores)


# ============================================================
# 2. FUNCIONÁRIOS ADMINISTRATIVOS
# ============================================================

cargos = [
    "Coordenação",
    "Secretaria",
    "Financeiro",
    "Recursos Humanos",
    "Tecnologia",
    "Recepção",
    "Manutenção",
    "Direção"
]

funcionarios = []

for i in range(1, 36):

    funcionarios.append({
        "id_funcionario": f"FUNC{i:04d}",
        "nome": gerar_nome(),
        "cargo": random.choice(cargos),
        "departamento": random.choice([
            "Administrativo",
            "Financeiro",
            "Acadêmico",
            "Operacional"
        ]),
        "tipo_contrato": random.choice([
            "CLT",
            "CLT",
            "CLT",
            "PJ"
        ]),
        "status": "Ativo"
    })

df_funcionarios = pd.DataFrame(funcionarios)


# ============================================================
# 3. TURMAS
# ============================================================

turmas = []

contador_turma = 1

for codigo_segmento, config in SEGMENTOS.items():

    for numero in range(1, config["turmas"] + 1):

        serie = random.choice(config["series"])

        turno = random.choice([
            "Manhã",
            "Tarde"
        ])

        professor = random.choice(
            df_professores[
                df_professores["segmento_principal"] == codigo_segmento
            ]["id_professor"].tolist()
        )

        capacidade = config["capacidade"]

        turmas.append({
            "id_turma": f"TURMA{contador_turma:03d}",
            "codigo_segmento": codigo_segmento,
            "segmento": config["nome"],
            "serie": serie,
            "turno": turno,
            "capacidade": capacidade,
            "id_professor": professor,
            "ano_letivo": ANO,
            "status": "Ativa"
        })

        contador_turma += 1


df_turmas = pd.DataFrame(turmas)


# ============================================================
# 4. ALUNOS
# ============================================================

alunos = []

numero_aluno = 1

for _, turma in df_turmas.iterrows():

    capacidade = int(turma["capacidade"])

    ocupacao = random.uniform(0.72, 0.98)

    quantidade = int(capacidade * ocupacao)

    for _ in range(quantidade):

        if turma["codigo_segmento"] == "EI":
            idade_min, idade_max = 3, 5

        elif turma["codigo_segmento"] == "FI":
            idade_min, idade_max = 6, 10

        elif turma["codigo_segmento"] == "FII":
            idade_min, idade_max = 11, 14

        else:
            idade_min, idade_max = 15, 17

        alunos.append({
            "id_aluno": f"ALU{numero_aluno:05d}",
            "nome": gerar_nome(),
            "cpf": gerar_cpf_ficticio(numero_aluno),
            "data_nascimento": gerar_data_nascimento(
                idade_min,
                idade_max
            ),
            "sexo": random.choice([
                "F",
                "M"
            ]),
            "id_turma": turma["id_turma"],
            "codigo_segmento": turma["codigo_segmento"],
            "segmento": turma["segmento"],
            "serie": turma["serie"],
            "turno": turma["turno"],
            "status": "Ativo",
            "ano_letivo": ANO
        })

        numero_aluno += 1


df_alunos = pd.DataFrame(alunos)


# ============================================================
# 5. MATRÍCULAS
# ============================================================

matriculas = []

for _, aluno in df_alunos.iterrows():

    data_matricula = date(
        ANO - 1,
        random.randint(9, 12),
        random.randint(1, 28)
    )

    matriculas.append({
        "id_matricula": f"MAT{len(matriculas) + 1:06d}",
        "id_aluno": aluno["id_aluno"],
        "id_turma": aluno["id_turma"],
        "data_matricula": data_matricula,
        "tipo_matricula": random.choice([
            "Rematrícula",
            "Nova matrícula",
            "Transferência"
        ]),
        "status": "Ativa",
        "valor_matricula": random.choice([
            350,
            450,
            550,
            650
        ])
    })


df_matriculas = pd.DataFrame(matriculas)


# ============================================================
# 6. MENSALIDADES
# ============================================================

mensalidades = []

valores_segmento = {
    "EI": 1450,
    "FI": 1650,
    "FII": 1850,
    "EM": 2100
}

for _, aluno in df_alunos.iterrows():

    valor_base = valores_segmento[aluno["codigo_segmento"]]

    for mes in range(1, 13):

        vencimento = date(
            ANO,
            mes,
            10
        )

        valor = valor_base * random.uniform(
            0.97,
            1.03
        )

        status = random.choices(
            [
                "Pago",
                "Em aberto",
                "Vencido"
            ],
            weights=[
                82,
                10,
                8
            ]
        )[0]

        data_pagamento = None

        if status == "Pago":

            data_pagamento = vencimento + timedelta(
                days=random.randint(-3, 8)
            )

        mensalidades.append({
            "id_mensalidade": f"MEN{len(mensalidades) + 1:08d}",
            "id_aluno": aluno["id_aluno"],
            "competencia": date(ANO, mes, 1),
            "data_vencimento": vencimento,
            "data_pagamento": data_pagamento,
            "valor": round(valor, 2),
            "status": status
        })


df_mensalidades = pd.DataFrame(mensalidades)


# ============================================================
# 7. DESPESAS
# ============================================================

categorias_despesa = [
    "Folha de pagamento",
    "Fornecedores",
    "Infraestrutura",
    "Tecnologia",
    "Material didático",
    "Manutenção",
    "Marketing",
    "Administrativo"
]

despesas = []

for mes in range(1, 13):

    for categoria in categorias_despesa:

        if categoria == "Folha de pagamento":
            valor = random.uniform(
                450000,
                520000
            )

        elif categoria == "Fornecedores":
            valor = random.uniform(
                80000,
                120000
            )

        elif categoria == "Infraestrutura":
            valor = random.uniform(
                40000,
                70000
            )

        elif categoria == "Tecnologia":
            valor = random.uniform(
                15000,
                30000
            )

        else:
            valor = random.uniform(
                8000,
                35000
            )

        despesas.append({
            "id_despesa": f"DESP{len(despesas) + 1:05d}",
            "competencia": date(ANO, mes, 1),
            "categoria": categoria,
            "descricao": f"{categoria} - {mes:02d}/{ANO}",
            "valor": round(valor, 2),
            "status": random.choice([
                "Pago",
                "Pago",
                "Pago",
                "Em aberto"
            ])
        })


df_despesas = pd.DataFrame(despesas)


# ============================================================
# 8. NOTAS
# ============================================================

notas = []

disciplinas = [
    "Português",
    "Matemática",
    "Ciências",
    "História",
    "Geografia",
    "Inglês"
]

for _, aluno in df_alunos.iterrows():

    for disciplina in disciplinas:

        nota = random.uniform(
            5.5,
            9.8
        )

        notas.append({
            "id_nota": f"NOT{len(notas) + 1:08d}",
            "id_aluno": aluno["id_aluno"],
            "disciplina": disciplina,
            "periodo": random.choice([
                "1º Bimestre",
                "2º Bimestre",
                "3º Bimestre",
                "4º Bimestre"
            ]),
            "nota": round(nota, 1)
        })


df_notas = pd.DataFrame(notas)


# ============================================================
# 9. FREQUÊNCIA
# ============================================================

frequencia = []

for _, aluno in df_alunos.iterrows():

    for mes in range(1, 13):

        percentual = random.uniform(
            87,
            99
        )

        frequencia.append({
            "id_frequencia": f"FREQ{len(frequencia) + 1:08d}",
            "id_aluno": aluno["id_aluno"],
            "competencia": date(ANO, mes, 1),
            "percentual_frequencia": round(
                percentual,
                2
            )
        })


df_frequencia = pd.DataFrame(frequencia)


# ============================================================
# SALVAMENTO
# ============================================================

bases = {
    "alunos": df_alunos,
    "professores": df_professores,
    "funcionarios": df_funcionarios,
    "turmas": df_turmas,
    "matriculas": df_matriculas,
    "mensalidades": df_mensalidades,
    "despesas": df_despesas,
    "notas": df_notas,
    "frequencia": df_frequencia,
}


for nome, dataframe in bases.items():

    caminho = PASTA_SAIDA / f"{nome}.csv"

    dataframe.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"OK: {nome}.csv "
        f"({len(dataframe):,} registros)"
    )


# ============================================================
# RESUMO
# ============================================================

print("\n" + "=" * 60)
print("BASE DO COLÉGIO HORIZONTE GERADA")
print("=" * 60)

print(f"Escola: {ESCOLA}")
print(f"Ano: {ANO}")
print(f"Alunos: {len(df_alunos):,}")
print(f"Turmas: {len(df_turmas):,}")
print(f"Professores: {len(df_professores):,}")
print(f"Funcionários: {len(df_funcionarios):,}")
print(f"Mensalidades: {len(df_mensalidades):,}")
print(f"Despesas: {len(df_despesas):,}")
print(f"Notas: {len(df_notas):,}")
print(f"Frequências: {len(df_frequencia):,}")

print("\nArquivos salvos em:")
print(PASTA_SAIDA)