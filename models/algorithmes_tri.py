"""
Implémentation des algorithmes de tri
Correspond à l'étape 'Appliquer algorithme de tri' de l'organigramme
"""

from typing import List, Dict, Any, Callable
import time


class StatistiquesTri:
    """Stocke les statistiques d'exécution du tri"""
    
    def __init__(self):
        self.temps_execution = 0.0
        self.comparaisons = 0
        self.permutations = 0
        self.algorithm_utilise = ""
    
    def afficher(self):
        """Affiche les statistiques de tri"""
        print(f"\n=== STATISTIQUES DU TRI ===")
        print(f"Algorithme: {self.algorithm_utilise}")
        print(f"Temps d'exécution: {self.temps_execution:.6f} secondes")
        print(f"Nombre de comparaisons: {self.comparaisons}")
        print(f"Nombre de permutations: {self.permutations}")


class AlgorithmesTri:
    """Implémente les différents algorithmes de tri"""
    
    @staticmethod
    def tri_insertion(donnees: List[Dict[str, Any]], cle: str, ordre_croissant: bool = True) -> tuple:
        """Algorithme de tri par insertion"""
        stats = StatistiquesTri()
        stats.algorithm_utilise = "Tri par insertion"
        
        debut = time.time()
        donnees_triees = donnees.copy()
        
        for i in range(1, len(donnees_triees)):
            element_courant = donnees_triees[i]
            j = i - 1
            
            while j >= 0:
                stats.comparaisons += 1
                
                # Comparaison selon l'ordre
                if ordre_croissant:
                    condition = donnees_triees[j][cle] > element_courant[cle]
                else:
                    condition = donnees_triees[j][cle] < element_courant[cle]
                
                if condition:
                    stats.permutations += 1
                    donnees_triees[j + 1] = donnees_triees[j]
                    j -= 1
                else:
                    break
            
            donnees_triees[j + 1] = element_courant
        
        stats.temps_execution = time.time() - debut
        return donnees_triees, stats
    
    @staticmethod
    def tri_bulles(donnees: List[Dict[str, Any]], cle: str, ordre_croissant: bool = True) -> tuple:
        """Algorithme de tri à bulles"""
        stats = StatistiquesTri()
        stats.algorithm_utilise = "Tri à bulles"
        
        debut = time.time()
        donnees_triees = donnees.copy()
        n = len(donnees_triees)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                stats.comparaisons += 1
                
                # Comparaison selon l'ordre
                if ordre_croissant:
                    condition = donnees_triees[j][cle] > donnees_triees[j + 1][cle]
                else:
                    condition = donnees_triees[j][cle] < donnees_triees[j + 1][cle]
                
                if condition:
                    stats.permutations += 1
                    donnees_triees[j], donnees_triees[j + 1] = donnees_triees[j + 1], donnees_triees[j]
        
        stats.temps_execution = time.time() - debut
        return donnees_triees, stats
    
    @staticmethod
    def obtenir_algorithmes_disponibles() -> Dict[str, Callable]:
        """Retourne la liste des algorithmes disponibles"""
        return {
            "1": ("Tri par insertion", AlgorithmesTri.tri_insertion),
            "2": ("Tri à bulles", AlgorithmesTri.tri_bulles)
        }