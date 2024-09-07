#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 04:35:20 2024

@author: mateo
"""

import os
import tkinter as tk
from tkinter import simpledialog

def creer_lanceur(api_token, csv_path, python_path, script_path):
    contenu = (
        f"#!/bin/bash\n"
        f"REPLICATE_API_TOKEN='{api_token}' CSV_PATH='{csv_path}' "
        f"{python_path} {script_path}\n"
    )
    fichier_nom = "lanceur.sh"
    with open(fichier_nom, "w") as fichier:
        fichier.write(contenu)

    chemin_complet = os.path.abspath(fichier_nom)
    print(f"Fichier '{fichier_nom}' créé ou modifié avec succès.")
    print(f"Chemin complet du fichier : {chemin_complet}")

def lire_fichier_existant():
    try:
        with open("lanceur.sh", "r") as fichier:
            contenu = fichier.readlines()
        api_token = contenu[1].split("'")[1]  # Extraire la valeur entre les guillemets
        csv_path = contenu[1].split("'")[3]  # Extraire la valeur entre les guillemets
        python_path = contenu[1].split()[2]  # Extraire le chemin de l'environnement Python
        script_path = contenu[1].split()[3]  # Extraire le chemin du script Python
        return api_token, csv_path, python_path, script_path
    except FileNotFoundError:
        return None, None, None, None  # Si le fichier n'existe pas, renvoyer None pour chaque variable
    except IndexError:
        return None, None, None, None  # Gestion de l'erreur si les lignes ne sont pas comme prévu

def demander_infos():
    api_token_defaut, csv_path_defaut, python_path_defaut, script_path_defaut = lire_fichier_existant()

    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    
    api_token = simpledialog.askstring("Input", "Entrez votre clé API pour REPLICATE_API_TOKEN:", initialvalue=api_token_defaut or '', parent=root)
    csv_path = simpledialog.askstring("Input", "Entrez votre chemin pour csv_path:", initialvalue=csv_path_defaut or '', parent=root)
    python_path = simpledialog.askstring("Input", "Entrez le chemin de votre environnement Python:", initialvalue=python_path_defaut or '/usr/bin/python3', parent=root)
    script_path = simpledialog.askstring("Input", "Entrez le chemin de votre script Python à exécuter:", initialvalue=script_path_defaut or '', parent=root)

    if api_token and csv_path and python_path and script_path:
        creer_lanceur(api_token, csv_path, python_path, script_path)

if __name__ == "__main__":
    demander_infos()
