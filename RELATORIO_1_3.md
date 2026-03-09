# Relatório curto — Séance 01, item 1.3

## Objetivo

Le but du point 1.3 est d’implémenter un comportement très simple :
- le robot avance en ligne droite quand il n’y a pas d’obstacle devant lui,
- le robot tourne dans une direction aléatoire lorsqu’un obstacle est détecté devant lui.

## Modificações realizadas

As mudanças foram mantidas bem simples e localizadas.

### Arquivo modificado

- [tp_rob201/control.py](tp_rob201/control.py)

### O que foi feito

Na função `reactive_obst_avoid()` em [tp_rob201/control.py](tp_rob201/control.py#L7-L38):

1. leitura das distâncias do lidar com `get_sensor_values()`,
2. leitura dos ângulos do lidar com `get_ray_angles()`,
3. seleção apenas da zona frontal do robô,
4. detecção de obstáculo frontal com um seuil simples,
5. avanço reto quando a frente está livre,
6. rotação aleatória à esquerda ou à direita quando um obstáculo é detectado,
7. manutenção da rotação por alguns cycles pour éviter que la direction change à chaque itération.

## Choix simples retenus

Para evitar mudanças bruscas no código, foi escolhida uma estratégia muito básica:

- cône frontal : environ $\pm 25^\circ$,
- seuil de détection : distance frontale minimale inférieure à `80`,
- vitesse avant quand la voie est libre : `0.4`,
- vitesse de rotation pendant l’évitement : `-0.8` ou `0.8`,
- duração da rotação : entre `8` e `18` iterações de controle.

## Comportamento esperado

Com essa implementação:
- se não houver obstáculo à frente, o robô avança reto,
- se houver obstáculo à frente, o robô para de avançar,
- ele escolhe aleatoriamente virar para a esquerda ou para a direita,
- ele mantém essa rotação por alguns instantes antes de voltar a avançar.

## O que não foi mudado

Para manter a solução simples:
- nenhuma mudança estrutural foi feita em [tp_rob201/my_robot_slam.py](tp_rob201/my_robot_slam.py),
- nenhuma mudança foi feita em `TinySlam`,
- nenhum comportamento mais avançado de suivi de mur ou memória complexa foi adicionado.

## Observação

Esta etapa implementa apenas uma solution minimale pour le point 1.3, suficiente para um primeiro comportamento reativo básico.
