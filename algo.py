import toml
import os
import pdb

class Disease():
	def __init__(self,filename=''):
		self.name, self.file_extension = os.path.splitext(filename)
		self.path = self.name+self.file_extension	
		self.contents = self.read_file()
		if self.contents == None:
			return
		self.always_positive_ihc = set(map(str.lower,self.contents['always_positive_ihc']))
		self.always_negative_ihc = set(map(str.lower,self.contents['always_negative_ihc']))
		self.usually_positive_ihc = set(map(str.lower,self.contents['usually_positive_ihc']))
		self.usually_negative_ihc = set(map(str.lower,self.contents['usually_negative_ihc']))
		self.score = 0 

	def __str__(self):
		return self.name

	def read_file(self):		
		try:
			filedump = toml.load(self.path) #?.lower()			
			return filedump
		except:
			print('No contents in the file:',self.path)
			# Don't create an object for this disease
			return	

	def update_score(self,score):
		self.score = score

def search_diseases():
	# This function goes through the folder and returns disease objects
	temporary_list_of_diseases = []
	for file in os.listdir('.'):
		if file.endswith('.toml'):
			disease = Disease(file)
			temporary_list_of_diseases.append(disease)
	return temporary_list_of_diseases

def disease_eliminator(bloated_list,positives,negatives):
	# This function accepts a list of IHC results and excludes impossible diseases.
	
	# A dictinary (of disease and expected ihc) to remember the conflicting results used to exclude diseases.
	explanations_danger_pos = {}
	explanations_danger_neg = {}
	bloated_list = set(bloated_list)
	real_life_positives = positives
	real_life_negatives = negatives
	eliminated = []

	# go through the diseases
	for possible_disease in bloated_list:
		# Go through what the disease would normally always be positive for
		print("\ninspecting disease: ", possible_disease.name)
		# check if common elements to conflicting sets		
		danger_pos = real_life_positives.intersection(possible_disease.always_negative_ihc)

		if danger_pos:
			print('\texpected %s to be negative, but was positive.'%danger_pos)
			explanations_danger_pos[possible_disease.name] = str(danger_pos)

	
		# check if common elements to conflicting sets		
		danger_neg = real_life_negatives.intersection(possible_disease.always_positive_ihc)

		if danger_neg:
			print('\texpected %s to be positive, but was negative.'%danger_neg)
			explanations_danger_neg[possible_disease.name] = str(danger_neg)

		#If there are conflicting positive or negative stains, exclude the disease
		if danger_pos != set() or danger_neg != set():
			print('eliminated: ',possible_disease)
			eliminated.append(possible_disease)

	survived = bloated_list - set(eliminated)
	return survived, explanations_danger_pos, explanations_danger_neg

def disease_scorer(ddx_list,positives,negatives):
	# Takes a list of diseases and scores how many matched immuno results there are
	real_life_positives = positives
	real_life_negatives = negatives
	
	# 2 points for an 'always positive' major match, 1 point for a 'usually positive' minor match
	maj_pts = 2
	min_pts = 1
	
	ranked_list = {}
	
	# go through differentials
	for unranked_differential in ddx_list:
		print("\ninspecting differential: ", unranked_differential.name)
		
		# positives
		good_pos_major = real_life_positives.intersection(unranked_differential.always_positive_ihc)
		good_pos_minor = real_life_positives.intersection(unranked_differential.usually_positive_ihc)
		
		# negatives
		good_neg_major = real_life_negatives.intersection(unranked_differential.always_negative_ihc)
		good_neg_minor = real_life_negatives.intersection(unranked_differential.usually_negative_ihc)
		
		# Calculate arbitrary score
		points = maj_pts*len(good_pos_major)+min_pts*len(good_pos_minor)+maj_pts*len(good_neg_major)+min_pts*len(good_neg_minor)

		# Attach points to disease
		unranked_differential.update_score(points)
		
		# Add to ranking
		ranked_list[unranked_differential] = unranked_differential.score
		
	# return ranked_list # of the form {diseas:1, disease:2, disease:3}
	
	return ranked_list

def display_rankings(scoreboard):
	# accepts a the dictionary scoreboard, prints the ranked results
	
	ranked = sorted(scoreboard.items(), key=lambda kv: kv[1])
	for disease in ranked:
		print('\nCandidate: %s\n\tScore: %s\n---------------------'%(disease[0],disease[1]))

	
	print(done)	

def help_me_choose_ihc():
	# This function takes the list of possible diseases
	#  and suggests the IHC that would help solve the diagnosis.
	# Method: For the remaining diseases, go through the 'always'
	#  list and find the smallest non-ambiguous set of ihc to run.
	pass

def start_program():
	# This function sets up the problem and allows user to input known IHC
	# Type of input (undifferentiated lymphoid / follicles / other 'classic' problems)
	type_of_query = str(input("What do you have? \n1 = undifferentiated lymphoid\n2 = follicle thing\n3 = Some weird thingo\n--->  ")).lower()

	ihc_done_positive = []
	ihc_done_negative = []

	asking_for_ihc = True
	while asking_for_ihc:		
		ihc_entered = str(input("What IHC stains have you done? \n(no punctuation)\n(s to skip/begin)---> ")).lower()
		if ihc_entered=='s':
			asking_for_ihc = False
			break
		else: 
			ihc_result = str(input("+ or - ? ---> ")).lower()
			if ihc_result =='+':
				ihc_done_positive.append(ihc_entered)
			elif ihc_result == '-':
				ihc_done_negative.append(ihc_entered)
			else:
				print('oops typo, try again')
				pass

	list_of_diseases = search_diseases()
	candidate_diseases, eliminated_danger_pos, eliminated_danger_neg = disease_eliminator(list_of_diseases,set(ihc_done_positive),set(ihc_done_negative))

	for ddx in candidate_diseases:
		print('\nddx: ',ddx.name)
	
	if eliminated_danger_pos != set():			
		for killed_name,killed_ihc in eliminated_danger_pos.items():
			print('\t%s eliminated (we have positive %s, but needed negative)'%(killed_name,killed_ihc))
	if eliminated_danger_neg != set():	
		for killed_name,killed_ihc in eliminated_danger_neg.items():
			print('\t%s eliminated (we have negative %s, but needed positive)'%(killed_name,killed_ihc))

	scoreboard = disease_scorer(candidate_diseases,set(ihc_done_positive),set(ihc_done_negative))
	display_rankings(scoreboard)

start_program()

