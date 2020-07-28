#!/bin/env python3

import pickle
import datetime
import tkinter as tk
from PIL import ImageTk,Image

root = tk.Tk()
root.title("2020 Calendar")
root.geometry("708x629")
root.iconbitmap("lib/icon.ico")

for x in range(1, 13):
	command = "frame{} = tk.Frame(root)".format(x)
	exec(command)

date_raw = str(datetime.datetime.now()).split(" ")
currentYear, currentMonth, currentDay = date_raw[0].split("-")

day_count = 1
current_frame = 0

month_nums = {
	1:"January",
	2:"Febuary",
	3:"March",
	4:"April",
	5:"May",
	6:"June",
	7:"July",
	8:"August",
	9:"September",
	10:"October",
	11:"November",
	12:"December"
}

weekdays = {
	0:"Sunday",
	1:"Monday",
	2:"Teusday",
	3:"Wednesday",
	4:"Thursday",
	5:"Friday",
	6:"Saturday"
}

with open("data", 'rb') as file:
	month_colours, day_notes = pickle.load(file)

# # Clear variables
# month_colours = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[] ,[] ,[]]]
# day_notes = [[], [], [], [], [], [], [], []]
# for i in range(0, 8):
# 	for x in (range(1, 367)):
# 		day_notes[i].append("")

def save_data():
	with open("data", 'wb') as file:
		pickle.dump([month_colours, day_notes], file)

