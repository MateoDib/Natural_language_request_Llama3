# Environmental News AI News Checker (système Unix ou Linux y compris macOS)

Ce projet tente de mobiliser et combiner la littérature scientifique et l’IA afin de lutter contre la désinformation. 
En particulier, nous tentons d’entrainer un modèle d’intelligence artificielle sur la littérature de l’économie de l’environnement afin qu’il puisse vérifier les articles de presse écrite.

## Prérequis

Avant de commencer, assurez-vous d'avoir Python installé sur votre machine. Ce script a été testé avec Python 3.8 et supérieur. 
Vous aurez également besoin d'une clé API de Replicate, que vous pouvez obtenir en vous inscrivant sur leur [site officiel](https://replicate.com).

## Installation du projet GitHub

Pour installer le code Python et les bibliothèques nécessaires, suivez les étapes ci-dessous :

1. **Cloner le dépôt**
   
   Ouvrez votre terminal et exécutez la commande suivante pour télécharger les fichiers nécessaires :
   ```bash
   git clone https://github.com/MateoDib/Natural_language_request_Llama3.git
   ```
   
2. **Vérifier le téléchargement des documents**

   Pour vérifier que les documents sont présents (si la sortie n'est pas vide, c'est que tout va bien), exécutez les commandes suivantes dans le terminal :
   ```bash
   cd Natural_language_request_Llama3
   ```
   Puis :
   ```bash
   ls
   ```

3. **Copier le chemin d'accès au code**
   Tant que vous y êtes, récupérez le chemin vers le dossier en exécutant la commande suivante à la suite dans le terminal :
   ```bash
   pwd
   ```

   Copiez ce chemin et enregistrez-le quelque part afin d’y avoir facilement accès plus tard. 
Cela devrait ressembler à ceci :
   ```bash
   /Users/nom_user/Natural_language_request_Llama3/Natural_language_to_R.py
   ```

4. **Installer les dépendances dans le dossier du projet**

   Toujours dans le terminal, exécutez la commande suivante :
   ```bash
   pip install -r requirements.txt
   ```

5. **Installer `xsel` (pour les utilisateurs Linux uniquement)**

   Si vous êtes sur Linux, installez `xsel` avec la commande suivante :
   ```bash
   sudo apt-get update && sudo apt-get install -y xsel
   ```

Vous avez dorénavant téléchargé tout ce qu'il fallait. Vous pouvez continuer la configuration.


## Créez un raccourci vers le script Python : 

Pour vous permettre d'exécuter facilement le script Python et donc d'avoir un raccourci, vous pouvez créer un raccourci à partir de l'application Raccourcis de Mac (disponible par défaut normalement). Voici les étapes à suivre pour cela :

1. **Ouvrez l'application Raccourcis sur votre Mac.**

2. **Créez un nouveau raccourci en cliquant sur le bouton "+", en haut à droite.**

3. **Dans la barre de recherche à droite, tapez "Shell" et l'option "Exécuter un script Shell" apparaîtra. Sélectionnez-la.**

4. **Dans la zone de texte du script Shell, supprimez le texte apparent s'il y en a un.**

5. **Entrez la commande Python pour exécuter votre script dans le script Shell**
   
	En remplaçant le chemin par ceux adaptés à votre chemin, la commande devrait ressembler à ceci :
   ```bash
   chmod +x /Users/nom_user/lanceur.sh && ./lanceur.sh
   ```

	Pour savoir quoi mettre à la place de /Users/nom_user/votre_chemin_vers_environnement_python/python3, lancez la commande   suivante sur votre terminal :
   ```bash
   which lanceur.sh
   ```

6. **Vérifier le Shell et la sortie **

	L’option ‘Shell’ présente différentes options. Pour savoir laquelle choisir parmi les options « sh » (pour bash) ou « zsh », exécutez le code suivant :
   ```bash
   echo $SHELL
    ```

	De plus, pour l’option « Transmettre l’entrée », il faudra choisir l’option « vers stdin ».

Si la sortie est « /bin/zsh », vous devrez renseigner « zsh », si c’est « /bin/bash », alors vous devrez choisir « sh ».


