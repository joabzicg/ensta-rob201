# Relatório curto — Séance 01, item 1.3

## Objetivo

O objetivo do item 1.3 é implementar um comportamento bem simples:
- o robô avança em linha reta quando não há obstáculo à frente,
- o robô gira em uma direção aleatória quando um obstáculo é detectado à frente.

## Modificações realizadas

As mudanças foram mantidas simples e localizadas.

### Arquivo modificado

- [tp_rob201/control.py](../../tp_rob201/control.py)

### O que foi feito

Na função `reactive_obst_avoid()` em [tp_rob201/control.py](../../tp_rob201/control.py#L7-L38):

1. leitura das distâncias do lidar com `get_sensor_values()`,
2. leitura dos ângulos do lidar com `get_ray_angles()`,
3. seleção apenas da zona frontal do robô,
4. detecção de obstáculo frontal com um limiar simples,
5. avanço reto quando a frente está livre,
6. rotação aleatória à esquerda ou à direita quando um obstáculo é detectado,
7. manutenção da rotação por alguns ciclos para evitar que a direção mude a cada iteração.

## Escolhas simples adotadas

Para evitar mudanças bruscas no código, foi escolhida uma estratégia muito básica:

- cone frontal: aproximadamente $\pm 25^\circ$,
- limiar de detecção: distância frontal mínima inferior a `30`,
- velocidade à frente quando o caminho está livre: `0.9`,
- velocidade de rotação durante o desvio: `-0.8` ou `0.8`,
- duração da rotação: entre `8` e `18` iterações de controle.

## Comportamento esperado

Com essa implementação:
- se não houver obstáculo à frente, o robô avança reto,
- se houver obstáculo à frente, o robô para de avançar,
- ele escolhe aleatoriamente virar para a esquerda ou para a direita,
- ele mantém essa rotação por alguns instantes antes de voltar a avançar.

## O que não foi mudado

Para manter a solução simples:
- nenhuma mudança estrutural foi feita em [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py),
- nenhuma mudança foi feita em `TinySlam`,
- nenhum comportamento mais avançado de seguimento de parede ou memória complexa foi adicionado.

## Observação

Esta etapa implementa apenas uma solução mínima para o item 1.3, suficiente para um primeiro comportamento reativo básico.
