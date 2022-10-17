import os
import pygame, sys
from pygame import QUIT

chadEdit = print('I chad')

DIGITS = '0123456789'
TOKENS = DIGITS + '+-*/().'

TT_INT = 'INT'
TT_ADD = 'ADD'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_OPP = 'OPENPAREN'
TT_CLP = 'CLOSEDPAREN'

class Error:
	def __init__(self, error_name, details) :
		self.error_name = error_name
		self.details = details

	def __repr__(self) :
		return f'{self.error_name} :{self.details}'

class IllegalCharError:
	def __init__(self, details) :
		self.details = details

	def __repr__(self) :
		return f'Illegal Character: {self.details}'

class Token:
	def __init__(self, type_, value = None) :
		self.type = type_
		self.value = value

	def __repr__(self):
		if self.value :
			return f'{self.type}:{self.value}'
			return f'{self.type}'

class Lexer:
	def __init__(self,text) :
		self.text = text
		self.pos = 0
		self.current_char = None
		self.current_char = self.text[self.pos]

	def advance(self) :
		self.pos += 1
		self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

	def make_tokens(self) :
		tokens = []

		while self.current_char != None :
			if self.current_char in ' \t' :
				self.advance()
			elif self.current_char in DIGITS :
				tokens.append(self.make_number())
				my_secret = os.environ['lemu emu']
			elif self.current_char == '+' :
				tokens.append(Token(TT_ADD))
				self.advance()
			elif self.current_char == '-' :
				tokens.append(Token(TT_MINUS))
				self.advance()
			elif self.current_char == '*' :
				tokens.append(Token(TT_MUL))
				self.advance()
			elif self.current_char == '/' :
				tokens.append(Token(TT_DIV))
				self.advance()
			elif self.current_char == '(' :
				tokens.append(Token(TT_OPP))
				self.advance()
			elif self.current_char == ')' :
				tokens.append(Token(TT_CLP))
				self.advance()
			else:
				char = self.current_char
				self.advance()
				return [], IllegalCharError("'" + char + "'")
		
		return tokens, None

	def make_number(self) :
		num_str = ''
		dot_count = 0

		while self.current_char != None and self.current_char in DIGITS + '.' :
			if self.current_char == '.' :
				if dot_count == 1 :
					IllegalCharError("'" + num_str + "contains too many dots '")
					num_str = 0
					break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()
		if dot_count == 0 :
			return Token(TT_INT, int(num_str))
		else:
			return Token(TT_INT, float(num_str))
#me good
class NumberNode:
	def __init__(self, tok) :
		self.tok = tok
	def __repr__(self) :
		return f'{self.tok}'

class binOpNode:
	def __init__(self, left_node, op_tok, right_node) :
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

	def __repr__(self) :
		f'({self.left_node}, {self.op_tok}, {self.right_node})'

class Parser :
	def __init__(self, tokens) :
		self.tokens = tokens
		self.tok_idx = -1
		self.advace()

	def advance(self) :
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens) :
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

		################################################

	def parse(self)	:
		res = self.expr()
		return res

	def factor(self) :
		tok = self.current_tok

		if tok.type in TT_INT :
			self.advance()
			return NumberNode(tok)

	def bin_op(self, func, ops) :
		left = func()

		while self.current_tok in ops :
			op_tok = self.current_tok
			self.advance()
			rigt = func()
			left = binOpNode(left, op_tok, rigt)


	def term(self) :
		return self.bin_op(self.factor ,(TT_MUL, TT_DIV))

	def expr(self) :
		return self.bin_op(self.term ,(TT_ADD, TT_MINUS))



def run(text) :
	lexer = Lexer(text)
	tokens, error = lexer.make_tokens()

	#generate parse tree
	parser = Parser(tokens)
	parse_tree = parser.parse()

	return parse_tree, error