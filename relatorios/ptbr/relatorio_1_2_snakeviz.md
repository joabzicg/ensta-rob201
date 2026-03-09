# Relatório curto — Séance 01, item 1.2

## Comando executado

O profile analisado foi aberto com:

```bash
python3 -m snakeviz mon_script.prof
```

Arquivo de profile utilizado:
- [tp_rob201/mon_script.prof](../../tp_rob201/mon_script.prof)

## Objetivo do item 1.2

O item 1.2 pede para:
- executar o profiler no script principal,
- identificar as funções mais custosas em tempo,
- separar o que pertence às bibliotecas do que pertence ao código do projeto,
- determinar o que pode ser otimizado.

## Resultado geral observado no SnakeViz

A maior parte do tempo de execução está concentrada em funções do simulador e da pilha gráfica, especialmente:
- `simulator.run()`
- funções de `arcade` e `pyglet`
- renderização de janela (`flip`)
- atualização do simulador e sensores

Essas funções pertencem majoritariamente às bibliotecas usadas pelo projeto, então não são o melhor alvo de otimização neste trabalho.

## Funções do código do projeto que mais consomem tempo

Entre as funções editáveis do projeto, as mais relevantes no profile foram:

1. `control()` em `MyRobotSlam`
2. `control_tp1()` em `MyRobotSlam`
3. `compute()` em `TinySlam`
4. `reactive_obst_avoid()` em `control.py`

Valores extraídos do profile:

| Função | Arquivo | Tempo cumulativo aprox. | Tempo próprio aprox. |
|---|---|---:|---:|
| `control()` | [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py#L49) | 1.559 s | 0.000 s |
| `control_tp1()` | [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py#L55-L62) | 1.558 s | 0.035 s |
| `compute()` | [tp_rob201/tiny_slam.py](../../tp_rob201/tiny_slam.py#L62) | 1.515 s | 1.388 s |
| `reactive_obst_avoid()` | [tp_rob201/control.py](../../tp_rob201/control.py#L7) | 0.001 s | 0.001 s |

## Interpretação

A função mais custosa do código modificável é claramente `TinySlam.compute()`.

Isso é coerente com o conteúdo da função: ela realiza uma conversão polar → cartesiana com um laço Python sobre 3600 pontos, usando `cos` e `sin` a cada iteração e acumulando os pontos em uma lista.

Esse tipo de tratamento é tipicamente mais lento do que uma implementação vetorizada com NumPy.

Além disso, essa função não é necessária para o comportamento principal do TP1. Ela está presente sobretudo como suporte ao exercício de profiling.

## Conclusão para o item 1.2

A análise do SnakeViz mostra que:
- a maior parte do tempo é gasta nas bibliotecas de simulação e gráficos,
- entre as funções do projeto, `TinySlam.compute()` é o principal gargalo,
- `reactive_obst_avoid()` ainda tem impacto muito pequeno,
- a primeira função a tratar no código do projeto é `TinySlam.compute()`.

## Escolha de otimização adotada

Em vez de reescrever `TinySlam.compute()` nesta etapa, a solução escolhida foi retirar sua execução do ciclo de controle principal.

Com isso:
- a função lenta deixa de ser chamada a cada iteração,
- o comportamento do TP1 permanece o mesmo,
- o custo desnecessário no loop principal é removido.

Essa escolha é coerente com o item 1.2, pois o profiler permitiu identificar uma função custosa do código modificável e mostrou que ela podia ser retirada do fluxo principal sem impacto no comportamento esperado do robô.

## Observação

Este arquivo registra a análise do profile pedida no item 1.2 e a decisão de otimização associada: remover do fluxo principal a chamada da função mais custosa e não essencial.
