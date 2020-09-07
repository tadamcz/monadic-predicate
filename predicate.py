from anytree import Node, RenderTree


string = '((Ax+Dx) + (Bx * Cx))'
# string = 'Ax + Dx'

def lexer(string):
	return string.replace(' ','')
def find_matching_paren(string,left_paren_index=0):
	stack = 0
	for i in range(left_paren_index,len(string)):
		if string[i] == '(':
			stack += 1
		if string[i] == ')':
			stack -= 1
		if stack == 0:
			return i
def parser(string):
	if string == '':
		raise Exception("Empty string")
	string = lexer(string)
	tree = Node("root")
	i =0
	while i<len(string):
		current_character = string[i]
		if current_character in ('+','*'):
			new_tree = Node(current_character)
			new_tree.children = tree.children
			tree = new_tree
			i += 1
		elif current_character == '(':
			subexpression_left = i+1
			subexpression_right = find_matching_paren(string,left_paren_index=i)
			subexpression = string[subexpression_left:subexpression_right]
			parser(subexpression).parent = tree
			i = subexpression_right+1

		elif string[i:i+2] in ('Ax','Bx','Cx','Dx'):
			Node(string[i:i + 2],parent=tree)
			i += 2
		else:
			raise Exception("What's this char?")
		print_my_tree(tree)
	return tree

def print_my_tree(tree):
	for pre, fill, node in RenderTree(tree):
		print("%s%s" % (pre, node.name))

result = parser(string)
print_my_tree(result)