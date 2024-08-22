from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import re

patterns = {
	"film_description": r'FILM\s+DESCRIPTION(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"clip_description": r'CLIP\s+DESCRIPTION(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"cast": r'CAST(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"copyright": r'CREDIT(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"producer": r'PRODUCER(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"director": r'DIRECTOR(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)',
	"screenwriter": r'SCREE(N)?WRITER(S)?:\s*(\n|\\n)?(.*?)\s*(\n|\\n)'
}

title_pattern = r'^(.*?) \((\d{4})\)$'
query_pattern_1 = r'^(.*?) Scene$'
query_pattern_2 = r'^(.*?) Scene \((\d+)\/(\d+)\)'

list_type = {"cast", "producer", "director", "screenwriter"}

def title_parsing(full_title):
	dash_splits = full_title.split(' - ')
	if dash_splits[0][-6] == '(' and dash_splits[0][-5:-1].isdigit():
		return dash_splits[0], ' - '.join(dash_splits[1:])
	else:
		return dash_splits[-1], ' - '.join(dash_splits[:-1])
	
def potential_clip_description(descriptions):
	clip_description = ''
	for i in range(len(descriptions) - 17):
		if descriptions[i : i + 13] == "BUY THE MOVIE":
			j = i - 1
			if descriptions[j] == '\n':
				j -= 1
			if descriptions[j - 1 : j + 1] == '\\n':
				j -= 2
			while j >= 0 and descriptions[j] != '\n' and descriptions[j] != ':' and descriptions[j - 1 : j + 1] != '\\n' and descriptions[j - 1 : j + 1] != "='" and descriptions[j - 1 : j + 1] != '="' and descriptions[j - 1 : j + 1] != '"':
				if descriptions[j - 5] == '\\' and descriptions[j - 4] == 'u':
					clip_description = bytes(r"\u" + descriptions[j - 3 : j + 1], "utf-8").decode("unicode-escape") + clip_description
					j -= 6
				else:
					if descriptions[j] != '\\':
						clip_description = descriptions[j] + clip_description
					j -= 1
			if clip_description[0] == ' ':
				return clip_description[1:]
			return clip_description
	return clip_description

def clean(descriptions):
	result, j = '', 0
	while j < len(descriptions):
		if j < len(descriptions) - 5 and descriptions[j] == '\\' and descriptions[j + 1] == 'u':
			result += bytes(r"\u" + descriptions[j + 2 : j + 6], "utf-8").decode("unicode-escape")
			j += 6
		else:
			if descriptions[j] != '\\':
				result += descriptions[j]
			j += 1
	return result

def movieclips_scraping():
	driver = webdriver.Chrome()
	for year in range(2020, 2025):
		json_file = f'movieCLIP_dataset_{year}.json'
		title_to_url = dict()
		f = open(f'video_info_{year}.txt', 'r')
		lines = f.readlines()
		for line in lines:
			try:
				title_to_url[line.split(' | Movieclips: ')[0]] = line.split(' | Movieclips: ')[1]
			except:
				pass
			
		for full_title in title_to_url:
			json_dict = dict()
			if os.path.exists(json_file):
				with open(json_file, 'r') as file:
					json_dict = json.load(file)
		
			if full_title.replace('/', '_') in json_dict:
				continue

			if len(json_dict) % 40 == 39:
				driver.quit()
				driver = webdriver.Chrome()		
        
			url = title_to_url[full_title].split('\n')[0]
			id = url.split('?')[1].split('&')[0][2:]

			driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url))
			content = driver.page_source.encode('utf-8').strip()
			descriptions = str(BeautifulSoup(content, 'lxml'))
			
			title, query = title_parsing(full_title)
			full_title = full_title.replace('/', '_')
			json_dict[full_title] = {"id": id, "year": year, "url": url}
			
			for pattern in patterns:
				all = re.findall(patterns[pattern], descriptions, re.IGNORECASE)
				if len(all):
					if pattern in list_type:
						json_dict[full_title][pattern] = clean(max(all[0], key=len)).split(', ')
					else:
						json_dict[full_title][pattern] = clean(max(all[0], key=len))
				else:
					if pattern == 'clip_description':
						json_dict[full_title][pattern] = potential_clip_description(descriptions)
					elif pattern in list_type:
						json_dict[full_title][pattern] = []
					else:
						json_dict[full_title][pattern] = ''
				
			match = re.match(title_pattern, title)
			if match:
				group = match.groups()
				title, release_year = group[0].strip(), group[1]
			else:
				title = title.strip()
				match = re.match(title_pattern, json_dict[full_title]["copyright"])
				if match:
					group = match.groups()
					release_year = group[1]
			display_title = f'{title} {release_year}'
			match = re.match(query_pattern_2, query)
			if match:
				group = match.groups()
				query, scene, total_scene = group[0].strip(), group[1], group[2]
				title = f'{title} ({scene}/{total_scene}) - {release_year}'
			else:
				match = re.match(query_pattern_1, query)
				if match:
					group = match.groups()
					query = group[0].strip()
				else:
					query = query.strip()
				title = f'{title} - {release_year}'
			json_dict[full_title]["title"] = title
			json_dict[full_title]["query"] = query
			json_dict[full_title]["display_title"] = display_title

			with open(json_file, 'w', encoding="utf-8") as file:
				json.dump(json_dict, file, indent=3, ensure_ascii=False)

movieclips_scraping()
