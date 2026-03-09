# Rapport court — Séance 01, point 1.2

## Commande exécutée

Le profil analysé a été ouvert avec :

```bash
python3 -m snakeviz mon_script.prof
```

Fichier de profil utilisé :
- [tp_rob201/mon_script.prof](../../tp_rob201/mon_script.prof)

## Objectif du point 1.2

Le point 1.2 demande de :
- exécuter le profiler sur le script principal,
- identifier les fonctions les plus coûteuses en temps,
- séparer ce qui appartient aux bibliothèques de ce qui appartient au code du projet,
- déterminer ce qui peut être optimisé.

## Résultat général observé dans SnakeViz

La plus grande partie du temps d’exécution est concentrée dans des fonctions du simulateur et de la pile graphique, notamment :
- `simulator.run()`
- des fonctions de `arcade` et `pyglet`
- le rendu de la fenêtre (`flip`)
- la mise à jour du simulateur et des capteurs

Ces fonctions appartiennent majoritairement aux bibliothèques utilisées par le projet, donc elles ne sont pas la meilleure cible d’optimisation dans ce travail.

## Fonctions du code du projet qui consomment le plus de temps

Parmi les fonctions modifiables du projet, les plus importantes dans le profil sont :

1. `control()` dans `MyRobotSlam`
2. `control_tp1()` dans `MyRobotSlam`
3. `compute()` dans `TinySlam`
4. `reactive_obst_avoid()` dans `control.py`

Valeurs extraites du profil :

| Fonction | Fichier | Temps cumulé approx. | Temps propre approx. |
|---|---|---:|---:|
| `control()` | [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py#L49) | 1.559 s | 0.000 s |
| `control_tp1()` | [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py#L55-L62) | 1.558 s | 0.035 s |
| `compute()` | [tp_rob201/tiny_slam.py](../../tp_rob201/tiny_slam.py#L62) | 1.515 s | 1.388 s |
| `reactive_obst_avoid()` | [tp_rob201/control.py](../../tp_rob201/control.py#L7) | 0.001 s | 0.001 s |

## Interprétation

La fonction la plus coûteuse du code modifiable est clairement `TinySlam.compute()`.

C’est cohérent avec le contenu de la fonction : elle réalise une conversion polaire → cartésienne avec une boucle Python sur 3600 points, en utilisant `cos` et `sin` à chaque itération et en accumulant les points dans une liste.

Ce type de traitement est typiquement plus lent qu’une implémentation vectorisée avec NumPy.

De plus, cette fonction n’est pas nécessaire pour le comportement principal du TP1. Elle est surtout présente comme support à l’exercice de profiling.

## Conclusion pour le point 1.2

L’analyse de SnakeViz montre que :
- la plus grande partie du temps est dépensée dans les bibliothèques de simulation et de graphisme,
- parmi les fonctions du projet, `TinySlam.compute()` est le principal goulot d’étranglement,
- `reactive_obst_avoid()` a encore un impact très faible,
- la première fonction à traiter dans le code du projet est `TinySlam.compute()`.

## Choix d’optimisation retenu

Au lieu de réécrire `TinySlam.compute()` à cette étape, la solution choisie a été de retirer son exécution de la boucle principale de contrôle.

Avec cela :
- la fonction lente n’est plus appelée à chaque itération,
- le comportement du TP1 reste inchangé,
- le coût inutile dans la boucle principale est supprimé.

Ce choix est cohérent avec le point 1.2, car le profiler a permis d’identifier une fonction coûteuse du code modifiable et a montré qu’elle pouvait être retirée du flux principal sans impact sur le comportement attendu du robot.

## Remarque

Ce fichier enregistre l’analyse du profil demandée au point 1.2 ainsi que la décision d’optimisation associée : retirer du flux principal l’appel de la fonction la plus coûteuse et non essentielle.
