class Monster:
  def __init__(self, name, damage):
    self.name = name
    self.hp = 10
    self.damage = damage
  
  def info(self):
    print("sono", self.name, "hp:", self.hp, "/10")

  def attack(self, enemy):
    if self.hp <= 0:
      print(self.name, "prova ad attaccare da morto con scarsi risultati")
    else: 
      print(self.name, "attacca", enemy.name)

      if (enemy.hp <= 0):
        print(enemy.name, "e' morto")
      else:
        enemy.hp -= self.damage
  

m1 = Monster("Pino", 6)
m1.info()

m2 = Monster("Pluto", 2)
m2.info()

m1.attack(m2)
m2.info()
m2.attack(m1)
m1.attack(m2)
m2.info()
m1.attack(m2)
m2.info()
m2.attack(m1)
m1.attack(m2)