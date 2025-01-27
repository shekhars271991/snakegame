import pygame
import random
import sys
from config import proximity_factor, initial_speed, speed_increment, block_size, wall_width_multiple

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



clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 75)

def generate_food(snake, level, wall_rects):
    """Generate food at random position not occupied by snake or walls."""
    max_offset = proximity_factor * block_size * level

    while True:
        x = random.randrange(0, screen_width, block_size)
        y = random.randrange(0, screen_height, block_size)
        
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

def main():
    # Align initial position to grid
    start_x = (screen_width // 2) // block_size * block_size
    start_y = (screen_height // 2) // block_size * block_size
    snake = [[start_x, start_y]]
    
    level = 1
    dx, dy = block_size, 0
    score = 0
    current_speed = initial_speed
    game_active = True

    # Initialize walls
    wall_rects = draw_walls()
    food = generate_food(snake, level, wall_rects)

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

            # Move snake
            new_head = [snake[0][0] + dx, snake[0][1] + dy]
            snake.insert(0, new_head)

            # Check food collision
            if snake[0] == food:
                score += 1
                if score % 2 == 0:
                    level += 1
                    current_speed += speed_increment
                food = generate_food(snake, level, wall_rects)
            else:
                snake.pop()

            # Check collisions with walls and boundaries
            head_x, head_y = snake[0]
            if any(wall.collidepoint(head_x, head_y) for wall in wall_rects):
                game_active = False
            
            for segment in snake[1:]:
                if snake[0] == segment:
                    game_active = False

            # Draw elements
            screen.fill(BLACK)
            wall_rects = draw_walls()  # Redraw walls every frame
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0], segment[1], block_size, block_size))
            pygame.draw.rect(screen, RED, (food[0], food[1], block_size, block_size))
            
            # Display score
            score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            pygame.display.update()
            clock.tick(current_speed)

        # Game Over screen
        screen.fill(BLACK)
        game_over_text = game_over_font.render("Game Over!", True, RED)
        restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
        
        screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2 - 50))
        screen.blit(restart_text, (screen_width//2 - restart_text.get_width()//2, screen_height//2 + 50))
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
