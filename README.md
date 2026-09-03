# Colégio Horizonte — Gestão Escolar com Power BI

## Sobre o projeto

O Colégio Horizonte é um projeto de Business Intelligence aplicado à gestão escolar, desenvolvido para portfólio. A proposta é explorar diferentes formas de analisar e visualizar uma mesma base de dados, utilizando Power BI e componentes HTML.

Todos os dados são fictícios, gerados em Python exclusivamente para demonstração. A implementação concentra a apresentação em receitas, mensalidades e despesas, com recortes por segmento escolar. A base também contempla alunos, turmas, matrículas, professores, funcionários, notas e frequência.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
| --- | --- |
| Python | Geração dos dados fictícios utilizados no projeto. |
| CSV | Armazenamento das bases de origem e das tabelas tratadas. |
| Power Query / M | Importação, transformação e tipagem dos dados. |
| Power BI | Modelagem dos dados e construção do relatório. |
| DAX | Cálculo dos indicadores e geração de conteúdo HTML dinâmico. |
| HTML / CSS e HTML Content | Personalização de cartões, tabelas e gráficos no relatório. |

## Preparação dos dados

As bases foram organizadas em tabelas de dimensões e fatos. O tratamento incluiu padronização de status, inclusão de uma chave de competência no formato AAAAMM em mensalidades, despesas e frequência, além da criação de um calendário diário para 2026.

No Power Query, foram configurados a leitura de CSV em UTF-8, a promoção de cabeçalhos e os tipos de dados das principais tabelas. As consultas financeiras utilizam tipo monetário e conversão com cultura en-US, compatível com o ponto decimal dos arquivos. Datas de pagamento vazias foram convertidas em nulos, e os nomes dos alunos receberam padronização de capitalização.

## Estrutura dos dados

| Tabela | Conteúdo |
| --- | --- |
| dim_alunos | Cadastro e classificação dos alunos. |
| dim_calendario | Datas e atributos de ano, mês, trimestre e dia da semana. |
| dim_turmas | Segmento, série, turno, capacidade e professor da turma. |
| dim_professores | Cadastro e informações contratuais dos professores. |
| dim_funcionarios | Cadastro, cargo e departamento dos funcionários. |
| fato_matriculas | Registros, tipos e valores de matrícula. |
| fato_mensalidades | Competência, vencimento, pagamento, valor e status. |
| fato_despesas | Despesas por competência, categoria e status. |
| fato_notas | Notas por aluno, disciplina e bimestre. |
| fato_frequencia | Percentual de frequência por aluno e competência. |

## Modelagem e medidas

O modelo utiliza o cadastro de alunos para os recortes de mensalidades, matrículas e notas. O calendário foi relacionado por competência às tabelas de mensalidades, despesas e frequência. Turmas e professores foram relacionados pelo identificador do professor.

Foram desenvolvidas 43 medidas DAX, incluindo indicadores, medidas auxiliares, cores, rótulos e expressões HTML. As medidas utilizam funções como CALCULATE, DIVIDE, KEEPFILTERS, ALLSELECTED, ADDCOLUMNS e CONCATENATEX para calcular valores no contexto de filtro e construir os elementos visuais.

## Principais indicadores

| Indicador | Regra de cálculo |
| --- | --- |
| Receita prevista | Soma das mensalidades de todos os status. |
| Receita recebida | Soma das mensalidades com status Pago. |
| Receita em aberto | Soma das mensalidades com status Em Aberto. |
| Inadimplência | Soma das mensalidades com status Vencido. |
| Taxa de inadimplência | Valor vencido dividido pela receita prevista. |
| Total de despesas | Soma das despesas pagas e em aberto. |
| Resultado | Receita recebida menos o total de despesas. |
| Taxa de ocupação | Alunos ativos divididos pela capacidade total das turmas. |

## Visualizações desenvolvidas

A página Visão Geral reúne seis componentes em HTML: cabeçalho institucional, cartões financeiros, composição das mensalidades por segmento, evolução mensal de receita prevista e despesas, despesas por categoria e resumo financeiro por segmento.

Os componentes são gerados por medidas DAX e exibidos no visual HTML Content. A apresentação utiliza HTML e CSS para definir cores, tipografia, espaçamento, barras proporcionais e tabelas. As expressões incluem valores monetários em reais, formatação pt-BR e atributos title para consulta de valores ao passar o mouse.

O PBIX também contém uma página com cartões, matrizes, gráficos de barras e tabelas nativas, além de uma página com o cabeçalho HTML. Essas composições exploram formas distintas de apresentar os dados do projeto.

## Identidade visual

A identidade visual utiliza azul principal (#102D50), azul de receita (#2C6CB0) e amarelo de destaque (#F2C94C), com fundos claros e cores específicas para alertas. Cores e rótulos também foram organizados em medidas DAX para apoiar a padronização da apresentação.

## Como utilizar

1. Abra Colegio_Horizonte_Gestao.pbix no Power BI Desktop.
2. Disponibilize os CSVs tratados em uma pasta local.
3. Ajuste os caminhos das fontes no Power Query para essa pasta e confira os nomes dos arquivos.
4. Atualize os dados e navegue pelas páginas do relatório.

As consultas esperam os nomes dos CSVs sem o sufixo “(1)” presente em alguns anexos. A leitura mensal dos indicadores financeiros utiliza a competência das mensalidades e despesas.

## Autoria

Priscila Cavalcante | Cavalcante Data
Projeto demonstrativo de portfólio com dados inteiramente fictícios.
