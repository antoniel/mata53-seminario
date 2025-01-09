Explicação dos inputs

Linha 1: 5 10 4
	1.	5: Quantidade de vértices (ou nós) no grafo.
	2.	10: Quantidade de tarefas/passageiros que serão atendidos (ou arcos de origem-destino).
	3.	4: Capacidade do veículo (ou outro parâmetro de limitação, como número de assentos).

Em alguns contextos, esse último número também pode representar outra restrição do problema (como quantidade de veículos), mas comumente é interpretado como capacidade.

Próximas 5 linhas (matriz de custos ou distâncias)

0 215 203 200 173
215 0 127 237 126
203 127 0 128 194
200 237 128 0 245
173 126 194 245 0

	•	Matriz ￼ de distâncias (ou custos) entre os 5 nós.
	•	Cada linha ￼ e coluna ￼ representa o custo de ir do nó ￼ ao nó ￼.
	•	Como é simétrica (ex.: 215 em ￼ e ￼), denota distâncias iguais nos dois sentidos.

Próximas 5 linhas (matriz de tempos)

0 177 196 234 200
177 0 223 199 151
196 223 0 113 102
234 199 113 0 194
200 151 102 194 0

	•	Outra matriz ￼, agora representando tempo de deslocamento de um nó ao outro.
	•	Mesmo esquema: linha ￼, coluna ￼ indica quanto tempo se leva de ￼ a ￼.

Próximas 10 linhas (dados das tarefas/passageiros)

0 3 404 875 590 885
0 3 437 747 590 885
1 3 488 563 295 590
1 3 490 782 590 885
2 3 434 232 590 885
2 1 480 660 0 295
3 1 664 740 0 295
3 0 721 497 590 885
4 3 765 544 0 295
4 2 587 298 0 295

Normalmente, cada linha descreve um passageiro (ou tarefa) a ser atendido, com campos que podem representar:
	1.	Origem (nó de onde parte o passageiro).
	2.	Destino (nó para onde ele vai).
	3.	Início da janela de tempo de embarque (pickup earliest).
	4.	Fim da janela de tempo de embarque (pickup latest).
	5.	Início da janela de tempo de desembarque (dropoff earliest).
	6.	Fim da janela de tempo de desembarque (dropoff latest).

Por exemplo, na primeira linha 0 3 404 875 590 885:
	•	Origem = nó 0
	•	Destino = nó 3
	•	Pode embarcar entre 404 e 875 (janela de pickup)
	•	Deve desembarcar entre 590 e 885 (janela de dropoff)

Últimas 5 linhas (coordenadas dos nós)

0 0
195 26
94 32
93 53
81 27

	•	Cada linha corresponde às coordenadas (x, y) de um nó.
	•	A primeira linha 0 0 é o nó 0 com coordenadas ￼.
	•	A segunda linha 195 26 é o nó 1 com coordenadas ￼ e assim por diante.

Essas coordenadas podem ser usadas para:
	•	Exibir ou plotar o mapa dos nós.
	•	Calcular distância se, por algum motivo, a matriz de distâncias não for diretamente fornecida (embora aqui a matriz já esteja dada).