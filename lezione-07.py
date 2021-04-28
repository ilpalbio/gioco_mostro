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

      if enemy.hp <= 0 and isinstance(enemy, Monster):
        print(enemy.name, "e' morto")
        self.field.entities.remove(enemy)
        self.field.n_monster -= 1

      elif enemy.hp <= 0 and isinstance(enemy, Player):
        self.field.entities.remove(enemy)
        enemy.lose()

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
      self.check_entity
    elif isinstance(entity, Gold):
      self.field.score += entity.value
      self.field.entities.remove(entity)

  # metodo per vedere se ci sono delle entità
  def check_entity(self):
    for e in self.field.entities:
      if self.field.n_monster == 0:
        self.win()
   
  # metodo per la vittoria
  def win(self):
    clear_screen()
    for e in self.field.entities:
      self.field.entities.remove(e)

    print('Complimenti', self.name, 'hai vinto')
    self.field.score += 500
    self.field.levelNumber += 1

  # metodo per la perdita
  def lose(self):
    clear_screen()
    for e in self.field.entities:
      self.field.entities.remove(e)

    print('Mi dispiace, hai perso')
    self.field.score = 0

class Field:
  def __init__(self):
    self.entities = []
    self.score = 0
    self.levelNumber = 1
    self.n_monster = 0
  
    f = open("./level" + str(self.levelNumber) + ".level", "r")
    rows = f.read().split("\n")
    f.close()

    self.h = len(rows)
    self.w = len(rows[0])

    for y in range(self.h):
      row = rows[y]
      for x in range(self.w):
        char = row[x]
        if char == "p":
          self.player = Player(x, y, "Player", self)
        elif char == "#":
          Wall(x, y, self)
        elif char == "$":
          Gold(x, y, self)
        elif char == "m":
          Monster(x, y, "Monster", self)
          self.n_monster += 1

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

    print(self.n_monster)

field = Field()

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
  elif command == "w": field.player.move("up")
  elif command == "a": field.player.move("left")
  elif command == "s": field.player.move("down")
  elif command == "d": field.player.move("right")



