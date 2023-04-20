# example input data
list1 = [{'Code': '00', 'Name': 'John'}, {'Code': '01', 'Name': 'Mary'}, {'Code': '03', 'Name': 'Peter'}]
list2 = [{'Code': '00', 'Age': 25}, {'Code': '02', 'Age': 30}, {'Code': '03', 'Age': 35}]

# create a set of all possible 'Code' values
possible_codes = set(['{:02d}'.format(code) for code in range(92)])

# create a dictionary from each input list where the keys are the 'Code' values
dict1 = {d['Code']: d for d in list1}
dict2 = {d['Code']: d for d in list2}

# merge the two dictionaries into a single dictionary
merged_dict = {}
for code in possible_codes:
    if code in dict1:
        merged_dict[code] = dict1[code]
    elif code in dict2:
        merged_dict[code] = dict2[code]

# convert the merged dictionary back into a list of dictionaries
merged_list = list(merged_dict.values())
merged_list = sorted(merged_list, key=lambda merged_list: merged_list['Code']) 
# print the result
print(merged_list)
