import pygame
import random
import time
import asyncio

# Initialize Pygame
pygame.init()

# Initialize mixer for music
pygame.mixer.init()

# Load background music
pygame.mixer.music.load('music1.mp3')
pygame.mixer.music.set_volume(0.5)  # Set volume if needed

# Get screen size
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Define window size based on screen size (e.g., 80% of screen size)
win_width = int(screen_width * 0.8)
win_height = int(screen_height * 0.8)
win = pygame.display.set_mode((win_width, win_height))

# Window title
pygame.display.set_caption("Tangkap Gas Rumah Kaca")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Game speed
clock = pygame.time.Clock()
fps = 50
gas_speed = 5

# Load images with error handling
try:
    player_img = pygame.image.load('player.png')
    background_imgs = [
        pygame.image.load('background1.png'),
        pygame.image.load('background2.png')
    ]
    background3_img = pygame.image.load('background3.png')
    gas_images = {
        "CO2": pygame.image.load('co2.png'),
        "CH4": pygame.image.load('ch4.png'),
        "N2O": pygame.image.load('n2o.png'),
        "CFC": pygame.image.load('cfc.png'),
        "SO2": pygame.image.load('so2.png'),
        "NO": pygame.image.load('no.png'),
        "renewable": pygame.image.load('renewable.png'),
        "tree": pygame.image.load('tree.png'),
        "recycle": pygame.image.load('recycle.png'),
        "regulation": pygame.image.load('regulation.png')
    }
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Scale images to match the new window size
player_width = 64
player_height = 64
player_img = pygame.transform.scale(player_img, (player_width, player_height))

background_imgs = [pygame.transform.scale(img, (win_width, win_height)) for img in background_imgs]
background3_img = pygame.transform.scale(background3_img, (win_width, win_height))

gas_width = 50
gas_height = 50
for key in gas_images:
    gas_images[key] = pygame.transform.scale(gas_images[key], (gas_width, gas_height))

# Player position and speed
player_x = win_width // 2 - player_width // 2
player_y = win_height - player_height - 10
player_speed = 15

# Score
score = 50

# Gas object
class Gas:
    def __init__(self, x, y, type, value):
        self.x = x
        self.y = y
        self.type = type
        self.value = value

    def draw(self, win):
        win.blit(gas_images[self.type], (self.x, self.y))

    def move(self):
        self.y += gas_speed

