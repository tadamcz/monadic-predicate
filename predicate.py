from anytree import Node, RenderTree, LevelOrderIter
import string as stringpackage


string = '!y@x(-(Ax+Dx) > ((-Bx * Cx)+(x=y)))'

variables = stringpackage.ascii_lowercase
sentence_letters = stringpackage.ascii_uppercase
right_arrow = '>'
for_all = '@'
exists = '!'
equality = '='
and_op = '+'
or_op = '*'
negation = '-'

quantifiers = for_all+exists
binary_operators = and_op + or_op + equality + right_arrow + quantifiers
unary_operators = negation
operators = binary_operators+unary_operators

def find_matching_paren(string, start_index=0):
	stack = None
	for i in range(start_index, len(string)):
		if string[i] == '(':
			if stack is None:
				stack = 1
			else:
				stack += 1
		if string[i] == ')':
			stack -= 1
		if stack == 0:
			return i
		if stack is not None:
			if stack < 0:
				raise Exception("Missing a left parenthesis, '('")
	raise Exception("Missing a right parenthesis, ')'")

def add_parens(string):
	# Add parens to sentence letter + variable pairs, such as Px
	translation = {}
	for letter in sentence_letters:
		for variable in variables:
			translation[letter+variable] = '('+letter+variable+')'
	for key,value in translation.items():
		string = string.replace(key,value)

	# Add parens around the negation sign in front of a subexpression
	i = 0
	while i < len(string):
		two_character_window = string[i:i+2]
		existential_quantifier_with_variable = ['!'+x for x in variables]
		universal_quantifier_with_variable = ['@'+x for x in variables]
		candidate_strings = ['-(']+existential_quantifier_with_variable+universal_quantifier_with_variable
		if two_character_window in candidate_strings:
			subexpression_right = find_matching_paren(string, start_index=i + 1)
			string = string[:i]+'('+string[i:subexpression_right+1]+')'+string[subexpression_right+1:]

			i += 1 #we need to move forward one index to stay in the same place because we added a parens to the left!
		i += 2
	return string

def pre_processing(string):
	string = string.replace(' ','')
	string = add_parens(string)
	return string

def parser(string):
	if string == '':
		raise Exception("Empty string")
	tree = Node("root")
	i =0
	while i<len(string):
		current_character = string[i]
		if current_character == '(':
			subexpression_left = i+1
			subexpression_right = find_matching_paren(string, start_index=i)
			subexpression = string[subexpression_left:subexpression_right]
			parser(subexpression).parent = tree
			i = subexpression_right+1
		elif current_character in operators+sentence_letters:
			new_tree = Node(current_character)
			new_tree.children = tree.children
			tree = new_tree
			i += 1
		elif current_character in variables:
			Node(current_character,parent=tree)
			i += 1
		else:
			raise Exception("Syntax error. Unknown character",current_character)
	return tree

def print_my_tree(tree):
	for pre, fill, node in RenderTree(tree):
		print("%s%s" % (pre, node.name))

string = pre_processing(string)
result = parser(string)
print_my_tree(result)

def check_tree_syntax(tree):
	for node in LevelOrderIter(tree):
		name = node.name
		if name in sentence_letters:
			if len(node.children)!=1:
				raise Exception()
			variable = node.children[0]
			if variable.name not in variables:
				raise Exception
		if name in binary_operators:
			if len(node.children) != 2:
				raise Exception
		if name in unary_operators:
			if len(node.children)!=1:
				raise Exception
		if name == equality:
			for variable in [x.name for x in node.children]:
				if variable not in variables:
					raise Exception

		if name in quantifiers:
			number_of_variables = 0
			for child in node.children:
				if child.name in variables:
					number_of_variables += 1
			if number_of_variables != 1:
				raise Exception("Quantifier needs exactly one free variable")

		if name in variables:
			variable = node.name
			found_quantifier = False
			candidate = node.parent
			while found_quantifier == False:
				if candidate == None:
					raise Exception("Unbound variable",variable)
				if candidate.name in quantifiers:
					if variable in [x.name for x in candidate.children]:
						found_quantifier = True
				candidate = candidate.parent
			if found_quantifier == False:
				raise Exception("Unbound variable",variable)







check_tree_syntax(result)