# Traducteur de Langage naturel en R avec Llama3 (système Unix ou Linux y compris macOS)

Ce projet contient un script Python qui permet de traduire une demande en langage naturel en code directement via un raccourci.

## Prérequis

Avant de commencer, assurez-vous d'avoir Python installé sur votre machine. Ce script a été testé avec Python 3.8 et supérieur. Vous aurez également besoin d'une clé API de Replicate, que vous pouvez obtenir en vous inscrivant sur leur [site officiel](https://replicate.com).

## Installation

Pour installer le code Python et les bibliothèques nécessaires, suivez les étapes ci-dessous :

1. **Cloner le dépôt**
   
   Ouvrez un terminal et exécutez la commande suivante pour télécharger les fichiers nécessaires :
   ```bash
   git clone https://github.com/MateoDib/Natural_language_Llama3_shortcut.git
   ```
   
2. **Vérifier le téléchargement des documents**

   Pour vérifier que les documents sont présents (si la sortie n'est pas vide, c'est que tout va bien), exécutez les commandes suivantes dans le terminal :
   ```bash
   cd Natural_language_Llama3_shortcut
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

   Copiez ce chemin et ajoutez-y "/Natural_language_to_R.py" de manière à construire le chemin vers le code Python qui nous sera utile plus tard. Cela devrait ressembler à ceci :
   ```bash
   /Users/nom_user/Natural_language_Llama3_shortcut/Natural_language_to_R.py
   ```
   Vous pouvez simplement le garder de côté, nous en aurons besoin par la suite.

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



## Configurer la clé API (cette étape n'est pas nécessaire

   Configurez votre clé API en créant la variable d'environnement REPLICATE_API_TOKEN. Pour cela, il va falloir modifier votre fichier .bashrc ou .zshrc. La modification est ainsi "permanente", c'est-à-dire que vous aurez toujours accès à cette variable, jusqu'à modification/suppression.

1. **Ouvrir le terminal sur votre machine**

   Appuyez sur Command + Espace, puis écrivez "Terminal" dans la barre de recherche. Et enfin tapez sur Entrer.


Vous allez maintenant devoir éditer le fichier .bashrc pour les utilisateurs de Bash ou .zshrc pour les utilisateurs de Zsh. Pour réaliser correctement cette tâche suivez les étapes suivantes :

2. **Connaître l'interpréteur de commandes**

   Pour savoir si vous êtes en Bash ou Zsh exécutez la commande suivante dans le terminal :
    ```bash
   echo $SHELL
   ```

3. **Ouverture du fichier .bashrc ou .zshrc**
    En fonction de la sortie précédent, exécuté :
   ```bash
   # Pour les utilsateurs de Bash (.bashrc)
   nano ~/.bashrc
   ```
   ```bash
    # Pour les utilisateurs de Zsh (.zshrc)
   nano ~/.zshrc
   ```

4. **Définir la clé API**

   Ajouter la ligne suivante à la fin du fichier (la configuration est étonante mais faites-vous confiance, la fin du fichier c'est juste en bas, vous avez simplement à copier la ligne suivante):
   ```bash
   # Assurez-vous de remplacer 'votre_clé_api' par votre clé API de Replicate, tout en gardant les guillements comme tels.
   export REPLICATE_API_TOKEN='votre_clé_api'
   ```
   
5. **Sauvegarder le fichier et quitter l'éditeur**

Sauvegardez le fichier et quittez l'éditeur en appuyant sur Control+O (c'est un O comment dans ouvrir), puis Enter, et quitter avec Ctrl+X.

6. **Appliquer les modifications**

   Pour être sûr que les  modifications ont bien été prises en compte exécutez les commandes suivantes sur le terminal toujours :
   ```bash
   # Pour les utilisateurs de Bash (.bashrc)
   source ~/.bashrc
   ```
   
   ```bash
   # Pour les utilisateurs de Zsh (.zshrc)
   source ~/.zshrc
   ```
7. **Vérifier la création de la variable d'environnement**
   
   Vérifiez que la variable d'environnement s'est bien enregistrée en fermant le terminal puis en l'ouvrant de nouveau pour exécuter la commande suivante
   ```bash
   echo $REPLICATE_API_TOKEN
   ```
Si la valeur de votre clé apparait, c'est que la variable d'environnement s'est bien enregistrée.

En ajoutant cette ligne à votre fichier .bashrc ou .zshrc, vous configurez votre clé API pour être automatiquement disponible dans toutes les nouvelles sessions de terminal, ce qui facilite l'utilisation de scripts et d'outils nécessitant cette clé sans avoir à la configurer à chaque fois.


## Si vous ne souhaitez pas définir la clé API en tant que variable d'environnement

  Vous devrez simplement spécifier la clé API via la commande suivante lors de l'écriture du code dans le shell afin de créer le raccourci :
  ```bash
   REPLICATE_API_TOKEN='votre_clé_api' /Users/nom_user/votre_chemin_vers_environnement_python/python3 /Users/nom_user/Natural_language_Llama3_shortcut/Natural_language_to_R.py
   ```
   À la place du code suivant :
   ```bash
   /Users/nom_user/votre_chemin_vers_environnement_python/python3 /Users/nom_user/Natural_language_Llama3_shortcut/Natural_language_to_R.py
   ```



## Créez un raccourci vers le script Python : 

Pour vous permettre d'exécuter facilement le script Python et donc d'avoir un raccourci, vous pouvez créer un raccourci à partir de l'application Raccourcis de Mac (disponible par défaut normalement). Voici les étapes à suivre pour cela :

1. **Ouvrez l'application Raccourcis sur votre Mac.**

2. **Créez un nouveau raccourci en cliquant sur le bouton "+", en haut à droite.**

3. **Dans la barre de recherche à droite, tapez "Shell" et l'option "Exécuter un script Shell" apparaîtra. Sélectionnez-la.**

4. **Dans la zone de texte du script Shell, supprimez le texte apparant s'il y en a un.**

5. **Entrez la commande Python pour exécuter votre script dans le script Shell**
   
   En remplaçant les chemins de l'environnement python et du script par ceux adaptés à vos chemins, a commande devrait ressembler à ceci :
   ```bash
   /Users/nom_user/votre_chemin_vers_environnement_python/python3 /Users/nom_user/Natural_language_Llama3_shortcut/Natural_language_to_R.py
   ```

   Pour savoir quoi mettre à la place de /Users/nom_user/votre_chemin_vers_environnement_python/python3, lancez la commande   suivante sur votre terminal :
   ```bash
   which python3
   ```
   Et si cela ne vous ressort pas un chemin similaire, exécutez la commande suivante :
   ```bash
   which python
   ```

6. **Donnez un nom à votre raccourci et enregistrez-le.**
   
   Vous pouvez l'épingler à la barre des menus afin de cliquer dessus lorsque vous souhaitez l'utiliser.

7. **Erreur de reconnaissance de la clé API?**

   Si vous êtes sur que votre clé fonctionne mais qu'une erreur apparait lors du lancement du raccourci, tentez de modifier le script du shell dans le raccourci que vous avez créé comme suit :
   ```bash
   REPLICATE_API_TOKEN='votre_clé_api' /Users/nom_user/votre_chemin_vers_environnement_python/python3 /Users/nom_user/Natural_language_Llama3_shortcut/Natural_language_to_R.py
   ```

   Cela devrait maintenant fonctionne correctement.

Voilà, vous pouvez maintenant copier un texte, cliquer sur votre raccourci, et coller le texte corrigé n'importe où.



## Mise à jour 

Si vous avez déjà effectué toutes ces étapes auparavant mais que vous souhaitez simplement avoir la nouvelle versionne du repository, exécutez les commandes suivantes dans le terminal :
   ```bash
   # Veillez à remplacer le chemin par le votre
   # Pour rappel vous pouvez connaître ce chemin simplement en exécutant "cd Natural_language_to_R"
   cd /Users/nom_user/Natural_language_Llama3_shortcut
   ```
   Puis :
   ```bash
   git pull origin main
   ```

Voilà ! La mise-à-jour est faite.