def redraw_window(start_time, game_duration):
    current_time = time.time()
    background_img = background_imgs[int((current_time - start_time) // 15) % 2]
    win.blit(background_img, (0, 0))
    win.blit(player_img, (player_x, player_y))
    for gas in gases:
        gas.draw(win)
    
    # Display score
    score_text = font.render(f'Score: {score}', True, white)
    win.blit(score_text, (10, 10))
    
    # Score bar with gradient
    bar_width = int(win_width * 0.375)
    bar_height = int(win_height * 0.033)
    bar_x = 10
    bar_y = 50
    fill_width = (score / 100) * bar_width
    
    # Gradient color
    gradient_color = (
        int(255 * (score / 100)), 0, int(255 * (1 - score / 100))
    )
    
    pygame.draw.rect(win, white, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(win, gradient_color, (bar_x, bar_y, fill_width, bar_height))
    
    # Display timer
    remaining_time = max(0, int(game_duration - (current_time - start_time)))
    timer_text = font.render(f'Time: {remaining_time}s', True, white)
    win.blit(timer_text, (win_width - 120, 10))

    pygame.display.update()

def game_description():
    win.blit(background3_img, (0, 0))
    y_offset = 20
    line_height = 30
    title = font.render("Game Description", True, white)
    win.blit(title, (win_width // 2 - title.get_width() // 2, y_offset))
    y_offset += 50

    # Display gas images and names horizontally
    gases_info = [
        ("CO2", 6), ("CH4", 5), ("N2O", 4), ("CFC", 3), ("SO2", 2), ("NO", 1),
        ("renewable", -5), ("tree", -4), ("recycle", -3), ("regulation", -2)
    ]

    num_columns = 2  # Number of columns to display gas info
    column_width = win_width // num_columns

    for i, (gas_name, gas_value) in enumerate(gases_info):
        column = i % num_columns
        row = i // num_columns
        x_pos = column * column_width + (column_width - gas_width) // 2
        y_pos = y_offset + row * (gas_height + line_height)
        
        img = gas_images[gas_name]
        name = font.render(f"{gas_name} (Score: {gas_value})", True, white)
        win.blit(img, (x_pos, y_pos))
        win.blit(name, (x_pos + (gas_width - name.get_width()) // 2, y_pos + gas_height + 5))
    
    pygame.display.update()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main_menu():
    while True:
        win.blit(background3_img, (0, 0))
        title = end_font.render("Tangkap Gas Rumah Kaca", True, white)
        start_button = font.render("Start Game", True, white)
        description_button = font.render("Game Description", True, white)

        title_x = win_width // 2 - title.get_width() // 2
        start_x = win_width // 2 - start_button.get_width() // 2
        desc_x = win_width // 2 - description_button.get_width() // 2

        title_y = win_height // 3 - title.get_height() // 2
        start_y = win_height // 2 - start_button.get_height() // 2
        desc_y = win_height // 2 + description_button.get_height()

        win.blit(title, (title_x, title_y))
        win.blit(start_button, (start_x, start_y))
        win.blit(description_button, (desc_x, desc_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_x <= mouse_x <= start_x + start_button.get_width() and start_y <= mouse_y <= start_y + start_button.get_height():
                    return
                if desc_x <= mouse_x <= desc_x + description_button.get_width() and desc_y <= mouse_y <= desc_y + description_button.get_height():
                    game_description()

# List of gases
gases = []

# Gas types and values
gas_types = {
    "CO2": 6,
    "CH4": 5,
    "N2O": 4,
    "CFC": 3,
    "SO2": 2,
    "NO": 1,
    "renewable": -5,
    "tree": -4,
    "recycle": -3,
    "regulation": -2
}

# Proportions of greenhouse gases vs non-greenhouse gases
greenhouse_gas_types = ["CO2", "CH4", "N2O", "CFC", "SO2", "NO"]
non_greenhouse_gas_types = ["renewable", "tree", "recycle", "regulation"]

# Font for score
font = pygame.font.SysFont('Arial', 24)
end_font = pygame.font.SysFont('Arial', 48)

# Main function
async def main():
    global player_x, player_y, score  # Declare global variables

    main_menu()

    # Start the music
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    run = True
    global start_time
    start_time = time.time()
    game_duration = 60  # Game lasts for 1 minute

    while run:
        clock.tick(fps)
        await asyncio.sleep(0)  # Yield control to the event loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < win_width - player_width:
            player_x += player_speed

        # Create gas randomly
        if random.randint(1, 30) == 1:
            x = random.randint(0, win_width - gas_width)
            if random.random() < 0.75:  # 75% greenhouse gases, 25% non-greenhouse gases
                type = random.choice(greenhouse_gas_types)
            else:
                type = random.choice(non_greenhouse_gas_types)
            value = gas_types[type]
            gases.append(Gas(x, 0, type, value))

        # Move gas and check if captured
        for gas in gases[:]:
            gas.move()
            if gas.y > win_height:
                gases.remove(gas)
            if player_x < gas.x + gas_width and player_x + player_width > gas.x and player_y < gas.y + gas_height and player_y + player_height > gas.y:
                score += gas.value
                gases.remove(gas)
                if score >= 100:  # End game if score reaches 100
                    end_text = 'SUPERHOT'
                    run = False
                elif score <= 0:  # End game if score reaches 0
                    end_text = 'SUPERCOLD'
                    run = False

        # End game after 1 minute
        if time.time() - start_time >= game_duration:
            run = False
            end_text = f'Waktu Habis! Skor Akhir: {score}'
            if 40 <= score <= 60:
                end_text += ' Anda berhasil menjaga bumi.'
            elif score > 60:
                end_text += ' SuperHot!'
            elif score < 40:
                end_text += ' SuperCold!'

        redraw_window(start_time, game_duration)

    # Stop the music when the game ends
    pygame.mixer.music.stop()

    # Display end message for 5 seconds
    end_run = True
    end_start_time = time.time()
    while end_run:
        clock.tick(fps)
        await asyncio.sleep(0)  # Yield control to the event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_run = False
        if time.time() - end_start_time > 5:
            end_run = False
        win.fill(white)
        
        end_text_lines = []
        words = end_text.split()
        current_line = words[0]
        
        for word in words[1:]:
            if end_font.size(current_line + " " + word)[0] > win_width - 20:
                end_text_lines.append(current_line)
                current_line = word
            else:
                current_line += " " + word
        end_text_lines.append(current_line)
        
        y_offset = win_height // 2 - (len(end_text_lines) * end_font.get_height()) // 2
        for line in end_text_lines:
            color = black
            if 'SUPERHOT' in end_text:
                color = red
            elif 'SUPERCOLD' in end_text:
                color = blue
            end_text_rendered = end_font.render(line, True, color)
            win.blit(end_text_rendered, (win_width // 2 - end_text_rendered.get_width() // 2, y_offset))
            y_offset += end_font.get_height()
        
        pygame.display.update()

    pygame.quit()

# Run the game
asyncio.run(main())
