#!/usr/bin/env python3
"""
Programme de tri de données - Point d'entrée principal
Version avec interface graphique simple
"""

from tri_interface import ApplicationTri

def main():
    """Début du programme - Point d'entrée principal"""
    app = ApplicationTri()
    app.demarrer()

if __name__ == "__main__":
    main()