import pygame
import math

pygame.init()

WIDTH, HEIGHT = 500, 500
fov = 120
num_rays = 10
angle_step = math.radians(fov) / num_rays
max_ray_length = 10000

map = [
    [0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0]
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
obstacles = []

pixel_positions = []

for i in range(len(map)):
    for j in range(len(map[i])):
        if map[j][i] == 1:
            surface = pygame.Surface((100, 100))
            surface.fill((255, 255, 255))
            obstacles.append((surface, (i*100, j*100)))

            pixel_array = pygame.PixelArray(surface)

            for y in range(surface.get_height()):
                for x in range(surface.get_width()):
                    screen_x = x + i*100
                    screen_y = y + j*100
                    pixel_positions.append((screen_x, screen_y))
            del pixel_array

def cast_rays(mouse_pos, pixel_positions, angle_step, num_rays, max_ray_length):
    mousex, mousey = mouse_pos
    camera_angle = math.atan2(mousey - HEIGHT//2, mousex - WIDTH//2)
    ray_info = {}
    
    pixel_positions_set = set(pixel_positions)

    for i in range(num_rays):
        ray_angle = camera_angle - math.radians(30) + (i * angle_step)
        x, y = WIDTH // 2, HEIGHT // 2
        sin, cos = (0.02*math.sin(ray_angle), 0.02*math.cos(ray_angle))
        n = 0
        while n < max_ray_length:
            x, y = (x + cos, y + sin)
            n += 1
            end_pos = (x, y)
            z = 1/(0.02 * n)
            ray_info[i] = [end_pos, z, ray_angle, camera_angle]
            if (round(x), round(y)) in pixel_positions_set or x >= WIDTH or y >= HEIGHT or x <= 0 or y <= 0:
                break
                
    return ray_info

    
def draw(obstacles, ray_info, num_rays):

    screen.fill((0, 0, 0))

    for obstacle_surface, position in obstacles:
        screen.blit(obstacle_surface, position)

    if ray_info != None:
        for i in range(num_rays):
            if i in ray_info:
                pygame.draw.line(screen, (255, 0, 0), (WIDTH//2, HEIGHT//2), ray_info[i][0])

running = True
ray_info = None
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            ray_info = cast_rays(mouse_pos, pixel_positions, angle_step, num_rays, max_ray_length)

    draw(obstacles, ray_info, num_rays)
    pygame.display.update()
pygame.quit()