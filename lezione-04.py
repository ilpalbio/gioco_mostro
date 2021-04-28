class Entity: 
  def __init__(self, x, y, field):
    self.x = x
    self.y = y
    self.field = field
    self.field.entities.append(self)

  def move(self, direction):
    if direction == "up" and self.y > 0:
      self.y -= 1
    elif direction == "down" and self.y < self.field.h - 1:
      self.y += 1
    elif direction == "left" and self.x > 0:
      self.x -= 1
    elif direction == "right" and self.x < self.field.w - 1:
      self.x += 1

  def check_collision(self, x, y):
    pass

class Monster(Entity):
  def __init__(self, x, y, name, damage, field):
    super().__init__(x, y, field)
    self.name = name
    self.hp = 10
    self.damage = damage

  def info(self):
    print("sono", self.name, "hp:", self.hp, "/10", "e mi trovo a", self.x, ",", self.y)

  def attack(self, enemy):
    if self.hp <= 0:
      print(self.name, "prova ad attaccare da morto con scarsi risultati")
    else: 
      print(self.name, "attacca", enemy.name)

      if (enemy.hp <= 0):
        print(enemy.name, "e' morto")
      else:
        enemy.hp -= self.damage

class Field:
  def __init__(self):
    self.w = 5
    self.h = 5
    self.entities = []

  def draw(self):
    for y in range(self.h):
      for x in range(self.w):
        for e in self.entities:
          if x == e.x and y == e.y:
            print("[x]", end = "")
            break    
        else:
          print("[ ]", end = "")
      print()

field = Field()
m1 = Monster(2, 2, "Pino", 10, field)
m2 = Monster(1, 1, "Gino", 10, field)

for i in range(10):
  m1.move("right")

field.draw()

