import tkinter as tk
import configparser
import re
import os
import sys

NEWCOMMAND=None
EXITED=None

# Custom ConfigParser to preserve case sensitivity
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cord = int((screen_width / 2) - (width / 2))
    y_cord = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_cord}+{y_cord}")



def lire_fichier_existant():

    platform = sys.platform

    # Methode Mac OS
    if platform == "darwin":
        try:
            with open("lanceur.sh", "r") as fichier:
                contenu = fichier.readlines()
            old_api_token = contenu[1].split("'")[1]
            old_csv_path = contenu[1].split("'")[3]
            old_python_path = contenu[1].split()[2]
            old_script_path = contenu[1].split()[3]

        except FileNotFoundError:
            return None, None, None, None  # Si le fichier n'existe pas
        except IndexError:
            print("Erreur lors du parsing des paramètres. Vérifiez le format du fichier.")
            return None, None, None, None

    #Methode Linux
    elif platform.startswith("linux"):
        # Initialize a ConfigParser instance
        config = configparser.ConfigParser()

        # Read the .desktop file
        desktop_file = '/home/werner/Desktop/NLtoR.desktop'
        config.read(desktop_file)

        # Access the "Desktop Entry" section
        desktop_entry = config['Desktop Entry']
        command = desktop_entry.get("Exec")

        # Extract Existing Values
        pattern = r'env\s+REPLICATE_API_TOKEN="([^"]*)"\s+CSV_PATH="([^"]*)"\s+([^ ]+)\s+([^ ]+)'
        match = re.match(pattern, command)
        if match:
            old_api_token, old_csv_path, old_python_path, old_script_path = match.groups()
    return old_api_token, old_csv_path, old_python_path, old_script_path or None



def demander_infos():
    # Retrieve old values
    old_token, old_csv_path, old_env_path, old_script_path = lire_fichier_existant()

    # Create the main window
    root = tk.Tk()
    root.title("Settings")

    # Adjust the window size and center it
    window_width = 890
    window_height = 240
    center_window(root, window_width, window_height)

    def show_inputs_and_close():
        global NEWCOMMAND
        # Get the input values
        new_token_value = token_entry.get()
        csv_path_value = csv_path_entry.get()
        env_path_value = env_path_entry.get()
        script_path_value = script_path_entry.get()

        # Ensure values fall back to old values if left empty
        new_token = new_token_value if new_token_value else old_token
        csv_path = csv_path_value if csv_path_value else old_csv_path
        env_path = env_path_value if env_path_value else old_env_path
        script_path = script_path_value if script_path_value else old_script_path

        platform = sys.platform

        # Methode Mac OS
        if platform == "darwin":
            NEWCOMMAND=(
        f"#!/bin/bash\n"
        f"REPLICATE_API_TOKEN='{new_token}' CSV_PATH='{csv_path}' "
        f"{env_path} {script_path}\n"
        )

        elif platform.startswith("linux"):
            NEWCOMMAND = f'env REPLICATE_API_TOKEN="{new_token}" CSV_PATH="{csv_path}" {env_path} {script_path}'
        # Close the window
#    def on_close():
        print("Closing window...")
        root.withdraw()
        root.update()
    #    root.quit()
        root.quit()

    def on_close():
        global EXITED
        EXITED = 1
        root.withdraw()
        root.update()
        # Stop the main loop and close the window
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Create and place the input fields and labels
    label_width = 37  # Width for each label
    entry_width = 50  # Width for each input field

    tk.Label(root, text="Entrez votre clé API pour REPLICATE_API_TOKEN:",
             width=label_width).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    token_entry = tk.Entry(root, width=entry_width)
    token_entry.grid(row=0, column=1, padx=10, pady=10)
    token_entry.insert(0, old_token or 'r8_')

    tk.Label(root, text="Entrez votre chemin pour csv_path:",
             width=label_width).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    csv_path_entry = tk.Entry(root, width=entry_width)
    csv_path_entry.grid(row=1, column=1, padx=10, pady=10)
    csv_path_entry.insert(0, old_csv_path or 'path/to/dossier/')

    tk.Label(root, text="Entrez votre chemin pour env_path:",
             width=label_width).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    env_path_entry = tk.Entry(root, width=entry_width)
    env_path_entry.grid(row=2, column=1, padx=10, pady=10)
    env_path_entry.insert(0, old_env_path or '/usr/bin/python3')

    tk.Label(root, text="Entrez votre chemin pour script_path:",
             width=label_width).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    script_path_entry = tk.Entry(root, width=entry_width)
    script_path_entry.grid(row=3, column=1, padx=10, pady=10)
    script_path_entry.insert(0,
        old_script_path or '/Users/nom_user/Natural_language_Llama3_shortcut')

    # Create and place the Submit button
    submit_button = tk.Button(root, text="Submit", command=show_inputs_and_close, width=15)
    submit_button.grid(row=4, column=0, columnspan=2, pady=15)

    close_button = tk.Button(root, text="Close", command=on_close, width=15)
    close_button.grid(row=4, column=1, columnspan=1, pady=2)
    # Start the main event loop
    root.mainloop()

    # Perform cleanup after `mainloop` ends
    root.destroy()



# Function to update the launcher
def update_launcher():
    if EXITED == 1:
        print("Changements non sauvegardés")
        return None
    platform = sys.platform

    #Methode Mac OS
    if platform == "darwin":
        fichier_nom = "lanceur.sh"
        with open(fichier_nom, "w", encoding='utf-8') as fichier:
            fichier.write(NEWCOMMAND)

        chemin_complet = os.path.abspath(fichier_nom)
        print(f"Fichier '{fichier_nom}' créé ou modifié avec succès.")
        print(f"Chemin complet du fichier : {chemin_complet}")

    #Methode Linux
    elif platform.startswith("linux"):
        # Initialize a custom CaseSensitiveConfigParser instance
        config = CaseSensitiveConfigParser()

        # Add a section with key-value pairs
        config['Desktop Entry'] = {
            'Name': 'NLtoR',
            'Exec': NEWCOMMAND,
            'Icon': '/usr/share/icons/datlinux/about.png',
            'Type': 'Application',
            'Categories': 'Utility;',
            'Comment': 'Launch the Natural Language to R Script',
            'Terminal': 'true'
        }

        # Write to a new .desktop file
        desktop_file = '/home/werner/Desktop/NLtoR.desktop'
        with open(desktop_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        # Ensure the file is executable
        os.chmod(desktop_file, 0o755)
        return print("Sucessfully changed  command to :",NEWCOMMAND)

    else: print("Unsupported OS")
    return None

if __name__ == "__main__":
    demander_infos()
    update_launcher()
