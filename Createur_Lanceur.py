#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 22:22:22 2024

@author: mateo
"""
print('d')
creer_lanceur("ezd","cds","rtbv","jil")
import os
import tkinter as tk
from tkinter import simpledialog

def creer_lanceur(api_token, csv_path, python_path, script_path):
    contenu = (
        "#!/bin/bash\n"
        f"REPLICATE_API_TOKEN='{api_token}'\n"
        f"CSV_PATH='{csv_path}"+"/'"
        f"\nPYTHON_PATH='{python_path}'\n"
        f"SCRIPT_PATH='{script_path}'\n"
        f"$PYTHON_PATH $SCRIPT_PATH\n"
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
        if len(contenu) < 5:
            raise ValueError("Le fichier lanceur.sh ne contient pas assez de lignes.")
        
        api_token = contenu[1].split("'")[1]
        csv_path = contenu[2].split("'")[1]
        python_path = contenu[3].split("'")[1]
        script_path = contenu[4].split("'")[1]
        
        return api_token, csv_path, python_path, script_path
    except FileNotFoundError:
        return None, None, None, None  # Si le fichier n'existe pas
    except IndexError:
        print("Erreur lors du parsing des paramètres. Vérifiez le format du fichier.")
        return None, None, None, None


def demander_infos():
    api_token_defaut, csv_path_defaut, python_path_defaut, script_path_defaut = lire_fichier_existant()

    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    
    api_token = simpledialog.askstring("Input", "Entrez votre clé API pour REPLICATE_API_TOKEN:", initialvalue=api_token_defaut or 'r8_', parent=root)
    csv_path = simpledialog.askstring("Input", "Entrez votre chemin pour csv_path:", initialvalue=csv_path_defaut or 'path/to/dossier/', parent=root)
    python_path = simpledialog.askstring("Input", "Entrez le chemin de votre environnement Python:", initialvalue=python_path_defaut or '/usr/bin/python3', parent=root)
    script_path = simpledialog.askstring("Input", "Entrez le chemin de votre script Python à exécuter:", initialvalue=script_path_defaut or '/Users/nom_user/Natural_language_Llama3_shortcut', parent=root)

    if api_token and csv_path and python_path and script_path:
        creer_lanceur(api_token, csv_path, python_path, script_path)

if __name__ == "__main__":
    demander_infos()
