# Bix-challenge
Este é um repositório para resolução do desafio da BIX 

O desafio consiste em reunir as informações de 3 fontes de dados distintas em uma única, que será acessada por um usuário através de uma Query. E para orquestrar este pipeline foi utilizado Apache Airflow como sugerido, PostgreSQL como Banco de Dados e Python como ferramenta de ingestão e tratamento dos dados.

# Desafio:

![Screenshot from 2022-10-11 15-37-23](https://user-images.githubusercontent.com/42456578/195172595-56e2d277-5c4f-474e-965b-0c2ca79b4eb5.png)

1) A sequência de tarefas escolhida por mim está representada na figura abaixo. 
![Screenshot from 2022-10-11 15-39-41](https://user-images.githubusercontent.com/42456578/195173100-9cc8c2e7-21ee-451e-b4cd-2211add391b6.png)

Foi observado que aa API era responsável por retornar as informações sobre os funcionários e o _parquet.file_ foi responsável por retornar os nomes das categorias. Ambas as fontes de dados assossiavam o ID do PostgreSQL ao nome  do funcionário ou categoria. Com isso, eu concentrei todas as informações na _task_ "_transform_load_". É lá que acontece a junção das 3 fontes de informação.

