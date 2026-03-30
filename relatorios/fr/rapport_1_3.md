# Rapport court — Séance 01, point 1.3

## Objectif

L’objectif du point 1.3 est d’implémenter un comportement très simple :
- le robot avance en ligne droite lorsqu’il n’y a pas d’obstacle devant lui,
- le robot tourne dans une direction aléatoire lorsqu’un obstacle est détecté devant lui.

## Modifications réalisées

Les changements ont été volontairement simples et localisés.

### Fichier modifié

- [tp_rob201/control.py](../../tp_rob201/control.py)

### Ce qui a été fait

Dans la fonction `reactive_obst_avoid()` de [tp_rob201/control.py](../../tp_rob201/control.py#L7-L38) :

1. lecture des distances du lidar avec `get_sensor_values()`,
2. lecture des angles du lidar avec `get_ray_angles()`,
3. sélection de la zone frontale du robot,
4. détection d’un obstacle frontal avec un seuil simple,
5. avance en ligne droite quand l’avant est libre,
6. rotation aléatoire à gauche ou à droite lorsqu’un obstacle est détecté,
7. maintien de la rotation pendant quelques cycles pour éviter que la direction change à chaque itération.

## Choix simples retenus

Pour éviter des changements brusques dans le code, une stratégie très simple a été choisie :

- cône frontal : environ $\pm 25^\circ$,
- seuil de détection : distance frontale minimale inférieure à `30`,
- vitesse avant quand la voie est libre : `0.9`,
- vitesse de rotation pendant l’évitement : `-0.8` ou `0.8`,
- durée de la rotation : entre `8` et `18` itérations de contrôle.

## Comportement attendu

Avec cette implémentation :
- s’il n’y a pas d’obstacle devant, le robot avance droit,
- s’il y a un obstacle devant, le robot arrête d’avancer,
- il choisit aléatoirement de tourner à gauche ou à droite,
- il maintient cette rotation pendant quelques instants avant de repartir.

## Ce qui n’a pas été modifié

Pour garder une solution simple :
- aucun changement structurel n’a été fait dans [tp_rob201/my_robot_slam.py](../../tp_rob201/my_robot_slam.py),
- aucun changement n’a été fait dans `TinySlam`,
- aucun comportement plus avancé de suivi de mur ou de mémoire complexe n’a été ajouté.

## Remarque

Cette étape implémente seulement une solution minimale pour le point 1.3, suffisante pour un premier comportement réactif de base.
