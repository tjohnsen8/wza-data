import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

get_data = 0
show_data = 1
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
csv_headers = ['Name', 'WOD 1', 'WOD 2', 'WOD 3']
workout_key_map = {'workout_5605' : 'WOD 1', 
				   'workout_5606' : 'WOD 2', 
				   'workout_5607' : 'WOD 3'}
wza_divison_names = ['elite_men', 'elite_women', 'int_men', 'int_women']
wza_division_urls = {'elite_men': 'https://qualifier.wodapalooza.com/events/1244/results/scoring-group/male_5031/json?', 
					 'elite_women': 'https://qualifier.wodapalooza.com/events/1244/results/scoring-group/female_5809/json?', 
					 'int_men': 'https://qualifier.wodapalooza.com/events/1244/results/scoring-group/male_5032/json?', 
					 'int_women' : 'https://qualifier.wodapalooza.com/events/1244/results/scoring-group/female_5810/json?'}

def plot_workout_1(wod1, division):
	wod1.hist(grid=True, bins='auto', rwidth=0.9, color='#607c8e')
	plt.text(1000, 80, wod1.describe())
	def fmtsec(x,pos):
		return "{:02d}:{:02d}".format(int(x//60), int(x%60))
	plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(fmtsec))
	# Use nice tick positions as multiples of 30 seconds
	plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(60))
	plt.xlabel('time')
	plt.ylabel('frequency')
	plt.title('wza wod1 {}'.format(division))
	plt.show()

def plot_workout_2(wod2, division):
	wod2.hist(grid=True, bins=48, rwidth=0.9, color='#607c8e')
	plt.text(33, 50, wod2.describe())
	#wod3.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
	#plt.text(300, 80, wod3.describe())
	plt.xlabel('reps')
	plt.ylabel('frequency')
	plt.title('wza wod2 {}'.format(division))
	#wod3.hist(bins=50)
	plt.show()

def plot_workout_3(wod3, division):
	wod3.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
	plt.text(300, 80, wod3.describe())
	plt.xlabel('weight')
	plt.ylabel('frequency')
	plt.title('wza wod3 {}'.format(division))
	#wod3.hist(bins=50)
	plt.show()

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
		workout_result[workout_key_map[workout_name]] = res
	return workout_result

def get_data_from_leaderboard(division, url):
	# get updated data from website
	response = requests.get(url)
	json_data = response.json()
	with open('{}.json'.format(division), 'w') as outfile:
		json.dump(json_data, outfile)
	return json_data

def get_data_from_file():
	with open('wzadata.json', 'r') as infile:
		json_data = json.load(infile)
	return json_data

def write_data_to_csv(division, athletes):
	with open('{}.csv'.format(division), 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
			writer.writeheader()
			for athlete in athletes:
				ath_scores = get_workout_result(athlete['WorkoutScores'])
				ath_scores['Name'] = athlete['Name']
				writer.writerow(ath_scores)

def get_all_results():
	# loop through the divisions and get the results
	for division, url in wza_division_urls.items():
		json_data = get_data_from_leaderboard(division, url)
		write_data_to_csv(division, json_data['Athletes'])


if __name__ == '__main__':
	
	if get_data:
		get_all_results()
	
	# viz data
	if show_data:
		for division in wza_divison_names:
			wza_data = pd.read_csv('{}.csv'.format(division), sep=',', header=0)
			# remove 0 scores
			wod1 = wza_data.loc[:,csv_headers[1]]
			wod2 = wza_data.loc[:,csv_headers[2]]
			wod3 = wza_data.loc[:,csv_headers[3]]
			wod1 = wod1[wod1 > 0]
			wod2 = wod2[wod2 > 0]
			wod3 = wod3[wod3 > 0]
			plot_workout_1(wod1, division)
			plot_workout_2(wod2, division)
			plot_workout_3(wod3, division)