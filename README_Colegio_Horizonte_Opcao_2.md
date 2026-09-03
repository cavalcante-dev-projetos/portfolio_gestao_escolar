# Colégio Horizonte — Opção 2

> Visão financeira com gráficos nativos do Power BI e uso pontual de HTML.

## Sobre esta versão

A segunda opção do projeto Colégio Horizonte apresenta uma visão financeira e de recebimentos com maior utilização de visuais nativos do Power BI. A proposta mantém a identidade visual do projeto e explora outra forma de organizar e comunicar as informações da mesma base de dados.

Os dados são fictícios, gerados em Python exclusivamente para portfólio. Esta documentação descreve a composição apresentada da segunda página e as técnicas utilizadas em sua construção.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
| --- | --- |
| Python e CSV | Geração dos dados fictícios e armazenamento das bases do projeto. |
| Power Query / M | Importação e tratamento dos dados utilizados no modelo. |
| Power BI | Construção dos gráficos, cartões e tabela da visão financeira. |
| DAX | Cálculo dos indicadores, rótulos e conteúdo do menu lateral. |
| HTML / CSS | Uso pontual na apresentação, com destaque para o cabeçalho e o menu lateral. |

## Dados e modelagem

A página reutiliza a base analítica do projeto. As tabelas fato_mensalidades e fato_despesas fornecem os valores financeiros; dim_alunos permite os recortes por segmento escolar; e dim_calendario organiza a evolução por competência.

A base de mensalidades contém valores e status Pago, Em Aberto e Vencido. A base de despesas contém categorias, valores e status financeiros. Os relacionamentos e as medidas DAX dão suporte às agregações exibidas nos gráficos e na tabela.

## Composição da página

| Elemento | Descrição |
| --- | --- |
| Cabeçalho | Identificação do Colégio Horizonte e título “Visão financeira e recebimentos”. |
| Menu lateral | Faixa azul à esquerda, com ícones, nomes das visões e destaque amarelo no item selecionado. |
| Cartões financeiros | Resumo dos valores de mensalidades e despesas no contexto da análise. |
| Evolução financeira | Gráfico combinado de colunas e linha para comparar receita prevista, receita recebida e despesas por mês. |
| Participação na receita prevista | Gráfico de barras horizontais para comparar valores e participação dos segmentos escolares. |
| Tabela por segmento | Detalhamento de receita prevista, receita recebida e receita em aberto, com total consolidado. |
| Composição das mensalidades | Gráfico de barras empilhadas para apresentar mensalidades pagas, em aberto e vencidas por segmento. |

## Indicadores utilizados

| Indicador | Regra de cálculo |
| --- | --- |
| Receita prevista | Soma dos valores das mensalidades. |
| Receita recebida | Soma das mensalidades com status Pago. |
| Receita em aberto | Soma das mensalidades com status Em Aberto. |
| Mensalidades vencidas | Soma das mensalidades com status Vencido. |
| Despesas totais | Soma das despesas pagas e em aberto. |
| Participação por segmento | Receita prevista do segmento em relação ao total dos segmentos no contexto selecionado. |

## Implementação visual

Os gráficos financeiros desta opção utilizam recursos nativos do Power BI. Foram trabalhados títulos, subtítulos, legendas, rótulos monetários e percentuais para facilitar a leitura e a comparação dos dados. As dicas de ferramenta complementam a consulta de valores ao passar o mouse.

A composição das mensalidades utiliza cores distintas para identificar cada status: azul para pagas, amarelo para em aberto e azul-escuro para vencidas. O gráfico de participação organiza os segmentos em barras horizontais, enquanto a tabela apresenta os valores detalhados.

## Uso pontual de HTML

O HTML foi concentrado em elementos de apresentação. O menu lateral foi construído por uma medida DAX que monta o conteúdo HTML/CSS, utilizando UNION e ROW para definir os itens e CONCATENATEX para gerar sua apresentação.

A medida permite definir a altura do menu pela variável AlturaMenu e destacar um item pela variável PaginaAtual. A lateral utiliza fundo azul-escuro, textos claros e destaque amarelo. A aparência do menu é produzida pelo HTML; ações de navegação entre páginas são configuradas separadamente em botões nativos do Power BI.

## Identidade visual

A página mantém as cores do projeto: azul principal #102D50, azul de receita #2C6CB0 e amarelo de destaque #F2C94C. O fundo claro da área de análise cria contraste com a lateral e o cabeçalho, preservando a unidade visual entre as opções do portfólio.

## Como utilizar

Abra o PBIX no Power BI Desktop e acesse a página correspondente à segunda opção. Para atualizar os dados, ajuste os caminhos dos CSVs tratados no Power Query. Consulte a evolução mensal, compare os segmentos e utilize as dicas de ferramenta para visualizar os valores.

A leitura financeira mensal utiliza a competência. Os valores de despesas representam a escola como um todo, sem rateio por segmento.

## Autoria

Priscila Cavalcante | Cavalcante Data
Projeto demonstrativo de portfólio com dados inteiramente fictícios.
