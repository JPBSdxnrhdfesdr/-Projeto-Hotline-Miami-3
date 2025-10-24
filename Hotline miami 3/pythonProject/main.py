import pygame
import sys
import random
import math
from enum import Enum

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Constantes
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 64
FPS = 60

# Cores
RED = (255, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 180)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BLOOD_RED = (138, 7, 7)
ORANGE = (255, 165, 0)
DARK_RED = (100, 0, 0)


# Estados do jogo
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    LEVEL_COMPLETE = 3
    DIALOG = 4
    CUTSCENE = 5


# Tipos de personagem
class CharacterType(Enum):
    VETERAN = 0
    INVESTIGATOR = 1
    SUCCESSOR = 2
    EXECUTIONER = 3
    SOLDIER = 4  # Novo personagem - Soldado da guerra


# Tipos de arma
class WeaponType(Enum):
    FISTS = 0
    KNIFE = 1
    BAT = 2
    KATANA = 3
    PISTOL = 4
    SHOTGUN = 5
    UZI = 6
    SNIPER = 7
    RIFLE = 8  # Nova arma para soldado


# Estados do inimigo
class EnemyState(Enum):
    ALIVE = 0
    STUNNED = 1
    DEAD = 2


# Estados do jogador
class PlayerState(Enum):
    ALIVE = 0
    DOWNED = 1
    DEAD = 2


class DialogSystem:
    def __init__(self):
        self.dialogs = {
            # Veterano
            1: ["50 BLESSINGS: A RÚSSIA PRECISA SER PUNIDA...", "ENCONTRE O PACOTE NO ESCRITÓRIO."],
            2: ["VOCÊ: ESSE LUGAR PARECE FAMILIAR...", "PRECISO ENCONTRAR RESPOSTAS."],
            3: ["VOCÊ: ELES SABIAM... TUDO ISSO FOI UM EXPERIMENTO."],

            # Investigadora
            4: ["DETETIVE: ESSE É O LOCAL DO MASSACRE...", "PRECISO DE EVIDÊNCIAS."],
            5: ["DETETIVE: A 50 BLESSINGS AINDA ESTÁ ATIVA!", "ALGUÉM ESTÁ DANDO AS ORDENS AGORA."],
            6: ["DETETIVE: ENCONTREI ALGO...", "UMA NOVA MÁSCARA, UM NOVO ASSASSINO."],

            # Sucessor
            7: ["VOCÊ: ELES SÃO FRACOS...", "A VIOLÊNCIA É A ÚNICA LINGUAGEM QUE ENTENDEM."],
            8: ["VOCÊ: ISSO É ARTE...", "CADVER CAÍDO É UMA OBRA-PRIMA."],
            9: ["VOCÊ: EU SOU A EVOLUÇÃO..."],

            # Executioner
            10: ["EXECUTIONER: A ORDEM DEVE SER RESTAURADA.", "MATEM TODOS OS SOBREVIVENTES."],
            11: ["EXECUTIONER: VOCÊS SÃO IMPUREZAS...", "SERÃO ELIMINADOS."],
            12: ["EXECUTIONER: EU SOU O VERDADEIRO SUCESSOR."],

            # Soldier
            13: ["SOLDADO: 1989, HAWAII...", "OS FÃS ESTÃO AQUI PARA LIMPAR A SUJEIRA."],
            14: ["SOLDADO: ESTE É O VERDADEIRO TRABALHO...", "ANTES DA 50 BLESSINGS."],
            15: ["SOLDADO: NÓS CRIAMOS O MONSTRO...", "AGORA PRECISAMOS DESTRUÍ-LO."],

            # Cutscenes
            "intro": ["1990: O LEGADO DA 50 BLESSINGS CONTINUA...",
                      "UMA NOVA GERAÇÃO HERDOU O CAOS...",
                      "TRÊS ALMAS PERDIDAS, UM DESTINO SANGRENTO..."],

            "mid_game": ["O CICLO SE REPETE...",
                         "MAS ALGO MUDA DESTA VEZ...",
                         "UM NOVO JOGADOR ENTRA EM CENA..."],

            "final": ["A VERDADE É PIOR QUE A FICÇÃO...",
                      "50 BLESSINGS NUNCA FOI SOBRE PATRIOTISMO...",
                      "ERA SOBRE CONTROLE... EXPERIMENTOS...",
                      "E O EXPERIMENTO CONTINUA..."],

            "soldier_intro": ["1989 - HAWAII",
                              "ANTES DA 50 BLESSINGS...",
                              "O ESQUADRÃO 'THE FANS' EM AÇÃO...",
                              "A ORIGEM DO PESADELO"]
        }
        self.current_dialog = []
        self.dialog_index = 0
        self.dialog_timer = 0
        self.is_cutscene = False

    def start_dialog(self, dialog_key):
        if dialog_key in self.dialogs:
            self.current_dialog = self.dialogs[dialog_key]
            self.dialog_index = 0
            self.dialog_timer = 180  # 3 segundos
            self.is_cutscene = isinstance(dialog_key, str)
            return True
        return False

    def update(self):
        if self.current_dialog and self.dialog_timer > 0:
            self.dialog_timer -= 1
            if self.dialog_timer == 0:
                self.next_line()

    def next_line(self):
        self.dialog_index += 1
        if self.dialog_index < len(self.current_dialog):
            self.dialog_timer = 180
        else:
            self.current_dialog = []
            self.dialog_index = 0

    def draw(self, screen):
        if self.current_dialog and self.dialog_timer > 0:
            if self.is_cutscene:
                # Fundo para cutscene
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                text = self.current_dialog[self.dialog_index]
                font = pygame.font.SysFont('Arial', 36)
                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2,
                                           SCREEN_HEIGHT // 2 - 50))

                # Instrução para pular
                skip_font = pygame.font.SysFont('Arial', 18)
                skip_text = skip_font.render("Pressione ESPAÇO para continuar", True, YELLOW)
                screen.blit(skip_text, (SCREEN_WIDTH // 2 - skip_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 + 50))
            else:
                # Dialogo normal durante o jogo
                text = self.current_dialog[self.dialog_index]
                font = pygame.font.SysFont('Arial', 24)

                # Fundo do diálogo
                dialog_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100)
                pygame.draw.rect(screen, (30, 30, 30), dialog_rect)
                pygame.draw.rect(screen, WHITE, dialog_rect, 2)

                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (70, SCREEN_HEIGHT - 130))


