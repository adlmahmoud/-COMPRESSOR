"""
Gestion du chargement des données depuis différentes sources
Correspond à l'étape 'Charger liste' de l'organigramme
"""

import csv
import json
from typing import List, Dict, Any, Optional


class GestionnaireDonnees:
    """Gère le chargement des données depuis CSV, JSON ou saisie manuelle"""
    
    @staticmethod
    def charger_csv(chemin_fichier: str) -> List[Dict[str, Any]]:
        """Charge les données depuis un fichier CSV"""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                lecteur = csv.DictReader(fichier)
                donnees = [ligne for ligne in lecteur]
            
            print(f"✅ {len(donnees)} enregistrements chargés depuis CSV")
            return donnees
        
        except FileNotFoundError:
            raise Exception("❌ Fichier CSV non trouvé")
        except Exception as e:
            raise Exception(f"❌ Erreur lecture CSV: {str(e)}")
    
    @staticmethod
    def charger_json(chemin_fichier: str) -> List[Dict[str, Any]]:
        """Charge les données depuis un fichier JSON"""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                donnees = json.load(fichier)
            
            if not isinstance(donnees, list):
                donnees = [donnees]
            
            print(f"✅ {len(donnees)} enregistrements chargés depuis JSON")
            return donnees
        
        except FileNotFoundError:
            raise Exception("❌ Fichier JSON non trouvé")
        except json.JSONDecodeError:
            raise Exception("❌ Format JSON invalide")
        except Exception as e:
            raise Exception(f"❌ Erreur lecture JSON: {str(e)}")
    
    @staticmethod
    def saisie_manuelle() -> List[Dict[str, Any]]:
        """Permet la saisie manuelle des données"""
        print("\n=== SAISIE MANUELLE ===")
        donnees = []
        
        while True:
            print(f"\nEnregistrement #{len(donnees) + 1}")
            enregistrement = {}
            
            # Saisie des champs
            while True:
                champ = input("Nom du champ (ou 'fin' pour terminer): ").strip()
                if champ.lower() == 'fin':
                    break
                if champ:
                    valeur = input(f"Valeur pour '{champ}': ").strip()
                    enregistrement[champ] = valeur
            
            if enregistrement:
                donnees.append(enregistrement)
            
            continuer = input("\nAjouter un autre enregistrement? (o/n): ").strip().lower()
            if continuer != 'o':
                break
        
        print(f"✅ {len(donnees)} enregistrement(s) saisi(s) manuellement")
        return donnees
    
    @staticmethod
    def afficher_donnees(donnees: List[Dict[str, Any]], limite: int = 10):
        """Affiche les données chargées"""
        if not donnees:
            print("❌ Aucune donnée à afficher")
            return
        
        print(f"\n=== DONNÉES CHARGÉES ({len(donnees)} enregistrements) ===")
        
        # Affiche les en-têtes
        entetes = list(donnees[0].keys())
        print(" | ".join(entetes))
        print("-" * 50)
        
        # Affiche les données (limitées)
        for i, item in enumerate(donnees[:limite]):
            ligne = " | ".join(str(item.get(entete, "")) for entete in entetes)
            print(ligne)
        
        if len(donnees) > limite:
            print(f"... et {len(donnees) - limite} autres enregistrements")