class create_days:
	def __init__(self, day_num, num_in_month, month_num):
		self.num = day_num
		self.pos_in_month = num_in_month
		self.month_num = month_num
		self.month_name = month_nums.get(month_num)
		self.col = None

		if num_in_month in month_colours[(month_num - 1)][0]:
			self.colour = "firebrick1"
		elif num_in_month in month_colours[(month_num - 1)][1]:
			self.colour = "green yellow"
		elif num_in_month in month_colours[(month_num - 1)][2]:
			self.colour = "cyan"
		else:
			self.colour = "gray91"

		frame = "frame{}".format(month_num)

		if month_num == int(currentMonth) and num_in_month == int(currentDay):
			global today
			today = self.num
			command = f"self.button = tk.Button({frame}, font='Helvetica 16 bold', wraplength=80, height=3, width=7, text='{num_in_month}      Today', bg='yellow', command=lambda: create_days.button_click({num_in_month}, {self.col}, {self.month_num}, {self.num}))"
		else:
			command = f"self.button = tk.Button({frame}, font='Helvetica 16 bold', height=3, width=7, text={num_in_month}, bg='{self.colour}', command=lambda: create_days.button_click({num_in_month}, {self.col}, {self.month_num}, {self.num}))"
		exec(command)

	@staticmethod
	def button_click(num_in_month, col, month_num, day_num):
		global new_colour
		new_colour = None
		global selecter_pos
		if num_in_month in month_colours[(month_num - 1)][0]:
			selecter_pos = 0
		elif num_in_month in month_colours[(month_num - 1)][1]:
			selecter_pos = 1
		elif num_in_month in month_colours[(month_num - 1)][2]:
			selecter_pos = 2
		else:
			selecter_pos = 3

		popup = tk.Tk()
		popup.title("Day Entry")
		popup.geometry("400x300")
		popup.iconbitmap("lib/icon.ico")

		frame1 = tk.Frame(popup)
		frame2 = tk.Frame(popup)	

		def switch_to_1(colour):
			write_note_text()
			save_data()
			frame2.pack_forget()
			frame1.pack()
			if new_colour:
				global today
				if day_num != today:
					command5 = "day_{}.button.configure(bg = '{}')".format(day_num, new_colour)
					exec(command5)

		def switch_to_2():
			frame1.pack_forget()
			frame2.pack()

		command = "day = weekdays.get(day_{}.col - 1)".format(day_num)
		exec(command, globals())
	
		month_name = month_nums.get(month_num)
		heading = "{} {} {}".format(num_in_month, day, month_name)
		heading_label = tk.Label(frame1, text=heading, padx=5, pady=5, font='Helvetica 13 bold')
		heading_label.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
		
		textbox = tk.Frame(frame1, borderwidth=3, highlightbackground="black", highlightthickness=1, height=180, width=340)
		textbox.pack_propagate(0)
		textbox.grid(row=1, column=1, columnspan=3)

		note_text = day_notes[0][(day_num - 1)] + day_notes[1][(day_num - 1)] + day_notes[2][(day_num - 1)] + day_notes[3][(day_num - 1)] + day_notes[4][(day_num - 1)] + day_notes[5][(day_num - 1)] + day_notes[6][(day_num - 1)] + day_notes[7][(day_num - 1)]

		note = tk.Label(textbox, wraplength=335, justify=tk.LEFT, text=note_text)  #(day_notes[day_num - 1]))
		note.pack(pady=10)

		edit_button = tk.Button(frame1, command=lambda:switch_to_2(), padx=8, text="Edit", bg="gray91",  font='Helvetica 11 bold')
		edit_button.grid(row=4, column=0, pady=15, columnspan=2, sticky=tk.W)

		frame1.pack()

		def select_colour(colour):
			global selecter_pos
			global month_colours
			global new_colour
			if colour == 'red' and num_in_month not in month_colours[(month_num - 1)][0]:
				month_colours[(month_num - 1)][0].append(num_in_month)
				selecter_pos = 0
				new_colour = 'red'
				if num_in_month in month_colours[(month_num - 1)][1]:
					month_colours[(month_num - 1)][1].remove(num_in_month)
				if num_in_month in month_colours[(month_num - 1)][2]:
					month_colours[(month_num - 1)][2].remove(num_in_month)

			elif colour == 'green yellow' and num_in_month not in month_colours[(month_num - 1)][1]:
				month_colours[(month_num - 1)][1].append(num_in_month)
				selecter_pos = 1
				new_colour = 'green yellow'
				if num_in_month in month_colours[(month_num - 1)][0]:
					month_colours[(month_num - 1)][0].remove(num_in_month)
				if num_in_month in month_colours[(month_num - 1)][2]:
					month_colours[(month_num - 1)][2].remove(num_in_month)

			elif colour == 'cyan' and num_in_month not in month_colours[(month_num - 1)][2]:
				month_colours[(month_num - 1)][2].append(num_in_month)
				selecter_pos =2
				new_colour = 'cyan'
				if num_in_month in month_colours[(month_num - 1)][0]:
					month_colours[(month_num - 1)][0].remove(num_in_month)
				if num_in_month in month_colours[(month_num - 1)][1]:
					month_colours[(month_num - 1)][1].remove(num_in_month)

			elif colour == 'gray91':
				if num_in_month in month_colours[(month_num - 1)][0]:
					month_colours[(month_num - 1)][0].remove(num_in_month)
				if num_in_month in month_colours[(month_num - 1)][1]:
					month_colours[(month_num - 1)][1].remove(num_in_month)
				if num_in_month in month_colours[(month_num - 1)][2]:
					month_colours[(month_num - 1)][2].remove(num_in_month)
				selecter_pos = 3
				new_colour = 'gray91'

			selecter.grid_forget()
			selecter.grid(row=0, column=selecter_pos)

		colour_box = tk.Frame(frame2)
		colour1_button = tk.Button(colour_box, padx=10, bg="red", command=lambda:select_colour('red'))
		colour1_button.grid(row=1, column=0)
		colour2_button = tk.Button(colour_box, padx=10, bg="green yellow", command=lambda:select_colour('green yellow'))
		colour2_button.grid(row=1, column=1)
		colour3_button = tk.Button(colour_box, padx=10, bg="cyan", command=lambda:select_colour('cyan'))
		colour3_button.grid(row=1, column=2)
		colour4_button = tk.Button(colour_box, padx=10, bg="gray91", command=lambda:select_colour('gray91'))
		colour4_button.grid(row=1, column=3)

		# arrow_icon = ImageTk.PhotoImage(Image.open("lib/arrow.png"))
		selecter = tk.Label(colour_box, text='⬇')
		selecter.grid(row=0, column=selecter_pos)
		colour_box.grid(row=10, column=0, pady=10, sticky=tk.N)

		def validate(inp):
			if inp is "":
				return True
			if len(inp) <= 60:
				return True
			else:
				return False

		input_box1 = tk.Entry(frame2, width=54)
		input_box1.grid(row=2, column=0, columnspan=3)
		input_box2 = tk.Entry(frame2, width=54)
		input_box2.grid(row=3, column=0, columnspan=3)
		input_box3 = tk.Entry(frame2, width=54)
		input_box3.grid(row=4, column=0, columnspan=3)
		input_box4 = tk.Entry(frame2, width=54)
		input_box4.grid(row=5, column=0, columnspan=3)
		input_box5 = tk.Entry(frame2, width=54)
		input_box5.grid(row=6, column=0, columnspan=3)
		input_box6 = tk.Entry(frame2, width=54)
		input_box6.grid(row=7, column=0, columnspan=3)
		input_box7 = tk.Entry(frame2, width=54)
		input_box7.grid(row=8, column=0, columnspan=3)
		input_box8 = tk.Entry(frame2, width=54)
		input_box8.grid(row=9, column=0, columnspan=3)

		reg = frame2.register(validate)

		for x in range(1, 9):
			command4 = "input_box{}.config(validate='key', validatecommand=(reg, '%P'))".format(x)
			exec(command4)

		for x in (range(1, 9)):
			command5 = "text{} = day_notes[{}][(day_num - 1)].strip()".format(x, (x - 1))
			exec(command5)
		
		for x in range(1, 9):
			command2 = "input_box{}.insert(0, text{})".format(x, x)
			exec(command2)	

		def write_note_text():
			text1 = input_box1.get() + "\n"
			text2 = input_box2.get() + "\n"
			text3 = input_box3.get() + "\n"
			text4 = input_box4.get() + "\n"
			text5 = input_box5.get() + "\n"
			text6 = input_box6.get() + "\n"
			text7 = input_box7.get() + "\n"
			text8 = input_box8.get() + "\n"

			day_notes[0][(day_num - 1)] = text1
			day_notes[1][(day_num - 1)] = text2
			day_notes[2][(day_num - 1)] = text3
			day_notes[3][(day_num - 1)] = text4
			day_notes[4][(day_num - 1)] = text5
			day_notes[5][(day_num - 1)] = text6
			day_notes[6][(day_num - 1)] = text7
			day_notes[7][(day_num - 1)] = text8

			note_text = day_notes[0][(day_num - 1)] + day_notes[1][(day_num - 1)] + day_notes[2][(day_num - 1)] + day_notes[3][(day_num - 1)] + day_notes[4][(day_num - 1)] + day_notes[5][(day_num - 1)] + day_notes[6][(day_num - 1)] + day_notes[7][(day_num - 1)]
			note.config(text=note_text)

		heading2 = tk.Label(frame2, text="Enter Notes", font='Helvetica 11 bold')
		heading2.grid(row=0, column=0, columnspan=3, pady=10)

		def clear_entrys():
			input_box1.delete(0, 'end')
			input_box2.delete(0, 'end')
			input_box3.delete(0, 'end')
			input_box4.delete(0, 'end')
			input_box5.delete(0, 'end')
			input_box6.delete(0, 'end')
			input_box7.delete(0, 'end')
			input_box8.delete(0, 'end')
			select_colour('gray91')

		clear_button = tk.Button(frame2, text="clear", font='Helvetica 11 bold', command=lambda:clear_entrys(), padx=5, bg='gray91')
		clear_button.grid(row=10, column=1, sticky=tk.E, pady=10)

		save_button = tk.Button(frame2, text="Save",  font='Helvetica 11 bold', command=lambda:[write_note_text(), switch_to_1(new_colour)], padx=5, bg='gray91')
		save_button.grid(row=10, column=2, sticky=tk.W, pady=25)

		popup.mainloop()

