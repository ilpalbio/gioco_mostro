import os
from random import choice

DIRECTIONS = "up", "down", "left", "right"

class Entity: 
  def __init__(self, x, y, field, graphic):
    self.x = x
    self.y = y
    self.field = field
    self.field.entities.append(self)
    self.graphic = graphic

  def move(self, direction):
    futureX = self.x
    futureY = self.y

    if direction == "up" and self.y > 0:
      futureY -= 1
    elif direction == "down" and self.y < self.field.h - 1:
      futureY += 1
    elif direction == "left" and self.x > 0:
      futureX -= 1
    elif direction == "right" and self.x < self.field.w - 1:
      futureX += 1

    if self.x == futureX and self.y == futureY:
      return

    e = self.field.get_entity_at_coords(futureX, futureY)

    if e == None:
      self.x = futureX
      self.y = futureY
    else:
      self.collide(e)

  def collide(self, entity):
    pass

  def update(self):
    pass

class Gold(Entity):
  def __init__(self, x, y, field):
    super().__init__(x, y, field, "$")
    self.value = 100

class Wall(Entity):
  def __init__(self, x, y, field):
    super().__init__(x, y, field, "#")

class Living_Entity(Entity):
  def __init__(self, x, y, name, hp, damage, field, graphic):
    super().__init__(x, y, field, graphic)
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage

  def info(self):
    print("sono", self.name, "hp:", self.hp, "/", self.max_hp, "e mi trovo a", self.x, ",", self.y)

  def attack(self, enemy):
    if self.hp <= 0:
      print(self.name, "prova ad attaccare da morto con scarsi risultati")
    else: 
      print(self.name, "attacca", enemy.name)

      if (enemy.hp <= 0):
        print(enemy.name, "e' morto")
        self.field.entities.remove(enemy)
      else:
        enemy.hp -= self.damage

class Monster(Living_Entity):
  def __init__(self, x, y, name, field):
    super().__init__(x, y, name, 10, 5, field, "m")
    
  def collide(self, entity):
    if isinstance(entity, Player):
      self.attack(entity)
  
  def move(self):
    super().move(choice(DIRECTIONS))

  def update(self):
    super().update()
    self.move()

class Player(Living_Entity):
  def __init__(self, x, y, name, field):
    super().__init__(x, y, name, 20, 5, field, "p")
  
  def collide(self, entity):
    if isinstance(entity, Monster):
      self.attack(entity)
    elif isinstance(entity, Gold):
      self.field.score += entity.value
      self.field.entities.remove(entity)

class Field:
  def __init__(self):
    self.w = 5
    self.h = 5
    self.entities = []
    self.score = 0

  def get_entity_at_coords(self, x, y):
    for e in self.entities:
      if e.x == x and e.y == y:
        return e

    return None
    
  def draw(self):
    print("score:", self.score)
    for y in range(self.h):
      for x in range(self.w):
        for e in self.entities:
          if x == e.x and y == e.y:
            print("[" + e.graphic + "]", end = "")
            break    
        else:
          print("[ ]", end = "")
      print()
  
  def update(self):
    for e in self.entities:
      e.update()

field = Field()
m1 = Monster(2, 2, "Pino", field)
m2 = Monster(1, 1, "Gino", field)
g = Gold(3, 3, field)
w = Wall(4, 4, field)
w = Wall(3, 4, field)
w = Wall(2, 4, field)
w = Wall(2, 3, field)
p = Player(0, 0, "Player", field)

def clear_screen():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")
    
clear_screen()
while True:  
  field.update()
  field.draw()

  command = input("input: ").lower()
  clear_screen()

  if command == "q": break
  elif command == "w": p.move("up")
  elif command == "a": p.move("left")
  elif command == "s": p.move("down")
  elif command == "d": p.move("right")