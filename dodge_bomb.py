import random  #issue1
import sys

import pygame as pg

# 練習4
delta = {
        pg.K_UP:(0, -1),
        pg.K_DOWN:(0, +1),
        pg.K_LEFT:(-1, 0),
        pg.K_RIGHT:(+1, 0),
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真理値タプルを返す
    引数１ scr_rct : 画面Surfaceのrect
    引数２ obj_rct : オブジェクト（爆弾、こうかとん）Surfaceのrect
    戻り値 : 横方向、縦方向のはみ出し判定結果（画面内: True/画面外: False）
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")  
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_r = pg.transform.flip(kk_img, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    tmr = 0
    bb_img = pg.Surface((20, 20))  # 練習1
    pg.draw.circle(bb_img, (255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    x, y = random.randint(1, 100), random.randint(1,900)  # 練習2とこうかとん即死対策
    #screen.blit(bb_img, [x, y])
    vx, vy = +1, +1
    bb_rct = bb_img.get_rect()
    bb_rct.center = x, y
# 追加機能1
    kadai1 = {
            (0, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
            (-1, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
            (-1, +1):pg.transform.rotozoom(kk_img, 45, 1.0),
            (0, +1):pg.transform.rotozoom(kk_img, 90, 1.0),
            (-1, -1):pg.transform.rotozoom(kk_img,-45,1.0),
            (0, -1):pg.transform.rotozoom(kk_img_r, 90, 1.0),
            (+1, -1):pg.transform.rotozoom(kk_img_r, 45, 1.0),
            (+1, 0):pg.transform.rotozoom(kk_img_r,0, 1.0),
            (+1, +1):pg.transform.rotozoom(kk_img_r,-45, 1.0),
            (0, +1):pg.transform.rotozoom(kk_img_r,-90, 1.0),
             }
    
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
        tmr += 1
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():  #　練習3
            if key_lst[k]:
                kk_rct.move_ip(mv)
        tup_lst = []  # 追加機能1
        for key, tup in delta.items():
            if key_lst[key]:
                tup_lst.append(tup)
        tu_x = 0
        tu_y = 0
        for tu in tup_lst:
            tu_x += tu[0]
            tu_y += tu[1]
        kk_img = kadai1[tu_x,tu_y]
        if check_bound(screen.get_rect(),kk_rct) != (True, True):  # 練習5
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0],-mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)   
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1 
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):  #　練習6
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()