from pygame import *

'''Необходимые классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #вместе 55,55 - параметры
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = width
        self.height = height
        self.player_image = player_image

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def standart_size(self, height):
        self.height = height
        self.image = transform.scale(image.load(self.player_image), (self.width, self.height))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.height:
           self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.height:
           self.rect.y += self.speed
    def change_size(self):
        self.height *= 0.9
        self.image = transform.scale(image.load(self.player_image), (self.width, int(self.height)))
        
class Button():
    def __init__(self, button_x, button_y, button_width, button_height,button_color,button_text,button_text_size):
        self.rect = Rect(button_x,button_y, button_width, button_height)
        self.button_color = button_color
        self.button_text = font.SysFont('verdana', button_text_size).render(button_text, True, Black)
    def fill(self):
        draw.rect(window,self.button_color,self.rect)
        window.blit(self.button_text, (self.rect.x + 20, self.rect.y + 20))
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
Black = (0,0,0)
bc = (187,65,47)
win_width = 900
win_height = 600
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги, отвечающие за состояние игры
game = True
finish = True
clock = time.Clock()
FPS = 60
racket_width = 50
racket_height = 250

#создания мяча и ракетки   
racket1 = Player('redracket.png', 30, win_height/2 - racket_height/2, 4, racket_width, racket_height) 
racket2 = Player('greenracket.png', win_width - racket_width - 30, win_height/2 - racket_height/2, 4, racket_width, racket_height)
ball = GameSprite('tenis_ball.png', win_width/2, win_height/2, 4, 50, 50)

font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3
pl_1 = 0
pl_2 = 0
win_score = 3
click_x = 0
click_y = 0

str_button_width = 200
str_button_height = 100
start_button = Button(win_width / 2 - str_button_width / 2,win_height / 2 - str_button_height / 2,str_button_width,str_button_height,bc, "play", 46)



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == MOUSEBUTTONDOWN:
            click_x,click_y = e.pos
  
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1.2
            speed_y *= 1
            if sprite.collide_rect(racket1, ball):
                racket1.change_size()
            if sprite.collide_rect(racket2, ball):
                racket2.change_size()

        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            pl_1 += 1
            ball.rect.x = win_width/2 - 25
            ball.rect.x = win_height/2 - 25
            speed_x *= -1
        if ball.rect.x > win_width:
            pl_2 += 1
            ball.rect.x = win_width/2 - 25
            ball.rect.x = win_height/2 - 25
            speed_x *= -1
            racket1.standart_size(racket_height)
            racket2.standart_size(racket_height)

        st = font.render(str(pl_1) + " : " + str(pl_2),1,(0,0,0))
        window.blit(st, (win_width/2 - 50, win_height - 500))

        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if pl_1 >= win_score or pl_2 >= win_score:
            if pl_1 >= win_score:
                window.blit(lose1, (win_width/2 - 150, win_height/2))
            elif pl_2 >= win_score:
                window.blit(lose2, (win_width/2 - 150, win_height/2))

            ball.rect.x = win_width/2 - 25
            ball.rect.y = win_height/2 - 25
            finish = True
            game_over = True


        racket1.reset()
        racket2.reset()
        ball.reset()


    else:
        if start_button.collidepoint(click_x,click_y):
            pl_1 = 0
            pl_2 = 0
            click_x = 0
            click_y = 0
            racket1.standart_size(racket_height)
            racket2.standart_size(racket_height)
            finish = False
        else:
            start_button.fill()

    display.update()
    clock.tick(FPS)
