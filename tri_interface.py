import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import time
from typing import List, Dict, Any


class ApplicationTri:
    """Application de tri avec interface graphique simple"""
    
    def __init__(self):
        self.fenetre = tk.Tk()
        self.donnees_chargees = []
        self.donnees_triees = []
        self.cles_disponibles = []
        
        self.configurer_fenetre()
        self.creer_widgets()
    
    def configurer_fenetre(self):
        """Configure la fenêtre principale"""
        self.fenetre.title("Programme de Tri de Données")
        self.fenetre.geometry("600x500")
        self.fenetre.configure(bg='#f0f0f0')
        
        # Style simple
        style = ttk.Style()
        style.configure('Titre.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        style.configure('SousTitre.TLabel', font=('Arial', 11, 'bold'), background='#f0f0f0')
    
    def creer_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self.fenetre, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        titre = ttk.Label(main_frame, text="PROGRAMME DE TRI DE DONNÉES", 
                         style='Titre.TLabel')
        titre.pack(pady=10)
        
        # === SECTION CHARGEMENT ===
        section_chargement = ttk.LabelFrame(main_frame, text="1. Chargement des données", padding="10")
        section_chargement.pack(fill=tk.X, pady=10)
        
        # Boutons de chargement
        boutons_chargement = ttk.Frame(section_chargement)
        boutons_chargement.pack(fill=tk.X)
        
        ttk.Button(boutons_chargement, text="Charger CSV", 
                  command=self.charger_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(boutons_chargement, text="Charger JSON", 
                  command=self.charger_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(boutons_chargement, text="Saisie Manuelle", 
                  command=self.saisie_manuelle).pack(side=tk.LEFT, padx=5)
        
        # Label statut chargement
        self.label_statut_chargement = ttk.Label(section_chargement, text="Aucune donnée chargée")
        self.label_statut_chargement.pack(pady=5)
        
        # === SECTION TRI ===
        section_tri = ttk.LabelFrame(main_frame, text="2. Paramètres de tri", padding="10")
        section_tri.pack(fill=tk.X, pady=10)
        
        # Critère de tri
        frame_critere = ttk.Frame(section_tri)
        frame_critere.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_critere, text="Critère:").pack(side=tk.LEFT)
        self.combo_critere = ttk.Combobox(frame_critere, state="readonly", width=20)
        self.combo_critere.pack(side=tk.LEFT, padx=10)
        
        # Ordre de tri
        frame_ordre = ttk.Frame(section_tri)
        frame_ordre.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_ordre, text="Ordre:").pack(side=tk.LEFT)
        self.var_ordre = tk.StringVar(value="croissant")
        ttk.Radiobutton(frame_ordre, text="Croissant", 
                       variable=self.var_ordre, value="croissant").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_ordre, text="Décroissant", 
                       variable=self.var_ordre, value="decroissant").pack(side=tk.LEFT, padx=10)
        
        # Algorithme
        frame_algo = ttk.Frame(section_tri)
        frame_algo.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_algo, text="Algorithme:").pack(side=tk.LEFT)
        self.var_algo = tk.StringVar(value="insertion")
        ttk.Radiobutton(frame_algo, text="Tri par insertion", 
                       variable=self.var_algo, value="insertion").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_algo, text="Tri à bulles", 
                       variable=self.var_algo, value="bulles").pack(side=tk.LEFT, padx=10)
        
        # Bouton trier
        ttk.Button(section_tri, text="Lancer le tri", 
                  command=self.effectuer_tri).pack(pady=10)
        
        # === SECTION RÉSULTATS ===
        section_resultats = ttk.LabelFrame(main_frame, text="3. Résultats", padding="10")
        section_resultats.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Zone de texte pour résultats
        self.texte_resultats = tk.Text(section_resultats, height=10, width=70)
        scrollbar = ttk.Scrollbar(section_resultats, orient=tk.VERTICAL, 
                                 command=self.texte_resultats.yview)
        self.texte_resultats.configure(yscrollcommand=scrollbar.set)
        
        self.texte_resultats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton recommencer
        ttk.Button(main_frame, text="Recommencer", 
                  command=self.recommencer).pack(pady=10)
    
    def charger_csv(self):
        """Charge les données depuis un fichier CSV"""
        try:
            fichier = filedialog.askopenfilename(
                title="Choisir un fichier CSV",
                filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
            )
            
            if fichier:
                with open(fichier, 'r', encoding='utf-8') as f:
                    lecteur = csv.DictReader(f)
                    self.donnees_chargees = [ligne for ligne in lecteur]
                
                self.mettre_a_jour_interface_apres_chargement()
                messagebox.showinfo("Succès", f"✅ {len(self.donnees_chargees)} enregistrements chargés depuis CSV")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors du chargement CSV: {str(e)}")
    
    def charger_json(self):
        """Charge les données depuis un fichier JSON"""
        try:
            fichier = filedialog.askopenfilename(
                title="Choisir un fichier JSON",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
            )
            
            if fichier:
                with open(fichier, 'r', encoding='utf-8') as f:
                    donnees = json.load(f)
                
                if isinstance(donnees, list):
                    self.donnees_chargees = donnees
                else:
                    self.donnees_chargees = [donnees]
                
                self.mettre_a_jour_interface_apres_chargement()
                messagebox.showinfo("Succès", f"✅ {len(self.donnees_chargees)} enregistrements chargés depuis JSON")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors du chargement JSON: {str(e)}")
    
    def saisie_manuelle(self):
        """Ouvre une fenêtre pour la saisie manuelle"""
        fenetre_saisie = tk.Toplevel(self.fenetre)
        fenetre_saisie.title("Saisie Manuelle")
        fenetre_saisie.geometry("400x300")
        
        ttk.Label(fenetre_saisie, text="Saisie manuelle des données").pack(pady=10)
        
        # Frame pour la saisie
        frame_saisie = ttk.Frame(fenetre_saisie)
        frame_saisie.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame_saisie, text="Format: clé=valeur, séparé par des virgules").pack()
        ttk.Label(frame_saisie, text="Exemple: nom=Jean,age=25,ville=Paris").pack(pady=5)
        
        # Zone de saisie
        texte_saisie = tk.Text(frame_saisie, height=8, width=50)
        texte_saisie.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def valider_saisie():
            texte = texte_saisie.get("1.0", tk.END).strip()
            if texte:
                self.traiter_saisie_manuelle(texte)
                fenetre_saisie.destroy()
            else:
                messagebox.showwarning("Attention", "Veuillez saisir des données")
        
        ttk.Button(frame_saisie, text="Valider", command=valider_saisie).pack()
    
    def traiter_saisie_manuelle(self, texte_saisie):
        """Traite la saisie manuelle"""
        try:
            self.donnees_chargees = []
            lignes = texte_saisie.split('\n')
            
            for ligne in lignes:
                ligne = ligne.strip()
                if ligne:
                    enregistrement = {}
                    paires = ligne.split(',')
                    
                    for paire in paires:
                        if '=' in paire:
                            cle, valeur = paire.split('=', 1)
                            enregistrement[cle.strip()] = valeur.strip()
                    
                    if enregistrement:
                        self.donnees_chargees.append(enregistrement)
            
            self.mettre_a_jour_interface_apres_chargement()
            messagebox.showinfo("Succès", f"✅ {len(self.donnees_chargees)} enregistrement(s) saisi(s)")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur dans la saisie: {str(e)}")
    
    def mettre_a_jour_interface_apres_chargement(self):
        """Met à jour l'interface après le chargement des données"""
        if self.donnees_chargees:
            self.cles_disponibles = list(self.donnees_chargees[0].keys())
            self.combo_critere['values'] = self.cles_disponibles
            if self.cles_disponibles:
                self.combo_critere.set(self.cles_disponibles[0])
            
            self.label_statut_chargement.config(
                text=f"✅ {len(self.donnees_chargees)} enregistrements chargés - {len(self.cles_disponibles)} champs disponibles"
            )
        else:
            self.label_statut_chargement.config(text="❌ Aucune donnée chargée")
    
    def effectuer_tri(self):
        """Effectue le tri selon les paramètres choisis"""
        if not self.donnees_chargees:
            messagebox.showwarning("Attention", "Veuillez d'abord charger des données")
            return
        
        if not self.combo_critere.get():
            messagebox.showwarning("Attention", "Veuillez choisir un critère de tri")
            return
        
        try:
            cle_tri = self.combo_critere.get()
            ordre_croissant = self.var_ordre.get() == "croissant"
            algorithme = self.var_algo.get()
            
            # Appliquer le tri
            debut = time.time()
            
            if algorithme == "insertion":
                self.donnees_triees, stats = self.tri_insertion(cle_tri, ordre_croissant)
            else:
                self.donnees_triees, stats = self.tri_bulles(cle_tri, ordre_croissant)
            
            temps_execution = time.time() - debut
            
            # Afficher les résultats
            self.afficher_resultats(stats, temps_execution)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Erreur lors du tri: {str(e)}")
    
    def tri_insertion(self, cle: str, ordre_croissant: bool):
        """Algorithme de tri par insertion"""
        donnees_triees = self.donnees_chargees.copy()
        comparaisons = 0
        permutations = 0
        
        for i in range(1, len(donnees_triees)):
            element_courant = donnees_triees[i]
            j = i - 1
            
            while j >= 0:
                comparaisons += 1
                
                if ordre_croissant:
                    condition = donnees_triees[j][cle] > element_courant[cle]
                else:
                    condition = donnees_triees[j][cle] < element_courant[cle]
                
                if condition:
                    permutations += 1
                    donnees_triees[j + 1] = donnees_triees[j]
                    j -= 1
                else:
                    break
            
            donnees_triees[j + 1] = element_courant
        
        stats = {
            'algorithme': 'Tri par insertion',
            'comparaisons': comparaisons,
            'permutations': permutations
        }
        
        return donnees_triees, stats
    
    def tri_bulles(self, cle: str, ordre_croissant: bool):
        """Algorithme de tri à bulles"""
        donnees_triees = self.donnees_chargees.copy()
        n = len(donnees_triees)
        comparaisons = 0
        permutations = 0
        
        for i in range(n):
            for j in range(0, n - i - 1):
                comparaisons += 1
                
                if ordre_croissant:
                    condition = donnees_triees[j][cle] > donnees_triees[j + 1][cle]
                else:
                    condition = donnees_triees[j][cle] < donnees_triees[j + 1][cle]
                
                if condition:
                    permutations += 1
                    donnees_triees[j], donnees_triees[j + 1] = donnees_triees[j + 1], donnees_triees[j]
        
        stats = {
            'algorithme': 'Tri à bulles',
            'comparaisons': comparaisons,
            'permutations': permutations
        }
        
        return donnees_triees, stats
    
    def afficher_resultats(self, stats, temps_execution):
        """Affiche les résultats du tri"""
        self.texte_resultats.delete(1.0, tk.END)
        
        # En-tête
        self.texte_resultats.insert(tk.END, "=== RÉSULTATS DU TRI ===\n\n")
        
        # Statistiques
        self.texte_resultats.insert(tk.END, f"Algorithme: {stats['algorithme']}\n")
        self.texte_resultats.insert(tk.END, f"Temps d'exécution: {temps_execution:.6f} secondes\n")
        self.texte_resultats.insert(tk.END, f"Comparaisons: {stats['comparaisons']}\n")
        self.texte_resultats.insert(tk.END, f"Permutations: {stats['permutations']}\n\n")
        
        # Données triées (premiers éléments)
        self.texte_resultats.insert(tk.END, "=== DONNÉES TRIÉES ===\n\n")
        
        if self.donnees_triees:
            # Afficher les en-têtes
            entetes = self.cles_disponibles
            ligne_entete = " | ".join(entetes) + "\n"
            self.texte_resultats.insert(tk.END, ligne_entete)
            self.texte_resultats.insert(tk.END, "-" * 50 + "\n")
            
            # Afficher les données (limité aux 10 premiers)
            for i, item in enumerate(self.donnees_triees[:10]):
                ligne = " | ".join(str(item.get(entete, "")) for entete in entetes)
                self.texte_resultats.insert(tk.END, ligne + "\n")
            
            if len(self.donnees_triees) > 10:
                self.texte_resultats.insert(tk.END, f"\n... et {len(self.donnees_triees) - 10} autres enregistrements")
        else:
            self.texte_resultats.insert(tk.END, "Aucune donnée à afficher")
    
    def recommencer(self):
        """Remet à zéro pour recommencer"""
        self.donnees_chargees = []
        self.donnees_triees = []
        self.cles_disponibles = []
        self.combo_critere.set('')
        self.texte_resultats.delete(1.0, tk.END)
        self.label_statut_chargement.config(text="Aucune donnée chargée")
        messagebox.showinfo("Recommencer", "Prêt pour une nouvelle session !")
    
    def demarrer(self):
        """Démarre l'application"""
        self.fenetre.mainloop()