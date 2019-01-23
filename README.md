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

### Utilizando o Swagger

Se você ainda não acessou o link da [**documentação**](http://localhost:5000/docs), acesse.

Todas as rotas, exceto a de login, exigem um **token** para autenticação no HEADER da request. Esse token é obtido através da rota de Login.

#### Pegando o Token
1. Com o Swagger aberto, clique na rota de login:
![Tela Inicial - Swagger](https://raw.githubusercontent.com/phakiller/pharmacy_stock/master/images/swagger_initial_login_route.png "Tela Inicial - Swagger")

2. Depois da rota aberta, clique em *Try it out*:
![Tela Rota de Login - Aberta](https://raw.githubusercontent.com/phakiller/pharmacy_stock/master/images/swagger_login_route_try_it_out.png "Tela Rota de Login - Aberta")

3. Logo em seguida clique em, *Execute*:
    > Obs.: Não será necessário modificar o usuário e senha, este já é o usuário para testes.

![Tela Rota de Login - Execute](https://raw.githubusercontent.com/phakiller/pharmacy_stock/master/images/swagger_login_route_execute.png "Tela Rota de Login - Execute")

4. Role a página para baixo para pegar o token, ele estará no *Response Body*:
![Tela Rota de Login - Get Token](https://raw.githubusercontent.com/phakiller/pharmacy_stock/master/images/swagger_login_route_get_token.png "Tela Rota de Login - Get Token")

> O Token tem validade de 1 hora.

Para consumir as outras rotas basta repetir os passos **1, 2, 3,**  nas mesmas, utilizando o token que foi gerado na rota de Login.
![Tela - Rota de Customers](https://raw.githubusercontent.com/phakiller/pharmacy_stock/master/images/swagger_another_rote.png "Tela - Rota de Customers")

### Regras de uma Venda

- Após iniciar uma venda, a mesma só podera ser finalizada se tiver um ou mais items associados a ela e que não estejam cancelados.
- Depois que uma venda é Finalizada não é mais possível cancelar um item da mesma, só será possível cancelar a venda por completo.
- Um item só poderá ser vinculado a venda se o mesmo tiver estoque suficiente.