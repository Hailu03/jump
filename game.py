import pygame
pygame.init()

# Variables
SCREENWIDTH = 840
SCREENHEIGHT = 600
tile_size = 60
WHITE = (255,255,255)
BLACK =(0,0,0)
GRAVITY = 0.75
FPS = 60
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
fpsclock = pygame.time.Clock()
sun_img = pygame.image.load('sun.png')
bg_img = pygame.image.load('sky.png')

def game_display():
    #define colours
    white = (255, 255, 255)
    blue = (0, 0, 255)
    #define font
    font = pygame.font.SysFont('Bauhaus 93', 70)
    font_score = pygame.font.SysFont('Bauhaus 93', 30)
    game_over = 0
    #load images
    restart_img = pygame.image.load('restart_btn.png')

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def draw(self):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            #draw button
            screen.blit(self.image, self.rect)

            return action

    # platform
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, move_x, move_y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('platform.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_counter = 0
            self.move_direction = 1
            self.move_x = move_x
            self.move_y = move_y

        def update(self):
            self.rect.x += self.move_direction * self.move_x
            self.rect.y += self.move_direction * self.move_y
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1
    platform_group = pygame.sprite.Group()

    # Player
    class Player():
        def __init__(self,x,y):
            self.reset(x,y)

        def move(self,game_over):
            dx = 0 
            dy = 0
            walk_cooldown = 5
            col_thresh = 20
            if game_over == 0:
                if self.move_right:
                    dx += self.speed
                    self.flip = False

                if self.move_left:
                    dx -= self.speed
                    self.flip = True 

                if player.jump and self.in_air == False:
                    self.vel_y = -11
                    self.jump = False
                    self.in_air = True
                
                self.vel_y += GRAVITY  
                if self.vel_y > 11:
                    self.vel_y = 11
                dy += self.vel_y

                if self.x < 0:
                    self.x = 0
                if self.x > 800:
                    self.x = 800

                # check collision with 
                for tile in world.tile_list:
                    if tile[1].colliderect(self.x + dx ,self.y,self.width,self.height):
                        dx = 0
                    if tile[1].colliderect(self.x,self.y + dy,self.width,self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            print(tile[1].bottom,"-",self.rect.top)  
                            self.vel_y = 0
                        elif self.vel_y >= 0: 
                            dy = tile[1].top - self.rect.bottom
                            self.in_air = False

                #check for collision with platforms
                    for platform in platform_group:
                        #collision in the x direction
                        if platform.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                            dx = 0
                        #collision in the y direction
                        if platform.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                            #check if below platform
                            if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                                self.vel_y = 0
                                dy = platform.rect.bottom - self.rect.top 
                            #check if above platform
                            elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                                self.rect.bottom = platform.rect.top - 1
                                self.in_air = False
                                dy = 0
                            #move sideways with the platform
                            if platform.move_x != 0:
                                self.x += platform.move_direction

                # check for collision with enemies
                if pygame.sprite.spritecollide(self,blob_group,False):
                    game_over = -1
                    self.alive = False
                
                # check for collision with lava
                if pygame.sprite.spritecollide(self,lava_group,False):
                    game_over = -1
                    self.alive = False

                if game_over == -1:
                    self.change = True

                self.x += dx
                self.y += dy

                return game_over

        def update_animation(self):
            #update animation
            ANIMATION_COOLDOWN = 100
            #update image depending on current frame
            self.img = self.image_list[self.action][self.index]

            # check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.index += 1
            
            # if the animation has run out the reset back to the start
            if self.index >= len(self.image_list[self.action]):
                self.index = 0

        def update_action(self,new_action):
            # check if the new action is difference to the previous one
            if new_action != self.action:
                self.action = new_action
                self.index = 0

        def get_rect(self):
            self.rect = self.img.get_rect()
            self.rect.topleft = (self.x,self.y)

        def draw(self):
            if self.change:
                self.img = self.dead_image
                if self.y > 200:
                    self.y -= 5

            self.get_rect()
            screen.blit(pygame.transform.flip(self.img,self.flip,False),self.rect)

        def reset(self,x,y):
            self.x = x
            self.y = y
            self.speed = 3
            self.action = 0
            self.move_right = False
            self.move_left = False
            self.alive = True
            self.jump = False
            self.vel_y = 0
            self.in_air = False
            self.dead_image = pygame.image.load("thanhhai.png")
            self.change = False


            self.update_time = pygame.time.get_ticks()
            self.flip = False
            self.index = 0
            self.image_list = []

            temp_list = []
            for i in range(0,4):
                img = pygame.image.load(f"img/walk/{i}.png")
                img = pygame.transform.scale(img,(50,80))
                temp_list.append(img)
            self.image_list.append(temp_list)
            temp_list = []
            for i in range(0,1):
                img = pygame.image.load(f"img/jump/{i}.png")
                img = pygame.transform.scale(img,(50,80))
                temp_list.append(img)
            self.image_list.append(temp_list)

            self.img = self.image_list[self.action][self.index]
            self.width = self.img.get_width()
            self.height = self.img.get_height()

    player = Player(60,460)

    # Enemies
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('alien.png')
            scale = 0.7
            self.image = pygame.transform.scale(self.image,(self.image.get_width()*scale,self.image.get_height()*scale))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y + 27
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1
            
    blob_group = pygame.sprite.Group()

    # fire
    class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('lava.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    lava_group = pygame.sprite.Group()

    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('coin.png')
            self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    coin_group = pygame.sprite.Group()

    # Create the game world

    class World():
        def __init__(self,data):
            self.tile_list = []

            dirt_img = pygame.image.load('dirt.png')
            grass_img = pygame.image.load('grass.png')
            row_count = 0
            for row in data:
                col_count = 0
                for column in row:
                    if column == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        self.img_rect = img.get_rect()
                        self.img_rect.x = col_count * tile_size
                        self.img_rect.y = row_count * tile_size
                        tile = (img, self.img_rect)
                        self.tile_list.append(tile)
                    if column == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                        self.img_rect = img.get_rect()
                        self.img_rect.x = col_count * tile_size
                        self.img_rect.y = row_count * tile_size
                        tile = (img, self.img_rect)
                        self.tile_list.append(tile)
                    if column == 3:
                        blob = Enemy(col_count * tile_size, row_count * tile_size + 15) 
                        blob_group.add(blob)
                    if column == 4:
                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lava_group.add(lava)
                    if column == 5:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                        platform_group.add(platform)
                    if column == 6:
                        platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                        platform_group.add(platform)
                    if column == 7:
                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)
                            
                    col_count += 1
                row_count += 1
                print(col_count,row_count)
        
        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0],tile[1])

    world_data = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [7,0,0,0,0,0,7,0,0,0,0,0,0,0],
    [2,0,0,0,5,0,5,0,5,0,0,2,2,2],
    [1,2,2,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,7,0,3,0,0,0,0,0,0],
    [0,0,0,0,0,2,2,2,2,2,0,5,0,7],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,0,0,0,7,0,0,0,0,2,1],
    [0,0,7,2,2,0,5,5,0,2,2,2,1,1],
    [2,2,2,1,1,4,4,4,4,1,1,1,1,1],
    ]

    world = World(world_data)
    restart_button = Button(SCREENWIDTH // 2 - 40, SCREENHEIGHT // 2, restart_img)

    # Win 
    winimg = pygame.image.load("hai.png")
    winimg = pygame.transform.scale(winimg,(70,100))
    win_rect = winimg.get_rect()
    win_rect.topleft = (770,26)
    def wincondition():
        screen.blit(winimg,win_rect)

    score = 0
    x = 0

    run = True
    while run:
        screen.fill(WHITE)
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))

        world.draw()

        # player
        player.draw()

        if player.alive:
            game_over = player.move(game_over)
            # player.Collision()

            if player.move_right or player.move_left:
                player.update_animation()
                
            if player.jump:
                player.update_action(1)
            else:
                player.update_action(0)
        else:
            game_over = -1

        wincondition()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player,coin_group,True):
                score += 1

            coin_group.update()
            draw_text('Score X '+ str(score) ,font_score,white,tile_size - 45,10)

            if win_rect.colliderect(player.rect):
                pygame.draw.rect(screen,(255,0,0),(0,0,840,x))
                blob_group.empty()
                platform_group.empty()
                coin_group.empty()
                lava_group.empty()

                if x < 600:
                    x = x + 3
                if restart_button.draw():
                    game_display()
                draw_text('You win my girl',font,blue,(SCREENWIDTH//2) - 230,SCREENHEIGHT//2-89)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)

        # game_over = player.update(game_over)  
            

        lava_group.update()
        
        if game_over == -1:
            if restart_button.draw():
                player.reset(60,460)
                game_over = 0
                score = 0
                game_display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move_right = True
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                if event.key == pygame.K_SPACE:
                    player.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.move_right = False
                    player.dx = 0
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                    player.dx = 0
                if event.key == pygame.K_SPACE:
                    player.jump = False

        fpsclock.tick(FPS)
        pygame.display.update()

    pygame.quit()

def main_menu():
    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


            #draw button
            screen.blit(self.image, self.rect)

            return action
    scale = 0.6
    start_img = pygame.image.load('start_btn.png')
    start_img = pygame.transform.scale(start_img,(start_img.get_width()*scale,start_img.get_height()*scale))

    exit_img = pygame.image.load('exit_btn.png')
    exit_img = pygame.transform.scale(exit_img,(start_img.get_width()*0.8,exit_img.get_height()*0.6))
    start_button = Button(SCREENWIDTH // 2 - 190, SCREENHEIGHT // 2 - 50, start_img)
    exit_button = Button(SCREENWIDTH // 2 + 30, SCREENHEIGHT // 2- 50 , exit_img)
    run = True
    while run:
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))
        screen.fill((255,255,255))
        if exit_button.draw():
            run = False
        if start_button.draw():
            game_display()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update() 
    pygame.quit()

main_menu()
