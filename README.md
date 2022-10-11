# Bix-challenge
Este é um repositório para resolução do desafio da BIX 

 O desafio consiste em reunir as informações de 3 fontes de dados distintas em uma única, que será acessada por um usuário através de uma Query. E para orquestrar este pipeline foi utilizado Apache Airflow como sugerido, PostgreSQL como Banco de Dados e Python como ferramenta de ingestão e tratamento dos dados.

# Desafio:

![Screenshot from 2022-10-11 15-37-23](https://user-images.githubusercontent.com/42456578/195172595-56e2d277-5c4f-474e-965b-0c2ca79b4eb5.png)

# Solução:
 A sequência de tarefas escolhida por mim está representada na figura abaixo. 
 
![Screenshot from 2022-10-11 15-39-41](https://user-images.githubusercontent.com/42456578/195173100-9cc8c2e7-21ee-451e-b4cd-2211add391b6.png)

 Foi observado que a API era responsável por retornar as informações sobre os funcionários e o _parquet.file_ foi responsável por retornar os nomes das categorias. Ambas as fontes de dados assossiavam o ID do PostgreSQL ao nome  do funcionário ou categoria. Com isso, eu concentrei todas as informações na _task_ "_transform_load_". É lá que acontece a junção das 3 fontes de informação. Todas as nuances dessas operações eu trato com um pouco mais de detalhes no video, porém todas as informações estão contidas nesta documentação.

 O Airflow foi configurado com MySQL para o **Database Backend**, assim eu pude alterar a configuração para executar atividades de forma paralela. Dessa forma o tempo de execução das tarefas categorias e funcionarios fica condicionada ao gargalo da operação, isso fica bem claro no gráfico em Gantt abaixo disponibilizado pelo próprio Airflow.

 ![Screenshot from 2022-10-11 15-53-56](https://user-images.githubusercontent.com/42456578/195175790-62f64ffb-8b27-4a6a-95c5-790324e994d9.png)

 
 Vale ressaltar que a task funcionario tem o maior tempo de execução devido a todos os requests para cada funcionário, uma possível melhoria em relação a performance (de acordo com a minha solução) seria fazer com que apenas uma requisição retornasse os valores de todos os funcionários.
 
E com isso um usuário já consegue executar Queries com o resultado final, abaixo segue algumas Queries de exemplo:

     SELECT funcionario, data_venda, venda FROM vendas_solution WHERE funcionario = 'Rob Carsson' ORDER BY data_venda DESC
     
![image](https://user-images.githubusercontent.com/42456578/195180098-9d2bdba7-b4ea-446e-95a7-e2b9aa92ec10.png)

     SELECT categoria, venda FROM vendas_solution WHERE  venda < 100000 LIMIT 5;


![Screenshot from 2022-10-11 16-22-44](https://user-images.githubusercontent.com/42456578/195180704-79902b3b-2029-4f6e-8729-0b7a214b0f48.png)

     SELECT funcionario, categoria, venda FROM vendas_solution WHERE funcionario = 'Helen Brolin' AND  categoria = 'Sportwear' 
     
![image](https://user-images.githubusercontent.com/42456578/195181049-a75276c3-d968-496a-8ede-046b9df6367a.png)


E pra exemplificar de uma maneira visual a solução deste desafio eu desenvolvi um dashboard utilizando Dash, Python, Plotly. Foi construindo um Data WareHouse simplificado no PostgreSQL da solução para criação deste dashboard, e depois realizei o deploy na Plataforma Cloud **Heroku**. Este dashboard pode ser acessado neste link: https://bix-challenge.herokuapp.com/

Vale resaltar também que o Banco de Dados da solução deste desafio foi hospedado na AWS RDS para ser acessado por vocês avaliadores, as credenciais de acesso são:

Host: bix-solution.c3ksuxpujoxa.sa-east-1.rds.amazonaws.com

Username: guilherme

password: |?7LXmg+FWL&,2( 

Port: 5432

obs: (mesma senha do desafio)