class create_months:
	def __init__(self, num_of_days, start_pos, month_num, start_day):
		self.start_pos = start_pos
		self.num_of_days = num_of_days
		self.month_num = month_num
		self.month_name = month_nums.get(month_num)
		self.start_day = start_day

		global day_count
		for x in (range(1, (num_of_days + 1))):
			command = "day_{} = create_days({}, {}, {})".format(day_count, day_count, x, month_num)
			exec(command, globals())
			day_count += 1

def init_months():
	global january, febuary, march, april, may, june, july, august, september, october, november, december
	january = create_months(31, 3, 1, 1)
	febuary = create_months(29, 6, 2, 32)
	march = create_months(31, 0, 3, 61)
	april = create_months(30, 3, 4, 92)
	may = create_months(31, 5, 5, 122)
	june = create_months(30, 1, 6, 153)
	july = create_months(31, 3, 7, 183)
	august = create_months(31, 6, 8, 213)
	september = create_months(30, 2, 9, 245)
	october = create_months(31, 4, 10, 275)
	november = create_months(30, 0, 11, 306)
	december = create_months(31, 2, 12, 336)
init_months()

heading = tk.Label(root, font='Helvetica 22 bold', text="2020", pady=10)
heading.grid(row=0, column=1, columnspan=2, padx=10)

