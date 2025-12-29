# === Importation des modules nécessaires ===
import pygame  # Module principal pour créer le jeu
from pygame.locals import *  # Importe les constantes de Pygame
import random  # Pour générer des positions aléatoires
import time  # Pour mesurer le temps de jeu

# === Initialisation de Pygame ===
pygame.init()  # Démarre tous les modules Pygame
pygame.key.set_repeat(10, 10)  # Permet la répétition des touches maintenues enfoncées

# === Configuration de la fenêtre de jeu ===
LARGEUR, HAUTEUR = 800, 600  # Dimensions de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))  # Crée la fenêtre
pygame.display.set_caption("Space Shooter")  # Titre de la fenêtre

# === Définition des couleurs ===
WHITE = (255, 255, 255)  # Blanc
RED = (255, 0, 0)  # Rouge
GREEN = (0, 255, 0)  # Vert
BLACK = (0, 0, 0)  # Noir

# === Chargement et préparation des images ===
# Image de fond
fond = pygame.image.load("space_bg.jpg").convert()  # Charge l'image de fond
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))  # Redimensionne le fond

# Vaisseau du joueur
vaisseau = pygame.image.load("spaceship.png").convert_alpha()  # Charge avec transparence
vaisseau = pygame.transform.scale(vaisseau, (64, 64))  # Redimensionne

# Ennemis
enemy_img = pygame.image.load("alien.png").convert_alpha()  # Charge l'ennemi
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Redimensionne

# Projectiles
bullet_img = pygame.image.load("laser_bullet.png").convert_alpha()  # Charge le laser
bullet_img = pygame.transform.scale(bullet_img, (10, 30))  # Redimensionne

# Explosions
explosion_img = pygame.image.load("explosion.png").convert_alpha()  # Charge l'explosion
explosion_img = pygame.transform.scale(explosion_img, (60, 60))  # Redimensionne

# === Chargement des sons ===
pygame.mixer.music.load("space.wav")  # Charge la musique de fond
pygame.mixer.music.play(-1)  # Joue en boucle (-1 = infini)
shoot_sound = pygame.mixer.Sound("shoot.wav")  # Son du tir
explosion_sound = pygame.mixer.Sound("explosion.wav")  # Son de l'explosion

# === Configuration des polices de texte ===
font = pygame.font.SysFont(None, 28)  # Police normale
big_font = pygame.font.SysFont(None, 72)  # Grande police pour le Game Over

