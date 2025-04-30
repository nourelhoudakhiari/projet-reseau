# projet-reseau
Projet de Développement : Jeux en Ligne avec Agent DRL (tic_tac_toe)
Ce projet implémente un jeu de Tic-Tac-Toe avec plusieurs fonctionnalités :

Jeu contre une IA entraînée avec l'algorithme PPO (Proximal Policy Optimization)

Mode multijoueur en réseau via un serveur dédié

Deux interfaces graphiques :

Une interface Tkinter pour le jeu contre l'IA

Une interface Pygame pour le jeu local ou en réseau

Structure des fichiers
ai.py : Contient l'IA entraînée et l'interface Tkinter

client.py : Client Pygame pour jouer en local ou en réseau

game.py : Logique principale du jeu

server.py : Serveur pour le mode multijoueur en réseau

test_game.py : Tests unitaires pour la logique du jeu

Prérequis
Python 3.8+

Bibliothèques requises :

pip install numpy gymnasium stable-baselines3 tk pygame
Installation et exécution
1. Jeu contre l'IA (Tkinter)
Entraîner l'IA (peut prendre quelques minutes) :

python ai.py
(L'entraînement démarre automatiquement et l'interface graphique apparaît ensuite)

2. Jeu local (Pygame)
python client.py
3. Mode multijoueur en réseau
Serveur :
python server.py
Clients (2 instances) :
python client.py
(Le client se connecte automatiquement au serveur localhost)

Fonctionnalités avancées
IA
Utilise l'algorithme PPO de Stable Baselines3

Récompenses stratégiques pour encourager les coups intelligents

Système de fallback pour les coups invalides

Multijoueur
Serveur gérant plusieurs parties simultanées

Synchronisation de l'état du jeu en temps réel

Gestion des tours et des mouvements invalides

Interface Pygame
Affichage des symboles X/O stylisés

Ligne de victoire mise en évidence

Panel d'information sur l'état du jeu

Personnalisation
Vous pouvez modifier :

Les paramètres d'entraînement dans ai.py (learning_rate, etc.)

La taille de la grille et les couleurs dans client.py

Le port du serveur dans server.py

Tests
Pour lancer les tests unitaires :

python test_game.py

[BEN HARBI EMNA ]
