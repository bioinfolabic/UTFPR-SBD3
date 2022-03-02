import json



with open("cv_split_data.json", "r") as file:
	data = json.load(file)
	for k_fold in range(10):
		train = data[str(k_fold)]['train']
		test = data[str(k_fold)]['test'] 

		print("FOLD "+str(k_fold+1)+ " train: "+str(len(train))+ " test: " + str(len(test)))
