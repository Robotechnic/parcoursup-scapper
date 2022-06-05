LOGIN_URL = "https://dossierappel.parcoursup.fr/Candidat/authentification"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"

import os
import requests
import re
import json
import time
from bs4 import BeautifulSoup

config = os.environ

def get_wishes(username : str, password : str) -> str:
	"""
	Get the cookies for the connection to the dossier appel website.

	Args:
		username(str): The username of the user.
		password(str): The password of the user.

	Returns:
		str: The page content of the dossier appel website.
	"""
	headers = {
		"User-Agent": USER_AGENT,
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
	}
	
	# get the page for csrf token
	r = requests.get(LOGIN_URL, headers=headers)
	session_id = r.cookies["JSESSIONID"]
	csrf = re.search(f"id=\"CSRFToken\" value=\"(.*)\"", r.text).group(1)

	payload = {
		"ACTION": "1",
		"usermobile": "false",
		"CSRFToken": csrf,
		"g_cn_cod": username,
		"g_cn_mot_pas": password
	}

	cookies = {
		"JSESSIONID": session_id,
	}

	# post the login form
	r = requests.post(LOGIN_URL, data=payload, headers=headers, cookies=cookies)
	return r.text

def get_results(page_content : str) -> dict:
	"""
	Get the results of the dossier appel.

	Args:
		page_content(str): The page content of the dossier appel website.
		
	Returns:
		dict: The results of the dossier appel.
	"""
	soup = BeautifulSoup(page_content, "html.parser")
	results = {}
	admissions = soup.find("div", {"id": "div-tableau-voeux-admission"})
	if not admissions:
		print("Error: No admissions found.")
		return
	
	wishes = admissions.find_all("tr", {"class": "voeu"})
	print(f"Found {len(wishes)} wishes.")

	for wish in wishes:
		name = wish.find_all("td")[2].text.strip()
		if re.findall(r"avec internat", name):
			rang = wish.find_all("span", {"class": "strong"})[2].text
		else:
			rang = wish.find("span", {"class": "strong"}).text
		
		results[name] = [int(rang)]
	
	return results

def load_previous_data() -> dict:
	"""Try to load data.json

	Returns:
		dict: the loaded data
	"""
	try:
		with open("data.json", "r") as f:
			return json.load(f)
	except FileNotFoundError as e:
		pass
	except json.decoder.JSONDecodeError as e:
		pass

	return dict()

def save_data(data : dict) -> None:
	"""save dictionary to data.json

	Args:
		data (dict): the data to save into the dictionary
	"""
	with open("data.json", "w") as f:
		json.dump(data, f, indent=4, ensure_ascii=False)

def merge(dict1 : dict, dict2 : dict) -> None:
	"""Merge the two dict passed in parameters

	Args:
		dict1 (dict): the dict to merge into
		dict2 (dict): the dict to merge
	"""
	for key, value in dict2.items():
		if key not in dict1:
			dict1[key] = []
		
		dict1[key] += value


if __name__ =="__main__":
	if not config.get("PRODUCTION"):
		from dotenv import dotenv_values
		config = dotenv_values()
	
	data = load_previous_data()
	if data.get("date", None):
		if data["date"][-1] == time.strftime("%d/%m"):
			print("Data alrealy fetched today")
			exit(0)
	else:
		data["date"] = list()
	
	page_content = get_wishes(config["USER_ID"], config["PASSWORD"])
	results = get_results(page_content)

	merge(data, results)
	data["date"].append(time.strftime("%d/%m"))
	save_data(data)