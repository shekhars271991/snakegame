import pygame
import random
import sys
from config import proximity_factor, initial_speed, speed_increment, \
    block_size, wall_width_multiple, score_increase_by, regenfood_count_time, boost_speed_by, cooldown_for_seconds

# Initialize Pygame
pygame.init()

# Screen setup
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game with Walls")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 200)
boost_color = RED

clock = pygame.time.Clock()

# boost time
boost_for_seconds = 5

# Fonts
font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 100)
game_start_font = pygame.font.SysFont(None, 100)


# Load background image
background_image = pygame.image.load("grass2.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
# Load apple image
apple_image = pygame.image.load("APPLE_REAL-removebg-preview.png")
apple_image = pygame.transform.scale(apple_image, (int(block_size * 2), int(block_size * 2)))
background_OVERGAME = pygame.image.load("he he ha ha.jpg")
background_OVERGAME = pygame.transform.scale(background_OVERGAME, (screen_width, screen_height))
TITLE_LOGO = pygame.image.load("snake logo.png")

def generate_food(snake, level, wall_rects):
    global regenfood_count
    regenfood_count = 0
    """Generate food at random position not occupied by snake or walls."""
    wall_thickness = block_size * wall_width_multiple
    while True:
        x = random.randrange(wall_thickness, screen_width - wall_thickness, block_size)
        y = random.randrange(wall_thickness, screen_height - wall_thickness, block_size)
        
        # Ensure food does not overlap with snake or walls
        if [x, y] not in snake and not any(wall.collidepoint(x, y) for wall in wall_rects):
            return [x, y]

def draw_walls():
    """Draw walls around the edges of the screen."""
    wall_thickness = block_size * wall_width_multiple
    walls = [
        pygame.Rect(0, 0, screen_width, wall_thickness),  # Top wall
        pygame.Rect(0, 0, wall_thickness, screen_height),  # Left wall
        pygame.Rect(screen_width - wall_thickness, 0, wall_thickness, screen_height),  # Right wall
        pygame.Rect(0, screen_height - wall_thickness, screen_width, wall_thickness)  # Bottom wall
    ]
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)
    return walls

def show_start_screen():
    """Show the start screen with instructions."""
    title_txt = game_start_font.render("SNAKE GAME",True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(background_image, (0, 0))  # Draw background
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    screen.blit(title_txt, (screen_width // 2 - title_txt.get_width() // 2, screen_height // 4))
    pygame.display.update()

def main():
    # Align initial position to grid
    start_x = (screen_width // 2) // block_size * block_size
    start_y = (screen_height // 2) // block_size * block_size
    snake = [[start_x, start_y]]
    
    level = 1
    dx, dy = block_size, 0
    score = 0
    current_speed = initial_speed
    game_active = False
    global regenfood_count 
    boost_active = False
    cooldown_active = False
    boost_start_time = 0 

    # Initialize walls
    wall_rects = draw_walls()
    food = generate_food(snake, level, wall_rects)

    # Show the start screen
    show_start_screen()

    # Wait for space bar to start the game
    waiting_for_start = True
    while game_active == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    game_active = True # Start the game when space is pressed

    while True:
        while game_active:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    # Change direction (prevent 180-degree turns)
                    if event.key == pygame.K_LEFT and dx != block_size:
                        dx, dy = -block_size, 0
                    elif event.key == pygame.K_RIGHT and dx != -block_size:
                        dx, dy = block_size, 0
                    elif event.key == pygame.K_UP and dy != block_size:
                        dx, dy = 0, -block_size
                    elif event.key == pygame.K_DOWN and dy != -block_size:
                        dx, dy = 0, block_size
                    elif event.key == pygame.K_b and not boost_active and not cooldown_active:
                        boost_active = True
                        cooldown_active = True
                        boost_start_time = pygame.time.get_ticks()  
                    
                if boost_active and pygame.time.get_ticks() - boost_start_time > boost_for_seconds * 1000:
                    boost_active = False
                if cooldown_active and pygame.time.get_ticks() - boost_start_time > cooldown_for_seconds * 1000:
                    cooldown_active = False
                 
                current_speed = initial_speed + boost_speed_by if boost_active else initial_speed

            # Move snake
            new_head = [snake[0][0] + dx, snake[0][1] + dy]
            snake.insert(0, new_head)

            # Check food collision
            if snake[0] == food:
                score += score_increase_by
                if score % 2 == 0:
                    level += 1
                    current_speed += speed_increment
                food = generate_food(snake, level, wall_rects)
            else:
                snake.pop()
            if(regenfood_count == regenfood_count_time):
                food = generate_food(snake, level, wall_rects)
            regenfood_count += 1

            # Check collisions with walls and boundaries
            wall_thickness = block_size * wall_width_multiple
            head_rect = pygame.Rect(snake[0][0], snake[0][1], block_size, block_size)
            if any(head_rect.colliderect(wall) for wall in wall_rects):
                game_active = False

            # Prevent snake from going partially into walls by adjusting boundaries
            if snake[0][0] < wall_thickness or snake[0][1] < wall_thickness or \
               snake[0][0] >= screen_width - wall_thickness or snake[0][1] >= screen_height - wall_thickness:
                game_active = False
            
            # Check collisions with itself
            for segment in snake[1:]:
                if snake[0] == segment:
                    game_active = False

            # Draw elements
            screen.blit(background_image, (0, 0))  # Draw the background
            wall_rects = draw_walls()  # Redraw walls every frame
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0], segment[1], block_size, block_size))
            screen.blit(apple_image, (food[0], food[1]))  # Draw apple as food

            # Display score
            score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))

            if boost_active:
                boost_text = "Active"
                boost_color = BLUE
            else:
                boost_text = "Inactive"
                boost_color = RED
            boost_text = font.render(f"Boost: {boost_text}", True, boost_color)
            cooldown_txt = font.render(f"Cooldown: {cooldown_active}", True, WHITE)
            screen.blit(boost_text, (10, 50))
            screen.blit(cooldown_txt, (400, 10))
            
            pygame.display.update()
            clock.tick(current_speed)

        # Game Over screen
        screen.blit(background_OVERGAME, (0, 0)) 
        game_over_text = game_over_font.render("YOU DIED HA! U R NOT PROFFESONAL!", True, RED)
        restart_text = font.render("Press R to try again or Q to rage quit cuz u cant win :)", True, RED)
        
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))
        pygame.display.update()

        # Handle game over input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game state with aligned position
                        start_x = (screen_width // 2) // block_size * block_size
                        start_y = (screen_height // 2) // block_size * block_size
                        snake = [[start_x, start_y]]
                        dx, dy = block_size, 0
                        food = generate_food(snake, level, wall_rects)
                        score = 0
                        level = 1
                        current_speed = initial_speed
                        game_active = True
                        break
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            if game_active:
                break

if __name__ == "__main__":
    main()