class Weapon:
    def __init__(self, weapon_type):
        self.weapon_type = weapon_type
        self.damage = 10
        self.range = 40
        self.cooldown = 20
        self.ammo = 0
        self.max_ammo = 0
        self.is_ranged = False
        self.is_melee = True
        self.texture = None

        self.setup_weapon()

    def setup_weapon(self):
        if self.weapon_type == WeaponType.FISTS:
            self.damage = 999  # Hit kill
            self.range = 35
            self.cooldown = 15
            self.is_melee = True
        elif self.weapon_type == WeaponType.KNIFE:
            self.damage = 999
            self.range = 40
            self.cooldown = 10
            self.is_melee = True
        elif self.weapon_type == WeaponType.BAT:
            self.damage = 999
            self.range = 50
            self.cooldown = 25
            self.is_melee = True
        elif self.weapon_type == WeaponType.KATANA:
            self.damage = 999
            self.range = 60
            self.cooldown = 15
            self.is_melee = True
        elif self.weapon_type == WeaponType.PISTOL:
            self.damage = 999
            self.range = 300
            self.cooldown = 30
            self.ammo = 12
            self.max_ammo = 12
            self.is_ranged = True
            self.is_melee = False
        elif self.weapon_type == WeaponType.SHOTGUN:
            self.damage = 999
            self.range = 150
            self.cooldown = 60
            self.ammo = 6
            self.max_ammo = 6
            self.is_ranged = True
            self.is_melee = False
        elif self.weapon_type == WeaponType.UZI:
            self.damage = 999
            self.range = 200
            self.cooldown = 5
            self.ammo = 30
            self.max_ammo = 30
            self.is_ranged = True
            self.is_melee = False
        elif self.weapon_type == WeaponType.SNIPER:
            self.damage = 999
            self.range = 500
            self.cooldown = 90
            self.ammo = 5
            self.max_ammo = 5
            self.is_ranged = True
            self.is_melee = False
        elif self.weapon_type == WeaponType.RIFLE:
            self.damage = 999
            self.range = 400
            self.cooldown = 25
            self.ammo = 20
            self.max_ammo = 20
            self.is_ranged = True
            self.is_melee = False

    def can_attack(self):
        return self.cooldown <= 0 and (not self.is_ranged or self.ammo > 0)

    def attack(self):
        if self.can_attack():
            self.cooldown = self.get_cooldown()
            if self.is_ranged:
                self.ammo -= 1
            return True
        return False

    def get_cooldown(self):
        return self.cooldown

    def reload(self):
        if self.is_ranged:
            self.ammo = self.max_ammo
            return True
        return False


