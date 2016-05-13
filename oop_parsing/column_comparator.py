class Column_file:

    list_instances = 0

    #initialise the panel class
    def __init__(self, input_file):
	self.input_file = input_file
	self.column_objects = []
	self.comparison_output = {}

    def load(self):
	with open(self.input_file, "r") as f: 
	    headers_list = f.readline().strip('\n\r').split()
	    for header in headers_list:
	        self.column_objects.append(Column_as_list(header))
		self.list_instances += 1
	    for line in f:
	        for idx, item in enumerate(line.strip('\n\r').split('\t')):
		    #reject null values
		    if item:
		    	self.column_objects[idx].add_list_item(item)
	return self.column_objects

    def compare(self, first_column, second_column):
	set_one = set(self.column_objects[first_column].column_items)
	set_two = set(self.column_objects[second_column].column_items)
	uniq_to_one = set_one - set_two
	uniq_to_two = set_two - set_one
	shared = set_one & set_two
	self.comparison_output[str(self.column_objects[first_column].name) + ' vs ' + str(self.column_objects[second_column].name)] = [list(uniq_to_one), list(uniq_to_two), list(shared)]
        return self.comparison_output

class Column_as_list:
    def __init__(self, panel_name):
	self.name = panel_name
	self.column_items = []

    def add_list_item(self, item):
	self.column_items.append(item)	
	return self.column_items

if __name__ == "__main__":
    panel_lists = Column_file("master_panels.txt")
    panel_lists.load()
    print panel_lists.compare(0,1)