heading_frame = tk.Frame(root)
sunday_Label = tk.Label(heading_frame, text="Sunday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=19, pady=5)
monday_Label = tk.Label(heading_frame, text="Monday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=19, pady=5)
teusday_Label = tk.Label(heading_frame, text="Teusday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=17, pady=5)
wednesday_Label = tk.Label(heading_frame, text="Wednesday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=4, pady=5)
thursday_Label = tk.Label(heading_frame, text="Thursday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=12, pady=5)
friday_Label = tk.Label(heading_frame, text="Friday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=25, pady=5)
saturday_Label = tk.Label(heading_frame, text="Saturday", font='Helvetica 13 bold', borderwidth=1, relief="solid", padx=15, pady=5)

sunday_Label.grid(row=0, column=0)
monday_Label.grid(row=0, column=1)
teusday_Label.grid(row=0, column=2)
wednesday_Label.grid(row=0, column=3)
thursday_Label.grid(row=0, column=4)
friday_Label.grid(row=0, column=5)
saturday_Label.grid(row=0, column=6)

heading_frame.grid(row=1, column=0, columnspan=5, sticky=tk.W)

def update_month(choice):
	global current_frame
	new_month = choices.index(month_choice.get()) + 1
	command = "frame{}.grid_forget()".format(current_frame)
	exec(command)
	command2 = "frame{}.grid(row=2, column=0, columnspan=5)".format(new_month)
	exec(command2)
	current_frame = new_month

choices = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_choice = tk.StringVar()
month_choice.set(choices[0])
choose_month = tk.OptionMenu(root, month_choice, *choices, command=update_month)
choose_month.config(font='Helvetica 12 bold', width=9)
choose_month['menu'].configure(font=('Futura',12))
choose_month.grid(row=0, column=0, sticky=tk.W+tk.N)

def place_days(start_pos, start_day, num_of_days):
	row = 3
	col = start_pos

	for x in range(start_day, (start_day + num_of_days)):
		command = "day_{}.button.grid(row={}, column={})".format(x, row, col)
		exec(command)
		col += 1

		command2 = "day_{}.col = {}".format(x, col)
		exec(command2, globals())

		if col == 7:
			row += 1
			col = 0
		
for x in month_nums:
	month = month_nums.get(x).lower()
	command = "place_days({}.start_pos, {}.start_day, {}.num_of_days)".format(month, month, month)
	exec(command)

current_frame = int(currentMonth)
command3 = "frame{}.grid(row=2, column=0, columnspan=5)".format(current_frame)
exec(command3)
month_choice.set(choices[(current_frame - 1)])

root.mainloop()