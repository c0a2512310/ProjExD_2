import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect:pg.Rect)->tuple[bool,bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    画面内ならTrue/画面街ならFalse
    """
    yoko,tate=True,True
    if rect.left<0 or WIDTH<rect.right:
        yoko=False
    if rect.top<0 or HEIGHT<rect.bottom:
        tate=False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    width, height = 1100, 600
    width2, height2 = 700, 600
    width3, height3 = 1500, 600

    gmover = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gmover, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gmover.set_alpha(255)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    text = txt.get_rect(center=(width // 2, height // 2))
    gmover.blit(txt, text)

    cg_img = pg.image.load("fig/6.png")
    gm_rect = cg_img.get_rect(center=(width2 // 2, height2 // 2)) 
    gm_rect2 = cg_img.get_rect(center=(width3 // 2, height3 // 2))
       
    gmover.blit(cg_img, gm_rect)
    gmover.blit(cg_img, gm_rect2)
    screen.blit(gmover, [0,0])
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2：赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  # 練習2：爆弾の初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if bb_rct.colliderect(kk_rct) :
            gameover(screen)
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):# どこかしらはみ出てる
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])# 先ほどの動きをキャンセル
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2：爆弾動く
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img, bb_rct)  # 練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()