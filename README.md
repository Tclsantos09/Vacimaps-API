# Vacimaps

Instruções para preparar o ambiente:
*  Criar um  ambiente virtual (venv)
    ```bash
    virtualenv venv
    ```
* Acessar o ambiente virtual **venv**
    ```bash
    source venv/bin/activate
    ```
* Saindo do ambiente virtual **venv**
    ```bash
    deactivate
    ```

* Rode o projeto
    * Executar:
    ```bash
    python run.py
    ```

### Endpoints: ###

```bash
GET - Retorna dados do usuário
/usuario/<id_usuario>
```
```bash
POST - Cadastra um usuário
/usuario

{
    "nome": "Usuário1", 
    "email": "usuario@email.com", 
    "senha": "1234"
}
```
```bash
PUT - Atualiza informações do usuário logado
/usuário

{
    "nome": "Usuário",
    "email": "usuario1@email.com",
}
```
```bash
POST - Enviar o email pra redefinir senha
/forgot_password

{ 
    "email": "usuario@email.com", 
}
```
```bash
POST - Redefinir a senha
/forgot_password

{ 
    "senha": "novaSenha", 
}
```
```bash
GET - Retorna dados da vacina do ususario
/usuario/vacina/<id_vacina>
```
```bash
POST - Cadastra uma vacina
/usuario/vacina

{
    "id_vacina": 1,
    "ds_local_vacina": "Postinho de mongaguá",
    "data_vacina": "2019-01-17"
}

```
```bash
PUT - Atualiza informações da vacina
/usuário/vacina/<id_vacina>

{
    "ds_local_vacina": "Postinho de mongaguá vila atlantica",
    "data_vacina": "2019-02-17"
}
```
```bash
DELETE - Deleta vacina do usuário
/usuário/vacina/<id_vacina>
```

### Instruções Login usando o Postman ###

```bash

POST - Gerar token e adicionar no Headers
/login

* Aba Body:

    Selecionar o tipo *Raw* e trocar de *Text* para *JSON (application/json)*

    {
    "email": "usuario@email.com", 
    "password": "1234"
    }

    clicar em send e copiar a token gerada

* Aba Headers:

    key -> token
    value -> Token gerada
```
