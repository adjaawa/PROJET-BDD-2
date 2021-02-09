# ProjetConceptionSGBD

Afin de faciliter le déploiement d’applications embarquées en Client/Serveur sur des plateformes Raspberry avec un environnement Dockerisé, il est demandé de concevoir et implémenter un moteur de base de données Multi- utilisateur et Réseau.
<br/>
- L’écoute active de connexions entrantes par des sockets et sur le port 8888 <br/>
- Le formatage physique des données dans des fichiers JSON (1 BDD = 1 fichier JSON) <br/>
- Le support d’interactions grâce à du SQL avec les données (LDD, LED et LMD) avec une sortie tabulaire <br/>
- Le support d’interactions grâce un service REST unique et avec un langage de requête de votre choix sur le port 8889 <br/>
- Le support d’interactions transactionnelles de façon optionnelle <br/>
- La gestion de l’authentification (pas de gestion des privilèges) <br/>
