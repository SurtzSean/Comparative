import sys

#global vars
file = open(sys.argv[1], 'r')
wlist = file.read().split()
mitr = iter(wlist)

var_map = {}
exp_type = 0
reserved = ['let', 'in', 'end', ';','==','>','>=','<','<=','if','then','else','=','+','-','*',':','(',')',';']

#runs program
def main():
	prog()

#iterates through file
def lexan():
	global mitr
	try:
		return(next(mitr))
	except StopIteration:
		return('')

lookahead = lexan()

#checks order for correct grammar, prints syntax error if incorrect
def match(ch):
	global lookahead
	if ch == lookahead:
		lookahead = lexan()
	else:
		tinyError(lookahead, 'a')
		exit()

#runs letinend
def prog():
	global lookahead
	while lookahead == 'let':
		let_in_end()	

#let decl-list in type expr end ;
def let_in_end():
	global lookahead
	global var_map
	var_map = {}
	match('let')
	decl_list()
	match('in')
	tinyType()
	match('(')
	val = expr()
	match(')')
	match('end')
	match(';')
	print(val)

#declaring variables
def decl_list():
	global lookahead
	decl(lookahead)
	while(lookahead!='in'):
		decl(lookahead)

#inserts variables into var_map
def decl(name):
	global lookahead
	global var_map
	global reserved
	if name not in var_map.keys() and name not in reserved:
		lookahead = lexan()
		match(':')
		if lookahead == 'real':
			lookahead = lexan()
			match('=')
			if(isReal(lookahead)):
				var_map[name]=float(lookahead)
			elif lookahead in var_map.keys() and type(var_map[lookahead]) == type(0.0):
				exp_type = 0.0
				var_map[name] = expr()
			else:
				tinyError(lookahead, 'real value')
		elif lookahead == 'int':
			lookahead = lexan()
			match('=')
			if(isInt(lookahead)):
				var_map[name]=int(lookahead)
			elif lookahead in var_map.keys() and type(var_map[lookahead]) == type(0):
				exp_type = 0
				var_map[name] = expr()
			else:
				tinyError(lookahead, 'int value')
		else:
			tinyError(lookahead, 'real or int')
	else:
		tinyError(name, 'valid name')
	print(lookahead)
	lookahead = lexan()
	match(';')

#checks expression
def tinyType():
	global lookahead
	if lookahead == 'int':
		exp_type = 0
		lookahead = lexan()
	elif lookahead == 'real':
		exp_type = 0.0
		lookahead = lexan()
	else:
		tinyError(lookahead, 'int or real')

#adds/subtracts terms
def expr():
	global lookahead
	global exp_type
	if lookahead != 'if':
		a = term()
		while lookahead == '+' or lookahead == '-':
			if lookahead == '+':
				lookahead = lexan()
				b = term()
				if type(a) == type(b):
					a+=b
				else:
					tinyError(type(a), type(b))
			elif lookahead == '-':
				lookahead = lexan()
				b = term()
				if type(a) == type(b):
					a-=b
				else:
					tinyError(type(a), type(b))
	else:
		match('if')
		condition = cond()
		match('then')
		a = expr()
		match('else')
		b = expr()
		if condition!=True:
			a = b
	if type(a) == type(exp_type):
		return a
	else:
		tinyError(type(a), type(exp_type))

#multiplies/divides factors
def term():
	global lookahead
	a = factor()
	while lookahead == '*' or lookahead == '/':
		if lookahead == '*':
			lookahead = lexan()
			b = factor()
			if type(a) == type(b):
				a*=b
			else:
				tinyError(type(a),type(b))
		elif lookahead == '/':
			lookahead = lexan()
			b = factor()
			if type(a) == type(b):
				if type(exp_type) == type(a) and type(exp_type) == type(0):
					a = int(a/b)
				else:
					a/=b
			else:
				tinyError(type(a), type(b))
	if type(a) == type(exp_type):
		return a
	else:
		tinyError(type(a), type(exp_type))

#parens, id's, numbers, typecasting
def factor():
	global lookahead
	if lookahead == ('('):#parens
		num = expr()
		return num
	elif lookahead in var_map.keys(): #variable passed through
		num = var_map[lookahead]
		lookahead = lexan()
		return num
	elif isReal(lookahead): #real passed through
		num = float(lookahead)
		lookahead = lexan()
		return num
	elif isInt(lookahead): #integer passed through
		num = int(lookahead)
		lookahead = lexan()
		return num
	elif lookahead == 'real': #typecast to real
		lookahead = lexan()
		match('(')
		if lookahead in var_map.keys():
			num = float(var_map[lookahead])
			lookahead = lexan()
			match(')')
			return num
		else:
			tinyError(lookahead, 'variable name')
	elif lookahead == 'int': #typecast to int
		tmpvar = 'int'
		lookahead = lexan()
		match('(')
		if lookahead in var_map.keys():
			num = int(var_map[lookahead])
			lookahead = lexan()
			match(')')
			return num
	else: #error
		tinyError(lookahead, 'expression, variable, number, or typecast')

def cond():
	global lookahead
	op1 = oprnd()
	
	if lookahead == '>':
		lookahead = lexan()
		op2 = oprnd()
		if op1 > op2:
			return True
		else:
			return False
	elif lookahead == '>=':
		lookahead = lexan()
		op2 = oprnd()
		if op1 >= op2:
			return True
		else:
			return False
	elif lookahead == '<=':
		lookahead = lexan()
		op2 = oprnd()
		if op1 <= op2:
			return True
		else:
			return False
	elif lookahead == '<':
		lookahead = lexan()
		op2 = oprnd()
		if op1 < op2:
			return True
		else:
			return False
	elif lookahead == '==':
		lookahead = lexan()
		op2 = oprnd()
		if op1 == op2:
			return True
		else:
			return False
	elif lookahead == '<>':
		lookahead = lexan()
		op2 = oprnd()
		if op1 != op2:
			return True
		else:
			return False
	else:
		tinyError('bool operator', lookahead)

def oprnd():
	global lookahead
	if lookahead in var_map.keys():
		num = var_map[lookahead]
		lookahead = lexan()
		return num
	elif isInt(lookahead):
		num = int(lookahead)
		lookahead = lexan()
		return num
	elif isReal(lookahead):
		num = float(lookahead)
		lookahead = lexan()
		return num	

	else:
		tinyError(type(lookahead), 'variable, integer, or real')


###################
#Periphery Methods#
###################

#Checks if string, n, is an integer
def isInt(n):
	scount = 0
	nums = ['0','1','2','3','4','5','6','7','8','9']
	for c in n:
		if scount == 0 and c == '-':
			continue
		scount+=1
		if c in nums:
			continue
		return False
	return True

#Checks if a string, n, is a real/flaot
def isReal(n):
	nums = ['0','1','2','3','4','5','6','7','8','9']
	dec_count = 0
	scount = 0
	for c in n:
		if scount == 0 and c == '-':
			continue
		scount+=1
		if c in nums:
			continue
		elif c is '.' and dec_count<1:
			dec_count+=1
			continue
		return False
	if dec_count==1:
		return True
	return False

#error message
def tinyError(got, expected):
	print('Error got: ', got, ' expected: ', expected)
	exit()

#runs program
if __name__ == '__main__':
	main()