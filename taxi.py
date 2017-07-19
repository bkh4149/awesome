
# coding: utf-8
#2017/07/16 ver2 ライン上を動くようにする

#2017/07/15　タクシーをクラスで生成、スプライトを使って大量に画面に出す
#	背景が透明な画像の作成　by　gimp　実に簡単　
#　	基本は４番めのαレイヤーを作って
#　　　　　使うのだが、白を透明にする場合、それをやる必要さえない
#	出力はpng
#2017/07/14　都市を描く



""" taxi．py """ 
import sys 
import pygame 
from pygame.locals import *
#from pygame.locals import QUIT, Rect

SCR_RECT = Rect(0, 0, 800, 600)

class taxiSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)



pygame.init()
#SURFACE = pygame.display.set_mode(( 800, 600)) 
FPSCLOCK = pygame.time.Clock()

name=('青木','b','c','d','e','f','g','h','i','j')
plc=[[200, 200],[100, 300],[50, 500],[400, 100],[400, 300],[350, 500],[700, 250],[600, 350],[500, 450], [700, 500]]

tbl=[
[0,1,-1,4,3,-1,-1,-1,-1,-1],
[1,0,3,-1,-1,-1,-1,-1,-1,-1],
[-1,3,0,-1,-1,2,-1,-1,-1,-1],
[4,-1,-1,0,-1,-1,4,3,-1,-1],
[3,-1,-1,-1,0,3,-1,3,3,-1],
[-1,-1,2,-1,3,0,-1,-1,3,-1],
[-1,-1,-1,4,-1,-1,0,2,-1,5],
[-1,-1,-1,3,3,-1,2,0,3,3],
[-1,-1,-1,-1,3,3,-1,3,0,4],
[-1,-1,-1,-1,-1,-1,5,3,4,0],
]


#myfont = pygame.font.Font("myfont.ttf", 16)
myfont = pygame.font.SysFont( None, 36) 

def main():
    """ main routine """
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("taxi game")
    taxi=[]
    total=10

    for j in range (0,total):	
       taxi.append(taxiSprite("car.png", j, j, j, j))

    clock = pygame.time.Clock()

    while True:
    	for event in pygame.event.get(): 
    		if event. type == QUIT: 
    			pygame. quit() 
    			sys. exit()
    
    	screen.fill(( 255, 255, 255))
    
    	#red
    	pygame. draw. circle( screen, (255, 0, 0), (50, 50), 20) 
    
    	#更新
    	for j in range (0,total):	
    	  taxi[j].update()
    
    	#描画
    	for j in range (0,total):	
    	  taxi[j].draw(screen)
    	pygame.display.update()
    	for i in range (0,10):

    		pygame. draw. circle( screen,(0,0,255),plc[i], 30,10)
    		tx = myfont.render(name[i], False, (0,0,0))

    		x=plc[i][0]-10
    		y=plc[i][1]-10
    		screen.blit(tx,(x,y))
    		
    		for j in range (0,10):
    		  if tbl[i][j]>0:
    		    pygame.draw.line(screen,(0,0,0),plc[i],plc[j])
    
    
    	pygame. display. update() 
    	FPSCLOCK. tick( 3) 
    
if __name__ == '__main__': main()