7. ** Rattacher le raccourci à une commande clavier**

	Afin de relier le raccourci à une commande clavier, vous pouvez cliquer sur le « i » en haut à droite et de nouvelles options apparaîtront, dont l’option « Ajouter un raccourci clavier ». Avant d’entrer un raccourci clavier, veiller à ce que ce raccourci n’existe pas déjà pour une autre action.

8. **Donnez un nom à votre raccourci et enregistrez-le.**
   
   Vous pouvez l'épingler à la barre des menus afin de cliquer dessus lorsque vous souhaitez l'utiliser.



## Configurer les paramètres afin de pouvoir utiliser l’IA News Checker

  Afin de pouvoir utiliser l’IA News Checker, il vous faudra d’abord renseigner votre clé API Replicate, ainsi que les différents chemins d’accès aux dossiers que vous venez d’installer suite au téléchargement du projet GitHub. Pour enregistrer les paramètres nécessaires, et pour pouvoir par la suite les modifier, il est utile de créer un 


1. **Ouvrez l'application Raccourcis sur votre Mac.**

2. **Créez un nouveau raccourci en cliquant sur le bouton "+", en haut à droite.**

3. **Dans la barre de recherche à droite, tapez "Shell" et l'option "Exécuter un script Shell" apparaîtra. Sélectionnez-la.**

4. **Dans la zone de texte du script Shell, supprimez le texte apparent s'il y en a un.**

5. **Entrez la commande Python pour exécuter votre script dans le script Shell**
   
   En remplaçant le chemin par ceux adaptés à votre chemin, la commande devrait ressembler à ceci :
   ```bash
/opt/anaconda3/bin/python3 /Users/nom_user/Natural_language_request_Llama3/Createur_lanceur.py
   ```

   Pour savoir quoi mettre à la place de /Users/nom_user/votre_chemin_vers_environnement_python/python3, lancez la commande   suivante sur votre terminal :
   ```bash
   which python3
   ```
Ou, si cela ne fonctionne pas :
   ```bash
   which python
   ```

   Pour savoir quoi mettre à la place de /Users/nom_user/Natural_language_request_Llama3/Createur_lanceur.py, lancez la commande   suivante sur votre terminal :
   ```bash
   cd Natural_language_request_Llama3
   ```
Puis :
```bash
   pwd 
   ```

Vous obtenez ainsi le chemin vers Createur_lanceur.py que vous devrez remplacer dans le chemin.


6. **Vérifier la sortie **

	L’option ‘Shell’ présente différentes options. Pour savoir laquelle choisir parmi les options « sh » (pour bash) ou « zsh », exécutez le code suivant :
   ```bash
   echo $SHELL
    ```

	De plus, pour l’option « Transmettre l’entrée », il faudra choisir l’option « vers stdin ».

Si la sortie est « /bin/zsh », vous devrez renseigner « zsh », si c’est « /bin/bash », alors vous devrez choisir « sh ».


7. ** Rattacher le raccourci à une commande clavier**

	Afin de relier le raccourci à une commande clavier, vous pouvez cliquer sur le « i » en haut à droite et de nouvelles options apparaîtront, dont l’option « Ajouter un raccourci clavier ». Avant d’entrer un raccourci clavier, veiller à ce que ce raccourci n’existe pas déjà pour une autre action.


8. **Donnez un nom à votre raccourci et enregistrez-le.**
   
   Vous pouvez l'épingler à la barre des menus afin de cliquer dessus lorsque vous souhaitez l'utiliser.
Maintenant, vous devez lancer une première fois le Raccourci pour enregistrer votre clé API et les chemins d’accès.


## Configuration terminée

Voilà, vous pouvez maintenant copier un texte, cliquer sur votre raccourci, et coller le texte corrigé n'importe où.


## Mise à jour du projet 

Si vous avez déjà effectué toutes ces étapes auparavant mais que vous souhaitez simplement avoir la nouvelle version du repository, exécutez les commandes suivantes dans le terminal :
   ```bash
   # Veillez à remplacer le chemin par le votre
   # Pour rappel vous pouvez connaître ce chemin simplement en exécutant "cd Natural_language_to_R"
   cd /Users/mateo/Natural_language_request_Llama3
   ```
   Puis :
   ```bash
   git pull origin main
   ```

Voilà ! La mise-à-jour est faite.
