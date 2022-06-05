import json
import matplotlib.pyplot as plt
import re

DELETE_PREFIX = [
	r"Université Toulouse 3 Paul Sabatier \(31\) - ",
	r"Lycée ",
	r"\(.*\) - CPGE",
	r"- sans internat",
	r"Double [^-]* - ?",
	r"Mathématiques / Informatique - ",
	r"Licence - ",
]

IGNORE = [
	"Fermat"
]

def ignore(key : str) -> bool:
	"""check if the key should be ignored

	Args:
		key (str): the key to check
	"""
	for p in IGNORE:
		if p in key:
			return True
	
	return False

def load_data() -> dict:
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

def plot_data(data : dict) -> None:
	"""plot the data

	Args:
		data (dict): the data to plot
	"""
	date = data["date"]
	data.pop("date")

	plt.title("Progression de Victor dans le classement parcoursup 2022")
	
	ax = plt.subplot(111)
	plt.xlabel("Date")
	plt.ylabel("Position")


	for key, value in data.items():
		if ignore(key):
			continue
		for p in DELETE_PREFIX:
			key = re.sub(p, "", key)
		ax.plot(date, value, label=key)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	
	ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), framealpha=0.5, labelspacing=1.2)
	plt.grid()
	plt.show()

if __name__ == "__main__":
	data = load_data()
	plot_data(data)