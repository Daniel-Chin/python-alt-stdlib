from cocos import *
from cocos.actions.instant_actions import CallFunc
from time import sleep
from random import randint
from pyglet.window import key as KEY
WIDTH = 1280
HEIGHT = 720
# 16 : 9
CENTER = (WIDTH//2, HEIGHT//2)
DENSITY = 1
COLUMN = 16 * DENSITY
ROW = 9 * DENSITY
DIAMETER = WIDTH // COLUMN

FRISK_SPEED = 3

director.director.init(width = WIDTH, height = HEIGHT, 
                       caption = 'Color Tiles')

class MyLayer(layer.Layer):
    is_event_handler = True
    def __init__(self):
        layer.Layer.__init__(self)
        self.listen = False
        self.pressed = None
        self.referee = None
        self.map = None
        self.lock = False
        self.loaded = False
        self.sliding = None
    
    def on_key_press (self, key, modifiers):
        if key is KEY.R:
            director.director.window.set_caption('New game!')
            if self.loaded:
                self.remove(self.referee.player.visual)
                for column in self.map:
                    for tile in column:
                        self.remove(tile.visual)
            play()
            return
        if self.listen:
            if key in (KEY.W, KEY.A, KEY.S, KEY.D):
                self.pressed = key
                if not self.lock:
                    self.referee.check()
    
    def on_key_release (self, key, modifiers):
        if self.pressed == key:
            self.pressed = None
    
    def setReferee(self, referee):
        self.referee = referee

mainLayer = MyLayer()

class Tile:
    def __init__(self, x, y):
        self.type = randTile()
        self.x = x
        self.y = y
        self.visual = layer.ColorLayer(*self.type.color, 255, DIAMETER, DIAMETER)
        self.visual.position = x*DIAMETER, y*DIAMETER
        mainLayer.add(self.visual, 0)
    
class Red:
    color = 255, 0, 0
class Pink:
    color = 255, 180, 180
class Green:
    color = 0, 255, 0
class Blue:
    color = 0, 0, 255
class Purple:
    color = 160, 0, 200
class Orange:
    color = 255, 150, 0
class Yellow:
    color = 255, 255, 0

def randTile():
    all_tiles = [Red, Pink, Green, Blue, Purple, Orange, Yellow] 
    return all_tiles[randint(0,len(all_tiles)-1)]

def greet():
    label = text.Label(
        'cocos2d',
        font_name='Times New Roman',
        font_size=32,
        anchor_x='center', anchor_y='center'
    )
    label.position = CENTER
    label.opacity = 0
    mainLayer.add(label)
    def papyrize(label):
        print('papyrize')
        label.element.text = 'Color Tiles'
        label.element.font_name = 'Papyrus'
        label.element.font_size = 64
    label.do(actions.Delay(1) + 
             actions.FadeIn(1) + 
             actions.Delay(1) + 
             actions.FadeOut(1) +
             actions.Delay(1) +
             CallFunc(papyrize, label) + 
             actions.FadeIn(1) + 
             actions.Delay(1) + 
             actions.FadeOut(1) +
             actions.Delay(1) + 
             CallFunc(play, first=True) + 
             CallFunc(lambda : mainLayer.remove(label))
             )  

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.flavor = 'lemon'
        self.visual = sprite.Sprite('char.png', scale = .8 / DENSITY)
        mainLayer.add(self.visual, 1)
        self.referee = None
    
    def flash(self, x, y):
        self.x, self.y = x, y
        self.visual.position = self.GPU(x, y)
    
    def move(self, x, y, slide = False):
        self.x, self.y = x, y
        if slide:
            duration = .3/FRISK_SPEED
        else:
            duration = 1/FRISK_SPEED
        moveTo = actions.MoveTo(self.GPU(x, y), duration)
        mainLayer.lock = True
        self.visual.do(moveTo + CallFunc(self.referee.check))
    
    def GPU(self, x, y):
        return int((x+.53)*DIAMETER), int((y+.95)*DIAMETER)
    
class Referee():
    def __init__(self, map, player):
        self.map = map
        self.player = player
    
    def check(self):
        intention = mainLayer.pressed
        if mainLayer.sliding is not None:
            intention = mainLayer.sliding
        mainLayer.sliding = None
        mainLayer.lock = False
        if intention is not None:
            map = self.map
            player = self.player
            if intention is KEY.W:
                destination = (player.x, player.y+1)
            elif intention is KEY.A:
                destination = (player.x-1, player.y)
            elif intention is KEY.S:
                destination = (player.x, player.y-1)
            elif intention is KEY.D:
                destination = (player.x+1, player.y)
            else:
                raise AssertionError
            
            # check if destination exits
            legal = checkLegal(*destination)
            if legal:
                
                # check if destination is safe
                tile_destination = map[destination[0]][destination[1]]
                type = tile_destination.type
                if type is Pink:
                    director.director.window.set_caption(
                        "Pink tiles do nothing. flavor = "+player.flavor)
                    pass
                elif type is Red:
                    director.director.window.set_caption(
                        "You don't go into walls. (Sorry.) flavor = "+player.flavor)
                    return
                elif type is Green:
                    director.director.window.set_caption(
                        "Imagine a sound effect playing. flavor = "+player.flavor)
                    pass
                elif type is Orange:
                    player.flavor = 'orange'
                    director.director.window.set_caption(
                        "You smell like orange. flavor = "+player.flavor)
                    pass
                elif type is Purple:
                    player.flavor = 'lemon'
                    director.director.window.set_caption(
                        "You slide and smell like soap. flavor = "+player.flavor)
                    mainLayer.sliding = intention
                    player.move(*destination, slide=True)
                    return
                elif type is Yellow:
                    director.director.window.set_caption(
                        "You are zapped back. flavor = "+player.flavor)
                    return
                elif type is Blue:
                    if player.flavor == 'orange':
                        director.director.window.set_caption(
                            "Piranhas like orange...? flavor = "+player.flavor)
                        return
                    zappy = False
                    for tile in adjacent(tile_destination, map):
                        if tile.type is Yellow:
                            zappy = True
                    if zappy:
                        director.director.window.set_caption(
                            "Water conducts electricity. flavor = "+player.flavor)
                        return
                    director.director.window.set_caption(
                        "Swimming... flavor = "+player.flavor)
                    pass
                
                # passed. It is safe!
                player.move(*destination)

def checkLegal(x, y):
    legal_x = 0 <= x < COLUMN
    legal_y = 0 <= y < ROW
    return legal_x and legal_y

def adjacent(tile, map):
    stink = (
        (0, 1), 
        (0, -1), 
        (1, 0), 
        (-1, 0)
        )
    result = []
    for vector in stink:
        x = tile.x + vector[0]
        y = tile.y + vector[1]
        if checkLegal(x, y):
            result.append(map[x][y])
    return result

def play(first = False):
    if mainLayer.listen and first:
        return
    print('main loop')
    map = []
    for x in range(COLUMN):
        column = []
        for y in range(ROW):
            tile = Tile(x, y)
            column.append(tile)
        map.append(column)
    mainLayer.map = map
    player = Player()
    player.flash(0, 0)
    referee = Referee(map, player)
    player.referee = referee
    mainLayer.referee = referee
    dog = sprite.Sprite('god.png', scale = .13 / DENSITY)
    dog.position = (int((COLUMN-.5)*DIAMETER), 
        int((ROW-.5)*DIAMETER))
    mainLayer.add(dog, 2)
    mainLayer.loaded = True
    mainLayer.listen = True

def printMap(map):
    for column in map:
        for tile in column:
            print(tile.type, end=' ')
        print()

greet()
mainScene = scene.Scene(mainLayer)
director.director.run(mainScene)
