import pygame
import heapq
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 30
ROWS, COLS = WINDOW_SIZE // GRID_SIZE, WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER = (0, 100, 200)

# Heuristic function for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Pathfinding algorithm
def astar(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for direction in neighbors:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return []

# Draw button
def draw_button(screen, text, x, y, w, h, color, hover_color, mouse_pos, action=None):
    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if pygame.mouse.get_pressed()[0] and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)

# Draw path
def draw_path(screen, path):
    for node in path:
        pygame.draw.rect(screen, LIGHT_BLUE, (node[1] * GRID_SIZE, node[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Main function
def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))  # Added extra space for the button
    pygame.display.set_caption("Robot avoiding obstacles simulation")

    # Grid and obstacles setup
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    # Scatter obstacles randomly but ensure that start and goal are not blocked
    obstacle_count = 100  # Adjust number of obstacles
    for _ in range(obstacle_count):
        obstacle_row = random.randint(0, ROWS - 1)
        obstacle_col = random.randint(0, COLS - 1)
        if (obstacle_row, obstacle_col) != (0, 0) and (obstacle_row, obstacle_col) != (ROWS - 1, COLS - 1):
            grid[obstacle_row][obstacle_col] = 1  # Mark as obstacle
    
    # Start and goal positions
    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)
    
    # Load and scale the robot image
    robot_image = pygame.image.load("robot.png")  # Replace with your robot image path
    robot_image = pygame.transform.scale(robot_image, (GRID_SIZE, GRID_SIZE))

    # Pathfinding
    def reset_path():
        nonlocal path, path_index
        path = astar(grid, start, goal)
        if not path:
            print("No path found!")
            return
        path_index = 0

    path = []
    path_index = 0
    reset_path()

    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill(WHITE)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the grid and obstacles
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if grid[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines
        
        # Draw start and goal points
        pygame.draw.rect(screen, GREEN, (start[1] * GRID_SIZE, start[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (goal[1] * GRID_SIZE, goal[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw the path
        if path_index < len(path):
            draw_path(screen, path[:path_index + 1])
            robot_pos = path[path_index]
            screen.blit(robot_image, (robot_pos[1] * GRID_SIZE, robot_pos[0] * GRID_SIZE))
            path_index += 1

        # Draw the "Loop" button
        draw_button(screen, "Loop", 250, WINDOW_SIZE + 10, 100, 30, BUTTON_COLOR, BUTTON_HOVER, mouse_pos, reset_path)

        # Update the display
        pygame.display.flip()
        clock.tick(5)  # Adjust the speed of the robot movement
    
    pygame.quit()

if __name__ == "__main__":
    main()