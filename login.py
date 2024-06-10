import pygame
import sys
import os
import requests as req
import random

# Errors
'''
Error 0 Login Crend
Error 1 Reg Collision
'''
errors=[0]*10

# Load images
whale_image = pygame.image.load('whale.png')
whale_image = pygame.transform.scale(whale_image, (50, 50))

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗的大小
screen = pygame.display.set_mode((700, 900))
pygame.display.set_caption("Wha!quarim")

# 設定顏色
background_color = (0, 170, 255)
button_color = (255, 255, 255)
button_hover_color = (200, 200, 200)
text_color = (0, 0, 0)
input_box_color = (255, 255, 255)
input_text_color = (0, 0, 0)

# 字型設置
logo_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 36)

# 按鈕設置
button_width = 200
button_height = 60
button_margin = 20

# 登入按鈕位置
login_button_rect = pygame.Rect(
    (screen.get_width() // 2 - button_width // 2,
     screen.get_height() // 2 - button_height // 2 - button_height - button_margin),
    (button_width, button_height)
)

# 註冊按鈕位置
register_button_rect = pygame.Rect(
    (screen.get_width() // 2 - button_width // 2,
     screen.get_height() // 2 - button_height // 2 + button_height + button_margin),
    (button_width, button_height)
)

# 提交按鈕位置
submit_button_rect = pygame.Rect(
    (screen.get_width() // 2 - button_width // 2,
     screen.get_height() // 2 + 2 * button_height + 3 * button_margin),
    (button_width, button_height)
)

back_button_rect = pygame.Rect(
    (screen.get_width() // 2 - button_width // 2,
     screen.get_height() // 2 + 3 * button_height + 4 * button_margin),
    (button_width, button_height)
)

# 輸入框設置
input_box_width = 300
input_box_height = 50
input_box_margin = 20

username_input_box = pygame.Rect(
    (screen.get_width() // 2 - input_box_width // 2, screen.get_height() // 2 - 3 * input_box_height),
    (input_box_width, input_box_height)
)
password_input_box = pygame.Rect(
    (screen.get_width() // 2 - input_box_width // 2, screen.get_height() // 2 - input_box_height // 2),
    (input_box_width, input_box_height)
)
ip_input_box = pygame.Rect(
    (screen.get_width() // 2 - input_box_width // 2, screen.get_height() // 2 + 2 * input_box_height),
    (input_box_width, input_box_height)
)

# 狀態變量
show_login_form = False
show_register_form = False


# User attributes
user_name = "Player1"
user_money = 1000
user_level = 5

# Button settings
button_width = 160
button_height = 60

# Navigation bar buttons
nav_buttons = ["Purchase", "Aquarium", "Breeding", "Pokedex"]
nav_button_rects = [pygame.Rect((i * 175, 150), (175, 60)) for i in range(4)]

# Feed buttons
feed_button_rects = [pygame.Rect((i * 50, 800), (50, 50)) for i in range(5)]

# Fish settings
fish_image = pygame.image.load('whale.png')
fish_image = pygame.transform.scale(fish_image, (50, 50))
fish_x = 350
fish_y = 450
fish_speed = 2
fish_direction = -1

# Function to draw user attributes
def draw_user_attributes():
    pygame.draw.rect(screen, header_color, (0, 0, 700, 150))
    screen.blit(whale_image, (20, 20))
    name_text = text_font.render(f"Name: {user_name}", True, text_color)
    money_text = text_font.render(f"Money: ${user_money}", True, text_color)
    level_text = text_font.render(f"Level: {user_level}", True, text_color)
    screen.blit(name_text, (80, 20))
    screen.blit(money_text, (80, 60))
    screen.blit(level_text, (80, 100))

# Function to draw the fish
def draw_fish():
    global fish_x, fish_y, fish_direction, fish_image
    fish_x += fish_speed * fish_direction
    if fish_x <= 0 or fish_x >= 650:
        fish_direction *= -1
        fish_y += random.randint(-20, 20)
        if fish_y < 200:
            fish_y = 200
        elif fish_y > 650:
            fish_y = 650
        fish_image = pygame.transform.flip(fish_image, True, False)
    screen.blit(fish_image, (fish_x, fish_y))


# 輸入框內容
if os.path.exists('log.txt'):
    log=open('log.txt', 'r')
    log=log.read().split('\n')
    username_text=log[0]
    password_text=log[1]
    ip_text=log[2]
else:
    username_text = ''
    password_text = ''
    ip_text = ''

token=''

active_input = None

# 遊戲主頁介面函數
def draw_main_menu():
    screen.fill(background_color)
    
    # 繪製 LOGO
    logo_text = logo_font.render("Wha!quarim", True, text_color)
    screen.blit(logo_text, (screen.get_width() // 2 - logo_text.get_width() // 2, 100))
    
    # 繪製按鈕
    draw_button(login_button_rect, "Login")
    draw_button(register_button_rect, "Register")
    
    pygame.display.flip()

# 登入表單介面函數
def draw_login_form():
    screen.fill(background_color)
    if errors[0]:
        alert_text = text_font.render("Wrong Crenditial", True, (120, 20, 0))
        screen.blit(alert_text, (screen.get_width() // 2 - alert_text.get_width() // 2, 850))

    # 繪製 LOGO
    logo_text = logo_font.render("Login", True, text_color)
    screen.blit(logo_text, (screen.get_width() // 2 - logo_text.get_width() // 2, 200))
        
    # 繪製輸入框
    draw_input_box(username_input_box, username_text, "Username")
    draw_input_box(password_input_box, '*'*len(password_text), "Password")
    draw_input_box(ip_input_box, ip_text, "Game Server IP")
    
    # 繪製提交按鈕
    draw_button(submit_button_rect, "Submit")
    draw_button(back_button_rect, "Back")

    pygame.display.flip()

def draw_register_form():
    screen.fill(background_color)
    if errors[1]:
        alert_text = text_font.render("Username already been used", True, (120, 20, 0))
        screen.blit(alert_text, (screen.get_width() // 2 - alert_text.get_width() // 2, 850))

    # 繪製 LOGO
    logo_text = logo_font.render("Register", True, text_color)
    screen.blit(logo_text, (screen.get_width() // 2 - logo_text.get_width() // 2, 200))
        
    # 繪製輸入框
    draw_input_box(username_input_box, username_text, "Username")
    draw_input_box(password_input_box, '*'*len(password_text), "Password")
    draw_input_box(ip_input_box, ip_text, "Game Server IP")
    
    # 繪製提交按鈕
    draw_button(submit_button_rect, "Submit")
    draw_button(back_button_rect, "Back")

    pygame.display.flip()

# 繪製按鈕函數
def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = button_hover_color
    else:
        color = button_color
        
    pygame.draw.rect(screen, color, rect)
    button_text = button_font.render(text, True, text_color)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2,
                              rect.y + (rect.height - button_text.get_height()) // 2))

# 繪製輸入框函數
def draw_input_box(rect, text, placeholder):
    pygame.draw.rect(screen, input_box_color, rect)
    if text:
        input_text = input_font.render(text, True, input_text_color)
    else:
        input_text = input_font.render(placeholder, True, input_text_color)
    screen.blit(input_text, (rect.x + 10, rect.y + (rect.height - input_text.get_height()) // 2))

# 遊戲主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if token:
                req.get(ip_text+f'/api/userlogout/{token}')
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_login_form:
                if username_input_box.collidepoint(event.pos):
                    active_input = 'username'
                elif password_input_box.collidepoint(event.pos):
                    active_input = 'password'
                elif ip_input_box.collidepoint(event.pos):
                    active_input = 'ip'
                elif submit_button_rect.collidepoint(event.pos):
                    web=req.get(ip_text+f'/api/login/username/{username_text}/password/{password_text}')
                    token=web.text
                    temp=username_text+'\n'+password_text+'\n'+ip_text
                    f=open('log.txt', 'w')
                    f.write(temp)
                    f.close()
                    print(token)
                    if token == 'Wrong password or username':
                        errors[0]=1
                    else:
                        errors[0]=0
                        running=False
                elif back_button_rect.collidepoint(event.pos):
                    show_login_form=False
                else:
                    active_input = None
            elif show_register_form:
                if username_input_box.collidepoint(event.pos):
                    active_input = 'username'
                elif password_input_box.collidepoint(event.pos):
                    active_input = 'password'
                elif ip_input_box.collidepoint(event.pos):
                    active_input = 'ip'
                elif submit_button_rect.collidepoint(event.pos):
                    web=req.get(ip_text+f'/api/reg/username/{username_text}/password/{password_text}')
                    token=web.text
                    temp=username_text+'\n'+password_text+'\n'+ip_text
                    f=open('log.txt', 'w')
                    f.write(temp)
                    f.close()
                    print(token)
                    if token == 'Username already been used':
                        print(1)
                        errors[1]=1
                    else:
                        errors[1]=0
                elif back_button_rect.collidepoint(event.pos):
                    show_register_form=False
                else:
                    active_input = None

            else:
                if login_button_rect.collidepoint(event.pos):
                    show_login_form = True
                elif register_button_rect.collidepoint(event.pos):
                    show_register_form = True

        elif event.type == pygame.KEYDOWN and show_login_form:
            if active_input == 'username':
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                else:
                    username_text += event.unicode
            elif active_input == 'password':
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                else:
                    password_text += event.unicode
            elif active_input == 'ip':
                if event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                else:
                    ip_text += event.unicode

        elif event.type == pygame.KEYDOWN and show_register_form:
            if active_input == 'username':
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                else:
                    username_text += event.unicode
            elif active_input == 'password':
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                else:
                    password_text += event.unicode
            elif active_input == 'ip':
                if event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                else:
                    ip_text += event.unicode

    if show_login_form:
        draw_login_form()
    elif show_register_form:
        draw_register_form()
    else:
        draw_main_menu()

pygame.quit()
if token:
    os.system(f'python3 game.py {token} {ip_text}')
sys.exit()
