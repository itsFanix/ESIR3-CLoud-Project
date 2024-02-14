# **Projet: Pipeline de traitement de vidéo**

Ce projet est conçue pour traiter des vidéos à grande échelle de manière efficace et modulaire. L'architecture est basée sur des microservices déployés dans des conteneurs Docker, ainsi que sur des services cloud d'Amazon Web Services (AWS) pour le stockage et le déploiement.

## **Répertoires des Applications**
Dans ce projet, chaque composant de l'architecture est organisé dans des répertoires distincts, facilitant le développement, le déploiement et la gestion du système. Voici une brève description de chaque répertoire :

### ***DownscaleApp***
Ce répertoire contient l'application responsable de la réduction de la résolution ou de la taille des vidéos pour les préparer au traitement. Il s'agit d'un microservice Dockerisé conçu pour être déployé sur un orchestrateur de conteneurs.

### ***languageDetectionApp***
Ce répertoire héberge l'application chargée d'identifier la langue présente dans les vidéos ainsi que générer les sous-titrages. Il s'agit d'un microservice Dockerisé qui utilise un algorithme de traitement du langage naturel pour cette tâche spécifique.

### ***animaldetectAppp***
Ce répertoire contient l'application responsable de la détection des animaux dans les vidéos et de les afficher dans un tableau avec leur probabilité d'exactitude d'apparition. Il s'agit d'un service de reconnaissance visuelle en se basant sur les modèles d'apprentissage automatique afin d'identifier les animaux.

### ***videoViewerApp***
Ce répertoire se concentre sur la récupération et la manipulation des vidéos ainsi que de leurs métadonnées telles que la durée, le langage, les sous-titres et les animaux détectés dans la vidéo à partir du stockage AWS . 
