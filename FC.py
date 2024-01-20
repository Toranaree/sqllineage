import pygame as pg
from time import time
from random import randint
pg.init()



class Main:
    def __init__(self):
        self.title = 'OOP Fast Clicker v1.0'
        self.w = 500
        self.h = 300
        self.FPS = 10
        self.time_limit = 10
        self.mode = 0
        self.score = 0
        self.score_win = 5
        self.setup()

    def setup(self):
        self.screen = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.events_work = []
        self.time_start = 0
        self.colors = {'back': (177, 194, 190),
                        'back_win': (202, 234, 222),
                        'back_lose': (201, 153, 161),
                        'card_normal': (244, 219, 210),
                        'card_right': (185, 227, 211),
                        'card_wrong': (201, 153, 161),
                        'card_outline': (234,184,166),
                        'text': (110, 68, 53),
                        'text_win' : (98, 193, 157),
                        'text_lose' : (133, 26, 45),
                        }
        self.textes = {'win': 'you WIN!',
                       'lose': 'you LOSE!',
                       'time': 'Time:',
                       'score': 'Score:',
                       'yourScore': 'Your Score:',
                       }

    def tick(self):
        self.clock.tick(self.FPS)

    def start(self):
        self.time_start = time()

    def timer(self):
        return round(time() - self.time_start, 1)
    
    def check_rule(self):
        if self.timer() > self.time_limit:
            if self.score >= self.score_win:
                self.mode = 1
            else:
                self.mode = 2

    def events(self):
        events_raw = list(pg.event.get())
        if len(events_raw) != 0:
            self.events_work = list(events_raw)
        return self.events_work

    def events_reset(self):
        self.events_work.clear()

    def isRun(self):
        for e in self.events():
            if e.type == pg.QUIT:
                return False
        return True



class Label:
    def __init__(self, game, x, y, font_size):
        self.main = game
        self.x = x
        self.y = y
        self.font = pg.font.SysFont(None, font_size)
        self.text = ' '
        self.text_color = self.main.colors['text']
    
    def update(self):
        surface = self.font.render(self.text, True, self.text_color)
        self.main.screen.blit(surface, (self.x, self.y))



class Card(Label):
    def __init__(self, game, x, y):
        super().__init__(game, x + 8, y + 55, 28)
        self.rect = pg.Rect(x, y, 75, 125)
        self.color = self.main.colors['card_normal']

    def update(self):
        pg.draw.rect(self.main.screen, self.color, self.rect)
        pg.draw.rect(self.main.screen, self.main.colors['card_outline'], self.rect, 5)
        super().update()



class Cards:
    def __init__(self, game, card_class, card_map):
        self.game = game
        self.card_time = 10
        self.card_time_now = 0
        self.card = 0
        self.card_list = []
        self.card_list_len = len(card_map)
        for i in range(self.card_list_len):
            self.card_list.append(card_class(self.game, card_map[i][0], card_map[i][1]))
        self.reset()

    def reset(self):
        self.card_list[self.card].text = ''
        self.card = randint(0, self.card_list_len - 1)
        self.card_list[self.card].text = 'CLICK'

    def update(self):
        for i in range(self.card_list_len):
            self.card_list[i].update()

    def exchange(self):
        if self.card_time_now == self.card_time:
            self.reset()
            self.card_time_now = 0
        else:
            self.card_time_now += 1

    def check(self):
        click = False
        catch = False
        for el in self.game.events():
            if el.type == pg.MOUSEBUTTONDOWN and el.button == 1:
                x, y = el.pos
                click = True
                self.game.events_reset()
                break

        for i in range(self.card_list_len):
            self.card_list[i].color = self.game.colors['card_normal']
            if click:
                if self.card_list[i].rect.collidepoint(x, y):
                    if i == self.card:
                        self.card_list[i].color = self.game.colors['card_right']
                        self.game.score += 1
                        catch = True
                    else:
                        self.card_list[i].color = self.game.colors['card_wrong']
                        self.game.score -= 1

                if catch:
                    self.reset()
                    catch = False


           
game = Main()
label_score = Label(game, 20, 20, 30)
label_time = Label(game, 390, 20, 30)

label_win = Label(game, 100, 110, 100)
label_win.text = game.textes["win"]
label_win.text_color = game.colors['text_win']

label_your_score = Label(game, 100, 110, 22)
label_your_score.text = f'{game.textes["yourScore"]} {game.score}'
label_your_score.text_color = game.colors['text_win']

label_lose = Label(game, 75, 110, 100)
label_lose.text = game.textes['lose']
label_lose.text_color = game.colors['text_lose']

cards = Cards(game, Card, [(85, 90), (170, 90), (255, 90), (340, 90)])


game.start()


while game.isRun():
    game.check_rule()

    if game.mode == 0:
        cards.exchange()
        game.screen.fill(game.colors['back'])
        label_score.text = f'{game.textes["score"]} {game.score}'
        label_time.text = f'{game.textes["time"]} {game.timer()}'
        label_score.update()
        label_time.update()
        cards.check()
        cards.update()

    elif game.mode == 1:
        game.screen.fill(game.colors['back_win'])
        label_win.update()
        label_your_score.update()

    elif game.mode == 2:
        game.screen.fill(game.colors['back_lose'])
        label_lose.update()

    game.tick()
    pg.display.update()