import re

def parse_response_with_regex(response_text: str):
    """ Utilise des expressions régulières pour extraire les informations de la réponse textuelle. """
    try:
        # Dictionnaire pour stocker les paramètres extraits
        params_dict = {}
        
        # Regex pour extraire les paramètres
        patterns = {
            'min_tokens': r"min_tokens=(\d+)",
            'max_tokens': r"max_tokens=(\d+)",
            'temperature': r"temperature=([0-9\.]+)",
            'top_p': r"top_p=([0-9\.]+)",
            'top_k': r"top_k=(\d+)",
            'presence_penalty': r"presence_penalty=([0-9\.]+)",
            'frequency_penalty': r"frequency_penalty=([0-9\.]+)"
        }
        
        # Recherche des correspondances dans le texte de réponse
        for key, pattern in patterns.items():
            match = re.search(pattern, response_text)
            if match:
                params_dict[key] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
                response_text = response_text.replace(match.group(0), '')  # Enlever le paramètre du texte

        return {
            'paramètres': params_dict,
            'response_text': response_text  # Retourner le texte nettoyé pour être utilisé comme prompt
        }
    except Exception as e:
        print(f"Erreur lors de l'analyse de la réponse avec regex: {e}")
        return None
