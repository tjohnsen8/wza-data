import requests
import json
import csv
import pandas as pd

get_data = 0
write_csv = 0

'''
Response
dict_keys(['AffiliateFilterValues', 'DisplayNation', 'Workouts', 
'WorkoutColumns', 'IsMultiLeaderboard', 'Athletes', 'ScoringGroupName', '
ScoringGroup', 'CountryFilterValues', 'HasAthletes'])

Athlete
dict_keys(['Wd', 'TotalPoints', 'Pending', 'Affiliate', 'Index', 
'CountryShortCode', 'Dnf', 'Name', 'CountryCode', 'WorkoutScores',
 'AvatarPath', 'PtcpID', 'Place'])

Workouts
key name : {... 'Res': result ...}
'workout_5606': wod2 num reps
'workout_5605': wod1 time
'workout_5607': wod3 weight
'''

workout_key_list = ['workout_5605', 'workout_5606', 'workout_5607']

def get_workout_result(ath_scores):
	workout_result = {}
	for workout_name in ath_scores:
		workout_json = ath_scores[workout_name]
		if workout_json['Res'] == '' or workout_json['Res'] == '-':
			res = 0
		elif workout_name == 'workout_5605':
			# translate time to seconds for easier math
			time = workout_json['Res'].split('<span>')[0]
			if ':' in time:
				minutes = time.split(':')[0]
				seconds = time.split(':')[1]
				res = float(minutes) * 60 + float(seconds)
			else:
				res = float(0)
		elif workout_name == 'workout_5606':
			# number of reps
			res = float(workout_json['Res'].split('<span>')[0])
		elif workout_name == 'workout_5607':
			# weight
			res = float(workout_json['Res'].split('<span>')[0])
		workout_result[workout_name] = res
	return workout_result

def get_data_from_leaderboard():
	# get updated data from website
	response = requests.get('https://qualifier.wodapalooza.com/events/1244/results/scoring-group/male_5032/json?')
	json_data = response.json()
	with open('wzadata.json', 'w') as outfile:
		json.dump(json_data, outfile)
	return json_data

def get_data_from_file():
	
	with open('wzadata.json', 'r') as infile:
		json_data = json.load(infile)
	return json_data

if __name__ == '__main__':
	if get_data:
		wzajson = get_data_from_leaderboard()
	else:
		wzajson = get_data_from_file()

	if write_csv:
		with open('wzascores.csv', 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=workout_key_list)
			writer.writeheader()
			for athlete in wzajson['Athletes']:
				ath_scores = get_workout_result(athlete['WorkoutScores'])
				writer.writerow(ath_scores)

	# open csv for shit
	wza_data = pd.read_csv('wzascores.csv', sep=',', header=0)
	print(wza_data.values)