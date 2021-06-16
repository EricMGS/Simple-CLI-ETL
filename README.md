![Python](https://img.shields.io/badge/Python-3.8.5-green)
![Linux](https://img.shields.io/badge/Linux-WSL2--Ubuntu-orange)
![Postgres](https://img.shields.io/badge/Postgres-12.2-blue)

# Simple-CLI-ETL
Software básico de tratamento de dados, via linha de comando. Desenvolvido como trabalho para a disciplina Tópicos Especiais em Informática

`Desenvolvido e testado em ambiente WSL2 no Windows 10, com container Postgres 12.2`

![Screenshot](https://github.com/EricMGS/Simple-CLI-ETL/blob/main/screenshot.png)

### Sistema Operacional
Linux

### Versão Python
3.8.5

## Dependências Python
- xlrd
- xlwt
- lxml
- pandas 
- numpy
- requests
- pandassql
- urwid
- psycopg2

## Banco de dados
Postgres 12.2  
**host** = localhost  
**dbname** = trabpython  
**user** = postgres  
**password** = root  

## Tabelas:
### login
```
CREATE TABLE public.login
(
    id serial,
    username text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT login_pkey PRIMARY KEY (id),
    CONSTRAINT un_username UNIQUE (username)
)

TABLESPACE pg_default;

ALTER TABLE public.login
    OWNER to postgres;
```

### macros
```
CREATE TABLE public.macros
(
    id serial,
    username text COLLATE pg_catalog."default" NOT NULL,
    command text COLLATE pg_catalog."default" NOT NULL,
    command_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT macros_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.macros
    OWNER to postgres;
```

## Execução
Após ter todas dependências instaladas e o banco de dados rodando com as tabelas criadas, execute com python o arquivo `ui.py`

## Arquivos
- **ui.py**: arquivo principal, contém toda a estrutura de telas, execução de funcionalidades e controle de erros
- **macros.py**: controlador da tabela macros do banco de dados
- **login.py**:  controlador da tabela login do banco de dados
- **etl.py**: arquivo core das funcionalidades do software, realiza o carregamento de tabelas, transformação e extração
- **edit.py**: código para o editor de texto em tempo de execução
- **edit.txt**: texto salvo pelo editor
