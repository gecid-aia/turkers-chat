## Setup da aplicação

Esse é um projeto Django clássico, então o processo é o tradicional:

```bash
# Clonar o repositório:
git clone git@github.com:gecid/turkers-chat.git

# Criar um virtualenv:
mkvirtualenv turkers-chat -p /usr/bin/python3.6

# Ativar o virtualenv
cd turkers-chat
cp env.example .env  # talvez você precisará editar o .env de acordo com suas configurações

# Instalar dependências
pip install -r requirements.txt
```

## Executando a aplicação

Para acessar a aplicação, será necessário criar um usuário administrativo com o comando:

```bash
python project/manage.py migrate
python project/manage.py createsuperuser
python project/manage.py runserver
```
