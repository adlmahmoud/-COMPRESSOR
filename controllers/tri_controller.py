"""
Contrôleur principal qui orchestre le flux du programme
Correspond exactement à l'organigramme fourni
"""

from typing import List, Dict, Any, Tuple
from models.gestion_donnees import GestionnaireDonnees
from models.algorithmes_tri import AlgorithmesTri


class ControleurTri:
    """Contrôle le flux complet du programme selon l'organigramme"""
    
    def __init__(self):
        self.donnees_chargees: List[Dict[str, Any]] = []
        self.donnees_triees: List[Dict[str, Any]] = []
        self.cles_disponibles: List[str] = []
    
    def charger_donnees(self) -> bool:
        """Étape: Charger liste"""
        print("\n=== CHOIX DE LA SOURCE DES DONNÉES ===")
        print("1. Fichier CSV")
        print("2. Fichier JSON") 
        print("3. Saisie manuelle")
        
        choix = input("\nChoisissez la source (1-3): ").strip()
        
        try:
            if choix == "1":
                fichier = input("Chemin du fichier CSV: ").strip()
                self.donnees_chargees = GestionnaireDonnees.charger_csv(fichier)
            
            elif choix == "2":
                fichier = input("Chemin du fichier JSON: ").strip()
                self.donnees_chargees = GestionnaireDonnees.charger_json(fichier)
            
            elif choix == "3":
                self.donnees_chargees = GestionnaireDonnees.saisie_manuelle()
            
            else:
                print("❌ Choix invalide")
                return False
            
            # Extraction des clés disponibles
            if self.donnees_chargees:
                self.cles_disponibles = list(self.donnees_chargees[0].keys())
                return True
            else:
                print("❌ Aucune donnée chargée")
                return False
        
        except Exception as e:
            print(f"❌ {str(e)}")
            return False
    
    def choisir_critere_tri(self) -> str:
        """Étape: Choisir critère de tri"""
        print(f"\n=== CRITÈRES DE TRI DISPONIBLES ===")
        for i, cle in enumerate(self.cles_disponibles, 1):
            print(f"{i}. {cle}")
        
        while True:
            try:
                choix = int(input(f"\nChoisissez le critère (1-{len(self.cles_disponibles)}): "))
                if 1 <= choix <= len(self.cles_disponibles):
                    return self.cles_disponibles[choix - 1]
                else:
                    print("❌ Choix hors limites")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
    
    def choisir_ordre_tri(self) -> bool:
        """Étape: Choisir ordre"""
        print("\n=== ORDRE DE TRI ===")
        print("1. Croissant (A-Z, 0-9)")
        print("2. Décroissant (Z-A, 9-0)")
        
        while True:
            choix = input("Choisissez l'ordre (1-2): ").strip()
            if choix == "1":
                return True  # Croissant
            elif choix == "2":
                return False  # Décroissant
            else:
                print("❌ Choix invalide")
    
    def choisir_algorithme(self) -> Tuple[str, callable]:
        """Étape: Choisir algorithme"""
        algorithmes = AlgorithmesTri.obtenir_algorithmes_disponibles()
        
        print("\n=== ALGORITHMES DE TRI ===")
        for cle, (nom, _) in algorithmes.items():
            print(f"{cle}. {nom}")
        
        while True:
            choix = input("Choisissez l'algorithme (1-2): ").strip()
            if choix in algorithmes:
                nom, fonction = algorithmes[choix]
                return nom, fonction
            else:
                print("❌ Algorithme non disponible")
    
    def appliquer_tri(self, cle: str, ordre_croissant: bool, algorithme: callable) -> bool:
        """Étape: Appliquer algorithme de tri"""
        try:
            print(f"\n🔧 Application du tri...")
            print(f"Critère: {cle}")
            print(f"Ordre: {'Croissant' if ordre_croissant else 'Décroissant'}")
            
            self.donnees_triees, stats = algorithme(
                self.donnees_chargees, cle, ordre_croissant
            )
            
            # Afficher liste triée
            print(f"\n✅ LISTE TRIÉE ({len(self.donnees_triees)} éléments):")
            GestionnaireDonnees.afficher_donnees(self.donnees_triees)
            
            # Afficher statistiques
            stats.afficher()
            
            return True
        
        except Exception as e:
            print(f"❌ Erreur lors du tri: {str(e)}")
            return False
    
    def executer_flux_complet(self) -> bool:
        """Exécute le flux complet selon l'organigramme"""
        # Début - Charger les données
        if not self.charger_donnees():
            return False
        
        # Afficher liste chargée
        print(f"\n✅ LISTE CHARGÉE ({len(self.donnees_chargees)} éléments):")
        GestionnaireDonnees.afficher_donnees(self.donnees_chargees)
        
        # Choisir critère de tri
        critere = self.choisir_critere_tri()
        
        # Choisir ordre
        ordre_croissant = self.choisir_ordre_tri()
        
        # Choisir algorithme
        nom_algo, algorithme = self.choisir_algorithme()
        
        # Appliquer le tri
        return self.appliquer_tri(critere, ordre_croissant, algorithme)