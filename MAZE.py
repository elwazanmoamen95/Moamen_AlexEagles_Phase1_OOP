import numpy as np
import random
import heapq
import pygame
import sys
import math


WIDTH, HEIGHT = 400, 400
CELL_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Grid:
    def __init__(self, size, start, end, obstacle_prob):
        self.size = size
        self.start = start
        self.end = end
        self.obstacle_prob = obstacle_prob
        self.grid = self._create_grid()

    def _create_grid(self):
        grids = np.full(self.size, '', dtype=str)
        # R and T was in represent state of the matrix for start and end location 
        # grids[self.start[0], self.start[1]] = 'R'
        # grids[self.end[0], self.end[1]] = 'T'
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (i, j) != self.start and (i, j) != self.end and random.random() < self.obstacle_prob:
                    grids[i, j] = '#'
        return grids

    def draw(self, path=None):
        screen.fill(WHITE)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (i, j) == self.start:
                    pygame.draw.rect(screen, RED, rect)
                elif (i, j) == self.end:
                    pygame.draw.rect(screen, BLUE, rect)
                elif self.grid[i, j] == '#':
                    pygame.draw.rect(screen, BLACK, rect)
                elif (i, j) in (path or []):
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)
        pygame.display.flip()

class AStarSearch:
    def __init__(self, grid):
        self.grid = grid
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # for Diagonal Distance
        # self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # for Manhattan distance

    # Diagonal Distance
    def heuristic(self, node, goal, D=CELL_SIZE, D2=(math.sqrt(2*(pow(CELL_SIZE,2))))):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
    # Manhattan distance
    # def heuristic(self, node, goal):
    #     dx = abs(node[0] - goal[0])
    #     dy = abs(node[1] - goal[1])
    #     return  (dx + dy)

    def search(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))
        g_score = {start: 0}
        close_list = {}
        
        while open_list:
            current_f, current = heapq.heappop(open_list)

            if current == goal:
                return self.return_path(close_list, current)
            
            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.grid.size[0] and 0 <= neighbor[1] < self.grid.size[1]:
                    if self.grid.grid[neighbor[0], neighbor[1]] == '#':
                        continue
                    
                    tentative_g_score = g_score[current] + self.heuristic(current, neighbor)
                    
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score, neighbor))
                        close_list[neighbor] = current
        
        return None

    def return_path(self, close_list, current):
        path = []
        while current in close_list:
            path.append(current)
            current = close_list[current]
        path.reverse()
        return path

def main():
    # Pygame setup
    pygame.init()
    pygame.display.set_caption('A* Path_finding')
    maze_size = (8, 8)
    robot_position = (5, 4)
    treasure_position = (2, 7)
    obstacle_prob = 0.33

    grid = Grid(maze_size, robot_position, treasure_position, obstacle_prob)
    a_star = AStarSearch(grid)
    path = a_star.search(robot_position, treasure_position)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid.draw(path)

if __name__ == "__main__":
    main()