class Player:
    def __init__(self, character_type):
        self.character_type = character_type

        # Definir atributos baseados no tipo de personagem ANTES de chamar reset()
        if character_type == CharacterType.VETERAN:
            self.speed = 4
            self.max_health = 3  # 2-3 tiros para morrer
            self.mask_ability = "slow_time"
        elif character_type == CharacterType.INVESTIGATOR:
            self.speed = 3.5
            self.max_health = 2
            self.mask_ability = "mark_enemy"
        elif character_type == CharacterType.SUCCESSOR:
            self.speed = 4.5
            self.max_health = 2
            self.mask_ability = "berserk"
        elif character_type == CharacterType.EXECUTIONER:
            self.speed = 3.8
            self.max_health = 3
            self.mask_ability = "execute"
        elif character_type == CharacterType.SOLDIER:
            self.speed = 4.2
            self.max_health = 4  # Mais resistente
            self.mask_ability = "grenade"

        self.weapons = [Weapon(WeaponType.FISTS)]
        self.current_weapon_index = 0
        self.state = PlayerState.ALIVE
        self.downed_timer = 0
        self.reset()

        self.ability_cooldown = 0
        self.ability_duration = 0
        self.marked_enemy = None
        self.texture = self.load_texture()
        self.downed_texture = self.load_downed_texture()

    def load_texture(self):
        # Criar texturas detalhadas baseadas no tipo
        texture = pygame.Surface((TILE_SIZE - 20, TILE_SIZE - 20), pygame.SRCALPHA)

        if self.character_type == CharacterType.VETERAN:
            # Veterano - azul com detalhes
            texture.fill(BLUE)
            pygame.draw.rect(texture, (100, 100, 255), (5, 5, TILE_SIZE - 30, TILE_SIZE - 30))
            pygame.draw.circle(texture, WHITE, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 8)
            # Detalhes da máscara
            pygame.draw.line(texture, BLACK, (15, 20), (TILE_SIZE - 25, 20), 2)

        elif self.character_type == CharacterType.INVESTIGATOR:
            # Investigadora - verde com detalhes
            texture.fill(GREEN)
            pygame.draw.rect(texture, (100, 200, 100), (8, 8, TILE_SIZE - 36, TILE_SIZE - 36))
            pygame.draw.circle(texture, WHITE, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 10)
            # Olhos
            pygame.draw.circle(texture, BLACK, (20, 20), 3)
            pygame.draw.circle(texture, BLACK, (TILE_SIZE - 25, 20), 3)

        elif self.character_type == CharacterType.SUCCESSOR:
            # Sucessor - vermelho com detalhes
            texture.fill(RED)
            pygame.draw.polygon(texture, (255, 100, 100), [
                (10, 10), (TILE_SIZE - 30, 10), (TILE_SIZE // 2 - 10, TILE_SIZE - 30)
            ])
            # Padrão agressivo
            for i in range(3):
                pygame.draw.line(texture, BLACK, (10 + i * 10, 15), (TILE_SIZE - 30, 15 + i * 5), 1)

        elif self.character_type == CharacterType.EXECUTIONER:
            # Executioner - roxo com detalhes
            texture.fill(PURPLE)
            pygame.draw.rect(texture, (150, 50, 150), (5, 5, TILE_SIZE - 30, TILE_SIZE - 30), 3)
            # X marcado
            pygame.draw.line(texture, WHITE, (10, 10), (TILE_SIZE - 30, TILE_SIZE - 30), 3)
            pygame.draw.line(texture, WHITE, (TILE_SIZE - 30, 10), (10, TILE_SIZE - 30), 3)

        elif self.character_type == CharacterType.SOLDIER:
            # Soldier - camuflagem
            texture.fill((100, 80, 60))  # Marrom base
            # Padrão de camuflagem
            colors = [(80, 100, 60), (120, 100, 80), (60, 80, 100)]
            for i in range(8):
                color = random.choice(colors)
                x = random.randint(5, TILE_SIZE - 25)
                y = random.randint(5, TILE_SIZE - 25)
                size = random.randint(8, 15)
                pygame.draw.ellipse(texture, color, (x, y, size, size))
            # Capacete
            pygame.draw.ellipse(texture, DARK_GRAY, (10, 5, TILE_SIZE - 30, 15))

        return texture

    def load_downed_texture(self):
        # Textura quando o jogador está caído
        texture = pygame.Surface((TILE_SIZE - 20, TILE_SIZE - 20), pygame.SRCALPHA)
        texture.fill((100, 100, 100, 180))  # Cinza semi-transparente
        pygame.draw.ellipse(texture, RED, (10, 10, TILE_SIZE - 40, TILE_SIZE - 40))
        return texture

    def reset(self):
        self.x = 100
        self.y = 100
        self.health = self.max_health
        self.direction = (1, 0)
        self.attack_cooldown = 0
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.legacy_points = 0
        self.weapons = [Weapon(WeaponType.FISTS)]
        self.current_weapon_index = 0
        self.state = PlayerState.ALIVE
        self.downed_timer = 0

    def move(self, dx, dy, walls):
        if self.state != PlayerState.ALIVE:
            return

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Verificar colisão com paredes
        future_rect = pygame.Rect(new_x, new_y, TILE_SIZE - 20, TILE_SIZE - 20)
        collision = False

        for wall in walls:
            if future_rect.colliderect(wall):
                collision = True
                break

        if not collision:
            self.x = new_x
            self.y = new_y
            if dx != 0 or dy != 0:
                self.direction = (dx, dy)

    def attack(self, enemies):
        if self.state != PlayerState.ALIVE:
            return None

        weapon = self.weapons[self.current_weapon_index]

        if weapon.can_attack() and weapon.attack():
            if weapon.is_ranged:
                # Criar projétil
                return self.create_projectile()
            else:
                # Ataque corpo a corpo - sempre derruba inimigos
                attack_rect = pygame.Rect(
                    self.x + self.direction[0] * weapon.range,
                    self.y + self.direction[1] * weapon.range,
                    weapon.range, weapon.range
                )

                for enemy in enemies:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, TILE_SIZE - 20, TILE_SIZE - 20)
                    if attack_rect.colliderect(enemy_rect) and enemy.state == EnemyState.ALIVE:
                        enemy.state = EnemyState.STUNNED
                        enemy.stun_timer = 180  # 3 segundos caído
                        self.combo += 1
                        self.combo_timer = 60
                        self.score += 10 * self.combo
                        self.legacy_points += 1
                        return True
        return None

    def execute_enemy(self, enemies):
        """Executar inimigo caído (como no HM2)"""
        if self.state != PlayerState.ALIVE:
            return False

        weapon = self.weapons[self.current_weapon_index]
        execute_rect = pygame.Rect(
            self.x + self.direction[0] * 50,
            self.y + self.direction[1] * 50,
            60, 60
        )

        for enemy in enemies:
            if enemy.state == EnemyState.STUNNED:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, TILE_SIZE - 20, TILE_SIZE - 20)
                if execute_rect.colliderect(enemy_rect):
                    # Execução baseada na arma
                    if weapon.is_melee:
                        enemy.health = 0
                        enemy.state = EnemyState.DEAD
                        self.score += 50
                        return True
                    elif weapon.is_ranged:
                        # Headshot - instant kill
                        enemy.health = 0
                        enemy.state = EnemyState.DEAD
                        self.score += 75
                        return True
        return False

    def create_projectile(self):
        weapon = self.weapons[self.current_weapon_index]
        return Projectile(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2,
                          self.direction[0], self.direction[1],
                          weapon.damage, weapon.range, weapon.weapon_type)

    def use_ability(self, enemies):
        if self.state != PlayerState.ALIVE or self.ability_cooldown > 0:
            return None

        if self.mask_ability == "slow_time":
            self.ability_duration = 180
            self.ability_cooldown = 600
            return "LENTIDÃO TEMPORAL ATIVADA"

        elif self.mask_ability == "mark_enemy" and enemies:
            alive_enemies = [e for e in enemies if e.state == EnemyState.ALIVE]
            if alive_enemies:
                self.marked_enemy = random.choice(alive_enemies)
                self.ability_cooldown = 300
                return "INIMIGO MARCADO"

        elif self.mask_ability == "berserk":
            self.ability_duration = 120
            self.ability_cooldown = 480
            return "MODO BERSERK"

        elif self.mask_ability == "execute" and enemies:
            # Executar inimigo mais próximo
            closest_enemy = None
            min_dist = float('inf')

            for enemy in enemies:
                if enemy.state == EnemyState.ALIVE:
                    dist = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
                    if dist < 100 and dist < min_dist:
                        closest_enemy = enemy
                        min_dist = dist

            if closest_enemy:
                closest_enemy.health = 0
                closest_enemy.state = EnemyState.DEAD
                self.ability_cooldown = 300
                return "INIMIGO EXECUTADO"

        elif self.mask_ability == "grenade":
            # Nova habilidade - granada
            self.ability_cooldown = 600
            return self.create_grenade()

        return None

    def create_grenade(self):
        return Grenade(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2,
                       self.direction[0], self.direction[1])

    def take_damage(self, damage):
        if self.state != PlayerState.ALIVE:
            return

        # Chance aleatória de sobreviver
        survival_chance = random.random()
        if survival_chance < 0.3:  # 30% de chance de sobreviver
            self.health -= 1
        else:
            self.health -= damage

        if self.health <= 0:
            self.state = PlayerState.DOWNED
            self.downed_timer = 300  # 5 segundos para se levantar
            self.health = 1  # Fica com 1 de vida quando se levantar

    def update(self):
        if self.state == PlayerState.DOWNED:
            self.downed_timer -= 1
            if self.downed_timer <= 0:
                self.state = PlayerState.ALIVE
                self.show_message("RECUPERADO!")

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualizar cooldown das armas
        for weapon in self.weapons:
            if weapon.cooldown > 0:
                weapon.cooldown -= 1

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        if self.ability_duration > 0:
            self.ability_duration -= 1
            if self.ability_duration == 0 and self.mask_ability == "berserk":
                # Reverter efeitos do berserk
                pass

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0

    def show_message(self, message):
        # Método auxiliar para mostrar mensagens
        pass

    def switch_weapon(self, direction):
        if self.state != PlayerState.ALIVE:
            return
        self.current_weapon_index = (self.current_weapon_index + direction) % len(self.weapons)

    def add_weapon(self, weapon_type):
        if self.state != PlayerState.ALIVE:
            return False

        # Não adicionar armas duplicadas
        for weapon in self.weapons:
            if weapon.weapon_type == weapon_type:
                weapon.ammo = weapon.max_ammo  # Recarregar se já tiver a arma
                return False

        new_weapon = Weapon(weapon_type)
        self.weapons.append(new_weapon)
        return True

    def draw(self, screen, camera_x, camera_y):
        if self.state == PlayerState.DOWNED:
            screen.blit(self.downed_texture, (self.x - camera_x, self.y - camera_y))
            # Animação de rastejar
            crawl_offset = math.sin(pygame.time.get_ticks() * 0.01) * 5
            pygame.draw.circle(screen, RED,
                               (int(self.x - camera_x + TILE_SIZE // 2),
                                int(self.y - camera_y + TILE_SIZE // 2 + crawl_offset)), 3)
        else:
            screen.blit(self.texture, (self.x - camera_x, self.y - camera_y))

            # Indicador de direção
            dir_x = self.x + (TILE_SIZE - 20) // 2 + self.direction[0] * 20 - camera_x
            dir_y = self.y + (TILE_SIZE - 20) // 2 + self.direction[1] * 20 - camera_y
            pygame.draw.circle(screen, YELLOW, (dir_x, dir_y), 5)


class Grenade:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx * 5
        self.dy = dy * 5
        self.timer = 90  # 1.5 segundos
        self.exploded = False
        self.radius = 150

    def update(self, walls, enemies):
        if self.exploded:
            return True

        self.x += self.dx
        self.y += self.dy
        self.timer -= 1

        # Verificar colisão com paredes
        grenade_rect = pygame.Rect(self.x - 8, self.y - 8, 16, 16)
        for wall in walls:
            if grenade_rect.colliderect(wall):
                self.explode(enemies)
                return True

        if self.timer <= 0:
            self.explode(enemies)
            return True

        return False

    def explode(self, enemies):
        self.exploded = True
        # Matar todos os inimigos no raio
        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            if dist < self.radius:
                enemy.health = 0
                enemy.state = EnemyState.DEAD

    def draw(self, screen, camera_x, camera_y):
        if not self.exploded:
            pygame.draw.circle(screen, ORANGE, (int(self.x - camera_x), int(self.y - camera_y)), 8)
            # Timer visual
            pygame.draw.circle(screen, RED, (int(self.x - camera_x), int(self.y - camera_y)),
                               max(3, self.timer // 10))


class Projectile:
    def __init__(self, x, y, dx, dy, damage, range, weapon_type):
        self.x = x
        self.y = y
        self.dx = dx * 15  # Velocidade aumentada
        self.dy = dy * 15
        self.damage = damage
        self.range = range
        self.distance_traveled = 0
        self.weapon_type = weapon_type
        self.active = True

    def update(self, walls, enemies):
        if not self.active:
            return None

        self.x += self.dx
        self.y += self.dy
        self.distance_traveled += math.sqrt(self.dx ** 2 + self.dy ** 2)

        # Verificar colisão com paredes
        proj_rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)
        for wall in walls:
            if proj_rect.colliderect(wall):
                self.active = False
                return "wall"

        # Verificar colisão com inimigos
        for enemy in enemies:
            if enemy.state == EnemyState.ALIVE:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, TILE_SIZE - 20, TILE_SIZE - 20)
                if proj_rect.colliderect(enemy_rect):
                    enemy.take_damage(self.damage)
                    self.active = False
                    return enemy

        # Verificar alcance máximo
        if self.distance_traveled >= self.range:
            self.active = False

        return None

    def draw(self, screen, camera_x, camera_y):
        if self.active:
            if self.weapon_type in [WeaponType.PISTOL, WeaponType.SNIPER, WeaponType.RIFLE]:
                color = YELLOW
                size = 4
            elif self.weapon_type == WeaponType.SHOTGUN:
                color = ORANGE
                size = 6
            else:  # UZI
                color = WHITE
                size = 3

            pygame.draw.circle(screen, color,
                               (int(self.x - camera_x), int(self.y - camera_y)), size)
            # Efeito de rastro
            for i in range(3):
                trail_x = self.x - self.dx * (i + 1) * 0.3 - camera_x
                trail_y = self.y - self.dy * (i + 1) * 0.3 - camera_y
                alpha = 150 - i * 50
                trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (*color, alpha), (size, size), size - i)
                screen.blit(trail_surface, (trail_x - size, trail_y - size))


class Enemy:
    def __init__(self, x, y, enemy_type="guard"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.health = 1  # Hit kill para inimigos também
        self.speed = 2
        self.attack_cooldown = 0
        self.detection_range = 150
        self.attack_range = 50
        self.has_weapon = random.choice([True, False])
        self.weapon = None
        self.state = EnemyState.ALIVE
        self.stun_timer = 0
        self.texture = self.load_texture()
        self.stun_texture = self.load_stun_texture()

        if enemy_type == "heavy":
            self.health = 2  # Leva 2 hits
            self.speed = 1.5
        elif enemy_type == "fast":
            self.speed = 3.5
        elif enemy_type == "sniper":
            self.detection_range = 300
            self.attack_range = 250
            self.has_weapon = True

        if self.has_weapon:
            self.weapon = Weapon(random.choice([WeaponType.PISTOL, WeaponType.KNIFE, WeaponType.BAT]))

    def load_texture(self):
        texture = pygame.Surface((TILE_SIZE - 20, TILE_SIZE - 20), pygame.SRCALPHA)

        if self.enemy_type == "guard":
            texture.fill(LIGHT_GRAY)
            # Detalhes do inimigo
            pygame.draw.rect(texture, DARK_GRAY, (10, 5, TILE_SIZE - 40, 10))  # Cabeça
            pygame.draw.rect(texture, (80, 80, 80), (15, 20, TILE_SIZE - 50, TILE_SIZE - 40))  # Corpo
            pygame.draw.circle(texture, RED, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 6)  # Alvo

        elif self.enemy_type == "heavy":
            texture.fill(PURPLE)
            pygame.draw.rect(texture, (120, 0, 120), (5, 5, TILE_SIZE - 30, TILE_SIZE - 30))
            pygame.draw.circle(texture, RED, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 8)
            # Armadura
            pygame.draw.rect(texture, DARK_GRAY, (8, 8, TILE_SIZE - 36, 12))

        elif self.enemy_type == "fast":
            texture.fill(YELLOW)
            pygame.draw.polygon(texture, (200, 200, 0), [
                (10, 10), (TILE_SIZE - 30, TILE_SIZE // 2 - 10), (10, TILE_SIZE - 30)
            ])
            pygame.draw.circle(texture, RED, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 5)

        elif self.enemy_type == "sniper":
            texture.fill(DARK_GRAY)
            pygame.draw.rect(texture, (60, 60, 60), (5, 5, TILE_SIZE - 30, TILE_SIZE - 30))
            pygame.draw.circle(texture, GREEN, (TILE_SIZE // 2 - 10, TILE_SIZE // 2 - 10), 7)
            # Mira de sniper
            pygame.draw.line(texture, WHITE, (15, TILE_SIZE // 2 - 10), (TILE_SIZE - 25, TILE_SIZE // 2 - 10), 1)
            pygame.draw.line(texture, WHITE, (TILE_SIZE // 2 - 10, 15), (TILE_SIZE // 2 - 10, TILE_SIZE - 25), 1)

        return texture

    def load_stun_texture(self):
        texture = pygame.Surface((TILE_SIZE - 20, TILE_SIZE - 20), pygame.SRCALPHA)
        texture.fill((150, 150, 150, 200))  # Cinza quando caído
        pygame.draw.ellipse(texture, (100, 100, 100), (10, 15, TILE_SIZE - 40, TILE_SIZE - 50))
        return texture

    def take_damage(self, damage):
        if self.state != EnemyState.ALIVE:
            return False

        self.health -= damage
        if self.health <= 0:
            self.state = EnemyState.DEAD
            return True
        return False

    def update(self, player, walls, projectiles):
        if self.state == EnemyState.DEAD:
            return None
        elif self.state == EnemyState.STUNNED:
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.state = EnemyState.ALIVE
            return None

        # IA melhorada: persegue o jogador se estiver no alcance
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.detection_range and player.state == PlayerState.ALIVE:
            if self.enemy_type == "sniper" and dist < self.attack_range:
                # Sniper fica parado e atira
                if dist > 0:
                    dx, dy = dx / dist, dy / dist

                if self.attack_cooldown <= 0 and self.weapon and self.weapon.can_attack():
                    self.attack_cooldown = self.weapon.get_cooldown()
                    return self.create_projectile(dx, dy)
            else:
                # Movimento normal
                if dist > 0:
                    dx, dy = dx / dist, dy / dist

                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed

                # Verificar colisão com paredes
                future_rect = pygame.Rect(new_x, new_y, TILE_SIZE - 20, TILE_SIZE - 20)
                collision = False

                for wall in walls:
                    if future_rect.colliderect(wall):
                        collision = True
                        break

                if not collision:
                    self.x = new_x
                    self.y = new_y

                # Atacar se estiver perto o suficiente
                if dist < self.attack_range and self.attack_cooldown <= 0:
                    if self.weapon and self.weapon.is_ranged:
                        self.attack_cooldown = self.weapon.get_cooldown()
                        return self.create_projectile(dx, dy)
                    else:
                        player.take_damage(999)  # Hit kill do inimigo
                        self.attack_cooldown = 60

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        return None

    def create_projectile(self, dx, dy):
        if self.weapon and self.weapon.attack():
            return Projectile(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2,
                              dx, dy, self.weapon.damage, self.weapon.range,
                              self.weapon.weapon_type)
        return None

    def draw(self, screen, camera_x, camera_y, is_marked=False):
        if self.state == EnemyState.STUNNED:
            screen.blit(self.stun_texture, (self.x - camera_x, self.y - camera_y))
            # Indicador de que pode ser executado
            pygame.draw.circle(screen, RED,
                               (int(self.x - camera_x + TILE_SIZE // 2),
                                int(self.y - camera_y + TILE_SIZE // 2)), 5)
        elif self.state == EnemyState.ALIVE:
            screen.blit(self.texture, (self.x - camera_x, self.y - camera_y))

        if is_marked:
            # Efeito de inimigo marcado
            mark_rect = pygame.Rect(self.x - camera_x - 5, self.y - camera_y - 5,
                                    TILE_SIZE - 10, TILE_SIZE - 10)
            pygame.draw.rect(screen, RED, mark_rect, 3)


class Level:
    def __init__(self, level_num, character_type, legacy_points=0):
        self.level_num = level_num
        self.character_type = character_type
        self.walls = []
        self.enemies = []
        self.weapon_pickups = []
        self.spawn_point = (100, 100)
        self.exit_point = (900, 600)
        self.legacy_points = legacy_points
        self.background_texture = self.create_background()
        self.wall_textures = self.create_wall_textures()

        self.generate_level()

    def create_background(self):
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Padrão baseado no tipo de personagem e número do nível
        if self.character_type == CharacterType.VETERAN:
            base_color = (25, 25, 45)  # Azul escuro
            pattern_color = (40, 40, 80)
        elif self.character_type == CharacterType.INVESTIGATOR:
            base_color = (25, 45, 25)  # Verde escuro
            pattern_color = (40, 80, 40)
        elif self.character_type == CharacterType.SUCCESSOR:
            base_color = (45, 25, 25)  # Vermelho escuro
            pattern_color = (80, 40, 40)
        elif self.character_type == CharacterType.EXECUTIONER:
            base_color = (35, 25, 40)  # Roxo escuro
            pattern_color = (60, 40, 80)
        elif self.character_type == CharacterType.SOLDIER:
            base_color = (60, 50, 30)  # Camuflagem base
            pattern_color = (80, 70, 40)

        background.fill(base_color)

        # Padrão de textura mais elaborado
        for x in range(0, SCREEN_WIDTH, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                if (x // 40 + y // 40) % 2 == 0:
                    pygame.draw.rect(background, pattern_color, (x, y, 20, 20))
                # Adicionar ruído
                for i in range(3):
                    rx = random.randint(x, x + 39)
                    ry = random.randint(y, y + 39)
                    brightness = random.randint(-15, 15)
                    noise_color = (
                        max(0, min(255, base_color[0] + brightness)),
                        max(0, min(255, base_color[1] + brightness)),
                        max(0, min(255, base_color[2] + brightness))
                    )
                    pygame.draw.rect(background, noise_color, (rx, ry, 2, 2))

        return background

    def create_wall_textures(self):
        textures = []
        # Criar diferentes texturas para paredes
        for i in range(3):
            texture = pygame.Surface((TILE_SIZE, TILE_SIZE))
            if i == 0:
                # Tijolos
                texture.fill((80, 60, 60))
                for y in range(0, TILE_SIZE, 8):
                    for x in range(0, TILE_SIZE, 16):
                        offset = 0 if (y // 8) % 2 == 0 else 8
                        pygame.draw.rect(texture, (100, 80, 80), (x + offset, y, 14, 6))
            elif i == 1:
                # Concreto
                texture.fill((100, 100, 100))
                for _ in range(20):
                    x = random.randint(0, TILE_SIZE - 4)
                    y = random.randint(0, TILE_SIZE - 4)
                    pygame.draw.rect(texture, (120, 120, 120), (x, y, 2, 2))
            else:
                # Metal
                texture.fill((70, 70, 80))
                for y in range(0, TILE_SIZE, 4):
                    pygame.draw.line(texture, (90, 90, 100), (0, y), (TILE_SIZE, y), 1)

            textures.append(texture)
        return textures

    def generate_level(self):
        # Limpar level anterior
        self.walls = []
        self.enemies = []
        self.weapon_pickups = []

        # Gerar paredes básicas (bordas)
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            self.walls.append(pygame.Rect(x, 0, TILE_SIZE, TILE_SIZE))
            self.walls.append(pygame.Rect(x, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for y in range(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE):
            self.walls.append(pygame.Rect(0, y, TILE_SIZE, TILE_SIZE))
            self.walls.append(pygame.Rect(SCREEN_WIDTH - TILE_SIZE, y, TILE_SIZE, TILE_SIZE))

        # Gerar layout baseado no nível e personagem
        level_methods = [
            self._generate_office_layout, self._generate_urban_layout, self._generate_club_layout,
            self._generate_warehouse_layout, self._generate_suburban_layout,
            self._generate_military_layout  # Novo layout militar
        ]

        method_index = (self.level_num - 1) % len(level_methods)
        level_methods[method_index]()

        # Gerar inimigos baseado nos pontos de legado
        base_enemies = 3 + (self.level_num // 3)
        enemy_count = base_enemies + min(self.legacy_points // 15, 8)

        enemy_types = ["guard"] * 5 + ["heavy"] * 2 + ["fast"] * 2 + ["sniper"]

        for _ in range(enemy_count):
            x, y = self.find_valid_position()
            enemy_type = random.choice(enemy_types)
            self.enemies.append(Enemy(x, y, enemy_type))

        # Adicionar pickups de armas
        if self.level_num > 1:
            weapon_count = 1 + (self.level_num // 4)
            available_weapons = [WeaponType.KNIFE, WeaponType.BAT, WeaponType.PISTOL,
                                 WeaponType.SHOTGUN, WeaponType.UZI, WeaponType.KATANA, WeaponType.RIFLE]

            for _ in range(min(weapon_count, len(available_weapons))):
                x, y = self.find_valid_position()
                weapon_type = available_weapons.pop(0)
                self.weapon_pickups.append((x, y, weapon_type))

    def find_valid_position(self):
        while True:
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)

            # Verificar se a posição é válida
            test_rect = pygame.Rect(x, y, TILE_SIZE - 20, TILE_SIZE - 20)
            valid_position = True

            for wall in self.walls:
                if test_rect.colliderect(wall):
                    valid_position = False
                    break

            if valid_position:
                return x, y

    def _generate_office_layout(self):
        # Layout de escritório com cubículos
        for x in range(200, 700, 150):
            for y in range(150, 550, 120):
                self.walls.append(pygame.Rect(x, y, 100, 80))
                # Adicionar mesas
                if random.random() > 0.3:
                    self.walls.append(pygame.Rect(x + 20, y + 60, 60, 20))

    def _generate_urban_layout(self):
        # Layout urbano com prédios
        buildings = [
            (150, 150, 200, 300), (500, 200, 180, 250),
            (300, 400, 250, 200), (700, 100, 150, 200)
        ]

        for x, y, w, h in buildings:
            for i in range(0, w, TILE_SIZE):
                for j in range(0, h, TILE_SIZE):
                    if i == 0 or i >= w - TILE_SIZE or j == 0 or j >= h - TILE_SIZE:
                        self.walls.append(pygame.Rect(x + i, y + j, TILE_SIZE, TILE_SIZE))
            # Adicionar janelas
            for i in range(1, (w // TILE_SIZE) - 1):
                for j in range(1, (h // TILE_SIZE) - 1):
                    if random.random() > 0.5:
                        self.walls.append(pygame.Rect(x + i * TILE_SIZE + 10, y + j * TILE_SIZE + 10,
                                                      TILE_SIZE - 20, TILE_SIZE - 20))

    def _generate_club_layout(self):
        # Layout de boate
        self.walls.append(pygame.Rect(200, 150, 400, 50))  # Bar
        self.walls.append(pygame.Rect(200, 400, 400, 50))  # Palco

        for x in [150, 650]:
            for y in [200, 300, 500]:
                self.walls.append(pygame.Rect(x, y, 40, 40))

        # Pista de dança
        for x in range(300, 600, 50):
            for y in range(250, 350, 50):
                if random.random() > 0.7:
                    self.walls.append(pygame.Rect(x, y, 30, 30))

    def _generate_warehouse_layout(self):
        # Layout de armazém
        for x in range(200, 800, 200):
            self.walls.append(pygame.Rect(x, 200, 50, 400))
        # Estantes
        for y in range(250, 600, 100):
            self.walls.append(pygame.Rect(250, y, 300, 20))

    def _generate_suburban_layout(self):
        # Layout suburbano
        houses = [
            (200, 200, 150, 120), (500, 250, 140, 110),
            (300, 450, 160, 130), (650, 350, 130, 100)
        ]

        for x, y, w, h in houses:
            for i in range(0, w, TILE_SIZE):
                for j in range(0, h, TILE_SIZE):
                    if i == 0 or i >= w - TILE_SIZE or j == 0 or j >= h - TILE_SIZE:
                        self.walls.append(pygame.Rect(x + i, y + j, TILE_SIZE, TILE_SIZE))
            # Portas
            door_pos = random.randint(1, (w // TILE_SIZE) - 2)
            self.walls.append(pygame.Rect(x + door_pos * TILE_SIZE, y + h - TILE_SIZE,
                                          TILE_SIZE, 20))

    def _generate_military_layout(self):
        # Novo layout militar para o Soldier
        # Quartel
        self.walls.append(pygame.Rect(300, 200, 200, 150))
        # Torres de vigilância
        self.walls.append(pygame.Rect(150, 150, 50, 80))
        self.walls.append(pygame.Rect(750, 150, 50, 80))
        # Barricadas
        for x in range(200, 700, 100):
            self.walls.append(pygame.Rect(x, 400, 60, 20))
            self.walls.append(pygame.Rect(x, 500, 60, 20))

    def is_complete(self, player):
        exit_rect = pygame.Rect(self.exit_point[0], self.exit_point[1], TILE_SIZE, TILE_SIZE)
        player_rect = pygame.Rect(player.x, player.y, TILE_SIZE - 20, TILE_SIZE - 20)
        return exit_rect.colliderect(player_rect) and not [e for e in self.enemies if e.state == EnemyState.ALIVE]


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hotline Miami 3: Aftermath")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)

        self.state = GameState.MENU
        self.player = None
        self.level = None
        self.level_num = 1
        self.total_levels = 29  # 25 + 4 extras
        self.camera_x = 0
        self.camera_y = 0
        self.blood_particles = []
        self.message = ""
        self.message_timer = 0
        self.projectiles = []
        self.grenades = []
        self.dialog_system = DialogSystem()

        # Efeitos
        self.slow_motion = False
        self.normal_fps = FPS
        self.slow_fps = FPS // 3

        # Progressão por personagem (5 níveis cada + 4 extras)
        self.character_progression = {
            CharacterType.VETERAN: list(range(1, 6)),
            CharacterType.INVESTIGATOR: list(range(6, 11)),
            CharacterType.SUCCESSOR: list(range(11, 16)),
            CharacterType.EXECUTIONER: list(range(16, 21)),
            CharacterType.SOLDIER: list(range(21, 25)),  # 4 níveis extras
            "FINAL": list(range(25, 30))
        }

    def get_current_character(self):
        for char_type, levels in self.character_progression.items():
            if self.level_num in levels:
                return char_type
        return CharacterType.VETERAN

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_1:
                        self.start_game(CharacterType.VETERAN)
                    elif event.key == pygame.K_2:
                        self.start_game(CharacterType.INVESTIGATOR)
                    elif event.key == pygame.K_3:
                        self.start_game(CharacterType.SUCCESSOR)
                    elif event.key == pygame.K_4:
                        self.start_game(CharacterType.EXECUTIONER)
                    elif event.key == pygame.K_5:
                        self.start_game(CharacterType.SOLDIER)

                elif self.state == GameState.GAME_OVER or self.state == GameState.LEVEL_COMPLETE:
                    if event.key == pygame.K_r:
                        if self.state == GameState.GAME_OVER:
                            self.restart_level()
                        else:
                            self.next_level()
                    elif event.key == pygame.K_m:
                        self.state = GameState.MENU

                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_e:
                        ability_result = self.player.use_ability(self.level.enemies)
                        if isinstance(ability_result, str):
                            self.show_message(ability_result)
                            if self.player.mask_ability == "slow_time":
                                self.slow_motion = True
                        elif isinstance(ability_result, Grenade):
                            self.grenades.append(ability_result)
                    elif event.key == pygame.K_q:
                        self.player.switch_weapon(-1)  # Arma anterior
                    elif event.key == pygame.K_f:
                        self.player.switch_weapon(1)  # Próxima arma
                    elif event.key == pygame.K_r:
                        # Recarregar arma atual
                        weapon = self.player.weapons[self.player.current_weapon_index]
                        if weapon.is_ranged and weapon.ammo < weapon.max_ammo:
                            weapon.reload()
                            self.show_message("ARMA RECARREGADA")

                elif self.state in [GameState.DIALOG, GameState.CUTSCENE]:
                    if event.key == pygame.K_SPACE:
                        self.dialog_system.next_line()
                        if not self.dialog_system.current_dialog:
                            if self.state == GameState.CUTSCENE:
                                self.state = GameState.PLAYING
                            else:
                                self.state = GameState.PLAYING

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.PLAYING:
                    if event.button == 1:  # Mouse esquerdo - Atacar
                        projectile = self.player.attack(self.level.enemies)
                        if projectile:
                            self.projectiles.append(projectile)
                    elif event.button == 3:  # Mouse direito - Executar inimigos caídos
                        if self.player.execute_enemy(self.level.enemies):
                            self.show_message("EXECUTADO!")

        return True

    def update(self):
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()

            # Movimento do jogador
            dx, dy = 0, 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1

            # Normalizar movimento diagonal
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071

            self.player.move(dx, dy, self.level.walls)
            self.player.update()

            # Atualizar inimigos
            for enemy in self.level.enemies[:]:
                enemy_projectile = enemy.update(self.player, self.level.walls, self.projectiles)
                if enemy_projectile:
                    self.projectiles.append(enemy_projectile)

                if enemy.state == EnemyState.DEAD:
                    self.level.enemies.remove(enemy)
                    # Partículas de sangue
                    for _ in range(20):
                        self.blood_particles.append([
                            enemy.x + TILE_SIZE // 2,
                            enemy.y + TILE_SIZE // 2,
                            random.uniform(-8, 8),
                            random.uniform(-8, 8),
                            random.randint(30, 60)
                        ])

            # Atualizar projéteis
            for projectile in self.projectiles[:]:
                result = projectile.update(self.level.walls, self.level.enemies)
                if result == "wall" or isinstance(result, Enemy) or not projectile.active:
                    self.projectiles.remove(projectile)

            # Atualizar granadas
            for grenade in self.grenades[:]:
                if grenade.update(self.level.walls, self.level.enemies):
                    self.grenades.remove(grenade)
                    self.show_message("GRANADA DETONADA!")

            # Atualizar partículas de sangue
            for particle in self.blood_particles[:]:
                particle[0] += particle[2]
                particle[1] += particle[3]
                particle[4] -= 1

                if particle[4] <= 0:
                    self.blood_particles.remove(particle)

            # Verificar pickups de armas
            for pickup in self.level.weapon_pickups[:]:
                pickup_rect = pygame.Rect(pickup[0], pickup[1], TILE_SIZE - 20, TILE_SIZE - 20)
                player_rect = pygame.Rect(self.player.x, self.player.y, TILE_SIZE - 20, TILE_SIZE - 20)

                if pickup_rect.colliderect(player_rect):
                    weapon_added = self.player.add_weapon(pickup[2])
                    self.level.weapon_pickups.remove(pickup)
                    if weapon_added:
                        self.show_message("NOVA ARMA ADQUIRIDA!")
                    else:
                        self.show_message("MUNIÇÃO RECARREGADA")

            # Verificar se o nível foi completado
            if self.level.is_complete(self.player):
                self.state = GameState.LEVEL_COMPLETE
                # Dialogo ao completar nível
                dialog_key = (self.level_num - 1) % 3 + 1 + (self.level_num - 1) // 5 * 3
                if self.dialog_system.start_dialog(dialog_key):
                    self.state = GameState.DIALOG

            # Verificar game over
            if self.player.state == PlayerState.DEAD or (self.player.state == PlayerState.DOWNED and
                                                         any(e.state == EnemyState.ALIVE for e in self.level.enemies)):
                self.state = GameState.GAME_OVER

            # Atualizar câmera
            self.camera_x = self.player.x - SCREEN_WIDTH // 2
            self.camera_y = self.player.y - SCREEN_HEIGHT // 2

            # Atualizar mensagem
            if self.message_timer > 0:
                self.message_timer -= 1

            # Gerenciar slow motion
            if self.slow_motion and self.player.ability_duration <= 0:
                self.slow_motion = False

        elif self.state in [GameState.DIALOG, GameState.CUTSCENE]:
            self.dialog_system.update()
            if not self.dialog_system.current_dialog:
                self.state = GameState.PLAYING

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.draw_game()
            self.draw_level_complete()
        elif self.state in [GameState.DIALOG, GameState.CUTSCENE]:
            self.dialog_system.draw(self.screen)

        pygame.display.flip()

    def draw_menu(self):
        # Título
        title = self.title_font.render("HOTLINE MIAMI 3: AFTERMATH", True, RED)
        subtitle = self.font.render("29 FATES, 5 KILLERS, 1 TRUTH", True, WHITE)

        # Personagens
        veteran = self.font.render("1 - VETERANO (Lentidão Temporal)", True, BLUE)
        investigator = self.font.render("2 - INVESTIGADORA (Marcar Inimigos)", True, GREEN)
        successor = self.font.render("3 - SUCESSOR (Modo Berserk)", True, RED)
        executioner = self.font.render("4 - EXECUTIONER (Execução)", True, PURPLE)
        soldier = self.font.render("5 - SOLDIER (Granadas) - NOVO!", True, ORANGE)

        hint = self.small_font.render("Pressione 1-5 para selecionar o personagem", True, YELLOW)
        story = self.small_font.render("29 níveis: 25 principais + 4 bônus do Soldier", True, LIGHT_GRAY)
        controls = self.small_font.render("Mouse Esq: ATACAR | Mouse Dir: EXECUTAR | E: HABILIDADE", True, YELLOW)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 150))
        self.screen.blit(veteran, (SCREEN_WIDTH // 2 - veteran.get_width() // 2, 230))
        self.screen.blit(investigator, (SCREEN_WIDTH // 2 - investigator.get_width() // 2, 280))
        self.screen.blit(successor, (SCREEN_WIDTH // 2 - successor.get_width() // 2, 330))
        self.screen.blit(executioner, (SCREEN_WIDTH // 2 - executioner.get_width() // 2, 380))
        self.screen.blit(soldier, (SCREEN_WIDTH // 2 - soldier.get_width() // 2, 430))
        self.screen.blit(story, (SCREEN_WIDTH // 2 - story.get_width() // 2, 500))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 530))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 580))

    def draw_game(self):
        # Desenhar fundo
        self.screen.blit(self.level.background_texture, (0, 0))

        # Desenhar nível com texturas
        for i, wall in enumerate(self.level.walls):
            texture_index = i % len(self.level.wall_textures)
            wall_texture = self.level.wall_textures[texture_index]
            self.screen.blit(wall_texture, (wall.x - self.camera_x, wall.y - self.camera_y))

        # Desenhar saída
        exit_rect = pygame.Rect(self.level.exit_point[0] - self.camera_x,
                                self.level.exit_point[1] - self.camera_y,
                                TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, GREEN, exit_rect)
        exit_text = self.small_font.render("SAÍDA", True, BLACK)
        self.screen.blit(exit_text, (exit_rect.x + 10, exit_rect.y + 20))

        # Desenhar pickups de armas
        for x, y, weapon_type in self.level.weapon_pickups:
            pickup_rect = pygame.Rect(x - self.camera_x, y - self.camera_y, TILE_SIZE - 20, TILE_SIZE - 20)
            color = ORANGE if weapon_type.value >= 4 else YELLOW
            pygame.draw.rect(self.screen, color, pickup_rect)
            pygame.draw.rect(self.screen, BLACK, pickup_rect, 2)
            weapon_name = self.small_font.render(weapon_type.name[:3], True, BLACK)
            self.screen.blit(weapon_name, (pickup_rect.x + 5, pickup_rect.y + 15))

        # Desenhar partículas de sangue
        for particle in self.blood_particles:
            size = max(2, particle[4] // 8)
            alpha = min(255, particle[4] * 4)
            blood_color = (BLOOD_RED[0], BLOOD_RED[1], BLOOD_RED[2], alpha)
            blood_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(blood_surface, blood_color, (size, size), size)
            self.screen.blit(blood_surface,
                             (particle[0] - self.camera_x - size,
                              particle[1] - self.camera_y - size))

        # Desenhar projéteis
        for projectile in self.projectiles:
            projectile.draw(self.screen, self.camera_x, self.camera_y)

        # Desenhar granadas
        for grenade in self.grenades:
            grenade.draw(self.screen, self.camera_x, self.camera_y)

        # Desenhar inimigos
        for enemy in self.level.enemies:
            is_marked = (self.player.marked_enemy == enemy)
            enemy.draw(self.screen, self.camera_x, self.camera_y, is_marked)

        # Desenhar jogador
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Desenhar HUD
        self.draw_hud()

    def draw_hud(self):
        # Barra de saúde
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20

        pygame.draw.rect(self.screen, DARK_GRAY, (health_x, health_y, health_width, health_height))
        if self.player.max_health > 0:
            current_health_width = (self.player.health / self.player.max_health) * health_width
        else:
            current_health_width = 0

        health_color = GREEN if self.player.health > self.player.max_health * 0.6 else YELLOW if self.player.health > self.player.max_health * 0.3 else RED
        pygame.draw.rect(self.screen, health_color, (health_x, health_y, current_health_width, health_height))

        health_text = self.small_font.render(f"SAÚDE: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + 25))

        # Estado do jogador
        state_text = "NORMAL"
        state_color = GREEN
        if self.player.state == PlayerState.DOWNED:
            state_text = f"CAÍDO - {self.player.downed_timer // 60 + 1}s"
            state_color = RED
        state_surface = self.small_font.render(f"ESTADO: {state_text}", True, state_color)
        self.screen.blit(state_surface, (health_x, health_y + 50))

        # Arma atual
        current_weapon = self.player.weapons[self.player.current_weapon_index]
        weapon_text = self.small_font.render(f"ARMA: {current_weapon.weapon_type.name}", True, WHITE)
        ammo_text = ""
        if current_weapon.is_ranged:
            ammo_text = self.small_font.render(f"MUNIÇÃO: {current_weapon.ammo}/{current_weapon.max_ammo}", True,
                                               YELLOW)
        else:
            ammo_text = self.small_font.render("ARMA BRANCA", True, YELLOW)

        self.screen.blit(weapon_text, (health_x, health_y + 75))
        self.screen.blit(ammo_text, (health_x, health_y + 100))

        # Score e combo
        score_text = self.small_font.render(f"SCORE: {self.player.score}", True, WHITE)
        combo_text = self.small_font.render(f"COMBO: x{self.player.combo}", True, YELLOW)
        self.screen.blit(score_text, (health_x, health_y + 125))
        self.screen.blit(combo_text, (health_x, health_y + 150))

        # Nível e personagem
        level_text = self.small_font.render(f"NÍVEL: {self.level_num}/29", True, WHITE)
        char_text = self.small_font.render(f"PERSONAGEM: {self.player.character_type.name}", True,
                                           BLUE if self.player.character_type == CharacterType.VETERAN else
                                           GREEN if self.player.character_type == CharacterType.INVESTIGATOR else
                                           RED if self.player.character_type == CharacterType.SUCCESSOR else
                                           PURPLE if self.player.character_type == CharacterType.EXECUTIONER else
                                           ORANGE)
        self.screen.blit(level_text, (health_x, health_y + 175))
        self.screen.blit(char_text, (health_x, health_y + 200))

        # Habilidade
        ability_text = "PRONTO"
        ability_color = GREEN
        if self.player.ability_cooldown > 0:
            ability_text = f"RECARREGANDO: {self.player.ability_cooldown // 60 + 1}s"
            ability_color = YELLOW

        ability_surface = self.small_font.render(f"HABILIDADE (E): {ability_text}", True, ability_color)
        self.screen.blit(ability_surface, (health_x, health_y + 225))

        # Legado
        legacy_text = self.small_font.render(f"PONTOS DE LEGADO: {self.player.legacy_points}", True, PURPLE)
        self.screen.blit(legacy_text, (health_x, health_y + 250))

        # Controles
        controls = [
            "WASD: MOVER",
            "MOUSE ESQ: ATACAR",
            "MOUSE DIR: EXECUTAR",
            "E: HABILIDADE",
            "Q/F: TROCAR ARMA",
            "R: RECARREGAR"
        ]

        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, LIGHT_GRAY)
            self.screen.blit(control_text, (SCREEN_WIDTH - 180, 20 + i * 25))

        # Mensagem de habilidade
        if self.message_timer > 0:
            message_surface = self.font.render(self.message, True, YELLOW)
            self.screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 50))

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        game_over = self.title_font.render("GAME OVER", True, RED)
        score = self.font.render(f"Score Final: {self.player.score}", True, WHITE)
        level_info = self.small_font.render(f"Nível {self.level_num} - {self.player.character_type.name}", True, YELLOW)
        restart = self.small_font.render("Pressione R para reiniciar ou M para menu", True, YELLOW)

        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(level_info, (SCREEN_WIDTH // 2 - level_info.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def draw_level_complete(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        complete = self.title_font.render("NÍVEL COMPLETO!", True, GREEN)
        score = self.font.render(f"Score: {self.player.score}", True, WHITE)
        next_level = self.small_font.render("Pressione R para o próximo nível ou M para menu", True, YELLOW)

        self.screen.blit(complete, (SCREEN_WIDTH // 2 - complete.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(next_level, (SCREEN_WIDTH // 2 - next_level.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def show_message(self, message):
        self.message = message
        self.message_timer = 120

    def start_game(self, character_type):
        self.player = Player(character_type)
        self.level_num = self.character_progression[character_type][0]
        self.level = Level(self.level_num, character_type, self.player.legacy_points)
        self.state = GameState.PLAYING
        self.blood_particles = []
        self.projectiles = []
        self.grenades = []
        self.slow_motion = False

        # Cutscene de introdução
        intro_keys = [1, 6, 11, 16, 21]
        if self.level_num in intro_keys:
            dialog_key = "intro"
            if character_type == CharacterType.SOLDIER:
                dialog_key = "soldier_intro"
            if self.dialog_system.start_dialog(dialog_key):
                self.state = GameState.CUTSCENE

    def restart_level(self):
        self.player.reset()
        self.level = Level(self.level_num, self.get_current_character(), self.player.legacy_points)
        self.state = GameState.PLAYING
        self.blood_particles = []
        self.projectiles = []
        self.grenades = []

    def next_level(self):
        if self.level_num < self.total_levels:
            self.level_num += 1

            # Cutscene no meio do jogo
            if self.level_num == 11:
                if self.dialog_system.start_dialog("mid_game"):
                    self.state = GameState.CUTSCENE
            # Cutscene final
            elif self.level_num == 25:
                if self.dialog_system.start_dialog("final"):
                    self.state = GameState.CUTSCENE

            current_char = self.get_current_character()
            self.level = Level(self.level_num, current_char, self.player.legacy_points)

            # Reposicionar jogador
            self.player.x, self.player.y = self.level.spawn_point
            self.state = GameState.PLAYING
        else:
            # Fim do jogo
            self.state = GameState.MENU

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()

            # Controlar FPS baseado no slow motion
            if self.slow_motion:
                self.clock.tick(self.slow_fps)
            else:
                self.clock.tick(self.normal_fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()