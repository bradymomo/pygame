"""
程式名稱:馬力歐接金幣
姓名:王柏之
參考程式:https://inventwithpython.com/chapter20.html 的 DODGER


規則

接到金幣加一分

碰到怪物扣一命   總共四次機會

吃到蘑菇會長大   可抵一命  次數不能累計



"""
import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 30
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 4
BADDIEMAXSPEED = 4
ADDNEWBADDIERATE = 15
ADDNEWcherry = 40
ADDNEWmushroom = 120
PLAYERMOVERATE = 5

def terminate():      #關密程式
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():   #等待案件後執行
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return
def playerHasHitmushroom(playerRect, mushroom):   #吃到香菇
    for b in mushroom:
        if playerRect.colliderect(b['rect']):
            mushroomSound.play()
            mushroom.remove(b)
            return True
    return False
def playerHasHitBaddie(playerRect, baddies):     #撞到怪獸
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            boing.play()
            baddies.remove(b)
            return True
    return False
def playerHasHitcherry(playerRect, cherry):    #吃到金幣
    for b in cherry:
        if playerRect.colliderect(b['rect']):
            pickupSound.play()
            cherry.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):    #把文字畫入視窗
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))    #畫面設定 
pygame.display.set_caption('馬力歐')
pygame.mouse.set_visible(False)


font = pygame.font.SysFont(None, 48)


