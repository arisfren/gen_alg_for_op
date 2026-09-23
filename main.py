import tkinter as tk
from tkintermapview import TkinterMapView
import csv, json
from my_algorithms import *

def import_matrix(filename: str) -> list[list[float]]:
	with open(filename, 'r') as json_file:
		raw_data = json.load(json_file)
		return raw_data

def run_gen_alg():
	attr_profits = {cat: v.get() for v, cat in zip(scale_vals, attr_cat)}
	attr_costs = {cat: int(v.get())*60 for v, cat in zip(entry_vals, attr_cat)}
	attr_profits['train'] = 0
	attr_costs['train'] = 0

	profits = [attr_profits[attr['type']] for attr in attr_list]
	costs = [attr_costs[attr['type']] for attr in attr_list]
	total_time = float(total_time_var.get()) * 3600

	num_of_iter = 10000

	time_matrix = import_matrix('time_matrix.json')
	m = Map(time_matrix, profits, costs, total_time)  # 8h

	ga = GeneticAlgorithm(m, 200)
	ga.run_simulation(num_of_iter)
	best_tour = ga.best_chromosome.path
	show_path(best_tour)

def show_path(path: list[int]):
	global best_path
	new_path = [c for c in path if c]
	positions = [markers[p-1].position for p in new_path]
	if best_path is not None:
		best_path.set_position_list(positions)
	else:
		best_path = map_widget.set_path(positions)


# read csv file
attr_list = []
filename = 'atrakcje_bialystok.csv'
with open(filename, 'r', encoding='utf-8-sig') as file:
	reader = csv.DictReader(file, delimiter=';', lineterminator='\n')
	for row in reader:
		record = row
		record['lat'] = float(record['lat'])
		record['lng'] = float(record['lng'])
		attr_list.append(record)

# get categories
attr_cat = sorted(list(set([attr['type'] for attr in attr_list]) - {'train'}))

#create window
root_tk = tk.Tk()
root_width, root_height = 1150, 700
root_tk.geometry(f'{root_width}x{root_height}')

# create frames
map_frame = tk.Frame(root_tk, width=root_height+100, height=root_height)
control_frame = tk.Frame(root_tk, width=root_width-root_height-100, height=root_height)
map_frame.grid(column=0, row=0)
control_frame.grid(column=1, row=0)

# create map widget
map_widget = TkinterMapView(map_frame, width=root_height+100, height=root_height, corner_radius=0)
# map_widget.set_tile_server('https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga')
map_widget.pack()
map_widget.set_position(53.1282029, 23.1577988)
map_widget.set_zoom(13)

# position marker
markers = []
for attr in attr_list:
	new_marker = map_widget.set_marker(attr['lat'], attr['lng'])
	new_marker.data = attr
	markers.append(new_marker)

best_path = None

# labels
tk.Label(control_frame, text='profits', font=('Segoe UI', 20)).grid(row=0, column=0)
tk.Label(control_frame, text='costs (time in min)', font=('Segoe UI', 20)).grid(row=0, column=1)

# scales and entries
# scale_frame = tk.Frame(control_frame)
# scale_frame.pack()
cat_values = {
	'bear': [6, 5],
	'catholic church': [5, 20],
	'cemetery': [4, 20],
	'landmark': [7, 10],
	'library': [6, 30],
	'memorial': [7, 10],
	'museum': [8, 90],
	'orthodox church': [5, 20],
	'park': [2, 30],
	'university': [3, 30]
}

scale_vals = []
entry_vals = []
for i, category in enumerate(attr_cat):
	new_scale_var = tk.IntVar()
	new_scale_var.set(cat_values[category][0])
	new_scale = tk.Scale(control_frame, from_=0, to=15, orient='horizontal', label=category,
						 length=110, font=('Segoe UI', 14), variable=new_scale_var)
	new_scale.grid(row=i+1, column=0, padx=20)
	scale_vals.append(new_scale_var)

	new_entry_var = tk.StringVar()
	new_entry_var.set(str(cat_values[category][1]))
	new_entry = tk.Entry(control_frame, textvariable=new_entry_var, width=5, font=('Segoe UI', 14))
	new_entry.grid(row=i+1, column=1)
	entry_vals.append(new_entry_var)

# entry
tk.Label(control_frame, text='Total time (h):', font=('Segoe UI', 14)).grid(row=19, column=0)
total_time_var = tk.StringVar()
total_time_var.set('8')
total_time_entry = tk.Entry(control_frame, textvariable=total_time_var, width=3, font=('Segoe UI', 14))
total_time_entry.grid(row=20, column=0)

# button
button_gen = tk.Button(control_frame, command=run_gen_alg,
					   text='Run Simulation', font=('Segoe UI', 25))
button_gen.grid(row=20, column=1, pady=10)


root_tk.mainloop()
