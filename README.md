
# Projeto LuizaLabs

## Requisitos
Esse projeto utiliza [Falcon Web Framework](https://falcon.readthedocs.io), [SQLAlchemy](https://docs.sqlalchemy.org) e qualquer banco de dados relacional. Recomendo o [PostgreSQL](https://www.postgresql.org).

Confira se o [_Python 3.7.x_](https://www.python.org/downloads/) está instalado. Recomendo a utilização do _virtualenv_.
Caso prefira utilizar o Docker, garanta que o mesmo esteja instalado. O uso do [docker-compose](https://docs.docker.com/compose/install/) é altamente recomendado.


## Preparação do ambiente

### Variáveis de ambiente
Caso rodar o projeto localmente ou ambiente virtual, deve-se definir as configurações do banco de dados:
```
export DATABASE_PROTOCOL=<protocolo ou "postgresql+psycopg2" caso for utilizar PostgreSQL>
export DATABASE_HOST=<host do banco de dados>
export DATABASE_PORT=<port>
export DATABASE_NAME=<nome da base>
export DATABASE_USERNAME=<usuário do banco>
export DATABASE_PASSWORD=<senha>
```
Lembrando que se utilizar outro banco de dados, deve-se adicionar as dependencias necessárias no requirements.txt.


Caso for rodar o projeto em Docker e quiser utilizar um banco existente, deve-se editar o arquivo `docker-compose.yml`, na sessão `services.app.environment` os items relacionados às configurações acima.
Além disso, pode comentar a sessão correspondente a `services. postgres`.

### Instalação das dependências
Caso rodar o projeto localmente, digite no terminal:

```
$ pip install -r requirements.txt
```
Caso utilizar o PostgreSQL como banco de dados relacional e tiver problemas com a instalação das dependencias, dê uma olhada no [FAQ Oficial](http://initd.org/psycopg/docs/faq.html#faq-compile).



Caso utilizar o docker, basta utilizar o utilitário _make_:
```
$ make build
```

### Configurações iniciais
Caso rodar o projeto localmente, será necessário executar as migrações:
```
$ python -c "from src.db.manager import setup_database; setup_database()"
```

Caso utilizar Docker:
```
$ make migrate
```


### Rodando o projeto
Caso a instalação foi em ambiente local, basta executar:
```
$ gunicorn src.wsgi:app
```

Caso você estiver utilizando o Docker:
```
$ make run
```

Esse processo irá iniciar a aplicação e irá disponibiliza-la no endereço [http://localhost:8000](http://localhost:8000).

## Rodando os testes
A aplicação está coberta por testes de integração. O runner utilizado é o _pytest_.
Para rodar os testes, será preciso instalar as dependências de desenvolvimento:
```
$ pip install -r requirements-dev.txt```
```

Para executar os testes em uma instalação local:
```
$ pytest
```

Caso queria utilziar o Docker para rodar os testes, basta executar:
```
$ make test
```

## Documentação da API
A documentação da API está localizada em [./docs/API_specification](./docs/API_specification.md)


## TODO
A decisão de utilizar essas ferramentas partiu de 2 pontos: performance e aprender mais sobre essas tecnologias.
Por isso, alguns pontos ficaram pendentes e precisam ser melhorados ou mesmo implementados.

    - Autenticação e autorização de verdade. A estrutura está preparada, mas é necessário implementar um serviço de autorização existente ou criar uma estrutura de autenticação e geração de tokens de autorização;
    - Melhorar a consulta e estruturação dos dados de produtos da API externa. Algumas arquiteturas possíveis:
        - Consulta assíncrona para as requests. Eu até implementei assim utilizando asyncio e aiohttp, mas desisti pois a API de produtos não aguentou (sorry hahahaha);
        - Utilização de cache da resposta (não muito efetivo, mas diminuiria o tempo de persistência dos dados, evitando problemas com atualizações);
        - Armazenamento dos dados de produtos. A resposta para o usuário da API seria mais rápida, além de evitar sobrecarga na API de produtos, porém dependeria de uma arquitetura de webkooks ou alguma estrutura de fila para atualizar os dados ou alguma rotina para atualizar a lista de produtos;
    - Implementar alguma estrutura de serialização ou schemas;
    - Ferramenta de migração dos modelos de dados do SQLAlchemy;
    - Implementar testes unitários;
    - Implementar o campo UUID para externalizar os objetos e evitar expor o ID interno;

