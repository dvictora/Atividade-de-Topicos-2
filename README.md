# Atividade-de-Topicos-2
Atividade de Tópicos em sistemas de informação 2

## Atenção

Instalem todas as dependencias com o comando

``` 
pip install -r requirements.txt
```

## Construindo a imagem 

abral o terminal e execute o comando

```
docker build -t gerenciador-tarefas .
```

## Executando o container 

logo em seguida coloque este comando 

```
docker run -d -p 5000:5000 --name app-tarefas gerenciador-tarefas
```

## Local host 

Depois digite no seu navegador 
"http://localhost:5000"