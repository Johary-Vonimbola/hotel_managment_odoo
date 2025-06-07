# 🏨 Hotel Management System - Odoo 18

Ce projet est une solution complète de **gestion d’hôtel** développée sur la plateforme **Odoo 18**, avec une séparation claire entre la partie **Front Office** (destinée aux clients via le site web) et le **Back Office** (pour les gestionnaires et administrateurs de l’établissement).

---


## 📌 Fonctionnalités principales

### 🧾 Front Office (Website - clients)

- Consultation de la liste des chambres disponibles.
- Affichage des détails des chambres (prix, équipements inclus, capacité).
- Réservation d'une chambre avec sélection des dates.
- Création de compte client ou connexion si compte déjà existant.
- Suivi des réservations effectuées.

### 🛠️ Back Office (Administrateurs - Odoo)

- Gestion des chambres (prix de base, capacité, équipements associés, type de chambre, état).
- Gestion des réservations avec états (`booked`, `check_in`, `check_out`, `cancelled`).
- Historique des réservations avec calcul automatique du total.
- Gestion des équipements proposés dans les chambres (nom, description, prix).
- Liaison des équipements aux chambres par relation Many2many.
- Calcul automatique du prix total d’une chambre (base + équipements).
- Démonstration des données avec :
  - 10 équipements générés automatiquement.
  - 6 chambres de différents types avec ou sans équipements.

---

## 🧪 Données de Démo

Le module inclut des données de démonstration pour faciliter les tests en environnement local :
- Des **équipements types** comme TV, Climatisation, WiFi, Minibar, etc.
- Des **chambres de types variés**, prêtes à être réservées.
- Possibilité de tester l’interface client directement via `/hotel/reservations`.

---

## 🧑‍💻 Installation & Lancement

1. Cloner le dépôt :
```bash
git clone https://github.com/Johary-Vonimbola/hotel_managment_odoo.git
python odoo-bin -c <odoo.conf> -u hotel_backoffice, hotel_front_office
