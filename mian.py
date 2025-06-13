import tkinter as tk
from tkinter import messagebox
import random
import time
import math

class AwesomeSnake:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐍 Awesome Snake Game!")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Game settings
        self.board_width = 600
        self.board_height = 600
        self.cell_size = 20
        self.cols = self.board_width // self.cell_size
        self.rows = self.board_height // self.cell_size
        
        # Game state
        self.snake = [(15, 15)]  # Start in center
        self.direction = (1, 0)  # Moving right
        self.food = self.spawn_food()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.speed = 150  # milliseconds
        
        # Animation variables
        self.animation_frame = 0
        self.food_pulse = 0
        self.snake_shimmer = 0
        self.particle_effects = []
        self.text_animations = []
        
        # Power-ups
        self.power_up = None
        self.power_up_timer = 0
        self.power_up_pulse = 0
        self.invincible = 0
        self.speed_boost = 0
        
        # UI Setup
        self.setup_ui()
        
        # Key bindings - FIXED!
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.focus_set()
        
        # Start animation loop
        self.animate()
        # Start game loop
        self.game_loop()
    
    def setup_ui(self):
        # Title with gradient effect
        title = tk.Label(self.root, text="🐍 AWESOME SNAKE GAME 🐍", 
                        font=("Arial", 20, "bold"), 
                        fg="#00ff88", bg="#1a1a2e")
        title.pack(pady=5)
        
        # Score display
        self.score_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.score_frame.pack()
        
        self.score_label = tk.Label(self.score_frame, text="Score: 0", 
                                   font=("Arial", 14, "bold"), 
                                   fg="#ffff00", bg="#1a1a2e")
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.high_score_label = tk.Label(self.score_frame, text="High Score: 0", 
                                        font=("Arial", 14, "bold"), 
                                        fg="#ff6b35", bg="#1a1a2e")
        self.high_score_label.pack(side=tk.RIGHT, padx=20)
        
        # Game canvas
        self.canvas = tk.Canvas(self.root, 
                               width=self.board_width, 
                               height=self.board_height,
                               bg="#0f3460",
                               highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Status display
        self.status_label = tk.Label(self.root, text="Use WASD or Arrow Keys to move • Press R to restart", 
                                    font=("Arial", 12), 
                                    fg="#00ccff", bg="#1a1a2e")
        self.status_label.pack()
        
        # Controls
        controls_frame = tk.Frame(self.root, bg="#1a1a2e")
        controls_frame.pack(pady=5)
        
        self.new_game_btn = tk.Button(controls_frame, text="🎮 New Game", 
                                     command=self.restart_game,
                                     font=("Arial", 10, "bold"),
                                     bg="#00ff88", fg="black",
                                     relief="flat", padx=20)
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(controls_frame, text="⏯️ Pause", 
                                  command=self.toggle_pause,
                                  font=("Arial", 10, "bold"),
                                  bg="#ffff00", fg="black",
                                  relief="flat", padx=20)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
    
    def spawn_food(self):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def spawn_power_up(self):
        if random.random() < 0.3:  # 30% chance
            while True:
                x = random.randint(0, self.cols - 1)
                y = random.randint(0, self.rows - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    power_type = random.choice(['invincible', 'speed', 'double_points'])
                    self.power_up = (x, y, power_type)
                    self.power_up_timer = 100  # Disappears after 100 game ticks
                    break
    
    def add_particle_effect(self, x, y, color="#ffff00", count=5):
        """Add particle explosion effect"""
        for _ in range(count):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-3, 3),
                'life': 20,
                'color': color,
                'size': random.uniform(2, 4)
            }
            self.particle_effects.append(particle)
    
    def add_text_animation(self, text, x, y, color="#ffff00"):
        """Add floating text animation"""
        anim = {
            'text': text,
            'x': x,
            'y': y,
            'vy': -2,
            'life': 30,
            'color': color,
            'size': 16
        }
        self.text_animations.append(anim)
    
    def on_key_press(self, event):
        key = event.keysym.lower()
        
        # FIXED: Handle restart properly
        if key == 'r':
            self.restart_game()
            return
        
        if self.game_over:
            return
        
        # Movement controls
        if key in ['w', 'up'] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key in ['s', 'down'] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key in ['a', 'left'] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key in ['d', 'right'] and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif key == 'space':
            self.toggle_pause()
    
    def on_key_release(self, event):
        # Handle key release if needed
        pass
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.status_label.config(text="⏸️ PAUSED - Press SPACE to continue")
        else:
            self.update_status()
    
    def update_status(self):
        status = "Use WASD or Arrow Keys to move • Press R to restart"
        if self.invincible > 0:
            status = f"🛡️ INVINCIBLE! ({self.invincible//10}s left) • Press R to restart"
        elif self.speed_boost > 0:
            status = f"⚡ SPEED BOOST! ({self.speed_boost//10}s left) • Press R to restart"
        
        self.status_label.config(text=status)
    
    def move_snake(self):
        if self.paused or self.game_over:
            return
        
        # Get new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision (unless invincible)
        if self.invincible <= 0:
            if (new_head[0] < 0 or new_head[0] >= self.cols or 
                new_head[1] < 0 or new_head[1] >= self.rows):
                self.end_game()
                return
        else:
            # Wrap around when invincible
            new_head = (new_head[0] % self.cols, new_head[1] % self.rows)
        
        # Check self collision (unless invincible)
        if self.invincible <= 0 and new_head in self.snake:
            self.end_game()
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        ate_food = False
        if new_head == self.food:
            ate_food = True
            points = 10
            if self.speed_boost > 0:
                points *= 2  # Double points during speed boost
            
            self.score += points
            
            # Add cool effects when eating food
            food_x, food_y = self.food
            screen_x = food_x * self.cell_size + self.cell_size // 2
            screen_y = food_y * self.cell_size + self.cell_size // 2
            self.add_particle_effect(screen_x, screen_y, "#ff4444", 8)
            self.add_text_animation(f"+{points}", screen_x, screen_y, "#ffff00")
            
            self.food = self.spawn_food()
            
            # Chance to spawn power-up
            self.spawn_power_up()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        # Check power-up collision
        if self.power_up and new_head == (self.power_up[0], self.power_up[1]):
            power_type = self.power_up[2]
            power_x, power_y = self.power_up[0], self.power_up[1]
            screen_x = power_x * self.cell_size + self.cell_size // 2
            screen_y = power_y * self.cell_size + self.cell_size // 2
            
            if power_type == 'invincible':
                self.invincible = 50  # 5 seconds
                self.add_particle_effect(screen_x, screen_y, "#ff00ff", 12)
                self.add_text_animation("INVINCIBLE!", screen_x, screen_y, "#ff00ff")
            elif power_type == 'speed':
                self.speed_boost = 50  # 5 seconds
                self.add_particle_effect(screen_x, screen_y, "#ffff00", 12)
                self.add_text_animation("SPEED BOOST!", screen_x, screen_y, "#ffff00")
            elif power_type == 'double_points':
                self.score += 50  # Bonus points
                self.add_particle_effect(screen_x, screen_y, "#00ffff", 15)
                self.add_text_animation("+50 BONUS!", screen_x, screen_y, "#00ffff")
            
            self.power_up = None
        
        # Update power-up timer
        if self.power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up = None
        
        # Update power-up effects
        if self.invincible > 0:
            self.invincible -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
    
    def animate(self):
        """Handle all animations"""
        self.animation_frame += 1
        self.food_pulse = abs(math.sin(self.animation_frame * 0.2)) * 0.5 + 0.5
        self.snake_shimmer = abs(math.sin(self.animation_frame * 0.1)) * 0.3 + 0.7
        self.power_up_pulse = abs(math.sin(self.animation_frame * 0.3)) * 0.4 + 0.6
        
        # Update particles
        for particle in self.particle_effects[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            particle['size'] *= 0.98
            
            if particle['life'] <= 0:
                self.particle_effects.remove(particle)
        
        # Update text animations
        for text_anim in self.text_animations[:]:
            text_anim['y'] += text_anim['vy']
            text_anim['life'] -= 1
            
            if text_anim['life'] <= 0:
                self.text_animations.remove(text_anim)
        
        # Continue animation loop
        self.root.after(50, self.animate)
    
    def update_display(self):
        self.canvas.delete("all")
        
        # Draw animated grid
        grid_offset = (self.animation_frame % 20) * 0.1
        for i in range(0, self.board_width, self.cell_size):
            alpha = abs(math.sin((i + grid_offset) * 0.1)) * 0.3 + 0.1
            color = f"#{int(22 + alpha * 100):02x}{int(83 + alpha * 50):02x}{int(126 + alpha * 50):02x}"
            self.canvas.create_line(i, 0, i, self.board_height, fill=color, width=1)
        for i in range(0, self.board_height, self.cell_size):
            alpha = abs(math.sin((i + grid_offset) * 0.1)) * 0.3 + 0.1
            color = f"#{int(22 + alpha * 100):02x}{int(83 + alpha * 50):02x}{int(126 + alpha * 50):02x}"
            self.canvas.create_line(0, i, self.board_width, i, fill=color, width=1)
        
        # Draw snake with shimmer effect
        for i, (x, y) in enumerate(self.snake):
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            
            if i == 0:  # Head
                # Animated head color
                if self.invincible > 0:
                    shimmer = abs(math.sin(self.animation_frame * 0.5))
                    r = int(255 * shimmer)
                    g = int(0 * shimmer)
                    b = int(128 * shimmer)
                    color = f"#{r:02x}{g:02x}{b:02x}"
                else:
                    shimmer = self.snake_shimmer
                    r = int(0 * shimmer)
                    g = int(255 * shimmer)
                    b = int(136 * shimmer)
                    color = f"#{r:02x}{g:02x}{b:02x}"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=2)
                
                # Animated eyes
                eye_blink = 1 if (self.animation_frame % 60) > 55 else 0
                if not eye_blink:
                    self.canvas.create_oval(x1+5, y1+5, x1+8, y1+8, fill="white")
                    self.canvas.create_oval(x1+12, y1+5, x1+15, y1+8, fill="white")
                    self.canvas.create_oval(x1+6, y1+6, x1+7, y1+7, fill="black")
                    self.canvas.create_oval(x1+13, y1+6, x1+14, y1+7, fill="black")
                else:
                    self.canvas.create_line(x1+5, y1+6, x1+8, y1+6, fill="white", width=2)
                    self.canvas.create_line(x1+12, y1+6, x1+15, y1+6, fill="white", width=2)
                    
            else:  # Body
                intensity = max(0.3, 1 - (i * 0.1))
                body_shimmer = abs(math.sin(self.animation_frame * 0.1 + i * 0.3)) * 0.2 + 0.8
                
                if self.invincible > 0:
                    r = int(255 * intensity * body_shimmer)
                    g = int(0 * intensity * body_shimmer)
                    b = int(128 * intensity * body_shimmer)
                else:
                    r = int(0 * intensity * body_shimmer)
                    g = int(255 * intensity * body_shimmer)
                    b = int(136 * intensity * body_shimmer)
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ffffff", width=1)
        
        # Draw animated food
        fx, fy = self.food
        fx1, fy1 = fx * self.cell_size, fy * self.cell_size
        fx2, fy2 = fx1 + self.cell_size, fy1 + self.cell_size
        
        # Pulsing food
        pulse_size = int(self.food_pulse * 4)
        food_r = int(255 * self.food_pulse)
        food_color = f"#{food_r:02x}4444"
        
        self.canvas.create_oval(fx1+2-pulse_size, fy1+2-pulse_size, 
                               fx2-2+pulse_size, fy2-2+pulse_size, 
                               fill=food_color, outline="#ffffff", width=2)
        
        # Draw animated power-up
        if self.power_up:
            px, py, ptype = self.power_up
            px1, py1 = px * self.cell_size, py * self.cell_size
            px2, py2 = px1 + self.cell_size, py1 + self.cell_size
            
            colors = {'invincible': '#ff00ff', 'speed': '#ffff00', 'double_points': '#00ffff'}
            symbols = {'invincible': '🛡️', 'speed': '⚡', 'double_points': '💎'}
            
            # Pulsing power-up
            pulse_size = int(self.power_up_pulse * 3)
            base_color = colors[ptype]
            
            self.canvas.create_rectangle(px1-pulse_size, py1-pulse_size, 
                                       px2+pulse_size, py2+pulse_size, 
                                       fill=base_color, outline="white", width=2)
            
            # Rotating effect
            rotation_offset = math.sin(self.animation_frame * 0.2) * 2
            self.canvas.create_text(px1 + self.cell_size//2, py1 + self.cell_size//2 + rotation_offset,
                                  text=symbols[ptype], font=("Arial", 12))
        
        # Draw particle effects
        for particle in self.particle_effects:
            if particle['life'] > 0:
                alpha = particle['life'] / 20.0
                size = particle['size']
                self.canvas.create_oval(particle['x']-size, particle['y']-size,
                                      particle['x']+size, particle['y']+size,
                                      fill=particle['color'], outline="")
        
        # Draw text animations
        for text_anim in self.text_animations:
            if text_anim['life'] > 0:
                alpha = text_anim['life'] / 30.0
                size = int(text_anim['size'] * alpha)
                self.canvas.create_text(text_anim['x'], text_anim['y'],
                                      text=text_anim['text'], 
                                      font=("Arial", size, "bold"),
                                      fill=text_anim['color'])
        
        # Update score labels with animation
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        
        # Update status
        self.update_status()
    
    def end_game(self):
        self.game_over = True
        
        # Add explosion effect at crash site
        head_x, head_y = self.snake[0]
        screen_x = head_x * self.cell_size + self.cell_size // 2
        screen_y = head_y * self.cell_size + self.cell_size // 2
        self.add_particle_effect(screen_x, screen_y, "#ff0000", 20)
        
        # Game over text
        self.canvas.create_text(self.board_width//2, self.board_height//2,
                               text="💀 GAME OVER! 💀", 
                               font=("Arial", 36, "bold"),
                               fill="#ff4444")
        self.canvas.create_text(self.board_width//2, self.board_height//2 + 50,
                               text=f"Final Score: {self.score}", 
                               font=("Arial", 20),
                               fill="#ffffff")
        self.canvas.create_text(self.board_width//2, self.board_height//2 + 80,
                               text="Press 'R' or click 'New Game' to restart", 
                               font=("Arial", 14),
                               fill="#00ccff")
        
        self.status_label.config(text="💀 Game Over! Press R to restart")
    
    def restart_game(self):
        self.snake = [(15, 15)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.power_up = None
        self.invincible = 0
        self.speed_boost = 0
        self.particle_effects = []
        self.text_animations = []
        
        # Add restart effect
        center_x = self.board_width // 2
        center_y = self.board_height // 2
        self.add_particle_effect(center_x, center_y, "#00ff88", 15)
        self.add_text_animation("NEW GAME!", center_x, center_y, "#00ff88")
        
        self.update_status()
    
    def game_loop(self):
        if not self.game_over:
            self.move_snake()
            
            # Adjust speed based on power-ups
            current_speed = self.speed
            if self.speed_boost > 0:
                current_speed = max(50, self.speed // 2)  # Much faster!
            
            self.root.after(current_speed, self.game_loop)
        else:
            self.root.after(1000, self.game_loop)  # Keep checking for restart
        
        # Always update display
        self.update_display()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = AwesomeSnake()
    game.run()