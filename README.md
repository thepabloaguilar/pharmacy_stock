# Pharmacy Stock API

Aplicação para gerenciar o estoque de uma farmacia, provendo os seguintes recursos:
- Usuários:
    - Existem dois tipos de usuários, os Adminitradores e os Não Adminitradores
    - Os Não Administradores não podem interagir com algumas partes do sistema
- Fornecedores
- Medicamentos
- Clientes
- Vendas

## Utilização

### Tecnologias Utilizadas

* [**Python**](https://www.python.org)
    * [**Flask**](http://flask.pocoo.org)
    * [**Flask RESTFul**](https://flask-restful.readthedocs.io/en/latest/)
    * [**Flasgger**](https://github.com/rochacbruno/flasgger)
* [**PostgreSQL**](https://www.postgresql.org)
* [**Docker**](https://www.docker.com)

### Requisitos

* [**Docker**](https://www.docker.com)
* [**Docker Compose**](https://docs.docker.com/compose/install/)

### Subindo o sistema

1. Clone ou faça o download deste repositório.

2. Dentro da pasta execute o seguinte comando para subir os containers:
    ```sh
    make start
    ```
3. Entre no link [**localhost:5000/docs**](http://localhost:5000/docs).
Esse link dará o acesso ao Swagger onde você poderá fazer requisições para os EndPoints dos serviços.

4. Para parar os serviços, basta executar o seguinte comando no terminal, ainda dentro da pasta do projeto:
    ```sh
    make stop
    ```