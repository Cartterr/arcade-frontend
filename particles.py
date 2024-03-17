import pygame
import random
import math

class Particle:
    def __init__(self, screen, start_pos, color, velocity, size, lifetime):
        self.screen = screen
        self.x, self.y = start_pos
        self.color = color
        self.velocity = velocity
        self.size = size
        self.original_size = size  # Store the original size for size reduction
        self.lifetime = lifetime
        self.original_lifetime = lifetime  # Store the original lifetime for fading calculation

    def update(self):
        # Update position
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # Decrease lifetime
        self.lifetime -= 1
        # Gradually reduce size
        self.size = max(0, self.size - (self.original_size / self.original_lifetime))
        # Ensure size doesn't become negative
        self.size = max(self.size, 0)

    def draw(self):
        # Calculate fading effect by reducing alpha based on remaining lifetime
        alpha = int(255 * (self.lifetime / self.original_lifetime))
        color_with_alpha = self.color + (alpha,)  # Add alpha to the color tuple
        # Use a temporary surface to draw the particle with alpha transparency
        temp_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color_with_alpha, temp_surface.get_rect())
        self.screen.blit(temp_surface, (self.x, self.y))

    def is_dead(self):
        # Check if the particle should be removed (lifetime has expired)
        return self.lifetime <= 0


class ParticleSystem:
    def __init__(self, screen, center_pos, num_particles=50):
        self.screen = screen
        self.particles = []
        self.center_pos = center_pos
        self.num_particles = num_particles

    def emit(self):
        # Continuously generate new particles
        if len(self.particles) < self.num_particles:
            velocity = [random.randint(-5, 5) * 6, random.randint(-5, 5) * 6]
            size = random.randint(2, 5) * 2
            lifetime = 120  # Lifetime in frames, e.g., 120 frames = 2 seconds at 60FPS
            self.particles.append(Particle(self.screen, self.center_pos, (255, 255, 255), velocity, size, lifetime))

    def update(self):
        for particle in list(self.particles):  # Use list() to make a copy of the list
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()



# In particles.py, add this new class
class RotatingRingParticleSystem:
    def __init__(self, screen, center_pos, radius, num_particles=5):
        self.screen = screen
        self.center_pos = center_pos
        self.radius = radius
        self.num_particles = num_particles
        self.particles = []
        self.angle = 0
        self.visible = True

    def emit(self):
        # Calculate the current positions on the circle for two points opposite each other
        rad_angle = math.radians(self.angle)
        opposite_rad_angle = math.radians(self.angle + 180)  # Opposite point on the circle

        emit_x1 = self.center_pos[0] + math.cos(rad_angle) * self.radius
        emit_y1 = self.center_pos[1] + math.sin(rad_angle) * self.radius
        emit_x2 = self.center_pos[0] + math.cos(opposite_rad_angle) * self.radius
        emit_y2 = self.center_pos[1] + math.sin(opposite_rad_angle) * self.radius

        # Generate new particles at these positions
        for _ in range(self.num_particles):
            velocity1 = [random.uniform(-0.6, 0.6), random.uniform(-0.2, 0.2)]  # Small random velocity
            velocity2 = [random.uniform(-0.6, 0.6), random.uniform(-0.2, 0.2)]  # Small random velocity for the opposite point
            lifetime = 30  # Short lifetime for fade effect
            size = random.randint(6, 10)
            self.particles.append(Particle(self.screen, (emit_x1, emit_y1), (255, 255, 255), velocity1, size, lifetime))
            self.particles.append(Particle(self.screen, (emit_x2, emit_y2), (255, 255, 255), velocity2, size, lifetime))

        # Update angle for next emission
        self.angle = (self.angle + 5) % 360  # Adjust the speed of rotation by changing the angle increment

    def update(self):
        # Update and remove dead particles
        for particle in list(self.particles):
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def draw(self):
        if not self.visible:
            return
        for particle in self.particles:
            particle.draw()

    def set_visibility(self, visible):
        self.visible = visible
