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
import os
import replicate
from replicate.exceptions import ReplicateError
from clipboard_utils import get_clipboard, copy_to_clipboard
from attachment_utils import prepare_csv

# If API-KEY problem, just paste yours below
#os.environ['REPLICATE_API_TOKEN'] = ''

# Assurez-vous que la variable d'environnement est définie
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print(REPLICATE_API_TOKEN)
CSV_PATH=os.getenv("CSV_PATH")
if REPLICATE_API_TOKEN is None:
    raise EnvironmentError("REPLICATE_API_TOKEN is not set in the environment")
    time.sleep(30)

# Configuration initiale de Replicate
replicate.api_token = REPLICATE_API_TOKEN
test = """
*** Write the code for a classification regression using python*** 
-Datas are in the dataframe 'df'
-First we will create a dummy for each values of 'variety' in an automatic way.
- we want to create a multi-nomial model for categorial data (variety) to predict a plant variety using all variables about dimensions caracteritics as regressors (these are the 4 first columns in the dataframe below)
- Once the model is created we want to perform a generic statistical test.
- Then the code should print the interpretation of the result depending on the stat-value with conditionnal print()'s
- Finally predictions should be plotted on 2 plots ( 1 for `petal` variables, 1 for `sepal` variables) with mathplotlib and seaborn with variety as the color legend
"""
def translate_to_r_with_replicate(text):
    """Envoie le texte à l'API Replicate pour traduction en code Python."""
    prompt_objective = (
        '**Objective:** Refine human-written prompts requesting code snippets (Python) into clear, structured, and detailed prompts for another AI.'
    )
    prompt_instructions = (
        '**Instructions:**\n'
        '- **Role Definition:**\n'
        "  - Act as a 'Prompt Enhancer' to transform human-written prompts requesting Python code snippets into optimized and structured prompts for AI processing."
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
        '  - **Add Details:**\n'
        '    - Include essential background information (e.g., libraries, data structure).\n'
        '    - Specify functions, parameters, and desired outcomes.\n'
        '  - **Recommend values for min_tokens, max_tokens, temperature, top_p, top_k, presence_penalty, frequency_penalty to use with the enhanced prompt**'
        '  - **Refine Vocabulary:** Substitute vague adjectives and verbs with precise terms.\n'
        '  - **Comments:** Ensure the prompt requests comments within the code for clarity.'
    )
    prompt_additional_context = (
        '**Additional Context:**\n'
        '- **Questions Identification:**\n'
        "  - Questions are marked with `***question?***`.\n"
        "  - Everything outside the `***` markers is considered contextual information.\n"
        '\n'
        '- **Data Tables:**\n'
        "  - Tables are preceded by a line of 98 '#' symbols.\n"
        '  - Tables are provided in markdown format to understand data structure and often include row names.\n'
        '  - Tables will have a maximum of 10 rows.'
    )
    prompt_example_process = (
        '- **Example Process:**\n'
        '  1. **Input (Human-Written Prompt):**\n'
        "     - 'Write Python code to plot a bar graph using matplotlib.'\n"
        '  2. **Output (Enhanced Prompt):**\n'
        '     - **Prompt:**\n'
        "       - 'Write Python code to plot a bar graph using the matplotlib library.\n"
        '         - **Details:**\n'
        "           - **Input Data:**\n"
        "             - List of categories: `['A', 'B', 'C', 'D']`\n"
        "             - Corresponding values: `[10, 20, 15, 25]`\n"
        "             - Variables type: for each, numeric/character/factor/date/boolean, discret/continous, qualitative/quantitative etc..."
        '           - **Graph Characteristics:**\n'
        "             - Title: 'Sample Bar Graph'\n"
        "             - X-axis label: 'Categories'\n"
        "             - Y-axis label: 'Values'\n"
        '           - **Comments:**\n'
        "             - Include comments in the code to explain each step of the plotting process.'"
    )
    prompt_final_notes = (
        '**Final Notes:**\n'
        "- Always maintain the user's original intent.\n"
        '- Be creative yet precise to enable the best possible output.\n'
        '- Ensure code snippets are well-documented with appropriate comments.'
    )

    input_data = {
        'prompt': (
            f"{prompt_objective}\n\n"
            f"{prompt_instructions}\n\n"
            f"{prompt_guidelines}\n\n"
            f"{prompt_enhancement_instructions}\n\n"
            f"{prompt_additional_context}\n\n"
            f"{prompt_example_process}\n\n"
            f"{prompt_final_notes}\n\n"
            f"**Original Prompt:**\n{text}"
        )
    }

    try:
        output = replicate.run("meta/meta-llama-3-70b-instruct", input=input_data)
        enhanced_prompt = "".join(output)  # Joindre les parties de la réponse
        print(enhanced_prompt)
        input_data = {
            "prompt": (
                f"{enhanced_prompt}\n\n"
            ),
            "prompt_template": (
                "system\n\nTu es un Assistant très efficace pour générer du code Python "
                "à partir de demandes en langage naturel et tu dois suivre les "
                "instructions suivantes :\n\n{prompt}\n\n"
            )
        }
        try:
            output = replicate.run("meta/meta-llama-3-70b-instruct", input=input_data)
            response_text = "".join(output)  # Joindre les parties de la réponse
            print(response_text,"that's it")
            return response_text
        except ReplicateError as e:
            print(f"2nd step: Erreur liée à Replicate lors de l'envoi de la demande: {e}")
        except FileNotFoundError as e:
            print(f"2nd step: Erreur : Le fichier spécifié n'a pas été trouvé: {e}")
        except OSError as e:
            print(f"2nd step: Erreur système : {e}")
        except ValueError as e:
            print(f"2nd step: Erreur de valeur : {e}")
        return None
    except ReplicateError as e:
        print(f"Erreur liée à Replicate lors de l'envoi de la demande: {e}")
        time.sleep(30)
    except FileNotFoundError as e:
        print(f"Erreur : Le fichier spécifié n'a pas été trouvé: {e}")
        time.sleep(30)
    except OSError as e:
        print(f"Erreur système : {e}")
        time.sleep(30)
    except ValueError as e:
        print(f"Erreur de valeur : {e}")
        time.sleep(30)
    return None


def main():
    """Launches the whole process"""
    text_from_clipboard = get_clipboard() + prepare_csv()
    #prepare_pdf()
    print(f"Texte récupéré du presse-papiers : {text_from_clipboard}")
    translated_code = translate_to_r_with_replicate(text_from_clipboard)
    if translated_code:
        print("Code R généré par Replicate:")
        print(translated_code)
        copy_to_clipboard(translated_code)
        print("Code R copié de nouveau dans le presse-papiers.")
    else:
        print("Aucune réponse reçue ou erreur lors de la récupération de la réponse.")

if __name__ == "__main__":
    main()
    time.sleep(30)
