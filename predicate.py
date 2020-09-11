from anytree import Node, RenderTree, LevelOrderIter
import string as stringpackage
import itertools

variables = stringpackage.ascii_lowercase
sentence_letters = stringpackage.ascii_uppercase
right_arrow = '>'
for_all = '@'
exists = '!'
equality = '='
and_op = '+'
or_op = '*'
negation = '-'
quantifiers = for_all + exists
binary_operators = and_op + or_op + equality + right_arrow + quantifiers
unary_operators = negation
operators = binary_operators + unary_operators


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
			translation[letter + variable] = '(' + letter + variable + ')'
	for key, value in translation.items():
		string = string.replace(key, value)

	# Add parens around quantifiers or the negation sign in front of a subexpression
	i = 0
	while i < len(string):
		two_character_window = string[i:i + 2]
		existential_with_variable = ['!' + x for x in variables]
		universal_with_variable = ['@' + x for x in variables]
		candidate_strings = ['-('] + existential_with_variable + universal_with_variable
		if two_character_window in candidate_strings:
			subexpression_right = find_matching_paren(string, start_index=i + 1)
			string = string[:i] + '(' + string[i:subexpression_right + 1] + ')' + string[subexpression_right + 1:]

			i += 1  # we need to move forward one index to stay in the same place because we added a parens to the left!
		i += 1
	return string


def pre_processing(string):
	string = string.replace(' ', '')
	string = add_parens(string)
	return string


def parser(string):
	if string == '':
		raise Exception("Empty string")
	tree = Node("root")
	i = 0
	while i < len(string):
		current_character = string[i]
		if current_character == '(':
			subexpression_left = i + 1
			subexpression_right = find_matching_paren(string, start_index=i)
			subexpression = string[subexpression_left:subexpression_right]
			parser(subexpression).parent = tree
			i = subexpression_right + 1
		elif current_character in operators + sentence_letters:
			new_tree = Node(current_character)
			new_tree.children = tree.children
			tree = new_tree
			i += 1
		elif current_character in variables:
			Node(current_character, parent=tree)
			i += 1
		else:
			raise Exception("Syntax error. Unknown character", current_character)
	return tree


def print_my_tree(tree):
	for pre, fill, node in RenderTree(tree):
		print("%s%s" % (pre, node.name))

def check_tree_syntax(tree):
	for node in LevelOrderIter(tree):
		name = node.name
		if name in sentence_letters:
			if len(node.children) != 1:
				raise Exception()
			variable = node.children[0]
			if variable.name not in variables:
				raise Exception
		if name in binary_operators:
			if len(node.children) != 2:
				raise Exception
		if name in unary_operators:
			if len(node.children) != 1:
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
					raise Exception("Unbound variable", variable)
				if candidate.name in quantifiers:
					if variable in [x.name for x in candidate.children]:
						found_quantifier = True
				candidate = candidate.parent
			if found_quantifier == False:
				raise Exception("Unbound variable", variable)


