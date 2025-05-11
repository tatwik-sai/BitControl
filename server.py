import time
import ctypes
import subprocess   
import keyboard
import os
from connection import Connection
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import pygame
import random
import screen_brightness_control as sbc

class PongGame:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong Top-Bottom Paddle Game")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.BACKGROUND_COLOR = (50, 50, 50)

        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 100, 10
        self.BALL_SIZE = 15
        self.BALL_SPEED_X, self.BALL_SPEED_Y = 4, 4

        self.player = pygame.Rect(self.WIDTH//2 - self.PADDLE_WIDTH//2, self.HEIGHT - 30, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.enemy = pygame.Rect(self.WIDTH//2 - self.PADDLE_WIDTH//2, 20, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

        self.ball = pygame.Rect(self.WIDTH//2 - self.BALL_SIZE//2, self.HEIGHT//2 - self.BALL_SIZE//2, self.BALL_SIZE, self.BALL_SIZE)
        self.ball_speed_x = self.BALL_SPEED_X * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED_Y * random.choice([-1, 1])

        self.FONT = pygame.font.Font(None, 36)

        self.start_button = pygame.Rect(self.WIDTH//2 - 60, self.HEIGHT//2 - 20, 120, 40)
        self.resume_button = pygame.Rect(self.WIDTH//2 - 60, self.HEIGHT//2 - 20, 120, 40)

        self.high_score = 0
        self.score = 0
        self.run = True
        self.playing = False
        self.paused = False

        self.clock = pygame.time.Clock()

    def draw_start_screen(self):
        self.WIN.fill(self.BACKGROUND_COLOR)
        pygame.draw.rect(self.WIN, self.WHITE, self.start_button)
        play_text = self.FONT.render("Play", True, self.BLACK)
        self.WIN.blit(play_text, (self.start_button.x + 25, self.start_button.y + 5))
        hs_text = self.FONT.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.WIN.blit(hs_text, (self.WIDTH//2 - hs_text.get_width()//2, self.HEIGHT//2 - 80))
        pygame.display.update()

    def reset_game(self):
        self.ball.center = (self.WIDTH//2, self.HEIGHT//2)
        self.ball_speed_x = self.BALL_SPEED_X * random.choice([-1, 1])
        self.ball_speed_y = self.BALL_SPEED_Y * random.choice([-1, 1])
        self.player.x = self.WIDTH//2 - self.PADDLE_WIDTH//2
        self.enemy.x = self.WIDTH//2 - self.PADDLE_WIDTH//2
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.playing:
                        self.playing = True
                        self.paused = False
                        self.reset_game()
                    else:
                        self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.playing and self.start_button.collidepoint(event.pos):
                    self.playing = True
                    self.paused = False
                    self.reset_game()
                elif self.paused and self.resume_button.collidepoint(event.pos):
                    self.paused = False

    def move_objects(self):
        global AP, BP
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.left > 0:
            self.player.x -= 7
        if keys[pygame.K_RIGHT] and self.player.right < self.WIDTH:
            self.player.x += 7

        if self.enemy.centerx < self.ball.centerx and self.enemy.right < self.WIDTH:
            self.enemy.x += 5
        if self.enemy.centerx > self.ball.centerx and self.enemy.left > 0:
            self.enemy.x -= 5

        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.left <= 0 or self.ball.right >= self.WIDTH:
            self.ball_speed_x *= -1

        if self.ball.colliderect(self.player) and self.ball_speed_y > 0:
            self.ball_speed_y *= -1
            self.score += 1
        if self.ball.colliderect(self.enemy) and self.ball_speed_y < 0:
            self.ball_speed_y *= -1

        if self.ball.bottom >= self.HEIGHT or self.ball.top <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
            self.playing = False
            AP = False
            BP = False

    def draw_game(self):
        self.WIN.fill(self.BACKGROUND_COLOR)
        pygame.draw.rect(self.WIN, self.RED, self.player)
        pygame.draw.rect(self.WIN, self.BLUE, self.enemy)
        pygame.draw.ellipse(self.WIN, self.GREEN, self.ball)
        score_text = self.FONT.render(f"Score: {self.score}", True, self.WHITE)
        self.WIN.blit(score_text, (10, 10))

        if self.paused:
            pygame.draw.rect(self.WIN, self.WHITE, self.resume_button)
            resume_text = self.FONT.render("Resume", True, self.BLACK)
            self.WIN.blit(resume_text, (self.resume_button.x + 10, self.resume_button.y + 5))

        pygame.display.update()

    def game_loop(self):
        global AP, BP
        while self.run:
            self.clock.tick(60)
            self.handle_events()

            if not self.playing:
                self.draw_start_screen()
            else:
                if not self.paused:
                    if AP and self.player.left > 0:
                        self.player.x -= 7
                    elif BP and self.player.right < self.WIDTH:
                        self.player.x += 7
                    self.move_objects()
                self.draw_game()

        pygame.quit()

class CarDodgeGame:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Car Dodge Game")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.CAR_WIDTH, self.CAR_HEIGHT = 50, 100
        self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT = 50, 100
        self.OBSTACLE_SPEED = 5

        self.car = pygame.Rect(self.WIDTH // 2 - self.CAR_WIDTH // 2, self.HEIGHT - self.CAR_HEIGHT - 10, self.CAR_WIDTH, self.CAR_HEIGHT)
        self.obstacles = []

        self.road_img = pygame.transform.scale(pygame.image.load("images/road.png"), (self.WIDTH, self.HEIGHT))
        self.car_img = pygame.transform.scale(pygame.image.load("images/car.png"), (self.CAR_WIDTH, self.CAR_HEIGHT))
        self.enemy_car_imgs = [
            pygame.transform.scale(pygame.image.load("images/enemy1.png"), (self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)),
            pygame.transform.scale(pygame.image.load("images/enemy2.png"), (self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)),
            pygame.transform.scale(pygame.image.load("images/enemy3.png"), (self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)),
            pygame.transform.scale(pygame.image.load("images/enemy4.png"), (self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)),
            pygame.transform.scale(pygame.image.load("images/enemy0.png"), (self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)),
        ]

        self.FONT = pygame.font.Font(None, 36)

        self.start_button = pygame.Rect(self.WIDTH//2 - 60, self.HEIGHT//2 - 20, 120, 40)
        self.resume_button = pygame.Rect(self.WIDTH//2 - 60, self.HEIGHT//2 - 20, 120, 40)

        self.high_score = 0
        self.score = 0
        self.run = True
        self.playing = False
        self.paused = False
        self.clock = pygame.time.Clock()

        self.spawn_timer = 0

    def draw_start_screen(self):
        self.WIN.blit(self.road_img, (0, 0))
        pygame.draw.rect(self.WIN, self.WHITE, self.start_button)
        play_text = self.FONT.render("Play", True, self.BLACK)
        self.WIN.blit(play_text, (self.start_button.x + 25, self.start_button.y + 5))
        hs_text = self.FONT.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.WIN.blit(hs_text, (self.WIDTH//2 - hs_text.get_width()//2, self.HEIGHT//2 - 80))
        pygame.display.update()

    def reset_game(self):
        self.obstacles = []
        self.car.x = self.WIDTH // 2 - self.CAR_WIDTH // 2
        self.score = 0

    def spawn_obstacle(self):
        x = random.randint(0, self.WIDTH - self.OBSTACLE_WIDTH)
        obstacle_rect = pygame.Rect(x, -self.OBSTACLE_HEIGHT, self.OBSTACLE_WIDTH, self.OBSTACLE_HEIGHT)
        obstacle_img = random.choice(self.enemy_car_imgs)
        self.obstacles.append((obstacle_rect, obstacle_img))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.playing:
                        self.playing = True
                        self.paused = False
                        self.reset_game()
                    else:
                        self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.playing:
                    if self.start_button.collidepoint(event.pos):
                        self.playing = True
                        self.paused = False
                        self.reset_game()
                else:
                    if self.paused and self.resume_button.collidepoint(event.pos):
                        self.paused = False

    def update_game(self):
        global AP, BP
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.car.left > 0:
            self.car.x -= 7
        if keys[pygame.K_RIGHT] and self.car.right < self.WIDTH:
            self.car.x += 7

        self.spawn_timer += 1
        if self.spawn_timer > 30:
            self.spawn_obstacle()
            self.spawn_timer = 0

        for obs, img in self.obstacles:
            obs.y += self.OBSTACLE_SPEED

        self.obstacles = [(obs, img) for obs, img in self.obstacles if obs.y < self.HEIGHT]

        for obs, img in self.obstacles:
            if self.car.colliderect(obs):
                if self.score > self.high_score:
                    self.high_score = self.score
                self.playing = False
                AP = False
                BP = False

        self.score += 1

    def draw_game(self):
        self.WIN.blit(self.road_img, (0, 0))
        self.WIN.blit(self.car_img, (self.car.x, self.car.y))

        for obs, img in self.obstacles:
            self.WIN.blit(img, (obs.x, obs.y))

        score_text = self.FONT.render(f"Score: {self.score}", True, self.WHITE)
        self.WIN.blit(score_text, (10, 10))

        if self.paused:
            pygame.draw.rect(self.WIN, self.WHITE, self.resume_button)
            resume_text = self.FONT.render("Resume", True, self.BLACK)
            self.WIN.blit(resume_text, (self.resume_button.x + 10, self.resume_button.y + 5))

        pygame.display.update()

    def game_loop(self):
        global AP, BP
        while self.run:
            self.clock.tick(60)
            self.handle_events()
            if not self.playing:
                self.draw_start_screen()
            elif self.playing:
                if not self.paused:
                    if AP and self.car.left > 0: 
                        self.car.x -= 7
                    elif BP and self.car.right < self.WIDTH:
                        self.car.x += 7
                    self.update_game()
                self.draw_game()

        pygame.quit()

def increase_volume(step=0.05):
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + step)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume(step=0.05):
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - step)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def get_current_brightness():
    b = sbc.get_brightness()[0]
    return int(b)

def set_brightness(level):
    level = max(0, min(100, int(level)))
    sbc.set_brightness(level, display=0)

on_task = False
task = None
pong = None
car = None
AP = False
BP = False
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

def handle_pong(inp):
    global pong, AP, BP
    if not pong:
        return
    if inp == "AP":
        BP = False
        AP = True

    elif inp == "BP":
        AP = False
        BP = True
    elif inp == "LP":
        AP = False
        BP = False
        if not pong.playing:
            pong.playing = True
            pong.paused = False
            pong.reset_game()
            print("\t->Starting...")
        else:
            pong.paused = not pong.paused
            print(f"\t->{"Paused" if pong.paused else "Resumed"}")

def handle_music(inp):
    if inp == "A":
        print("\t-> Moving to Previous Track")
        keyboard.send("previous track")
        keyboard.send("previous track")
    elif inp == "B":
        print("\t-> Moving to Next Track")
        keyboard.send("next track")
    elif inp == "LP":
        print("\t-> Play/Pause")
        keyboard.send("play/pause media")
    elif inp == "TL":
        print("\t-> Decreasing Volume")
        decrease_volume()
    elif inp == "TR":
        print("\t-> Increasing Volume")
        increase_volume()

def handle_car(inp):
    global car, AP, BP
    if not car:
        return
    try:
        acc = int(inp)
        if acc > 200:
            AP = False
            BP = True
        elif acc < -200:
            BP = False
            AP = True
        else:
            BP = False
            AP = False
    except ValueError:
        if inp == "LP":
            AP = False
            BP = False
            if not car.playing:
                print("\t->Starting...")
                car.playing = True
                car.paused = False
                car.reset_game()
            else:
                car.paused = not car.paused
                print(f"\t->{"Paused" if car.paused else "Resumed"}")

def handle_brightness(inp):
    if inp == "A":
        print("\t-> Decreasing Brightness..")
        curr = get_current_brightness()
        set_brightness(curr - 10)
    elif inp == "B":
        print("\t-> Increasing Brightness..")
        curr = get_current_brightness()
        set_brightness(curr + 10)

def process_input(string: str):
    global on_task, task, pong, car, AP, BP
    if string in ["A", "B"]:
        AP = False
        BP = False
    if on_task:
        if string == "Stop":
            if task == "Music":
                print("[-] Quitting Spotify")
                subprocess.run(
                ["taskkill", "/f", "/im", "Spotify.exe"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            elif task == "Pong":
                print("[-] Quitting Pong Game")
                pong.run = False
                AP = False
                BP = False
            elif task == "Car":
                print("[-] Quitting CarDodge Game")
                car.run = False
                AP = False
                BP = False
            on_task = False
        else:
            if task == "Pong":
                handle_pong(string)
            elif task == "Music":
                handle_music(string)
            elif task == "Car":
                handle_car(string)
            elif task == "Brightness":
                handle_brightness(string)
    else:
        if string == "Pong":
            print("[+] Launching Pong Game")
            on_task = True
            task = string
            AP = False
            BP = False
            pong = PongGame()
            pong.game_loop()

        elif string == "Music":
            print("[+] Opening Spotify")
            on_task = True
            task = string
            subprocess.Popen(["spotify"])
            
        elif string == "Lock":
            print("[+] Locking the PC")
            ctypes.windll.user32.LockWorkStation()

        elif string == "Car":
            print("[+] Launching CarDodge Game")
            on_task = True
            task = string        
            car = CarDodgeGame()
            AP = False
            BP = False
            car.game_loop()

        elif string == "Brightness":
            print("[+] On Brightness controller")
            on_task = True
            task = string    

        elif string == "Shutdown":
            print("[+] Shutting Down PC")
            os.system("shutdown /s /f /t 0")

microbit_name = None
with Connection.find_microbit(microbit_name) as microbit:
    print("[+] Connected to Microbit....")
    microbit.uart.receive_string(process_input)
    while True:
        time.sleep(1)