mushroomSound = pygame.mixer.Sound('mushroom.wav')  #音檔匯入
jumpSound = pygame.mixer.Sound('jump.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
pickupSound = pygame.mixer.Sound('pickup.wav')
boing = pygame.mixer.Sound('boing.wav')
gamewinSound = pygame.mixer.Sound('win.wav')
pygame.mixer.music.load('back.wav')
pygame.mixer.music.set_volume(0.7)


back = pygame.image.load('back.png')              #圖片匯入及設定
back = pygame.transform.scale(back, (600, 600))
playerImage = pygame.image.load('Mario1.png')
playerImage = pygame.transform.scale(playerImage, (45, 60))
playerImage2 = pygame.image.load('Mario2.png')
playerImage2 = pygame.transform.scale(playerImage2, (45, 60))
playerRect = playerImage.get_rect()
mushroomImage = pygame.image.load('mushroom.png')
mushroomImage = pygame.transform.scale(mushroomImage, (40, 60))
baddieImage = pygame.image.load('moster.png')
cherryImage = pygame.image.load('coin.png')
cherryImage = pygame.transform.scale(cherryImage, (29, 46))

windowSurface.blit(back, [0, 0])                  #開始畫面設定
drawText('Mario', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
                           #變數設定
    dir=1
    isbig=0
    big=0
    small=0
    change=0
    jump=0
    baddies = []
    cherry = []
    mushroom=[]
    score = 0
    life = 3
    win=0
    level=0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False     #起始方向皆為FLASE
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    cherryAddCounter = 0
    mushroomAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    tt=0
    qq=0
    while True: 
        """score += 1 # increase score"""
        if score%5==0 and qq==0:               #關卡設定  五分一關  會加速
            baddies = []
            cherry = []
            BADDIEMINSPEED +=1 
            BADDIEMAXSPEED +=1
            
            windowSurface.fill(BACKGROUNDCOLOR)
            windowSurface.blit(back, [0, 0])
            
            level+=1
            qq=1
            if level==5:                                #獲勝
               windowSurface.fill(BACKGROUNDCOLOR)
               windowSurface.blit(back, [0, 0])
               drawText('you win!' , font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 3))
               pygame.display.update() 
               win=1
               break
            else:
               drawText('level %s' % (level), font, windowSurface, (WINDOWWIDTH / 2.5), (WINDOWHEIGHT / 3))
               pygame.display.update()
               pygame.time.wait(3000)
               windowSurface.fill(BACKGROUNDCOLOR)
               windowSurface.blit(back, [0, 0])
        if score%5==1:                      
            qq=0
        
        for event in pygame.event.get():               #獲取與判斷按鍵
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                    dir=2
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                    dir=1
                if (event.key == K_UP or event.key == ord('w')) and jump==0:
                    jump=50
                

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    
                if event.key == ord('x'):
                    slowCheat = False
                    
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                
                

           

        
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
            cherryAddCounter += 1
            mushroomAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:    #怪物生成
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }
            baddies.append(newBaddie)
        if cherryAddCounter == ADDNEWcherry:     #金幣生成
            cherryAddCounter = 0
            cherrySize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newcherry = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(cherryImage, (baddieSize, baddieSize)),
                            }
    
            cherry.append(newcherry)
            
            
            
        if mushroomAddCounter == ADDNEWmushroom:      #蘑菇生成
            mushroomAddCounter = 0
            mushroomSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newmushroom = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(mushroomImage, (baddieSize, baddieSize)),
                            }
    
            mushroom.append(newmushroom)
        
        
        if moveLeft and playerRect.left > 0:           #判斷移動方向
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and jump> 0:
            if jump==50:
                jumpSound.play()
            if jump>25:
                playerRect.move_ip(0, -(jump-25)/3)    
            else:
                playerRect.move_ip(0, 8.8-(jump/3))
            jump -=1
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        
        for b in baddies:                                     #怪物落下
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)
        for b in cherry:                              #金幣落下
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in cherry[:]:
            if b['rect'].top > WINDOWHEIGHT:
               cherry.remove(b)
        
        
        for b in  mushroom:                             #蘑菇落下
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in  mushroom[:]:
            if b['rect'].top > WINDOWHEIGHT:
                mushroom.remove(b)
        

        
        windowSurface.fill(BACKGROUNDCOLOR)       #先洗掉畫面
        windowSurface.blit(back, [0, 0])          #再顯示背景
        
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)               #分數  最高分  生命  顯示
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Chance: %s' % (life), font, windowSurface, 10, 80)
        
        
        
        if dir==2 :                                                                 #顯示玩家
            windowSurface.blit(playerImage2, playerRect)
        else :
            windowSurface.blit(playerImage, playerRect)
        
        
        for b in baddies:                                                        #顯示其他物件
            windowSurface.blit(b['surface'], b['rect'])
        for b in cherry:
            windowSurface.blit(b['surface'], b['rect'])
        for b in mushroom:
            windowSurface.blit(b['surface'], b['rect'])
        
        pygame.display.update()

        
        if playerHasHitBaddie(playerRect, baddies):                          #撞到怪物函式
            
            if life==0:
                break
            if isbig==1:
                small=50
                
            else:    
                life-=1
        if small<=50 and small!=0:                                         #縮小
            
            if small%3==0:
                playerImage = pygame.transform.scale(playerImage, (40+15, 60+20))
                playerImage2 = pygame.transform.scale(playerImage2, (40+15, 60+20))
            else:
                playerImage = pygame.transform.scale(playerImage, (40, 60))
                playerImage2 = pygame.transform.scale(playerImage2, (40, 60))
            if small==1:  
                ip=playerRect[0]
                playerRect=playerImage.get_rect()
                playerRect.topleft = (ip,WINDOWHEIGHT- 50 )
                isbig==0
            small-=1
                
        if playerHasHitcherry(playerRect, cherry):             #撞到金幣函式加分
            score+=1
            if score > topScore:
                topScore = score 
            """break"""
        if playerHasHitmushroom(playerRect, mushroom):          #撞到蘑菇函式
            isbig=1
            big=5
            change=50
            ip=playerRect[0]
            playerRect.topleft = (ip,WINDOWHEIGHT-(big*4)- 50 )
        if change<=50 and change!=0:                                #變大
            
            if change%3==0:
                playerImage = pygame.transform.scale(playerImage, (40+(big-5)*3, 60+(big-5)*4))
                playerImage2 = pygame.transform.scale(playerImage2, (40+(big-5)*3, 60+(big-5)*4))
            else:
                playerImage = pygame.transform.scale(playerImage, (40+big*3, 60+big*4))
                playerImage2 = pygame.transform.scale(playerImage2, (40+big*3, 60+big*4))
            if change==1:  
                ip=playerRect[0]
                playerRect=playerImage.get_rect()
                playerRect.topleft = (ip,WINDOWHEIGHT-(big*4)- 50 )
            change-=1
        mainClock.tick(FPS)

    
    pygame.mixer.music.stop()
    if win!=0:                                                              #勝利函式
        gamewinSound.play()
        waitForPlayerToPressKey()
        terminate()
    if win==0:                                                              #失敗函式
        gameOverSound.play()
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press a key to leave.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()
        terminate()
        gameOverSound.stop()
    