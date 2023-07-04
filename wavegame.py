import numpy as np
import pygame
import sounddevice as sd

device_id = None
devices = sd.query_devices()
for index, device in enumerate(devices):
    if 'BlackHole' in device['name']:
        device_id = index
        break

assert device_id is not None, "Could not find device"

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

platforms = []
platform_speed = 2

player = pygame.Rect(190, 250, 20, 20)
velocity = 0
jump_speed = 6
gravity = 0.2


def audio_callback(indata, frames, time, status):
    volume = np.linalg.norm(indata)*10
    platforms.append([780, 600-int(volume*20), 20, int(volume*20)])


with sd.InputStream(callback=audio_callback, device=device_id):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = -jump_speed

        screen.fill((0, 0, 0))

        for platform in platforms:
            platform[0] -= platform_speed
            if platform[0] < -20:
                platforms.remove(platform)
            platform_rect = pygame.Rect(*platform)
            if player.colliderect(platform_rect):
                running = False
            pygame.draw.rect(screen, (0, 255, 0), platform_rect)

        velocity += gravity
        player.y += velocity

        if player.y < 0 or player.y > 600:
            running = False

        pygame.draw.rect(screen, (255, 255, 0), player)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
