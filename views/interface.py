"""
Interface utilisateur du programme
Gère l'affichage des menus et la navigation
"""

from controllers.tri_controller import ControleurTri


class InterfaceTri:
    """Gère l'interface utilisateur et le flux de navigation"""
    
    def __init__(self):
        self.controleur = ControleurTri()
    
    def afficher_menu_principal(self):
        """Affiche le menu principal et gère la navigation"""
        print("\n" + "="*50)
        print("       PROGRAMME DE TRI DE DONNÉES")
        print("="*50)
        
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Lancer le tri des données")
            print("2. Quitter")
            
            choix = input("\nChoisissez une option (1-2): ").strip()
            
            if choix == "1":
                self.lancer_tri()
            elif choix == "2":
                print("\n👋 Au revoir !")
                break
            else:
                print("❌ Option invalide")
    
    def lancer_tri(self):
        """Lance le processus complet de tri"""
        try:
            # Exécute le flux complet selon l'organigramme
            succes = self.controleur.executer_flux_complet()
            
            if succes:
                self.demander_recommencer()
            else:
                print("❌ Le tri a échoué")
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Opération annulée par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {str(e)}")
    
    def demander_recommencer(self):
        """Demande si l'utilisateur veut recommencer"""
        while True:
            recommencer = input("\n🔄 Voulez-vous recommencer? (o/n): ").strip().lower()
            
            if recommencer == 'o':
                self.lancer_tri()
                break
            elif recommencer == 'n':
                print("Retour au menu principal...")
                break
            else:
                print("❌ Réponse invalide. Tapez 'o' pour oui ou 'n' pour non")