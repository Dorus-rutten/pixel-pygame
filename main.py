import pygame

# pygame setup

# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
# clock = pygame.time.Clock()

running = True
pygame.display.set_caption("PYgame")

class Game:
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.animation_cooldown = 150  # Time in milliseconds between frames
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        

    def run(self):
        # self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT)) 
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption("PYgame")
        return self.running, self.screen, self.clock 
        

    def settings(self):

        return self.WINDOW_WIDTH, self.WINDOW_HEIGHT

    def update(self):
        pass


class Slime:
    def __init__(self, name, health, attack, defense, speed, current_health, range):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.current_health = current_health
        self.range = range
        self.sprite_sheet_image = self.load_sprite_sheet()  # Load sprite sheet image
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        self.x = 300
        self.y = 300
        

    def load_sprite_sheet(self):
        sprite_sheet_image = pygame.image.load("sprites/Enemies/Slime.png").convert_alpha()
        return sprite_sheet_image
    
    def get_image(self, sheet, frame, animation, width, height, scale):
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), animation * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
    
    def load_animation(self, action, steps, width=32, height=32, scale=3):
        animation_list = []
        hitbox_list = []
        for x in range(steps):
            image = self.get_image(self.sprite_sheet_image, x, action, width, height, scale)
            animation_list.append(image)
            hitbox_list.append(pygame.mask.from_surface(image)) 
        return animation_list, hitbox_list 

    def slime_animation(self, action):
        animation_steps = {
            0: 4,  # idle_idle_animation
            1: 6,  # walk_idle_animation
            2: 5,  # die_idle_animation
        }
        steps = animation_steps.get(action, 6)
        return self.load_animation(action, steps)
    
    def run_slime_animation(self):
        
            # Handle slime animation (idle or walking)
        if slime.current_health == 0:
            slime_new_action = 2  # Die animation
        else:
            slime_new_action = 0  # Idle for now

        if slime_new_action != slime_current_action:
            slime_current_action = slime_new_action
            slime_animation, hitboxes = slime.slime_animation(slime_current_action)
            slime.frame_index = 0

        slime_current_time = pygame.time.get_ticks()
        if slime_current_time - slime.last_update >= game.animation_cooldown:
            slime.frame_index = (slime.frame_index + 1) % len(slime_animation)
            slime.last_update = slime_current_time 

    def take_damage(self, damage):
        self.current_health -= max(damage - self.defense, 0)
        if self.current_health < 0:
            self.current_health = 0
        return self.current_health

class MainCharacter:
    def __init__(self, name, health, attack, defense, speed, current_health, range):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.current_health = current_health
        self.range = range
        self.sprite_sheet_image = self.load_sprite_sheet()  # Load sprite sheet image
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        self.x = 100
        self.y = 100

    def load_sprite_sheet(self):
        sprite_sheet_image = pygame.image.load("sprites/Player/Player.png").convert_alpha()
        return sprite_sheet_image
    
    def get_image(self, sheet, frame, animation, width, height, scale):
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), animation * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
    
    def load_animation(self, action, steps, width=32, height=32, scale=3):
        animation_list = []
        hitbox_list = []
        for x in range(steps):
            image = self.get_image(self.sprite_sheet_image, x, action, width, height, scale)
            animation_list.append(image)
            hitbox_list.append(pygame.mask.from_surface(image)) 
        return animation_list, hitbox_list

    def player_animation(self, action):
        animation_steps = {
            0: 6,  # front_idle_animation
            1: 6,  # side_idle_animation
            2: 6,  # back_idle_animation
            3: 6,  # walk_front_animation
            4: 6,  # walk_side_animation
            5: 6,  # walk_back_animation
            6: 4,  # attack_down_animation
            7: 4,  # attack_side_animation
            8: 4,  # attack_up_animation
            9: 5   # die_animation
        }

        steps = animation_steps.get(action)
        return self.load_animation(action, steps)
    
    def movement(self, x, y):
        keys = pygame.key.get_pressed()
        movement_x, movement_y = 0, 0

        # Check movement keys
        if keys[pygame.K_a]:  # Move left
            movement_x = -self.speed
        if keys[pygame.K_d]:  # Move right
            movement_x = self.speed
        if keys[pygame.K_w]:  # Move up
            movement_y = -self.speed
        if keys[pygame.K_s]:  # Move down
            movement_y = self.speed

        # Update player's position
        x += movement_x
        y += movement_y

        # Determine current action (animation)
        if movement_x == 0 and movement_y == 0:
            new_action = 0  # Idle animation
        elif movement_y > 0:  # Moving down
            new_action = 3  # Walk down animation
        elif movement_y < 0:  # Moving up
            new_action = 5  # Walk up animation
        elif movement_x != 0:  # Moving left or right (horizontal movement)
            new_action = 4  # Walk sideways animation

        return x, y, new_action  # Return the new position and action
        

# Initialize the game characters
game = Game()
player = MainCharacter("Hero", 100, 20, 10, 5, 100, 10)
slime = Slime("Enemy", 100, 20, 10, 3, 100, 10)
clock = pygame.time.Clock()

#slime.run_slime_animation
# Initialize the first animation
slime_current_action = 0  # Start with idle animation
player_current_action = 0  # Start with idle animation

player_animation, player_hitboxes = player.player_animation(player_current_action)



# Movement variables
x_last_frame, y_last_frame = player.x, player.y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

    # Get player's new position and action
    player.x, player.y, new_action = player.movement(player.x, player.y)

    slime_animation, hitboxes = slime.slime_animation(slime_current_action)
    if slime.current_health == 0:
            slime_new_action = 2  # Die animation
    else:
            slime_new_action = 0  # Idle for now

    if slime_new_action != slime_current_action:
            slime_current_action = slime_new_action
            slime_animation, hitboxes = slime.slime_animation(slime_current_action)
            slime.frame_index = 0

    slime_current_time = pygame.time.get_ticks()
    if slime_current_time - slime.last_update >= game.animation_cooldown:
            slime.frame_index = (slime.frame_index + 1) % len(slime_animation)
            slime.last_update = slime_current_time 

    # If the action has changed, update the player's animation and hitboxes
    if new_action != player_current_action:
        player_current_action = new_action
        player_animation, player_hitboxes = player.player_animation(new_action)
        player.frame_index = 0

    player_current_time = pygame.time.get_ticks()
    if player_current_time - player.last_update >= game.animation_cooldown:
        player.frame_index = (player.frame_index + 1) % len(player_animation)
        player.last_update = player_current_time

    # Clear screen
    game.screen.fill((0, 0, 255))

    # Draw slime
    game.screen.blit(slime_animation[slime.frame_index], (slime.x, slime.y))

    # Draw player
    if x_last_frame > player.x:  # Flip the image if moving left
        flipped_image = pygame.transform.flip(player_animation[player.frame_index], True, False)
        game.screen.blit(flipped_image, (player.x, player.y))
    else:
        game.screen.blit(player_animation[player.frame_index], (player.x, player.y))

    # Check for collision (mask overlap)
    player_mask = player_hitboxes[player.frame_index]
    slime_mask = hitboxes[slime.frame_index]
    offset = (player.y - player.x, slime.y - slime.x)
    if player_mask.overlap(slime_mask, offset):
        print("Collision detected!")

    x_last_frame, y_last_frame = player.x, player.y  # Update for next frame

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
