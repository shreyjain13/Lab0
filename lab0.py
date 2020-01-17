from lab0_utilities import *
	
class Languages:
	def __init__(self):
		self.data_by_year = {}

	def build_trees_from_file(self, file_object):
		text = file_object.readlines()
		for i in range(1, len(text)): 
			line = text[i].split(",") 
			values = LanguageStat(line[1], int(line[0]), int(line[2]))
			data = Node(values)
			if int(line[0]) not in self.data_by_year: 
				self.data_by_year[int(line[0])] = BalancingTree(data)
			else: 
				self.data_by_year[int(line[0])].balanced_insert(data)
		
		return self.data_by_year		 

	def query_by_name(self, language_name):
		language_count = {}
		for (years, tree) in self.data_by_year.items(): 
			(final,count) = tree.search(language_name)
			if final == True: 
				language_count[years] = count 
		
		return language_count 
	
	def query_by_count(self, threshold = 0):		
		language_count = {}
		for (years, tree) in self.data_by_year.items(): 
			result = []
			self.traverse(tree.root, threshold, result)
			language_count[years] = result
		return language_count 
	
	def traverse(self, curr_node, threshold, result= []): 
		if curr_node == None:
			return
		if curr_node.val.count > threshold: 
			result.append(curr_node.val.name)
		self.traverse(curr_node.left, threshold, result)
		self.traverse(curr_node.right, threshold, result)
		return result 

class BalancingTree:
	def __init__(self, root_node):
		self.root = root_node
	
	def balanced_insert(self, node, curr = None):
		curr = curr if curr else self.root
		self.insert(node, curr)
		self.balance_tree(node)

	def insert(self, node, curr = None):
		curr = curr if curr else self.root
		# insert at correct location in BST
		if node._val < curr._val:
			if curr.left is not None:
				self.insert(node, curr.left)
			else:
				node.parent = curr
				curr.left = node
		else:
			if curr.right is not None:
				self.insert(node, curr.right)
			else:
				node.parent = curr
				curr.right = node
		return


	def balance_tree(self, node):
		current = node
		p = None
		
		while current != None:
			self.update_height(current)
			current.bf = self.find_balance_factor(current)
			if not abs(current.bf) < 2:
				p = current
				if p.bf >=2:
					child = p.right
					if child.bf >= 0:
						self.left_rotate(p)
					else:
						self.right_rotate(child)
						self.left_rotate(p)
				else:
					child = p.left
					if  child.bf <= 0:
						self.right_rotate(p)
					else:
						self.left_rotate(child)
						self.right_rotate(p)					
			else:
				current = current.parent
			
									
	def update_height(self, node):
		node.height = 1 + max(self.height(node.left), self.height(node.right))

	def height(self, node):
		return node.height if node else -1


	def left_rotate(self, z):
		y = z.right
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y
		z.right = y.left
		if z.right is not None:
			z.right.parent = z
		y.left = z
		z.parent = y
		self.update_height(z)
		
		self.update_height(y)
		z.bf = self.find_balance_factor(z)
		y.bf = self.find_balance_factor(y)


	def right_rotate(self, z):
		y = z.left
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.right is z:
				y.parent.right = y
			elif y.parent.left is z:
				y.parent.left = y
		z.left = y.right
		if z.left is not None:
			z.left.parent = z
		y.right = z
		z.parent = y
		self.update_height(z)
		z.bf = self.find_balance_factor(z)
		self.update_height(y)	
		y.bf = self.find_balance_factor(y)		
		
	def find_balance_factor(self, node):
		if node.right == None: 
			right = 0
		else: 
			right = node.right.height+1
		if node.left == None: 
			left = 0 
		else:
			left = node.left.height+1
		bf = right - left
		return bf 
		
	def is_balanced(self):
		if self.find_balance_factor(self.root) > 1 or self.find_balance_factor(self.root) < -1: 
			return False
		else: 
			return True 
	def search(self, val): 
		results = self.searchhelper(self.root, val)
		return results 
	
	def searchhelper(self, curr_node, val):
		if curr_node == None: 
		    return False, None  
		elif curr_node.val.name == val:
		    return True, curr_node.val.count 
		elif val < curr_node.val.name:
		    return self.searchhelper(curr_node.left, val) 
		elif val > curr_node.val.name:
		    return self.searchhelper(curr_node.right, val)
	