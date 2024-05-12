import random
from typing import List
import pygame
import scipy.stats as stats
import numpy as np

WIDTH = 450
HEIGHT = 450


def generate_bell_curve(num_particles):
    x_min = WIDTH / 2 - 100
    x_max = WIDTH / 2 + 100
    x_values = np.linspace(x_min, x_max, num_particles)
    print(len(x_values))
    mean = np.mean(x_values) + 1
    std_dev = np.std(x_values) / 4
    y_values = stats.norm.pdf(x_values, mean, std_dev)
    return x_values, y_values


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y - 200
        self.velocity = 0
        self.replicated = False

    def update(self, dvx, dvy):
        self.x += dvx
        self.y += dvy
        self.velocity = dvy

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 5, 5))
        char = " "
        if self.y < HEIGHT - 280:
            char = "|"
        elif self.y < HEIGHT - 210:
            char = "."
        screen.blit(
            pygame.font.SysFont("monospace", 11).render(char, True, (255, 255, 255)),
            (self.x - 10, self.y),
        )


class ParticleSystem:
    def __init__(self):
        self.num_particles = 101
        self.particles: List[Particle] = []
        self.mu = WIDTH / 2
        self.sigma = WIDTH / 4
        self.velocity = 200
        self.x_displacement = 1
        self.y_displacement = 10
        self.x_values, self.y_values = generate_bell_curve(self.num_particles)

        for i in range(self.num_particles):
            p = Particle(int(self.x_values[i]), HEIGHT)
            self.particles.append(p)

    def update_particle(self, particle):
        dvx = random.randint(-self.x_displacement, self.x_displacement)
        dvy = 0

        i = self.particles.index(particle)
        if i < len(self.y_values):
            dvy = -(self.y_values[i] * self.velocity)
        else:
            dvy = -(self.y_values[i % len(self.y_values)] * self.velocity)

        if (
            particle.y < HEIGHT - self.y_displacement * 10 - 300
            and not particle.replicated
        ):
            self.respawn_particle(i)
            particle.replicated = True
        else:
            particle.update(dvx, dvy)

    def respawn_particle(self, i):
        old_p = self.particles[i]
        new_p = Particle(old_p.x, HEIGHT)
        self.particles[i] = new_p

        if i < len(self.y_values):
            threshold = 0.5  # Adjust the threshold as needed
        if self.y_values[i] > threshold:
            for _ in range(
                int(self.y_values[i] * 10)
            ):  # Adjust the multiplier as needed
                self.particles.insert(i + 1, Particle(old_p.x, HEIGHT))

    def draw_coffee_cup(screen):
        # Define the coordinates and dimensions of the coffee cup
        cup_x = WIDTH // 2 - 270
        cup_y = HEIGHT - 240
        ascii_cup = """                                                   
                               ..........                                                 
                          ..::::::::::-----:-:-::::....                                   
                        .::---=++++*****+***++++##%%###*+=-:.   .                         
                        .:=****************+**###########%%%#+:...                        
                         .-+#%%%%%%%%%%%%%%%%##############%%#+...                        
                            .-=+**#####################**+=-::::::..........              
                                   ..::-----------:::.......:::::::...     ...            
                                                  ..........:::::::.         ..           
                                                   .........:::::..           .           
                                                  ..........:::.:             .           
                      ...                         ..........:::::--:..       .            
                  ........                       ..........:::::-------.    .             
               ............                     ...........::..-----::..  ..              
             ...............                   ...............:-:::... ..:::.             
            ..................              .................:::.....:::::....            
            .....................         ..................:...:::::::..... .            
            .............................................::::::::::........ .             
              ...............   .......................:-:::::::............              
                .............    ..  ................:--::................                
                   ...........             .............................                  
                       ..........                  ..................                     
                                                .................                         
                                 ...........................                                                                                                                   
"""
        # Draw the coffee cup
        cup_font = pygame.font.SysFont("monospace", 10)
        cup_lines = ascii_cup.splitlines()
        for i, line in enumerate(cup_lines):
            cup_text = cup_font.render(line, True, (255, 255, 255))
            screen.blit(cup_text, (cup_x, cup_y + i * 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle System")

    particle_system = ParticleSystem()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        ParticleSystem.draw_coffee_cup(screen)  # Draw the coffee cup

        for particle in particle_system.particles:
            particle_system.update_particle(particle)
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
