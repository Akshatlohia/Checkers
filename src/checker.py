import copy
import pygame as py


# CONSTANTS:
WIDTH = 700
HEIGHT = 700
ROWS = 8
COLS = 8

# Colors
OLIVE	= ( 119, 149, 86)
LYELLOW	= ( 238, 238, 210)
GREEN	= (   0, 255,   0)
WHITE	  	= ( 248, 248, 248)
BLACK	= (38, 38, 38)
GREY  = (128,128,128)
CROWN = py.transform.scale(py.image.load('assets/crown.png'), (22, 12))


class Game:
	def __init__(self):

		self.status = 'playing'
		self.turn = 1 # random.randrange(2)
		self.players = ['w','b']
		self.chips = [12, 12]
		self.kings = [0, 0]
		self.selectedChip = None
		self.jump = False
		self.board = [['w','-','w','-','w','-','w','-'],
						   ['-','w','-','w','-','w','-','w'],
						   ['w','-','w','-','w','-','w','-'],
						   ['-','-','-','-','-','-','-','-'],
						   ['-','-','-','-','-','-','-','-'],
						   ['-','b','-','b','-','b','-','b'],
						   ['b','-','b','-','b','-','b','-'],
						   ['-','b','-','b','-','b','-','b']]

	def validPieceMove(self, player, frLoc, toLoc):
		frRow = frLoc[0]
		frCol = frLoc[1]
		toRow = toLoc[0]
		toCol = toLoc[1]
		chip = self.board[frRow][frCol]
		if self.board[toRow][toCol] != '-':
			return False, None
		if (((chip.isupper() and abs(frRow - toRow) == 1) or (player == 'w' and toRow - frRow == 1) or
			 (player == 'b' and frRow - toRow == 1)) and abs(frCol - toCol) == 1) and not self.jump:
			return True, None
		if (((chip.isupper() and abs(frRow - toRow) == 2) or (player == 'w' and toRow - frRow == 2) or
			 (player == 'b' and frRow - toRow == 2)) and abs(frCol - toCol) == 2):
			jump_row = (toRow - frRow) / 2 + frRow
			jump_col = (toCol - frCol) / 2 + frCol
			if self.board[int(jump_row)][int(jump_col)].lower() not in [player, '-']:
				return True, [jump_row, jump_col]
		return False, None

	def getAllPc(self, player):
		pieces = []
		for a, x in enumerate(self.board):
			for b, y in enumerate(x):
				if y.lower() == player:
					pieces.append([a, b])
		return pieces

	def nextPlayerTurn(self):
		self.turn += 1
  
  

	def checkWiner(self):
		if len(self.getAllValidPcMoves(self.players[self.turn % 2])) == 0 and self.jump == False:
			return self.players[1]
		if self.chips[0] == 0:
			return self.players[1]
		if self.chips[1] == 0:
			return self.players[0]
		if self.chips[0] == 1 & self.chips[1] == 1:
			return 'draw'
		return None


	def clickEvaluation(self, mouseLoc):
		if self.status == 'playing':
			toLoc = getClickRow(mouseLoc), getClickCol(mouseLoc)
			player = self.players[self.turn % 2]
			if self.selectedChip:
				move = self.validPieceMove(player, self.selectedChip, toLoc)
				if move[0]:
					winer = self.run(player, self.selectedChip, toLoc, move[1])
					if winer is None:
						pass 
					elif winer == 'draw':
						print("DRAW! Click to start again")
					else:
						print("%s wins! Click to start again" % winer)
				elif toLoc[0] == self.selectedChip[0] and toLoc[1] == self.selectedChip[1]:
					self.selectedChip = None
					if self.jump:
						self.jump = False
						self.nextPlayerTurn()
				else:
					print('Not a valid move')
			else:
				if self.board[toLoc[0]][toLoc[1]].lower() == player:
					self.selectedChip = toLoc
		elif self.status == 'game over':
			self.__init__()


	def getAllValidPcMoves(self, player):
		moves = []
		for a in self.getAllPc(player):
			for p,t in [[1,1],[-1,-1],[1,-1],[-1,1]]:
				toLoc = [a[0]+p, a[1]+t]
				if (toLoc[0] < ROWS) & (toLoc[0] >= 0) & (toLoc[1] < COLS) & (toLoc[1] >= 0):
					b = [a[0]+p, a[1]+t]
					validPieceMove, jumped = self.validPieceMove(player, a, b)
					if validPieceMove == True:
						moves.append([a, [a[0]+p, a[1]+t], None])

			canJump = True
			frLoc = a
			jumpedList = []
			while canJump:
				canJump = False
				for p,t in [[2,2],[2,-2],[-2,2],[-2,-2]]:
					toLoc = [frLoc[0]+p, frLoc[1]+t]
					if (toLoc[0] < ROWS) & (toLoc[0] >= 0) & (toLoc[1] < COLS) & (toLoc[1] >= 0):
						validPieceMove, jumped = self.validPieceMove(player, frLoc, toLoc)
						if validPieceMove == True and jumped != None:
							canJump = True
							jumpedList.append(jumped)
							moves.append([a, toLoc, jumpedList])
							frLoc = toLoc
		return moves

	def run(self, player, frLoc, toLoc, jump, auto=False):
		frRow = frLoc[0]
		frCol = frLoc[1]
		toRow = toLoc[0]
		toCol = toLoc[1]
		chip = self.board[frRow][frCol]
		self.board[toRow][toCol] = chip
		self.board[frRow][frCol] = '-'
		if (player == 'w' and toRow == ROWS-1):
			self.board[toRow][toCol] = chip.upper()
			self.kings[player == 'w'] += 1
		elif (player == 'b' and toRow == 0):
			self.board[toRow][toCol] = chip.upper()
			self.kings[player == 'b'] += 1

		if auto and jump != None:
			for b in jump:
				self.board[int(b[0])][int(b[1])] = '-'
				self.chips[player == self.players[0]] -= 1
			self.selectedChip = None
			self.jump = False
			self.nextPlayerTurn()
		elif jump:
			self.board[int(jump[0])][int(jump[1])] = '-'
			self.selectedChip = [toRow, toCol]
			self.jump = True
			self.chips[player == self.players[0]] -= 1
		else:
			self.selectedChip = None
			self.nextPlayerTurn()
		winer = self.checkWiner()
		if winer != None:
			self.status = 'game over'
		return winer



	def fillBoard(self):
		for a in range(ROWS+1):
			for b in range(COLS+1):
				if (a+b) % 2 == 1:
					py.draw.rect(window, LYELLOW, (a * WIDTH / ROWS, b * HEIGHT / COLS, WIDTH / ROWS, HEIGHT / COLS))

		for a in range(len(self.board)):
			for b in range(len(self.board[a])):
				mark = self.board[a][b]
				if self.players[0] == mark.lower():
					color = WHITE
				else:
					color = BLACK
				if self.selectedChip:
					if self.selectedChip[0] == a and self.selectedChip[1] == b:
						color = GREY
				if mark != '-':
					x = WIDTH / ROWS * b + WIDTH / ROWS / 2
					y = HEIGHT / COLS * a + HEIGHT / COLS / 2
					radius = (WIDTH/ROWS)//2 - 13
					py.draw.circle(window, color, (int(x), int(y)), radius)
					if self.board[a][b].isupper():
						py.draw.circle(window, OLIVE, (int(x), int(y)), int(radius*7/8))
						py.draw.circle(window, color, (int(x), int(y)), int(radius*3/4))
						window.blit(CROWN, (x - CROWN.get_width()//2, y - CROWN.get_height()//2))

def evalv(game, player):
	bpieces = game.chips[player]
	wpieces = game.chips[(player+1)%2]
	bkings = game.kings[player]
	wkings = game.kings[(player+1)%2]
	return (bpieces - wpieces) + (bkings - wkings)*0.5

def getClickCol(mouseLoc):
	x = mouseLoc[0]
	for a in range(1, ROWS):
		if x < a * WIDTH / ROWS:
			return a - 1
	return ROWS-1

def getClickRow(mouseLoc):
	y = mouseLoc[1]
	for a in range(1, COLS):
		if y < a * HEIGHT / COLS:
			return a - 1
	return COLS-1

def minmax(game, depth, player, alpha=float('-inf'), beta=float('+inf')):
	currentPlayer = game.turn % 2
	winer = game.checkWiner()
	if winer != None: 
		if winer == game.players[player]: 
			return float('+inf'), None, []
		elif winer == game.players[(player + 1) % 2]:
			return float('-inf'), None, []
		else:
			return evalv(game, player), None, []
	elif depth == 0: 
		eval = evalv(game, player)
		return eval, None

	elif player == currentPlayer:
		maxEvaluation = float('-inf')
		bestStep = None
		moves = game.getAllValidPcMoves(game.players[currentPlayer])
		for m in moves:
			nGame = copy.deepcopy(game)
			nGame.run(game.players[currentPlayer], m[0], m[1], m[2], True)
			eval = minmax(nGame, depth-1, player, alpha, beta)[0]
			maxEvaluation = max(maxEvaluation, eval)
			alpha = max(alpha, eval)
			if beta <= alpha:
				break
			if maxEvaluation == eval:
				bestStep = m
		return maxEvaluation, bestStep

	else: 
		minEvaluation = float('+inf')
		bestStep = None
		moves = game.getAllValidPcMoves(game.players[currentPlayer])
		for m in moves:
			nGame = copy.deepcopy(game)
			nGame.run(game.players[currentPlayer], m[0], m[1], m[2], True)
			eval = minmax(nGame, depth-1, player, alpha, beta)[0]
			minEvaluation = min(minEvaluation, eval)
			beta = min(beta, eval)
			if beta <= alpha:
				break
			if minEvaluation == eval:
				bestStep = m
		return minEvaluation, bestStep

py.init()
size = (WIDTH, HEIGHT)
window = py.display.set_mode(size)
game = Game() 
done = False
clock = py.time.Clock()
framerate = 60
py.display.set_caption("CHECKERS")

_minmax = True
depth = 5
minmaxPlayer = 0

while not done:

	if game.turn % 2 == minmaxPlayer and _minmax:

		eval, bestStep = minmax(game, depth, minmaxPlayer)

		winer = game.checkWiner()
		if winer != None:
			self.status = 'game over'
		else:
			game.run(game.players[game.turn % 2], bestStep[0], bestStep[1], bestStep[2], True)

	else:
		for event in py.event.get(): 
			if event.type == py.QUIT:
				done = True 
			if event.type == py.KEYDOWN:
				entry = str(event.key)
			if event.type == py.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = py.mouse.get_pos()
				game.clickEvaluation(py.mouse.get_pos())

		window.fill(OLIVE) 
		game.fillBoard()
		py.display.flip() 
		clock.tick(60)

py.quit()
