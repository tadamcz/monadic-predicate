sentence_letters = 'PQRS'
from anytree import Node, RenderTree, LevelOrderIter
import itertools
def create_equivalence_classes(letters):
	partitions = Node('Universe')
	for letter in letters:
		for eq_class in partitions.leaves:
			inters_letter = Node('inters')
			inters_letter.children = [Node(letter)]

			minus_letter = Node('minus')
			minus_letter.children = [Node(letter)]

			inters_letter.parent = eq_class
			minus_letter.parent = eq_class

	for pre, fill, node in RenderTree(partitions):
		print("%s%s" % (pre, node.name))

	eq_class_descriptions = []
	for node in partitions.leaves:
		eq_class_description = [node.name for node in node.path]
		eq_class_descriptions.append(eq_class_description)

	emptiness_permutations = [i for i in itertools.product(['Empty', 'Nonempty'], repeat=len(partitions.leaves))]
	interpretation_eq_classes = []
	for permutation in emptiness_permutations:
		interpretation_eq_classes.append(zip(eq_class_descriptions,permutation))

	eq_class_counter = 0
	for eq_class in interpretation_eq_classes:
		eq_class_counter += 1
		print('interpretation equivalence class',eq_class_counter)
		partition_member_counter = 0
		for element in eq_class:
			partition_member_description,partition_member_emptiness = element
			partition_member_counter += 1
			print('    member',partition_member_counter,'of partition:',partition_member_description,'is',partition_member_emptiness)
	return interpretation_eq_classes

create_equivalence_classes(sentence_letters)
