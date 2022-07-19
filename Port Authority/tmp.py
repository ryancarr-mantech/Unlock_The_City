import ssl
import keyboard
import websocket
import pygame
import json
import time
playerId = 3
play = True

pygame.init()
window = pygame.display.set_mode((943,594))

drawThings = []
ships = []

def calculateRect(corner1, corner2):
    return (corner1[0]/2, corner1[1]/2, (corner2[0]-corner1[0])/2, (corner2[1]-corner1[1])/2)

# class Border:

#     def __init__(self)

# def colliding(rect1, rect2):
#     if rect1[0]+rect2[2] < rect2[0] and rect1[1]+rect1[3] > rect2[]

class Obstacle:

    def __init__(self, corner1, corner2):
        self.rect = calculateRect(corner1, corner2)

    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), self.rect)

class Ship:

    def __init__(self, id):
        if id == playerId:
            self.color = (0,0, 255)
        elif id == 0:
            self.color = (0,255,0)
        else:
            self.color = (255, 0, 0)

        self.id = id

    def update(self, corner1, corner2):
        self.rect = calculateRect(corner1, corner2)
        self.smallRect = (self.rect[0]+(self.rect[2]/2) - self.rect[3]/2, self.rect[1]+(self.rect[3]/2) - self.rect[2]/2, self.rect[3], self.rect[2])
        #self.miniRect = (self.rect[])

    def draw(self, window):
        pygame.draw.rect(window, (255,200,255,126), self.smallRect)
        pygame.draw.rect(window, self.color, self.rect)
        

def get_input():
    global play
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_0

def draw():
    window.fill((255,255,255))
    for thing in drawThings:
        thing.draw(window)

    pygame.display.flip()

def sendData(e):
    if e.name != str(playerId):
        return
    if e.name == "enter":
        print("RESTART")
        ws.send("{ \"type\": \"START_GAME\", \"level\": 5, \"password\": \"CTF{C4pt41N-4MErIc4}\" }")
    else:
        ws.send("{\"type\": \"SHIP_STEER\", \"shipId\": "+e.name+"}")

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE,"check_hostname": False})
ws.connect("wss://37f85f3716bde7436b3e3e770dcbf38e.challenge.hackazon.org/ws")
keyboard.on_press(sendData)

#ws.send("{\"type\": \"SHIP_STEER\", \"shipId\": "+e.name+"}")
ws.send("{ \"type\": \"START_GAME\", \"level\": 5, \"password\": \"CTF{C4pt41N-4MErIc4}\" }")
while play:
    data = json.loads(ws.recv())
    #print(data)
    if data["type"] == "TICK":
        for ship in data["ships"]:
            found = False
            for s in ships:
                if ship["id"] == s.id:
                    s.update((ship['area'][0]['x'], ship['area'][0]['y']), (ship['area'][1]['x'], ship['area'][1]['y']))
                    found = True
                    break
            if not found:
                print('ADDING SHIP')
                s = Ship(ship["id"])
                ships.append(s)
                drawThings.append(s)
                s.update((ship['area'][0]['x'], ship['area'][0]['y']), (ship['area'][1]['x'], ship['area'][1]['y']))
    elif data["type"] == "LOSS":
        ws.send("{ \"type\": \"START_GAME\", \"level\": 5, \"password\": \"CTF{C4pt41N-4MErIc4}\" }")

    elif data["type"] == "GAME_START":
        drawThings = []
        ships = []
        for obs in data['level']['board']['obstructions']:
            drawThings.append(Obstacle((obs['area'][0]['x'], obs['area'][0]['y']), (obs['area'][1]['x'], obs['area'][1]['y'])))
    elif data['type'] == "WIN":
        print(data['flag'])
        break

    get_input()
    draw()
    #print(ws.recv())