import pygame, sys
from pygame.locals import *
import pdb
import random

class Tetris():

	def __init__(self):
		self.board = [[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']],
				[['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','',''],['obstacle','','']]]

	def draw_board(self):
		BLACK = (0,0,0)
		WHITE = (255,255,255)	
		RED = (255,0,0)
		GREEN = (0,255,0)
		BLUE = (0,0, 255)
		PURPLE = (150,0,150)
		TURQUOISE = (0,150,150)
		YELLOW = (255,255,0)
		GREY = (125,125,125)
		DISPLAYSURF = pygame.display.set_mode((200,400),0,32)
		for i in range(3,23): #there are 24 rows total, 3 at the top and 1 at the bottom are NOT displayed
			for j in range(1,11): #there are 12 columns total, 1 on each side is NOT displayed
				y, x = i*20 - 60, j*20 - 20 #this maps to the coordinates being displayed, excluding borders
				piece_type = self.board[i][j][1]
				if piece_type == '':
					pygame.draw.rect(DISPLAYSURF,BLACK,(x,y,20,20))
				elif piece_type == 'line':
					pygame.draw.rect(DISPLAYSURF,GREEN,(x,y,20,20))
				elif piece_type == 'T':
					pygame.draw.rect(DISPLAYSURF,BLUE,(x,y,20,20))
				elif piece_type == 'J':
					pygame.draw.rect(DISPLAYSURF,WHITE,(x,y,20,20))
				elif piece_type == 'L':
					pygame.draw.rect(DISPLAYSURF,RED,(x,y,20,20))
				elif piece_type == 'S':
					pygame.draw.rect(DISPLAYSURF,PURPLE,(x,y,20,20))
				elif piece_type == 'Z':
					pygame.draw.rect(DISPLAYSURF,TURQUOISE,(x,y,20,20))
				elif piece_type == 'box':
					pygame.draw.rect(DISPLAYSURF,YELLOW,(x,y,20,20))
		if self.you_lose():
			#print 'You lose!'
			pygame.font.init()
			myfont = pygame.font.SysFont('sawasdee', 30, bold=1)
			pygame.draw.rect(DISPLAYSURF, GREY, (30,45,140,50))
			label = myfont.render('You lose!', 1, WHITE)
			DISPLAYSURF.blit(label, (40,50))
		pygame.display.update() 		

		

	def piece_fall(self):
		obstacle_hit = False
		for row in range(22,-1,-1):
			for column in range(12):
				#print 'row: %d column: %d' %(row,column)
				if self.board[row][column][0] == 'active':
					if self.board[row+1][column][0] == 'obstacle':
						obstacle_hit = True
						#print 'obstacle found at %d %d' %(row, column)
						
		if not obstacle_hit: #keep falling as long as obstacle not hit
			for row in range(22,-1,-1):
				for column in range(12):
					if self.board[row][column][0] == 'active':
						#print "found piece in piece_fall", row, column
						color, pivot_state = self.board[row][column][1], self.board[row][column][2]
						self.board[row][column] = ['','','']
						self.board[row+1][column] = ['active',color,pivot_state]

		elif obstacle_hit: #if obstacle encountered, active piece becomes obstacle
			for row in range(22,-1,-1):
				for column in range(12):
					if self.board[row][column][0] == 'active':
						self.board[row][column][0] = 'obstacle'

		#for row in range(24): #prints to terminal - used for debugging
		#	print self.board[row]	

						

	def user_input(self, event, piece):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.move_right()
			elif event.key == pygame.K_LEFT:
				self.move_left()
			elif event.key == pygame.K_DOWN:
				self.piece_fall()
			elif event.key == pygame.K_UP:
				self.rotate(piece)

	def move_left(self):
		obstacle_hit = False
		for row in range(22,-1,-1): #loop backwards from bottom to top - easier to check for obstacles
			for column in range(1,11):
				state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
				if state == 'active':
					if self.board[row][column-1][0] == 'obstacle': #checks state of cell to left
						obstacle_hit = True
		if not obstacle_hit: #obstacle not encountered
			for row in range(22,-1,-1):
				for column in range(1,11):			
					state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
					if state == 'active':
						self.board[row][column] = ['','','']
						self.board[row][column-1] = [state,piece_type,pivot_state] 
							#assigns cell on left to values of original cell
						
	def move_right(self):
		obstacle_hit = False
		for row in range(22,-1,-1):
			for column in range(11,0,-1): #loop from right to left
				state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
				if state == 'active':
					if self.board[row][column+1][0] == 'obstacle': #check state of cell to right
						obstacle_hit = True
		if not obstacle_hit: #obstacle not encountered
			for row in range(22,-1,-1):
				for column in range(11,0,-1):			
					state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
					if state == 'active':
						self.board[row][column] = ['','',''] #reset cell you're moving away from
						self.board[row][column+1] = [state,piece_type,pivot_state]
	def rotate(self, piece_type):
		if piece_type == 'line':
			self.rotate_line()
		elif piece_type == 'box':
			pass #rotating box does nothing
		else: #other five piece types
			pivot_row, pivot_col, pivot_state = self.find_pivot() #don't need pivot_state here, but find_pivot returns it
			self.rotate_grid(pivot_row, pivot_col)

	def rotate_line(self):
		print '\n'*3
		pivot_row, pivot_col, pivot_state = self.find_pivot()
		for row in range(pivot_row-2,pivot_row+3):
			for column in range(pivot_col-2,pivot_col+2):
				print self.board[row][column],
			print '\n'
		obstacle_hit = False
		if pivot_state == 'vertical': 			
			for cell in [self.board[pivot_row][pivot_col+1], self.board[pivot_row][pivot_col-1], self.board[pivot_row][pivot_col-2]]:
				if cell[0] == 'obstacle':
					obstacle_hit = True
			if not obstacle_hit:
				self.board[pivot_row][pivot_col+1] = self.board[pivot_row-1][pivot_col]
				self.board[pivot_row-1][pivot_col] = ['','','']
				self.board[pivot_row][pivot_col-1] = self.board[pivot_row+1][pivot_col]
				self.board[pivot_row+1][pivot_col] = ['','','']
				self.board[pivot_row][pivot_col-2] = self.board[pivot_row+2][pivot_col]
				self.board[pivot_row+2][pivot_col] = ['','','']
				self.board[pivot_row][pivot_col][2] = 'horizontal' #switch pivot state
		else: #pivot state is horizontal
			for cell in [self.board[pivot_row-1][pivot_col], self.board[pivot_row+1][pivot_col], self.board[pivot_row-2][pivot_col]]:
				if cell[0] == 'obstacle':
					obstacle_hit = True
					print obstacle_hit, cell
			if not obstacle_hit:
				self.board[pivot_row+1][pivot_col] = self.board[pivot_row][pivot_col-1]
				self.board[pivot_row][pivot_col-1] = ['','','']
				self.board[pivot_row-1][pivot_col] = self.board[pivot_row][pivot_col+1]
				self.board[pivot_row][pivot_col+1] = ['','','']
				self.board[pivot_row+2][pivot_col] = self.board[pivot_row][pivot_col-2]
				self.board[pivot_row][pivot_col-2] = ['','','']
				self.board[pivot_row][pivot_col][2] = 'vertical' #switch pivot state				

	def find_pivot(self):
		for row in range(23):
			for column in range(12):
				state, piece_type, pivot_state = self.board[row][column] #unpack list into elements
				if state == 'active' and pivot_state in ['pivot', 'vertical', 'horizontal']:
					return row, column, pivot_state
	
	def rotate_grid(self, pivot_row, pivot_col):
		top, bottom = pivot_row -1, pivot_row +1
		left, right = pivot_col -1, pivot_col +1
		new = [[0 for i in range(3)] for j in range(3)] #initializes 3x3 grid
		#MAPPING
		new[0][0] = self.board[bottom][left]		
		new[0][1] = self.board[pivot_row][left]		
		new[0][2] = self.board[top][left]
		new[1][0] = self.board[bottom][pivot_col]
		new[1][1] = self.board[pivot_row][pivot_col]	
		new[1][2] = self.board[top][pivot_col]
		new[2][0] = self.board[bottom][right]
		new[2][1] = self.board[pivot_row][right]
		new[2][2] = self.board[top][right]
		#Assign to self.board
		obstacle_hit = False
		for new_row in range(3):
			for new_column in range(3):
				if new[new_row][new_column][0] == 'active' and self.board[new_row+top][new_column+left][0] == 'obstacle':
					obstacle_hit = True
		if not obstacle_hit:
			for new_row in range(3):
				for new_column in range(3): #place new onto self.board
					if new[new_row][new_column][0] != 'obstacle':
						self.board[top+new_row][left+new_column] = new[new_row][new_column]


		


		


	def piece_is_active(self):  #returns True if any active cells on the board
		for row in range(23):
			for column in range(12):
				if self.board[row][column][0] == 'active':
					return True
		else: 
			return False

	def generate_piece(self):
		random_piece = random.choice(['line', 'T', 'J', 'L', 'box', 'S', 'Z'])
		coords = {
			'line' : [(0,6), (2,6), (3,6), (1,6)],
			'T'    : [(3,5), (3,7), (2,6), (3,6)],
			'J'    : [(3,5), (3,7), (2,5), (3,6)],
			'L'    : [(3,5), (3,7), (2,7), (3,6)],
			'box'  : [(3,6), (3,7), (2,6), (2,7)],
			'S'    : [(3,5), (2,6), (2,7), (3,6)],
			'Z'    : [(3,6), (2,5), (2,6), (3,7)],
		}

		for x, y in coords[random_piece]:
			self.board[x][y] = ['active', random_piece, '']

		pivot_x, pivot_y = coords[random_piece][3]
		self.board[pivot_x][pivot_y] = ['active', random_piece, 'pivot']

		return random_piece

	def line_drop(self):
		newline = [['obstacle','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['obstacle','','']]
		lines_dropped = 0
		for row in range(23): #must use range(23), not range(24), to avoid knocking out bottom row, which is just an obstacle.
			filled = all(status == 'obstacle' for status, _, _ in self.board[row])
			if filled:
				self.board.pop(row)
				self.board.insert(0,newline)
				lines_dropped += 1
		return lines_dropped

	def score(self, lines_dropped):
		points = {1 : 100, 2 : 300, 3 : 600, 4 : 1000}
		return points[lines_dropped]

	def you_lose(self):
		lose = False
		for column in range(1,11):
			if self.board[3][column][0] == 'obstacle':
				lose = True	
		return lose			

if __name__ == '__main__':

	board = Tetris()
	frames = 0
	points = 0

	while True:
		if not board.piece_is_active() and not board.you_lose():
			piece = board.generate_piece()
		board.draw_board()
		lines_dropped = board.line_drop()
		if lines_dropped > 0:
			points = points + board.score(lines_dropped)
			print points
		frames += 1
		if frames % 100 == 0:
			board.piece_fall()
			#pdb.set_trace()
		for event in pygame.event.get():
			board.user_input(event, piece)
			#print event.type, event
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
