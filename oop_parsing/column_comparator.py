class Panels:

    def __init__(self, input_file):
	self.input_file = input_file
	self.gene_list_objects = []
	self.comparison_output = {}

    #Panels.load()
    #opens the input file
    #takes each header and initialises each as the first element

    def load(self):
	with open(self.input_file, "r") as in_file: 
	    headers_list = in_file.readline().strip('\n\r').split()
	    print headers_list
	    for panel_name in headers_list:
	        self.gene_list_objects.append(Gene_list(panel_name))
	    for line in in_file:
	        for idx, gene_name in enumerate(line.strip('\n\r').split('\t')):
		    #add code to reject null values
		    self.gene_list_objects[idx].add_gene(gene_name)
	return self.gene_list_objects

    def compare(self, first_gene_list, second_gene_list):
	set_one = set(self.gene_list_objects[first_gene_list].genes)
	set_two = set(self.gene_list_objects[second_gene_list].genes)
	print "set one length %s" %len(set_one)
	print "set two length %s" %len(set_two)
	uniq_to_one = set_one - set_two
	print "uniq to one length %s" %len(uniq_to_one)
	uniq_to_two = set_two - set_one
	print "uniq to two length %s" %len(uniq_to_two)
	shared = set_one & set_two
	print "shared %s" %len(shared)
	#make a dictionary to include names: 1,2,3
	#key self.gene_list_objects[list_one]
	self.comparison_output[self.gene_list_objects[0].name] = uniq_to_one
	#comparison_output = [list(uniq_to_one), list(uniq_to_two), list(shared)]
#	for idx, item in enumerate(comparison_output[1]):
		#print str(idx) + ' ' + item
        return self.comparison_output

class Gene_list:
    def __init__(self, panel_name):
	self.name = panel_name
	self.genes = []

    def add_gene(self, gene_name):
	self.genes.append(gene_name)	
	return self.genes

if __name__ == "__main__":
    panel_lists = Panels("master_panels.txt")
    panel_lists.load()
    print panel_lists.compare(0,1)


'''
READ_ME
Panels class
    initialise function
    the input file as an instance object
    an empty list to be populated with Gene_list objects

    load function
    reads in the input_file into a list of gene_panel objects
    iterates through each row and, splits by white space into colunms
    iterates through each column, in each line using enuerate to index iterations
    adds each iteration to the appropriate gene list object (in the gene list class)
	using the  based on the gene_list_object (in the Gene_list class index

      - sections removed -
     1  add prefix to the filename, must be in cwd, could be usefule if need to store file path as an object
        prefix = os.getcwd()
        file = str(prefix) + "/" + str(self.input_file)
     2  took out below list comprehension in favour of nested list
        for row in(column.strip('\n\r').split('\t')) for column in gene_panels):

Gene_list class
    init
    the name of the Gene_list
    an empty list of genes to be appended by the add_gene function
    
    add_gene function
    appends gene_to the genes list  

'''