# === Classe pour gérer l'état du jeu ===
class GameState:
    def __init__(self):
        self.reset()  # Initialise l'état du jeu
    
    def reset(self):
        self.score = 0  # Score initial
        self.player_health = 200  # Points de vie initiaux
        self.max_health = 200  # Vie maximale
        self.lives = 3  # Nombre de vies
        self.game_over = False  # État du jeu
        self.start_time = time.time()  # Temps de début
        self.difficulty = 1.0  # Niveau de difficulté
        self.bullets = []  # Liste des projectiles
        self.enemies = []  # Liste des ennemis
        self.explosions = []  # Liste des explosions
        self.timer_enemy = 0  # Compteur pour la génération d'ennemis
        self.vaisseau_rect = vaisseau.get_rect(center=(LARGEUR // 2, HAUTEUR - 60))  # Position initiale

# Crée une instance de l'état du jeu
game_state = GameState()

# === Fonctions du jeu ===

def generer_ennemi():
    """Génère un ennemi à une position aléatoire en haut de l'écran"""
    x = random.randint(0, LARGEUR - enemy_img.get_width())  # Position X aléatoire
    rect = enemy_img.get_rect(topleft=(x, -50))  # Crée le rectangle de collision
    game_state.enemies.append(rect)  # Ajoute à la liste des ennemis

def afficher_infos():
    """Affiche toutes les informations du jeu (score, vie, temps)"""
    # Affiche le score
    texte = font.render(f"Score: {game_state.score}", True, WHITE)
    fenetre.blit(texte, (10, 10))
    
    # Affiche la barre de vie
    pygame.draw.rect(fenetre, RED, (10, 40, game_state.player_health, 20))
    pygame.draw.rect(fenetre, WHITE, (10, 40, game_state.max_health, 20), 2)
    
    # Affiche le nombre de vies
    texte_vies = font.render(f"Lives: {game_state.lives}", True, WHITE)
    fenetre.blit(texte_vies, (10, 70))
    
    # Affiche le temps écoulé
    elapsed = int(time.time() - game_state.start_time)
    texte_temps = font.render(f"Time: {elapsed}s", True, WHITE)
    fenetre.blit(texte_temps, (LARGEUR - 120, 10))

def game_over_screen():
    """Affiche l'écran de fin de jeu"""
    elapsed = int(time.time() - game_state.start_time)  # Calcule le temps écoulé
    
    # Crée un fond semi-transparent
    s = pygame.Surface((600, 300))
    s.set_alpha(200)
    s.fill(BLACK)
    fenetre.blit(s, (LARGEUR//2 - 300, HAUTEUR//2 - 150))
    
    # Affiche les textes de fin de jeu
    game_over_text = big_font.render("GAME OVER", True, RED)
    time_text = font.render(f"Time Survived: {elapsed} seconds", True, WHITE)
    score_text = font.render(f"Final Score: {game_state.score}", True, WHITE)
    retry_text = font.render("Press R to Retry or ESC to Quit", True, GREEN)

    fenetre.blit(game_over_text, (LARGEUR//2 - game_over_text.get_width()//2, HAUTEUR//2 - 100))
    fenetre.blit(time_text, (LARGEUR//2 - time_text.get_width()//2, HAUTEUR//2 - 20))
    fenetre.blit(score_text, (LARGEUR//2 - score_text.get_width()//2, HAUTEUR//2 + 20))
    fenetre.blit(retry_text, (LARGEUR//2 - retry_text.get_width()//2, HAUTEUR//2 + 70))

    pygame.display.update()  # Met à jour l'affichage

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:  # Si on clique sur la croix
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_r:  # Touche R pour recommencer
                    game_state.reset()
                    waiting = False
                if event.key == K_ESCAPE:  # Echap pour quitter
                    pygame.quit()
                    quit()

# === Boucle principale du jeu ===
clock = pygame.time.Clock()  # Crée une horloge pour contrôler le FPS
running = True  # Variable de contrôle de la boucle principale

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:  # Si on ferme la fenêtre
            running = False
        if event.type == KEYDOWN:
            if event.key == K_RETURN:  # Entrée pour tirer
                shoot_sound.play()  # Joue le son du tir
                bullet_rect = bullet_img.get_rect(center=(game_state.vaisseau_rect.centerx, game_state.vaisseau_rect.top))
                game_state.bullets.append(bullet_rect)  # Ajoute un nouveau projectile
            if event.key == K_ESCAPE:  # Echap pour quitter
                running = False

    if not game_state.game_over:
        # Contrôles du vaisseau
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and game_state.vaisseau_rect.left > 0:  # Flèche gauche
            game_state.vaisseau_rect.x -= 7  # Déplace à gauche
        if keys[K_RIGHT] and game_state.vaisseau_rect.right < LARGEUR:  # Flèche droite
            game_state.vaisseau_rect.x += 7  # Déplace à droite

        # Mouvement des lasers
        for bullet in game_state.bullets[:]:  # Parcourt une copie de la liste
            bullet.y -= 10  # Déplace le laser vers le haut
            if bullet.bottom < 0:  # Si sort de l'écran
                game_state.bullets.remove(bullet)  # Supprime le laser

        # Génération d'ennemis avec difficulté progressive
        game_state.timer_enemy += 1
        if game_state.timer_enemy > int(45 / game_state.difficulty):  # Intervalle variable
            generer_ennemi()
            game_state.timer_enemy = 0
            game_state.difficulty += 0.01  # Augmente légèrement la difficulté

        # Gestion des ennemis
        for enemy in game_state.enemies[:]:  # Parcourt une copie
            enemy.y += 3 * game_state.difficulty  # Déplace l'ennemi
            
            if enemy.top > HAUTEUR:  # Si sort par le bas
                game_state.enemies.remove(enemy)
                game_state.player_health -= 5  # Enlève de la vie

            # Collision balle-ennemi
            for bullet in game_state.bullets[:]:
                if enemy.colliderect(bullet):  # Détecte la collision
                    explosion_sound.play()
                    game_state.explosions.append([enemy.center, 30])  # Crée explosion
                    game_state.bullets.remove(bullet)
                    game_state.enemies.remove(enemy)
                    game_state.score += 10  # Augmente le score
                    break

            # Collision vaisseau-ennemi
            if enemy.colliderect(game_state.vaisseau_rect):
                explosion_sound.play()
                game_state.explosions.append([enemy.center, 30])
                game_state.enemies.remove(enemy)
                game_state.player_health -= 15  # Enlève plus de vie

        # Gestion des explosions
        for explosion in game_state.explosions[:]:
            position, timer = explosion
            fenetre.blit(explosion_img, explosion_img.get_rect(center=position))
            explosion[1] -= 1
            if explosion[1] <= 0:  # Si l'explosion est terminée
                game_state.explosions.remove(explosion)

        # Vérification fin de jeu
        if game_state.player_health <= 0:
            game_state.lives -= 1  # Enlève une vie
            if game_state.lives <= 0:  # Plus de vies
                game_state.game_over = True
            else:
                game_state.player_health = game_state.max_health  # Reset la vie

    # Affichage
    fenetre.blit(fond, (0, 0))  # Affiche le fond
    
    for bullet in game_state.bullets:  # Affiche tous les lasers
        fenetre.blit(bullet_img, bullet)
    
    for enemy in game_state.enemies:  # Affiche tous les ennemis
        fenetre.blit(enemy_img, enemy)
    
    fenetre.blit(vaisseau, game_state.vaisseau_rect)  # Affiche le vaisseau
    afficher_infos()  # Affiche les infos (score, vie, etc.)

    if game_state.game_over:  # Si jeu terminé
        game_over_screen()  # Affiche l'écran de fin

    pygame.display.update()  # Met à jour l'affichage
    clock.tick(60)  # 60 FPS

pygame.quit()  # Quitte proprement Pygame