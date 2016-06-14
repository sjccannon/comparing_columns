#---------------------------------------------------------------------------------------------------------
class Column_file:
    #input file as instance object
    #empty array to be appended with n instance objecs of Column_as_list
    #where n is the number of columns in the input data file
    #empty dictionary to contain the output of comparison between user specified columns

    #initialise the panel class
    def __init__(self, input_file):
	self.input_file = input_file
	self.column_objects = []
	self.comparison_output = {}
#---------------------------------------------------------------------------------------------------------
    #reads input file, creates a Column_as_list object for each column,
    #returns instance objects array
    #opens the user specified input file
    #reads first line of input file, removes newline characters and splits by whitespeace
    #iterates through column headers
    #appends a Column_as_list object to the column_objects array instance
    #with the column header as 'name'
    #iterates through remaining lines in the file (not header)
    #iterates each item and it's position in each line using enumerate() whilst
    #stripping newline characters and splitting by tab characters
    #rejects null values as columns are varying lengths
    #appends the item to its respective Column_as_list object in the column_objects array
    #returns column_objects array

    def load_to_list(self):
	with open(self.input_file, "r") as f: 
	    headers_list = f.readline().strip('\n\r').split()
	    for header in headers_list:
	        self.column_objects.append(Column_as_list(header))
	    for line in f:
	        for idx, item in enumerate(line.strip('\n\r').split('\t')):
		    if item:
		    	self.column_objects[idx].add_list_item(item)
	return self.column_objects
#----------------------------------------------------------------------------------------------------------
    #user specifies which columns are required for comparison
    #creates a set the column array for each column to be compared
    #subtracts contents of each set to identify vlaues uniqu to each set
    #calculates shared values
    #appends comparison_output dictionary instance in format      
    #{ 'column_a vs column_b' : [[unique to column_a], [unique to column_b], [shared in both columns]]}
    #returns comparison_output dictionary instance

    def compare(self, first_column, second_column):
	set_one = set(self.column_objects[first_column].column_items)
	set_two = set(self.column_objects[second_column].column_items)
	uniq_to_one = set_one - set_two
	uniq_to_two = set_two - set_one
	shared = set_one & set_two
	self.comparison_output[str(self.column_objects[first_column].name) + ' vs ' + str(self.column_objects[second_column].name)] = [list(uniq_to_one), list(uniq_to_two), list(shared)]
        return self.comparison_output
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#models each column in the file as a list

class Column_as_list:
    def __init__(self, panel_name):
	self.name = panel_name
	self.column_items = []
#---------------------------------------------------------------------------------------------------------
#adds specified item to the instance array

    def add_list_item(self, item):
	self.column_items.append(item)	
	return self.column_items
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    panel_lists = Column_file("master_panels.txt")
    panel_lists.load_to_list()
    print panel_lists.compare(2,3)

