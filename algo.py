import toml
import os

class Disease():
	def __init__(self,filename=''):
		self.name = filename.strip('.toml')
		self.filename = filename 		
		try:
			self.contents = toml.load(filename)
		except:
			print('No contents in the file:',self.filename)
			# Don't create an object for this disease
			return	
		self.always_positive_ihc = [self.contents['always_positive_ihc']]
		self.always_negative_ihc = [self.contents['always_negative_ihc']]
		self.usually_positive_ihc = [self.contents['usually_positive_ihc']]
		self.usually_negative_ihc = [self.contents['usually_negative_ihc']]


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
	explanations_needed_positive = {}
	explanations_needed_negative = {}
	# go through the diseases
	for possible_disease in bloated_list:
		# Go through what the disease would normally always be positive for
		for expected_positive in possible_disease.always_positive_ihc:
			# if it was actually negative
			if expected_positive in negatives:
				# expel
				bloated_list.remove(possible_disease)	
				# add explanation	
				explanations_needed_positive[possible_disease] = expected_positive	
		# Go through what the disease would normally always be negative for
		for expected_negative in possible_disease.always_negative_ihc:
			# if it was actually negative
			if expected_negative in positive:
				# expel
				bloated_list.remove(possible_disease)	
				# add explanation
				explanations_needed_negative[possible_disease] = expected_negative

	return bloated_list, explanations_needed_positive, explanations_needed_negative

def disease_scorer():
	# Takes a list of diseases and scores how many matched immuno results there are
	pass

def help_me_choose_ihc():
	# This function takes the list of possible diseases
	#  and suggests the IHC that would help solve the diagnosis.
	# Method: For the remaining diseases, go through the 'always'
	#  list and find the smallest non-ambiguous set of ihc to run.
	pass

def start_program():
	# This function sets up the problem and allows user to input known IHC
	# Type of input (undifferentiated lymphoid / follicles / other 'classic' problems)
	type_of_query = str(input("What do you have? \n1 = undifferentiated lymphoid\n2 = follicle thing\n3 = Some weird thingo\n--->  "))

	ihc_done_positive = []
	ihc_done_negative = []

	asking_for_ihc = True
	while asking_for_ihc:
		ihc_entered = str(input("What IHC stains have you done? \n(enter in lowercase, no punctuation)\n(s to skip/begin)---> "))
		if ihc_entered=='s':
			asking_for_ihc = False
			break
		else: 
			ihc_result = str(input("+ or - ? ---> "))
			if ihc_result =='+':
				ihc_done_positive.append(ihc_entered)
			elif ihc_result == '-':
				ihc_done_negative.append(ihc_entered)
			else:
				print('oops typo, try again')
				pass

	list_of_diseases = search_diseases()
	candidate_diseases, eliminated_needed_positive, eliminated_needed_negative = disease_eliminator(list_of_diseases,ihc_done_positive,ihc_done_negative)

	print(candidate_diseases,'in the running')
	print(eliminated_needed_positive,'eliminated, needed positive')
	print(eliminated_needed_negative,'eliminated, needed negative')	




start_program()