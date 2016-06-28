import os.path

#---------------------------------------------------------------------------------------------------------
class Column_file:
    #input file as instance object
    #empty array to be appended with n instance objecs of Column_as_list
    #where n is the number of columns in the input data file
    #empty dictionary to contain the output of comparison between user specified columns

    #initialise the panel class
    def __init__(self, input_file):
	assert (os.path.isfile(input_file)), 'input file can not be found! Check filepath is accurate'
        print 'Input file is: ' + str(input_file)
	self.input_file = input_file
	self.column_objects = []
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
	    header_count = len(headers_list)
	    print 'The following ' + str(header_count) + ' columns have been identified and' 
            print 'their contents appended to dictionary values as an array: '
	    for header in headers_list:
	        self.column_objects.append(Column_as_list(header))
		print '    ' + header
	    for line in f:
	        assert ('\t' in line and ',' not in line), 'Input file is not tab delimited and has been incorrectly split into columns see: ' + line
		line = line.strip('\n\r').split('\t')
	        for idx, item in enumerate(line):
		    remainder = idx % header_count
		    #print str(idx) + ' ' + str(item) + ' ' + str(remainder)
		    assert(remainder == idx), line + ' has more columns than headers and the extra column cannot be classified. Please romeve additional data or add a column header'
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
	self.comparison_output = {}
	print 'The following columns have been selected for comparison with each other:'
	print '    ' + self.column_objects[first_column].name
	print '    ' + self.column_objects[second_column].name
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

class Test_functions:
    def __init__(self, input_test_file):
        self.input_test_file = input_test_file

    def comparison_test(self):
	test_panel_list = Column_file(self.input_test_file)
	test_panel_list.load_to_list()
	c0_0 = test_panel_list.compare(0,0)
	for key, value in c0_0.iteritems():
	    assert (key == 'Illumina_Trusight_one_clinical_exome vs Illumina_Trusight_one_clinical_exome')
	    assert (not value[0])
	    assert (not value[1])
	    assert ("A2M" and "A4GALT" and "A4GNT" and "AAAS" and "AADAC" in value[2]) 
	c0_1 = test_panel_list.compare(0,1)
	for key, value in c0_1.iteritems():
	    assert ("AAAS" and "AADAC" in value[0])
	    assert ("A2M-AS1" and "A2ML1" in value[1])
	    assert ("A2M" and "A4GALT" and "A4GNT" in value[2])
	c0_2 = test_panel_list.compare(0,2)
	for key, value in c0_2.iteritems():
	    assert ("A4GALT" and "A4GNT" and "AAAS" and "AADAC" in value[0])
	    assert ("A1BG" and "A1BG-AS1" and "A2M-AS1" and "A1CF" in value[1])
	    assert ("A2M" in value[2])
	c0_3 = test_panel_list.compare(0,3)
	for key, value in c0_3.iteritems():
            assert ("A4GALT" and "A4GNT" and "AAAS" and "AADAC" in value[0])
            assert ("A1BG" and "A1BG-AS1" and "A2M-AS1" and "A1CF" in value[1])
            assert ("A2M" in value[2])
	c1_0 = test_panel_list.compare(1,0)
	for key, value in c1_0.iteritems():
            assert ("A2M-AS1" and "A2ML1" in value[0])
            assert ("AAAS" and "AADAC" in value[1])
            assert ("A2M" and "A4GALT" and "A4GNT" in value[2])
	c1_1 = test_panel_list.compare(1,1)
	for key, value in c1_1.iteritems():
	    assert (not value[0])
            assert (not value[1])
	    assert ("A2M" and "A2M-AS1" and "A2ML1" and "A4GALT" and "A4GNT" in value[2])
	c1_2 = test_panel_list.compare(1,2)
	for key, value in c1_2.iteritems():
	    assert ("A2ML1" and "A4GALT" and "A4GNT" in value[0])
            assert ("A1BG" and "A1BG-AS1" and "A1CF" in value[1])
            assert ("A2M" and "A2M-AS1" in value[2])
	c1_3 = test_panel_list.compare(1,3)
        for key, value in c1_3.iteritems():
	    assert ("A2M-AS1" and "A2ML1" and "A4GALT" and "A4GNT" in value[0])
            assert ("A1BG" and "A1BG-AS1" and "A1CF" in value[1])
            assert ("A2M" and "A2M-AS1" in value[2])
	c2_0 = test_panel_list.compare(2,0)
	for key, value in c2_0.iteritems():
	    assert ("A1BG" and "A1BG-AS1" and "A2M-AS1" and "A1CF" in value[0])
            assert ("A4GALT" and "A4GNT" and "AAAS" and "AADAC" in value[1])
            assert ("A2M" in value[2])
	c2_1 = test_panel_list.compare(2,1)
        for key, value in c2_1.iteritems():
	    assert ("A1BG" and "A1BG-AS1" and "A1CF" in value[0])
            assert ("A2ML1" and "A4GALT" and "A4GNT" in value[1])
            assert ("A2M" and "A2M-AS1" in value[2])
	c2_2 = test_panel_list.compare(2,2)
        for key, value in c2_2.iteritems():
            assert (not value[0])
            assert (not value[1])
            assert ("A2M" and "A2M-AS1" and "A1CF" and "A1B-AS1" and "A1BG" in value[2])
	c2_3 = test_panel_list.compare(2,3)
        for key, value in c2_3.iteritems():
	    assert (not value[0])
            assert (not value[1])
            assert ("A2M" and "A2M-AS1" and "A1CF" and "A1B-AS1" and "A1BG" in value[2])
	c3_0 = test_panel_list.compare(3,0)
        for key, value in c3_0.iteritems():
            assert ("A1BG" and "A1BG-AS1" and "A2M-AS1" and "A1CF" in value[0])
            assert ("A4GALT" and "A4GNT" and "AAAS" and "AADAC" in value[1])
            assert ("A2M" in value[2])	    
	c3_1 = test_panel_list.compare(3,1)
	for key, value in c3_1.iteritems():
            assert ("A1BG" and "A1BG-AS1" and "A1CF" in value[0])
            assert ("A2M-AS1" and "A2ML1" and "A4GALT" and "A4GNT" in value[1])
            assert ("A2M" and "A2M-AS1" in value[2])	    
	c3_2 = test_panel_list.compare(3,2)
	for key, value in c3_2.iteritems():
	    assert (not value[0])
            assert (not value[1])
            assert ("A2M" and "A2M-AS1" and "A1CF" and "A1B-AS1" and "A1BG" in value[2])
	c3_3 = test_panel_list.compare(3,3)
	for key, value in c3_3.iteritems():
	    assert (not value[0])
            assert (not value[1])
	    assert ("A2BG" and "A1BG-AS1" and "A1CF" and "A2M" and "A2M-AS1")

if __name__ == "__main__":
    test_class = Test_functions("test_file.txt")
    comparison_test = test_class.comparison_test()
    #panel_lists = Column_file("master_panels.txt")
    #panel_lists.load_to_list()
    #x = panel_lists.compare(1,3)
    #x = panel_lists.compare(1,2)
    #for key,value in x.iteritems():
	#print 'comparison' + key
	#print len(value[1])
	#in_v6_not_rde = value[1]


