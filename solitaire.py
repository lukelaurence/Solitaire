import random
random.seed(10)

class Card:
	def __init__(self,suit,value,visible=False):
		self.suit=suit
		self.value=value
		self.visible=visible
		self.rank="Ace" if not self.value else ['⏨',"Jack","Queen","King"][self.value-9] if 9<=self.value<13 else str(self.value+1)
		self.title = f"{self.rank} of {['Diamonds','Clubs','Hearts','Spades'][self.suit]}"
	def hide(self):
		self.visible=False
	def show(self):
		self.visible=True
	def display(self):
		return self.rank[0]+['♢','♣','♡','♠','♤','♥','♧','♦'][self.suit] if self.visible else "XX"

class Pile:
	def __init__(self,cards,suitsize=13):
		self.cards=cards
		self.cards[-1].show()
		self.suitsize=suitsize
	def add(self,*newcard):
		if len(self.cards):
			if newcard[0].value == self.cards[-1].value+1 and newcard[0].suit%2 != self.cards[-1].value%2:
				self.cards.expand(newcard)
				return True
		elif newcard[0].value == self.suitsize-1:
			self.cards.expand(newcard)
			return True
		return False
	def remove(self,destination,numcards=1):
		if not len(self.cards):
			return False
		if numcards > 1:
			if not self.cards[-numcards].visible:
				return False
		if destination.add(self.cards[-numcards:]):
			[self.cards.pop() for x in range(min(numcards,len(self.cards)))]
			return True
		return False
	def display(self):
		[print(c.display(),end=' ') for c in self.cards]
		print('')

class Foundations:
	def __init__(self,numsuits=4,suitsize=13):
		self.foundations={s:-1 for s in range(numsuits)}
		self.suitsize=suitsize
	def add(self,*card):
		if len(card) > 1:
			return False #change this to accept multiple cards
		if self.foundations[card[0].suit] == card[0].value - 1:
			self.foundations[card[0].suit] += 1
			return True
		return False
	def display(self):
		for k,v in self.foundations.items():
			print(Card(k,v,visible=True).display(),end='  ')
	def complete(self):
		return min(self.foundations.values()) == self.suitsize-1

class Deck:
	def __init__(self,numdecks=1,numsuits=4,suitsize=13):
		self.cards=[]
		self.numsuits=numsuits
		self.suitsize=suitsize
		self.waste=Waste()
		for d in range(numdecks):
			self.adddeck()
		self.shuffle()
	def adddeck(self):
		for s in range(self.numsuits):
			for v in range(self.suitsize):
				self.cards.append(Card(s,v))
	def hide(self):
		map(lambda x:x.hide(),self.cards)
		self.cards[-1].show()
	def shuffle(self):
		random.shuffle(self.cards)
		self.hide()
	def deal(self,drawnum=1):
		"Just for initalization"
		self.cards[-1].hide()
		if len(self.cards)>drawnum:
			self.cards[-1-drawnum].show()
		return [self.cards.pop() for d in range(min(drawnum,len(self.cards)))]
	def remove(self,destination,drawnum=1):
		if drawnum != 1:
			return False
		if destination.add(self.cards[-1:]):
			self.cards.pop()
			if len(self.cards):
				self.cards[-1].show()
			return True
		return False
	def draw(self,drawnum=1):
		[self.remove(self.waste,1) for x in range(min(drawnum,len(self.cards)))]
	def redeal(self):
		self.waste.remove(self.cards)
	def display(self):
		print(f"{self.cards[-1].display()} \t\t{len(self.cards)-1} draws remaining\n")

class Waste:
	def __init__(self):
		self.cards=[]
	def add(self,*card):
		[self.cards.append(c) for c in card]
		return True
	def remove(self,destination):
		destination.extend(reversed(self.cards))
		self.cards.clear()
		return True

class Game:
	def __init__(self,numpiles=7,numdecks=1,numsuits=4,suitsize=13):
		self.deck=Deck(numdecks,numsuits,suitsize)
		self.foundations=Foundations(numsuits,suitsize)
		self.piles = [Pile(self.deck.deal(drawnum=p+1),suitsize) for p in range(numpiles)]
	def move(self,origin,destination,numcards=1):
		if origin.remove(destination,numcards)
	def display(self):
		self.deck.display()
		for p in self.piles:
			p.display()
		print('')
		self.foundations.display()

# class Player:
# 	def __init__(self,game=Game()):
# 		self.game=game
# 	def move(self):
# 		for pile in self.game.piles:
# 			if pile.cards[-1].value==0:

#what you really want to do is to find a way to calculate if a game is winnable,
#and a formula that can give this


g = Game()
g.display()