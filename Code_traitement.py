# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 10:16:39 2024

@author: 13jer
"""
import numpy as np
import tkinter as tk
import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
import threading
from tkinter import messagebox

# Configuration du port série
port = 'COM6'  # Remplacez COM6 par le port utilisé par votre Arduino
baudrate = 9600
duration = 10  # Durée d'acquisition en secondes

# Fonction pour démarrer le décompte et l'enregistrement simultanément
def start_acquisition():
    start_button.pack_forget()  # Cache le bouton "Démarrer"
    # Démarre le décompte dans un thread séparé
    threading.Thread(target=start_countdown, args=(duration,)).start()
    # Démarre l'enregistrement des données
    threading.Thread(target=record_data).start()

# Fonction pour démarrer le décompte
def start_countdown(time_left):
    while time_left >= 0:
        # Met à jour le label avec le temps restant
        time_label.config(text=f"Temps restant : {time_left} secondes")
        # Attendre 1 seconde avant de décrémenter le temps
        time.sleep(1)
        time_left -= 1
    
    # Lorsque le temps est écoulé, afficher un message
    time_label.config(text="Le temps est écoulé!")

# Fonction pour enregistrer les données
def record_data():
    # Initialisation du port série
    ser = serial.Serial(port, baudrate, timeout=1)

    print("Acquisition en cours...")

    # Enregistrement des données
    start_time = time.time()
    data = []
    
    try:
        while time.time() - start_time < duration:
            line = ser.readline().decode('utf-8').strip()  # Lecture d'une ligne
            if line.isdigit():  # Vérifie si la ligne contient une valeur numérique
                data.append(int(line))  # Stocke la valeur
                print (data[-1])
    except KeyboardInterrupt:
        print("Acquisition interrompue.")
    
    # Fermeture du port série
    ser.close()

    # Enregistrement dans un fichier CSV
    with open("fsr_data.csv", "w") as f:
        f.write("Time,Value\n")
        for i, value in enumerate(data):
            f.write(f"{time.time()},{value}\n")  # Suppose un échantillonnage de 280 Hz (ou ajustez selon votre cas)

    # Charger les données et afficher le graphique
    data = pd.read_csv("fsr_data.csv")
    
    # Afficher les données dans un graphique
    plt.plot(data["Time"], data["Value"])
    plt.xlabel("Temps (s)")
    plt.ylabel("Valeur du capteur")
    plt.title("Données FSR")
    plt.show()  # Affiche le graphique

    # Appeler la fonction pour compter les pics
    peaks_count = count_peaks(data["Value"].tolist(), threshold=20, min_distance=50)  # Seuil = 20 et distance minimale = 50 indices
    
    # Afficher le nombre de pics trouvés
    print(f"Nombre de pics trouvés : {peaks_count}")
    messagebox.showinfo("Résultat", f"Nombre de pics trouvés : {peaks_count}")

# Fonction pour compter le nombre de pics au-dessus d'un seuil donné
# Ajout d'un paramètre min_distance pour fusionner les pics proches
def count_peaks(data, threshold=20, min_distance=50):
    peaks_count = 0
    last_peak = None  # Garder une trace du dernier pic trouvé

    for i in range(1, len(data) - 1):
        # Condition pour un pic (plus grand que ses voisins)
        if data[i] > data[i - 1] and data[i] > data[i + 1] and data[i] > threshold:
            # Vérifier si le pic est assez éloigné du dernier pic trouvé
            if last_peak is None or (i - last_peak) > min_distance:
                peaks_count += 1  # Un nouveau pic est trouvé
                last_peak = i  # Met à jour la position du dernier pic

    return peaks_count

# Création de la fenêtre principale
root = tk.Tk()
root.title("Acquisition FSR")

# Création du label pour afficher le décompte
time_label = tk.Label(root, text="Temps restant : 10 secondes", font=("Arial", 16))
time_label.pack(pady=20)

# Création du bouton "Démarrer"
start_button = tk.Button(root, text="Démarrer", command=start_acquisition, font=("Arial", 14))
start_button.pack(pady=20)

# Lancer l'interface
root.mainloop()




