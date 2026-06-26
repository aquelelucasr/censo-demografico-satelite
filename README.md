# Censo demográfico via satélite

## Visão Geral
Breve descrição do projeto (2-3 parágrafos)

## Requisitos de Software 
- Linguagem e Frameworks utilizados
- Versões específicas de bibliotecas
- Links para documentação

## Configuração do Ambiente
- Versões de IDE/toolchain
- Dependências e bibliotecas
- Passo a passo de configuração

## Como Usar
- Instruções de upload
- Configurações necessárias
- Exemplos de uso

## Estrutura do Projeto
Explicação da organização dos arquivos

## Troubleshooting
Problemas comuns e soluções

## Contribuidores
- Ian Martins Mendes (23205319) - Organização e Machine Learning
- Lucas Rodrigues da Silva (21205137) - banco de dados e backend de integração
- Pedro Otavio Vaz Alcantara (24103218) - Machine Learning e visão computacional
- Andre de Souza da Costa (23104086) - 

## Estrutura do projeto
```
projeto-software/
├── README.md
├── LICENSE
├── .env                        # chaves de api
├── .gitignore
├── .venv/                      # bibliotecas *
├── docs/
│   ├── assets/                 # imagens de referencia
│   ├── boas-praticas.md        # Organização dos dos commits e branches 
│   ├── controller.md           # tarefas e documentacao de cada parte
│   ├── model.md
│   └── view.md
├── src/
│   ├── main.py
│   ├── model/
│   ├── view/
│   └── controller/
├── scripts/                    # scripts de instalação
├── media/                      # imagens salvas pelo programa  *
│   ├── raw/
│   └── controller/
├── database/
│   └──  search_history.sqlite  # *
└── examples/

* criado pelo script de instalação ou em tempo de execução
```

# TODO: refactor code to new standard