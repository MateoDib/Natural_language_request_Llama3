import tkinter as tk
import configparser
import re
import os
import sys

# Custom ConfigParser to preserve case sensitivity
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

class SettingsApp:
    def __init__(self):
        self.NEWCOMMAND = None
        self.EXITED = None

        # Liste des clés à traiter
        self.keys = ["REPLICATE_API_TOKEN", "CSV_PATH", "PYTHON_PATH", "SCRIPT_PATH"]
        self.old_values = self.lire_fichier_existant(*self.keys)

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Settings")

        # Adjust the window size and center it
        window_width = 890
        window_height = 240
        self.center_window(window_width, window_height)

        # Create and place the input fields and labels
        label_width = 37  # Width for each label
        entry_width = 50  # Width for each input field

        # Dictionnaire pour stocker les entrées
        self.entries = {}

        # Générer dynamiquement les champs d'entrée
        for i, key in enumerate(self.keys):
            tk.Label(self.root, text=f"Entrez votre valeur pour {key}:",
                     width=label_width).grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = tk.Entry(self.root, width=entry_width)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entry.insert(0, self.old_values.get(key, ''))
            self.entries[key] = entry

        # Create and place the Submit button
        submit_button = tk.Button(self.root, text="Submit", command=self.show_inputs_and_close, width=15)
        submit_button.grid(row=len(self.keys), column=0, columnspan=2, pady=15)

        close_button = tk.Button(self.root, text="Close", command=self.on_close, width=15)
        close_button.grid(row=len(self.keys), column=1, columnspan=1, pady=2)

        # Start the main event loop
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

        # Perform cleanup after `mainloop` ends
        self.root.destroy()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width / 2))
        y_cord = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x_cord}+{y_cord}")

    def lire_fichier_existant(self, *args):
        platform = sys.platform
        old_values = {}

        if platform == "darwin":
            try:
                with open("lanceur.sh", "r", encoding='utf-8') as fichier:
                    contenu = fichier.readlines()
                if len(contenu) < len(args) + 1:
                    raise ValueError("Le fichier lanceur.sh ne contient pas assez de lignes.")

                for i, arg in enumerate(args, 1):
                    old_values[arg] = contenu[i].split("'")[1]

            except FileNotFoundError:
                return {arg: None for arg in args}
            except IndexError:
                print("Erreur lors du parsing des paramètres. Vérifiez le format du fichier.")
                return {arg: None for arg in args}

        elif platform.startswith("linux"):
            config = configparser.ConfigParser()
            desktop_file = os.path.join(os.environ['HOME'], 'Desktop', 'NLtoR.desktop')
            config.read(desktop_file)

            desktop_entry = config['Desktop Entry']
            command = desktop_entry.get("Exec")

            # Create a dynamic regex pattern based on *args
            pattern = r'env\s+REPLICATE_API_TOKEN="([^"]*)"\s+CSV_PATH="([^"]*)"'
            additional_args = [arg for arg in args if arg not in ["REPLICATE_API_TOKEN", "CSV_PATH", "PYTHON_PATH", "SCRIPT_PATH"]]
            for arg in additional_args:
                pattern += rf'\s+{arg}="([^"]*)"'
            pattern += r'\s+([^ ]+)\s+([^ ]+)'

            match = re.search(pattern, command)
            if match:
                values = match.groups()
                for i, arg in enumerate(args):
                    if arg in ["PYTHON_PATH", "SCRIPT_PATH"]:
                        old_values[arg] = values[-2 if arg == "PYTHON_PATH" else -1]
                    else:
                        old_values[arg] = values[i] if i < len(values) else None
        return old_values

    def show_inputs_and_close(self):
        # Récupérer les nouvelles valeurs
        new_values = {}
        for key in self.keys:
            new_value = self.entries[key].get()
            new_values[key] = new_value if new_value else self.old_values.get(key)

        # Ajouter les arguments supplémentaires
        additional_args = {key: value for key, value in self.old_values.items() if key not in self.keys}
        additional_args_str = " ".join([f'{key}="{value}"' for key, value in additional_args.items()])

        platform = sys.platform

        if platform == "darwin":
            self.NEWCOMMAND = (
                f"#!/bin/bash\n"
                f"REPLICATE_API_TOKEN='{new_values['REPLICATE_API_TOKEN']}' csv_path='{new_values['CSV_PATH']}' {additional_args_str} "
                f"{new_values['PYTHON_PATH']} {new_values['SCRIPT_PATH']}\n"
            )

        elif platform.startswith("linux"):
            self.NEWCOMMAND = f'env REPLICATE_API_TOKEN="{new_values["REPLICATE_API_TOKEN"]}" CSV_PATH="{new_values["CSV_PATH"]}" {additional_args_str} {new_values["PYTHON_PATH"]} {new_values["SCRIPT_PATH"]}'
        
        print("Closing window...")
        self.root.withdraw()
        self.root.update()
        self.root.quit()

    def on_close(self):
        self.EXITED = 1
        self.root.withdraw()
        self.root.update()
        self.root.quit()

def update_launcher(infos):
    if infos.EXITED == 1:
        print("Changements non sauvegardés")
        return None
    platform = sys.platform

    if platform == "darwin":
        fichier_nom = "lanceur.sh"
        with open(fichier_nom, "w", encoding='utf-8') as fichier:
            fichier.write(infos.NEWCOMMAND)

        chemin_complet = os.path.abspath(fichier_nom)
        print(f"Fichier '{fichier_nom}' créé ou modifié avec succès.")
        print(f"Chemin complet du fichier : {chemin_complet}")

    elif platform.startswith("linux"):
        config = CaseSensitiveConfigParser()

        config['Desktop Entry'] = {
            'Name': 'NLtoR',
            'Exec': infos.NEWCOMMAND,
            'Icon': '/usr/share/icons/datlinux/about.png',
            'Type': 'Application',
            'Categories': 'Utility;',
            'Comment': 'Launch the Natural Language to R Script',
            'Terminal': 'true'
        }
        desktop_file = os.path.join(os.environ['HOME'], 'Desktop', 'NLtoR.desktop')
        with open(desktop_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        os.chmod(desktop_file, 0o755)
        print("Successfully changed command to:", infos.NEWCOMMAND)

    else:
        print("Unsupported OS")
    return None

if __name__ == "__main__":
    infos = SettingsApp()
    update_launcher(infos)
