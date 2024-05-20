"""
main_script.py

This is the main script that orchestrates the translation of natural language 
requests to R code using Replicate's API.
It handles clipboard input and output, prepares attachment files, and interacts 
with the Replicate API.

Functions:
    - translate_to_r_with_replicate(text): Sends the text to Replicate's API 
      for translation into R code.
    - main(): The main function orchestrating the translation process.
"""
import time
from replicate.exceptions import ReplicateError
from clipboard_utils import get_clipboard, copy_to_clipboard
from attachment_utils import prepare_csv
import os
import pyperclip
import sys
import re
import pandas as pd
import replicate 
from response_parser import parse_response_with_regex



def generate_enhanced_prompt(user_request: str) -> str:
    """
    Generate an enhanced prompt for Llama3 based on the provided user request and predefined prompt structure.
    This prompt is designed to be adaptable to any type of user request, not limited to coding but inclusive of various fields such as marketing, research, and more.

    Args:
        user_request (str): The initial prompt provided by the user.

    Returns:
        str: The complete enhanced prompt ready to be processed by Llama3.
    """

    # Sections of the prompt as defined earlier
    prompt_objective = (
        '**Objective:** Refine human-written prompts into clear, structured, and detailed prompts for another AI.'
    )
    prompt_instructions = (
        '**Instructions:**\n'
        '- **Role Definition:**\n'
        "  - Act as a 'Prompt Enhancer' to transform human-written prompts into optimized and structured prompts for AI processing across various fields."
    )
    prompt_guidelines = (
        '- **Guidelines:**\n'
        '  - Use concise and clear language.\n'
        '  - Ensure prompts are detailed enough for accurate interpretation.\n'
        "  - Maintain the original context and intent of the human-written prompt.\n"
        '  - Avoid discriminatory, offensive, or prohibited content.'
    )
    prompt_enhancement_instructions = (
        '- **Enhancement Instructions:**\n'
        '  - **Identify Gaps:** Recognize missing context or details in the original prompt.\n'
        '  - **Clarify Ambiguity:** Resolve any unclear terms or requests.\n'
        '  - **Improve Structure:** Organize the prompt in bullet points or numbered steps.\n'
        '  - **Add Details:** Include essential background information relevant to the request.\n'
        '    - Specify necessary parameters, desired outcomes, or particular considerations relevant to the field of the request.\n'
        '  - **Refine Vocabulary:** Substitute vague adjectives and verbs with precise terms to enhance understanding.\n'
        '  - **Comments:** Encourage detailed comments to clarify complex points.\n'
        '  - **Parameter Specifications:** Please specify values for `min_tokens`, `max_tokens`, `temperature`, `top_p`, `top_k`, `presence_penalty`, `frequency_penalty` to tailor the response to the complexity of the request.'
    )
    prompt_additional_context = (
        '**Additional Context:**\n'
        '- **Questions Identification:**\n'
        "  - Questions are marked with `***question?***`.\n"
        "  - Everything outside the `***` markers is considered contextual information.\n"
        '- **Data Tables:**\n'
        "  - Tables are preceded by a line of 98 '#' symbols.\n"
        '  - Tables are provided in markdown format to understand data structure and often include row names.\n'
        '  - Tables will have a maximum of 10 rows.'
    )
    prompt_final_notes = (
        '**Final Notes:**\n'
        "- Always maintain the user's original intent.\n"
        '- Be creative yet precise to enable the best possible output.\n'
        '- Ensure responses are well-documented with appropriate comments and analyses.'
    )

    # Combine all prompt sections
    complete_prompt = (
        f"{prompt_objective}\n\n"
        f"{prompt_instructions}\n"
        f"{prompt_guidelines}\n"
        f"{prompt_enhancement_instructions}\n"
        f"{prompt_additional_context}\n"
        f"{prompt_final_notes}\n\n"
        f"### User Request:\n{user_request}"
    )

    return complete_prompt


def send_request_to_model(prompt_text: str, max_tokens=2000, temperature=0.5):
    """
    Envoie la requête structurée au modèle Llama3 et récupère la réponse.
    """
    replicate.api_token = os.getenv('REPLICATE_API_TOKEN')
    input_payload = {
        "prompt": prompt_text,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        output = replicate.run('meta/meta-llama-3-70b-instruct', input=input_payload)
        response_text = "".join(map(str, output))
        print("Réponse brute de l'API:", response_text)
        return response_text
    except replicate.exceptions.ReplicateError as e:
        print(f"Erreur de connexion avec l'API: {e}")
        return None



def main():
    user_request = get_clipboard() + prepare_csv()
    print(f"Requête récupérée : {user_request}")
    structured_prompt = generate_enhanced_prompt(user_request)
    response = send_request_to_model(structured_prompt)
    if response:
        parsed_response = parse_response_with_regex(response)
        if parsed_response:
            new_prompt_text = parsed_response['response_text']  # Utiliser le texte nettoyé comme nouveau prompt
            paramètres = parsed_response['paramètres']
            
            new_temperature = paramètres.get('temperature', 0.7)
            #new_top_p = paramètres.get('top_p', 0.9)
            #new_top_k = paramètres.get('top_k', 0)
            #new_presence_penalty = paramètres.get('presence_penalty', 0)
            #new_length_penalty = paramètres.get('length_penalty', 1)
            
            #new_response = send_request_to_model(new_prompt_text, max_tokens=3000, temperature=new_temperature, top_p=new_top_p, top_k=new_top_k, presence_penalty=new_presence_penalty, length_penalty=new_length_penalty)
            new_response = send_request_to_model(new_prompt_text, max_tokens=3000, temperature=new_temperature)
            
            if new_response:
                print("Réponse finale de l'API:", new_response)
                copy_to_clipboard(new_response)
                print("Réponse copiée dans le presse-papier.")
            else:
                print("Erreur lors de l'envoi de la seconde requête.")
        else:
            print("Erreur dans l'analyse de la réponse.")
    else:
        print("Aucune réponse valide reçue du modèle.")

if __name__ == "__main__":
    main()
    
    
