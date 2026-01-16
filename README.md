# Atividade-de-Topicos-2
Atividade de Tópicos em sistemas de informação 2

## Atenção

Instale todas as dependências com o comando:

```bash
pip install -r requirements.txt
```

## Construindo a imagem 

Abra o terminal e execute o comando:

```bash
docker build -t gerenciador-tarefas .
```

## Executando o container 

Logo em seguida, execute este comando:

```bash
docker run -d -p 5000:5000 --name app-tarefas gerenciador-tarefas
```

## Local host 

Depois digite no seu navegador 
"http://localhost:5000"