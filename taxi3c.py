
# coding: utf-8
#2017/07/17 ver4

#2017/07/17 ver3d
#  目的地に到着したらランダムで次の目的地を選び、そこに移動させたい
#  taxiオブジェクトは速度、vx,vyの形で内部変数を持っている
#　移動の方向はvx,vyを設定しなおせばいいだけなのだが
#　変数を勝手に増やせないので意外と厄介かも
#　taxiオブジェクトの外部から目的地に到着したことを知らせるべきなのか
#　taxiオブジェクト内部で目的地に到着したことを検知スべきなのか


#2017/07/17 ver3c 
#  	とりあえず意図した動きJないんだが面白いのでとっておく
#  	プログラムの意味を理解するためコメント付けまくり

#2017/07/16 ver3 ライン上を動くようにする
#　多分周辺のラインをサーチする必要がある
#　衝突判定　http://aidiary.hatenablog.com/entry/20080811/1281190612
#  一番シンプルなやり方　A,Bの差分をN等分するだけ　update2 いまいち


#2017/07/16 ver2 都市の描画を安定させたい
#　現状、都市とタクシーを毎回出しているだが、都市は最初に一度出せばいい
#   実際やってみたらタクシーの上書きで都市が消えてしまった
#　　やはり毎回書かないとダメみたい
#　でもタクシーと都市を二回描画しているのでチカチカする
#　　　とりあえず都市の描画を関数化し、両方合わせて最後に一回描画することにした
#		toshi(screen)

#2017/07/15　タクシーをクラスで生成、スプライトを使って大量に画面に出す
#	背景が透明な画像の作成　by　gimp　実に簡単　
#　	基本は４番めのαレイヤーを作って
#　　　　　使うのだが、白を透明にする場合、それをやる必要さえない
#	出力はpng

#2017/07/14　都市だけを描く



""" taxi．py """ 
import sys 
import pygame 
from pygame.locals import *
#from pygame.locals import QUIT, Rect

SCR_RECT = Rect(0, 0, 800, 600)

#タクシーオブジェクト
#()内は親のクラス、引数じゃないよ
class taxiSprite(pygame.sprite.Sprite):


    #コンストラクタ
    def __init__(self, filename, x, y, vx, vy):

        #Spriteを継承する場合は、__init__()（コンストラクタ）で
        #pygame.sprite.Sprite.__init__()を呼び出す必要があります。
        #意味不明　2017/07/17　とりあえずいれておく
        #親のコンストラクを呼んでいるようだが...
        pygame.sprite.Sprite.__init__(self)

        #クラス内部のself.imageオブジェクトに画像を読み込んでいる
        self.image = pygame.image.load(filename).convert_alpha()


        #幅と高さはimageオブジェクトから取得
        width = self.image.get_width()
        height = self.image.get_height()

        #RectというのはRect型のオブジェクト
        #pythonは代入される側は右辺のオブジェクトになる、つまりself.rectはRect型
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.ct=20

    #位置を計算
    def update(self):
        # Rectオブジェクトの描写位置を移動させます
        self.rect.move_ip(self.vx, self.vy)

        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)

    #位置を計算
    def update2(self):

        # Rectオブジェクトの描写位置を移動させます
        self.rect.move_ip(self.vx, self.vy)

        #目的地に到着したら、vx,vyを設定し直す

        self.vx = +2
        if self.ct<0:
           selt.ct=20
           self.vx = -2


        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)

    #描画
    def draw(self, screen):
        #Surface.blit - 画像を他の画像上に描写します。
        #引数（source, dest, area=None, special_flags = 0): return Rect
        #dest引数を使用して描写位置を設定することができます。
        #dest値はソース画像の左上隅が置かれる(x座標,y座標)を表します。
        #screen.blit（元画像,位置）　ってことだろう
        screen.blit(self.image, self.rect)


pygame.init()
#SURFACE = pygame.display.set_mode(( 800, 600)) 
FPSCLOCK = pygame.time.Clock()

#都市の初期設定
name=('青木','b','c','d','e','f','g','h','i','j')
plc=[[200, 200],[100, 300],[50, 500],[400, 100],[400, 300],[350, 500],[700, 250],[600, 350],[500, 450], [700, 500]]

#都市間の距離　-1は直接つながってないことを表す
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


#都市の描画
def toshi(screen):
    for i in range (0,10):

    	pygame. draw. circle( screen,(0,0,255),plc[i], 30,10)
    	tx = myfont.render(name[i], False, (0,0,0))

    	x=plc[i][0]-10
    	y=plc[i][1]-10
    	screen.blit(tx,(x,y))
    		
    	for j in range (0,10):
    	  if tbl[i][j]>0:
    	    pygame.draw.line(screen,(0,0,0),plc[i],plc[j])

#メイン　ここからスタート
#メイン　ここからスタート
def main():
    """ main routine """
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("taxi game")
    taxi=[]
    total=10

    #タクシーインスタンスをtotal台生成する
    for j in range (0,total):
       taxi.append(taxiSprite("car.png", j, j, j, j))
    clock = pygame.time.Clock()


    #メインのループ
    #メインのループ
    while True:

    	#スクリーン右上のボタンおした時終了
    	for event in pygame.event.get(): 
    		if event. type == QUIT: 
    			pygame. quit() 
    			sys. exit()
    
    	screen.fill(( 255, 255, 255))
    
    	#タクシー位置更新
    	for j in range (0,total):	
    	  taxi[j].update2()
#    	  taxi[j].update()
    
    	#タクシー描画
    	for j in range (0,total):	
    	  taxi[j].draw(screen)

    	#都市描画
    	toshi(screen)

    	pygame.display.update()


if __name__ == '__main__': main()