def generate_interpretations(tree):
	has_equality = False

	# use set() to find uniques
	variables_in_formula = set()
	sentence_letters_in_formula = set()
	for node in LevelOrderIter(tree):
		if node.name==equality:
			has_equality=True
		if node.name in variables:
			variables_in_formula.add(node.name)
		if node.name in sentence_letters:
			sentence_letters_in_formula.add(node.name)

	# convert to list so as to make subscriptable
	sentence_letters_in_formula = list(sentence_letters_in_formula)
	variables_in_formula = list(variables_in_formula)

	if sentence_letters_in_formula == []:
		partitions = {'Universe': True}
	else:
		letter_permutations = [i for i in itertools.product([True,False],repeat=len(sentence_letters_in_formula))]

		partitions = []
		for permutation_tuple in letter_permutations:
			permutation_dict = {}
			for i in range(len(sentence_letters_in_formula)):
				letter = sentence_letters_in_formula[i]
				truth_value = permutation_tuple[i]
				permutation_dict[letter] = truth_value
			partitions.append(permutation_dict)

	if has_equality:
		cardinality_permutations = [i for i in itertools.product(range(len(variables_in_formula)+1), repeat=len(partitions))]
	else:
		cardinality_permutations = [i for i in itertools.product([0,1], repeat=len(partitions))] #1 represents any cardinality greater than 0

	interpretation_eq_classes = []
	for permutation in cardinality_permutations:
		interpretation_eq_classes.append(list(zip(partitions, permutation)))

	# Printing (useful for debugging)
	'''
	eq_class_counter = 0
	for eq_class in interpretation_eq_classes:
		eq_class_counter += 1
		print('interpretation equivalence class', eq_class_counter)
		partition_member_counter = 0
		for element in eq_class:
			partition_member_description, partition_member_cardinality = element
			partition_member_counter += 1
			print('    member', partition_member_counter, 'of partition:', partition_member_description,
				  'has cardinality', partition_member_cardinality)
	'''

	interpretations = []
	for eq_class in interpretation_eq_classes:
		instantiation = instantiate_interpretation_equivalence_class(eq_class)
		if instantiation is not None:
			interpretations.append(instantiation)

	# Printing (useful for debugging)
	'''interpretation_counter = 0
	for interpretation in interpretations:
		interpretation_counter += 1
		print('interpretation',interpretation_counter,'with domain size',len(interpretation))
		for constant in interpretation.items():
			print(constant)'''
	return interpretations

def instantiate_interpretation_equivalence_class(equivalence_class):
	instantiated_interpretation = {}
	constant = 0
	for partition_element in equivalence_class:
		cardinality = partition_element[1]
		partition_element_description = partition_element[0]
		for j in range(cardinality):
			instantiated_interpretation['c'+str(constant)] = partition_element_description
			constant += 1
	if instantiated_interpretation != {}: #empty domains are not allowed
		return instantiated_interpretation

def check_tree_under_interpretation(node,interpretation):
	def replace_variable_with_constant_in_quantified_subtree(tree,constant):
		variable = tree.children[0].name
		expression = tree.children[1]
		for node in LevelOrderIter(expression):
			if node.name == variable:
				node.name = constant
		return tree

	if node.name == 'root':
		node = node.children[0]
	if node.name == '@':
		for constant in interpretation.keys():
			node = replace_variable_with_constant_in_quantified_subtree(node,constant)
			subtree = node.children[1]
			subtree_truth_value = check_tree_under_interpretation(subtree,interpretation)
			if subtree_truth_value == False:
				return False
		return True
	if node.name == '!':
		for constant in interpretation.keys():
			node = replace_variable_with_constant_in_quantified_subtree(node, constant)
			subtree = node.children[1]
			subtree_truth_value = check_tree_under_interpretation(subtree, interpretation)
			if subtree_truth_value == True:
				return True
		return False
	if node.name == '+':
		return check_tree_under_interpretation(node.children[0],interpretation) and check_tree_under_interpretation(node.children[1],interpretation)
	if node.name == '*':
		return check_tree_under_interpretation(node.children[0],interpretation) or check_tree_under_interpretation(node.children[1],interpretation)
	if node.name == '-':
		return not check_tree_under_interpretation(node.children[0],interpretation)
	if node.name == '=':
		return node.children[0].name == node.children[1].name
	if node.name in sentence_letters:
		letter = node.name
		constant = node.children[0].name
		return interpretation[constant][letter]

def check_tree_theoremhood(tree):
	interpretations = generate_interpretations(tree)
	for interpretation in interpretations:
		if check_tree_under_interpretation(tree,interpretation) == False:
			return {'Theoremhood':False, 'Counter-example':interpretation}
	return {'Theoremhood':True}


def main(string):
	string = pre_processing(string)
	print("string after pre-processing:", string)
	tree = parser(string)
	print_my_tree(tree)
	check_tree_syntax(tree)
	print(check_tree_theoremhood(tree))

# main('@x((-Ax+Dx) > (-(-Bx * Cx)))')
main('@x@y(-Bx*(Cx*Dx))')
main('@x(Ax>(Ax*Bx))')
main('@x(Px)')
main('@x!y(x=y)')