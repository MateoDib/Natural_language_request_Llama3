#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 00:38:38 2024

@author: mateo
"""

import os
import replicate

def create_prompt_for_llama3(user_request: str) -> str:
    """Crée un prompt pour Llama3 basé sur la requête de l'utilisateur."""
    return {
        "prompt": 
            f"Analyse la demande suivante pour générer une réponse structurée:\n\n"
            f"### Demande de l'utilisateur:\n***{user_request}***\n\n"
            f"### Instructions:\n"
            f"1. Identifier et résumer le contexte de la requête.\n"
            f"2. Déterminer le modèle de LLM approprié pour traiter la demande parmi les options suivantes: "
            f"meta/meta-llama-3-70b-instruct, meta/meta-llama-3-70b.\n"
            f"3. Spécifier les paramètres optimaux pour le modèle (min_tokens, max_tokens, temperature, top_p, top_k, presence_penalty, frequency_penalty).\n"
            f"4. Proposer un prompt spécifique qui sera utilisé pour la demande finale à envoyer à l'API.\n\n"
            f"### Considérations supplémentaires:\n"
            f"La demande est encadrée par *** et peut être suivie par des tableaux de données précédés par une ligne de 98 #.\n"
            f"Ta réponse contiendra uniquement les réponses attendues aux différentes demandes, sans explications."
            f"Ces tableaux serviront à comprendre la structure des données utilisées. Tu ne devras pas écrire dans ta réponse la partie data loading.\n\n"
            f"Toujours répondre dans la langue dans laquelle la question a été posée.\n\n"
            f"### Réponse attendue:\n"
            f"{{\n"
            f"  'contexte': 'Texte du contexte',\n"
            f"  'modèle choisi': 'Nom du modèle',\n"
            f"  'paramètres': {{\n"
            f"    'min_tokens': valeur, 'max_tokens': valeur, 'temperature': valeur, 'system_prompt': 'prompt_sytyeme', 'top_p': valeur, 'top_k': valeur, 'presence_penalty': valeur, 'length_penalty': valeur\n"
            f"  }},\n"
            f"  'prompt spécifique': 'Texte du prompt'\n"
            f"}}"
        , 'min_tokens': 0, 'max_tokens': 3000, 'temperature': 0.7, 'system_prompt': "You are a helpful assistant", 'top_p': 0.9, 'top_k': 0, 'presence_penalty': 0, 'length_penalty': 1}

def send_request_to_model(prompt: dict) -> str:
    """Envoie la requête structurée au modèle Llama3 et récupère la réponse."""
    try:
        replicate.api_token = os.getenv('REPLICATE_API_TOKEN')
        output = replicate.run('meta/meta-llama-3-70b-instruct', input=prompt)
        response_text = "".join(map(str, output))  # Convertir les parties de la réponse en une seule chaîne
        print("Réponse brute de l'API:", response_text)  # Imprimer la réponse brute pour débogage
        return response_text
    except replicate.exceptions.ReplicateError as e:
        print(f"Erreur de connexion avec l'API: {e}")
        return None
