import json
import csv
from wza_data import write_data_to_csv

def get_json_data(division):
	with open('{}.json'.format(division)) as jsonfile:
		json_data = json.load(jsonfile)
	return json_data

def do_scaled():
	divisions = ['int_men', 'int_women']

	for division in divisions:	
		# get the data from the .json file
		json_data = get_json_data(division)

		# find the scaled athletes
		scaled_aths = []
		for athlete in json_data['Athletes']:
			scaled_ath = {}
			for workout in athlete['WorkoutScores']:
				score = athlete['WorkoutScores'][workout]
				if '(s)' in score['Res']:
					scaled_ath['Name'] = athlete['Name']
					scaled_ath['WorkoutScores'] = athlete['WorkoutScores']
					scaled_aths.append(scaled_ath)
					break

		if len(scaled_aths) > 0:
			write_data_to_csv('{}_scaled'.format(division), scaled_aths)

if __name__ == '__main__':
	do_scaled()