import datetime
import random
import webbrowser

import pygame
from beepy import beep

from kivy.config import Config

# Config.set("kivy", "window_icon", "")
Config.set("graphics", "width", "300")
Config.set("graphics", "height", "500")
Config.set("graphics", "resizable", True)

import os
import pickle
import threading
import time
import tkinter
import string
import kivy

from kivy import clock
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window, WindowBase
from kivy.factory import Factory
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Canvas
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy_garden.filebrowser import FileBrowser
from kivymd.app import MDApp
from tkinter import filedialog
# Different Screens
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase, MDTabs
from playsound import playsound
import plyer
import app_manager  # Custom module

# Settings Screen properties ............................

pygame.mixer.init()

# ............................ Defining global variables , deriving user values from .dat files......................
# NOTE: set_data_get is returned by the app_manager module

set_data_rec = app_manager.Get_Records()  # <<<<<<<<<<<<<<<<<<<<<<<<<<<< Major user file records.dat
set_data_get = app_manager.On_Start_Settings()  # <<<<<<<<<<<<<<<<<<<<<<<< Major user file settings.dat

song_addresss_var = set_data_get['song_address']

# Controlling flow test result >>
flow_test_result = set_data_get['flow_limit']
flow_time_boolean = set_data_get['flow_time_boolean']
print("Flow Time Feature Status : (", flow_test_result, ",", flow_time_boolean, ")")
# Controlling Blinks record >>
blink_test_result = set_data_get['blinks']
final_blinks = 0
blink_sum = 0
# defining before use in for loop
for i in blink_test_result:
    blink_sum += int(i)
    final_blinks = blink_sum / len(blink_test_result)

print("final_blinks (avg blinks) : ", final_blinks)

# Break counter >>
break_count = 0

# Mark Exhaustion Setting up:
mark_exh_dict_var = set_data_get["mark_exhaustion_dict"]
mark_exh_bool = set_data_get["mark_exh_bool"]

# Records global variables >>
rec_list = set_data_rec['record_list']  # This is a dictionary
week_date_var = set_data_rec['week_date']

# updating the weekly date change , week_date
type(week_date_var)

date_diff = (datetime.date.today() - week_date_var)
if ((set_data_get['week_measure_option'] == "Weekly") and (date_diff.days > 7)) or \
        ((set_data_get['week_measure_option'] == "Monthly") and (date_diff.days > 30) or
         ((set_data_get['week_measure_option'] == "Fortnightly") and (date_diff.days > 14))):
    week_date_var = datetime.date.today()  # << week_date updated
    rec_list = {'pc_mobile': 0, 'study': 0, 'limited_time_task': 0, 'mind_wandering': 0, 'pomo': 0}
    print("Progress value updated to 0 , new session started .")
else:
    pass

# ................................Starting Program ....................................................................

# Extra Global Functions :


def make_avg(element_x, element_sum = 0):
    for i in element_x:
        element_sum = float(i) + float(element_sum)

    return element_sum / len(element_x)

# Get today's date and test to update current day's use time : -
today_date = datetime.date.today()
print(f'Checking date and updating todays today_hr : {today_date} & {set_data_rec["date"]}')
if today_date != set_data_rec['date']:  # Set the label to 0 hr and 0 min if diff. date
    with open("records.dat", "rb+") as records_rec:
        record_dict = pickle.load(records_rec)
        record_dict['today_hr'] = 0
        record_dict['date'] = today_date
        pickle.dump(record_dict, records_rec)
        # Change in the current run >>
        set_data_rec['today_hr'] = 0
        print("Date Changed ! ...", records_rec)  # <<...........................date changed new today's timing


class WhiteScreen(Screen, Widget):
    """For animations in Kivy you need to write a function for each animation
     you perform and the parameter must contain the id of the widget to be animated"""

    # some codes left
    def animate_blink_test_label(self, widget, *args):
        Window.fullscreen = True
        animate1 = Animation(text_color=(0, 1, 0, 0), duration=6)
        animate1 += Animation(opacity=0)
        animate1.start(widget)
        animate1.bind(on_complete=self.animate_blink_test_label2)

    def animate_blink_test_label2(self, *args):
        animate2 = Animation(text_color=(0, 1, 0, 1), duration=3, opacity=1)
        animate2 += Animation(duration=1, opacity=0)

        animate2.start(self.ids.test_blink_label_id2)

        animate2.bind(on_complete=self.return_now)

    def return_now(self, *args):
        Clock.usleep(10000000)
        Window.fullscreen = False
        self.parent.current = "intro"  # Screen change


class IntroWindow(MDBottomNavigationItem):
    # Clearing textbox (blink_num_textfield) on entering the screen (if it is filled)
    # as on_enter can be used as as IntroWindow(Screen) uses Screen

    #  blink_test_result is a global already defined in __main__
    def note_blink(self, *args):

        blink_test_result_length = 6  # In terms of indexing [0,1,2,3,4,5,6] limiting stack (list namely
        # blink_test_result) , blink_test_result can take only 7 elements
        top = len(blink_test_result) - 1
        if len(self.ids.blink_num_textfield_id.text) != 0:
            if top >= blink_test_result_length:  # clear records if more then 7 records
                blink_test_result.clear()
                blink_test_result.append(self.ids.blink_num_textfield_id.text)
                print(blink_test_result)
                if len(self.ids.blink_num_textfield_id.text) != 0:
                    self.ids.blink_num_textfield_id.text = ""  # remove the datat after use
            else:  # else add record
                blink_test_result.append(self.ids.blink_num_textfield_id.text)
                print(blink_test_result)
                if len(self.ids.blink_num_textfield_id.text) != 0:  # remove the data after use
                    self.ids.blink_num_textfield_id.text = ""

            animate_label_record_added = Animation(opacity=1, color=(1, 0, 0, 1), duration=2)
            animate_label_record_added += Animation(color=(0, 1, 0, 1), opacity=0, duration=2)
            animate_label_record_added.start(self.ids.label_added_id)

        else:
            pass
        """ **LEARNING NOTE:** if you use a globally defined variable in only one place(class) then you need not use global <var name>
        but if you use it in more then one class, the computer is confused about where to look for the value 
        (in local or global) and hence you need to use the global to clarify this dilemma to the computer - Sumit Gupta"""

        global final_blinks
        for j in blink_test_result:
            final_blinks += int(j) / len(blink_test_result)
            # use it during start of interval

    # Popup code starts >>

    def animate_blink_test_label(self, *args):
        Window.fullscreen = True
        animate1 = Animation(text_color=(0, 1, 1, 0), duration=5)
        animate1 += Animation(opacity=0)
        animate1.start(self.white_label1)
        animate1.bind(on_complete=self.animate_blink_test_label2)

    def animate_blink_test_label2(self, *args):
        animate2 = Animation(text_color=(0, 1, 0, 1), duration=5, opacity=1)
        animate2 += Animation(duration=1, opacity=0)
        animate2.start(self.white_label2)
        animate2.bind(on_complete=self.return_now)

    def return_now(self, *args):
        Clock.usleep(10000000)
        Window.fullscreen = False
        self.white_popup.dismiss()

    # Code for popup of white screen

    def start_test(self, *args):
        # excite the white screen test

        white_layout = GridLayout(cols=1, rows=2, padding=(5, 20, 5, 5), spacing=(0, 1))
        self.white_label1 = MDLabel(text="Just look at the black screen & COUNT your EYE BLINKS",
                                    font_size=40, theme_text_color="Custom", text_color=(1, 0, 0, 1),
                                    pos_hint={'x': .3, 'y': 0})
        self.white_label2 = MDLabel(text="START NOW !",
                                    font_size=40, theme_text_color="Custom", text_color=(0, 0, 0, 0),
                                    pos_hint={'x': .4, 'y': 0})

        white_layout.add_widget(self.white_label1)
        white_layout.add_widget(self.white_label2)

        self.white_popup = Popup(title="BLINK TEST", background_color=(0, 0, 0, 1), content=white_layout)

        self.white_popup.open()
        self.animate_blink_test_label()


class MainWindow(MDBottomNavigationItem):
    # Defining Properties

    # Setting flow_test_result >>
    flow_test_result_show = StringProperty(str(flow_test_result))
    break_count = 0
    duration_text = StringProperty()
    flow_test_result_label = StringProperty(str(flow_test_result))  # flow test limit (flow_test_result[not list])
    # of user >> to link to Flow Limit label as in kivy to link a variable to a widget you need a Property
    blink_test_result_labelmain = NumericProperty(final_blinks)
    # Setting up todays use data variable:
    todays_use_data = 0
    # Setting Up definitions for Today's Use Label (Quite clumsy but fast)
    todays_use_label = StringProperty(str(round((float(set_data_rec['today_hr'])), 2)))
    print("Today Use >", str(round((float(set_data_rec['today_hr'])), 2)))

    # On_Start activities.....................

    def greeting(self, *args):
        start_greeetings = ["Hello !", "What's up ?", "Good to see you !", "It's a rainy day", "Ready !", "Hey, hi",
                            "Made in India", "Busy day ?"]
        x = random.randint(0, 7)
        self.ids.common_msg_id.text = start_greeetings[x]

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.greeting, 0.1)

    # define ids # Create Properties

    def build(self):
        pass

    # Choosing break time functions and algorithms

    def spinner_clicked(self, value):  # Main Time Management Technique
        self.ids.spinner_id.is_open = True
        spinner_value = value
        # Disable and enable category only for AppName Algorithm
        if not spinner_value == "AppName Algorithm(RECOMMENDED)":
            self.ids.task_spinner_id.disabled = True
            self.ids.common_msg_id.text = """Select Task Category"""
        else:
            self.ids.task_spinner_id.disabled = False

        if spinner_value == "Pomodoro Technique":
            self.ids.common_msg_id.text = """25 min as interval is recommended"""
        if spinner_value == "60/10 Method":
            self.ids.common_msg_id.text = "60 min of task followed by 10 min \nof mind wandering(fixed)"

        # ...................................................
        """if not spinner_value == "AppName Algorithm(RECOMMENDED)":
            self.ids.task_spinner_id.disabled = True
            self.ids.common_msg_id.text = "Task categories only available in AppName Algorithm.\n Know about the " \
                                          "techniques in ABOUT TAB "
        else:
            self.ids.task_spinner_id.disabled = False
            self.ids.common_msg_id.text = " "
        """  # this part might not be needed (TESTING)

    def task_spinner_clicked(self, value):  # task_spinner DropDownItem Button Categories check
        if self.ids.spinner_id.text == "AppName Algorithm(RECOMMENDED)":
            self.ids.task_spinner_id.is_open = True
            # Common msg
            if self.ids.task_spinner_id.text == "PC or Mobile Related":
                self.ids.common_msg_id.text = "Manages screen exposure and productivity"

            elif self.ids.task_spinner_id.text == "Study":
                self.ids.common_msg_id.text = "Study efficiently"

            elif self.ids.task_spinner_id.text == "Limited Time Task":
                self.ids.common_msg_id.text = "High intensity work session(drains energy)"

            else:
                self.ids.common_msg_id.text = " "

            task_spinner_value = value

    def revise_now(self, revise_time, instance):
        def revise_notify_close():  # to close it automatically if not responded after 60 sec
            if dialog:
                dialog.dismiss()

        dialog = MDDialog(text=f"Time for a [color=#42f55a]quick revision[/color], in case you are not able to "
                               f"complete it in "
                               f": [color=#42f55a]{revise_time} min [/color], continue it in the next interval")
        dialog.open()
        Clock.schedule_once(revise_notify_close, 60)

        x = random.randint(1,4)
        if x == 1:
            playsound('Music/study_revise_1.mp3')
        elif x == 2:
            playsound('Music/study_revise_2.mp3')
        elif x == 3:
            playsound('Music/study_revise_3.mp3')
        elif x == 4:
            playsound('Music/study_revise_4.mp3')
        else:
            MDDialog(title="Error", text="An error occurred while notifying user of the revision break\n"
                                         "Please contact at sgsonu132@gmail.com with the error statement").open()

    #  Timer code ............................... 1st parts ..........................................................

    def Break_Manager(self, blink_num=15):

        # Make User Panel progress 0( before start)
        self.ids.current_progress_id.value = 0
        self.progress_count = 0

        # Stop beep call >> already done by the 2 nd dialog
        # Check file exists
        if not os.path.exists("records.dat"):
            with open("records.dat", "wb") as time_rec:
                pickle.dump({"total": '0', 'today': '0'}, time_rec)

        # IMP : Load file data in dictionary and update others (rb)

        try:
            with open("records.dat", "rb") as time_rec:
                rec_data = pickle.load(time_rec)
        except:
            pass

        # Testing ....................................
        """Whenever tou use clock.schedule to update label by using a counter (here say count) give the time 
        scheduling time and count increment value same ,#self for class  like Clock.schedule_interval(
        self.update_clock_label, 0.1) and self.count += 0.1 will increase label's value by 1 every 1 sec (delta-sec)**BUT KEEP**
         Clock.schedule_once(self.stop_update, <Ending_time>) ending time same (as it takes in sec (NOT delta_sec)"""

        # IF AUTO , for others code is left out

        if self.ids.auto_timer_id.active:  # Check Auto timer is active or not

            if (len(self.ids.duration_id.text) == 0) or (len(self.ids.total_duration_id.text) == 0) \
                    or (float(self.ids.duration_id.text)) <= 0 or (float(self.ids.total_duration_id.text)) <= 0:
                # Multi lining the code
                MDDialog(text="The INTERVAL textbox and TOTAL INTERVAL textbox can't be empty if auto interval/break"
                              " is switched on !").open()  # Check correct interval

            else:
                if self.ids.play_timer_id.text == "START":
                    self.ids.play_timer_id.text = "STOP"
                    # Update all variables
                    self.interval_time = float(self.ids.duration_id.text)
                    self.total_duration = float(self.ids.total_duration_id.text)
                    # Research based data (Flow Technique Upgraded Pomodoro)
                    if len(self.ids.total_duration_id.text) != 0:
                        if self.interval_time < 25:  # 25 min
                            self.expect_break = 5  # 5 min
                        elif 25 < self.interval_time < 50:  # 25 min and 50 min
                            self.expect_break = 8  # 8 min
                        elif 50 < self.interval_time < 90:  # 50 min and 90 min
                            self.expect_break = 10  # 10 min
                        elif self.interval_time > 90:  # 90 min
                            self.expect_break = 15  # 15 min

                        # hr/break_num
                        self.break_num = (60 * 60 * self.total_duration) // (self.expect_break + self.interval_time)
                        self.extra_time = (60 * 60 * self.total_duration) % (self.expect_break + self.interval_time)

                    if self.break_num == self.break_count:
                        if self.extra_time >= self.interval_time:
                            self.expect_break = 0
                        else:
                            self.interval_time = self.extra_time

                    self.count, self.count_sec = 0, 0
                    self.clock_handle = Clock.schedule_interval(self.update_clock_label, 0.1)  # starting the timer
                    Clock.schedule_once(self.stop_update_auto,
                                        (60 * self.interval_time))  # Converting to min input to sec in event stopper

                else:
                    Clock.unschedule(self.update_clock_label)
                    Clock.unschedule(self.stop_update_auto)
                    self.ids.play_timer_id.text = "START"
                    self.ids.clock_label.text = "ENDED!"

        # Timer code .......................... 2nd part ..............................................................

        # If auto is not checked/switched
        else:

            if (len(self.ids.duration_id.text) == 0) or float(self.ids.duration_id.text) <= 0:
                MDDialog(text="The interval textbox can't be empty !").open()  # Check correct interval

            else:
                if self.ids.play_timer_id.text == "START":
                    self.ids.play_timer_id.text = "STOP"

                    # Update all variables
                    self.interval_time = float(self.ids.duration_id.text)

                    # hr/break_num

                    self.count, self.count_sec = 0, 0
                    self.clock_handle = Clock.schedule_interval(self.update_clock_label, 0.1)
                    # Starting the clock
                    Clock.schedule_once(self.stop_update_not_auto,
                                        (60 * self.interval_time))  # Converting to min input to sec in event stopper

                    # Some special code for the category task "Study" (setting the revision time)
                    if self.ids.spinner_id.text == "AppSoch Algorithm" and self.ids.task_spinner_id.text == "Study":
                        special_clock = Clock.schedule_once(self.revise_now, (self.interval_time * 60) - (
                                (1 / 5) * self.interval_time * 60))  # Total time(min) - 1/5 of it

                else:
                    Clock.unschedule(self.update_clock_label)
                    Clock.unschedule(self.stop_update_not_auto)
                    self.ids.play_timer_id.text = "START"
                    self.ids.clock_label.text = "ENDED!"

    progress_count = 0

    def update_clock_label(self, instance):  # To be used in both auto/not auto # Will update user records.dat

        self.count += 0.1  # Counter variable to clock interval [updates in 1 sec]
        self.count_sec += 0.1
        if int(self.count_sec) == 60:
            self.count_sec = 00
        self.count_min = self.count / 60  # self.count sec in min
        self.time_list = [(self.count_min // 60), (self.count_min % 60)]
        self.ids.clock_label.text = f" {int(self.time_list[0])} : {int(self.time_list[1])} : {int(self.count_sec)} "
        print(self.time_list)  # ------To debug
        # Update records >>
        global rec_list

        # Update the HEADER progress bar >>
        # everything is in min
        self.progress_count += 0.1  # count in sec
        self.ids.current_progress_id.max = float(self.interval_time) * 60  # interval converted in sec
        self.ids.current_progress_id.value = 60 * (self.interval_time) - (self.progress_count)
        print("Clock Label Updated...", self.ids.current_progress_id.max, "  ", self.ids.current_progress_id.value)

        # Update records tab >>
        """Practical Knowledge by Sumit Gupta : While using kivy using classes, if u update value from one class to 
        other classes if takes a bit more time for the PC and time may disturb your ptogress bar values if you are 
        using , so be careful while using them () """

        if self.ids.spinner_id.text == "AppName Algorithm(RECOMMENDED)":
            if self.ids.task_spinner_id.text == "PC or Mobile Related":

                rec_list['pc_mobile'] += 0.1

            elif self.ids.task_spinner_id.text == "Study":

                rec_list['study'] += 0.1
            elif self.ids.task_spinner_id.text == "Limited Time Task":

                rec_list['limited_time_task'] += 0.1
            else:
                MDDialog(title="Error",
                         text="""-Please check, did you entered the time managing hint by scrolling down!
Yes see below :
Error while updating records tab. 
Please contact at sgsonu132@gmail.com with the error statement """).open()
                Clock.unschedule(self.update_clock_label)
                Clock.unschedule(self.stop_update_not_auto)


        else:
            if self.ids.spinner_id.text == "Pomodoro Technique":
                rec_list['pomo'] += 0.1
            elif self.ids.spinner_id.text == "60/10 Method":
                rec_list['mind_wandering'] += 0.1
            else:
                 MDDialog(title="Error",
                         text="""-Please check, did you entered the time managing hint by scrolling down!
Yes see below :
Error while updating records tab. 
Please contact at sgsonu132@gmail.com with the error statement""").open()

                 Clock.unschedule(self.update_clock_label)
                 Clock.unschedule(self.stop_update_not_auto)

        print("Changing progress data (List) >>>> ", rec_list)
        # Update the file >>
        print("File Update enter")
        # NOTE for Developer : Here we put 0.1 as an argument as we need to pass 1 sec per iteration to record total
        # today's use, do not use self.count as it adds it cumulatively like 0.1 +0.2+0.2

        self.todays_use_data = app_manager.Update_Records(0.1, rec_list, week_date_var)

        # Update Todays Use Label (in MainWindow):
        self.todays_use_label = str(round(float(self.todays_use_data), 2))

        print("File update done ! Todays Use Data extracted :", self.todays_use_data)

    def stop_update_not_auto(self, instance):  # Only for non auto timer
        Clock.unschedule(self.update_clock_label)
        self.ids.clock_label.text = "INTERVAL \n ENDED!"
        self.ids.play_timer_id.text = "START"
        plyer.notification.notify("Over", " ")

        # start break method :
        app_manager.On_Stop_Break(self.ids.spinner_id.text, self.ids.task_spinner_id.text,
                                  self.ids.duration_id.text, break_count, flow_test_result, final_blinks,
                                  flow_time_boolean, mark_exh_dict_var, self.todays_use_label, mark_exh_bool)

        # Change todays_use if extreme limit exceeded :
        extreme_limit_exceeded = make_avg(mark_exh_dict_var['extreme'])
        if float(self.todays_use_label) > float(extreme_limit_exceeded):
            self.todays_use_label = 0
            self.ids.common_msg_id.text = "Today's use re-set \nas you have recovered !"

    def stop_update_auto(self, instance):  # Only for auto timer
        Clock.unschedule(self.update_clock_label)
        self.ids.clock_label.text = "ENDED!"
        # if (".mp" in song_addresss_var) or (".wav" in song_addresss_var):
        # playsound(song_addresss_var) # MCI initialisation error ,Brut!
        if self.break_num != self.break_count:
            self.count = 0
            self.clock_handle = Clock.schedule_interval(self.update_clock_label, 0.1)
            Clock.schedule_once(self.stop_break, (60 * self.expect_break))

    def stop_break(self, *args):  # Only for auto timer
        Clock.unschedule(self.update_clock_label)
        self.break_count += 1
        # Starting task again
        self.Break_Manager()

    # Habit Maker .............................................................

    def habit_maker(self):

        x = random.randint(1, 4)
        if x == 1:
            self.gif_source = "Extra_Files/posture.gif"
            gif_delay = 0
            label_text_get = app_manager.habit_label_text("posture")  # Use module to generate text

        elif x == 2:
            self.gif_source = "Extra_Files/drinkwater.gif"
            gif_delay = 0
            label_text_get = app_manager.habit_label_text("drinkwater")  # Use module to generate text
        elif x == -3:  # Not to use now , later for promotion
            self.gif_source = "Extra_Files/star.gif"
            gif_delay = 0
            label_text_get = app_manager.habit_label_text("star")

        else:
            self.gif_source = "Extra_Files/walk.gif"
            gif_delay = 0.3
            label_text_get = app_manager.habit_label_text("walk")  # Use module to generate text

        close_button_text_get = app_manager.habit_close_button_text()

        self.layout = GridLayout(cols=1, rows=3, padding=(5, 20, 5, 5), spacing=(0, 1))
        gif_img = Image(source=self.gif_source, size_hint=(.5, .7), anim_delay=gif_delay)
        label = MDLabel(text=label_text_get, halign="center",
                        size_hint=(0.1, 0.1), font_size=28)
        close_button = MDRaisedButton(text=close_button_text_get, size_hint=(0.05, 0.15),
                                      font_size=20, on_press=self.popup_dismiss)
        self.layout.add_widsget(gif_img)
        self.layout.add_widget(label)
        self.layout.add_widget(close_button)

        # Defining Popup >>
        self.popup = Popup(title="Habit Maker Reminder:\nDisable it in settings if you learnt it :)",
                           background_color=(1, 1, 1, .5), content=self.layout)
        self.popup.open()

    def popup_dismiss(self, instance):
        self.popup.dismiss()

    # Mark Exhaustion Limit ...............................................

    def exhaustion_spinner_clicked(self, value):
        global mark_exh_dict_var
        if value == "Mild":

            mark_exh_dict_var['mild'].append(float(self.todays_use_label))
            if len(mark_exh_dict_var['mild']) > 7:
                mark_exh_dict_var['mild'].clear()
                mark_exh_dict_var['mild'].append(float(self.todays_use_label))
        elif value == "Moderate":

            mark_exh_dict_var['moderate'].append(float(self.todays_use_label))
            if len(mark_exh_dict_var['moderate']) > 7:
                mark_exh_dict_var['moderate'].clear()
                mark_exh_dict_var['moderate'].append(float(self.todays_use_label))

        elif value == "Extreme":

            mark_exh_dict_var['extreme'].append(float(self.todays_use_label))
            if len(mark_exh_dict_var['extreme']) > 7:
                mark_exh_dict_var['extreme'].clear()
                mark_exh_dict_var['extreme'].append(float(self.todays_use_label))

        else:
            MDDialog(title="Error", text="An Error occurred while updating exhaustion limit on exhaustion_spinner_id "
                                         "clicked. "
                                         "Please contact at sgsonu132@gmail.com with the error statement.  ").open()
        Snackbar(text="Status Recorded").open()

        # Developer Notes :
        print("Exhaustion Limit Updated , mark_exh_dict_var value (List) >>>>", mark_exh_dict_var)


class Options_tab(MDBottomNavigationItem):
    # Define properties
    song_wtf = StringProperty(str(song_addresss_var))  # To link the variable to the song_address label
    flow_test_result_label = StringProperty(str(flow_test_result))  # to link variable to the flow test label
    #  Find average eye blinks >> NOTE: final_blinks is the global final result
    blink_test_result_label = StringProperty(str(float(final_blinks)))
    dialog = None  # Defining the dialog
    flow_test_time_gap = 0  # to keep the flow state of the user updated

    # Setting up user settings on leave :
    def flow_time_boolean_pressed(self, bool_value, *args):
        global flow_time_boolean
        flow_time_boolean = bool_value
        print("Boolean value of flow_time_boolean changed to :", flow_time_boolean)


    def mark_exh_limit_boolean_pressed(self,bool_value, *args):
        global  mark_exh_bool
        mark_exh_bool = bool_value
        print("Boolean value of the mark_exh_boolean changed to :", mark_exh_bool)

    def on_pre_enter(self, *args):
        # set the bool switches of the flow limit and mark_exh_limit features :

        self.ids.flow_time_boolean_id.active = flow_time_boolean
        self.ids.exh_limit_bool_id.active = mark_exh_bool

    # Theme Picker ..............................

    def Open_theme_picker(self):
        theme_manager = MDThemePicker()
        theme_manager.open()

        # File Chooser **(Different for PC and Mobile)...........................

    def Open_file_chooser(self):  # FOR PC APP

        # using tkinter
        self.temp_tk_root = tkinter.Tk()
        self.temp_tk_root.withdraw()
        # tk dialog
        self.filename = tkinter.filedialog.askopenfilename(title="Choose .mp3 or .wav file ",
                                                           filetypes=(('mp3 files', '*.mp3')
                                                                      , ('.wav files', '*.wav')))
        # Update and closing dialog file chooser
        self.temp_tk_root.update()
        self.temp_tk_root.destroy()
        self.ids.song_address_id.text = self.filename

        global song_addresss_var
        song_addresss_var = self.filename

    # ..........................Flow Limit Test ........................................................................

    def flow_limit_test(self):
        if "Stop" in self.ids.test_flow_limit_id.text:
            Clock.unschedule(self.flow_test_clock)
            self.ids.test_flow_limit_id.text = "Test Flow Limit"
            print("stopped")

        else:
            self.dialog_text = """ 
NOTE: Do not switch to other tabs before completing the test.You can cancel it any time by press the same button. 
To test your work flow limit follow the steps:
              1. On Pressing START, the timer will start.
              2. Try to focus on any task(say reading a book) and continue it in one stretch.
              3. On notification sound, check the device and give the user input 
FOR MORE: 'What is Mind Flow Limit ?' Check About Tab """

            self.dialog = MDDialog(title="Work Flow Limit Test",
                                   text=self.dialog_text,
                                   buttons=[
                                       MDFlatButton(text="Cancel", font_size=20,
                                                    on_press=self.dismiss_dialog),
                                       MDRectangleFlatButton(text="Start", font_size=20,
                                                             on_press=self.start_flow_test)

                                   ])
            print("Dialog box created !")
            self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def start_flow_test(self, moderate="None", flow_test_time_gap=0, *args):  # flow_test_time_gap should be in min

        if len(self.ids.test_flow_limit_id.text) < 17:
            # change test_flow_limit_id.text to "STOP FLOW LIMIT TEST"
            self.ids.test_flow_limit_id.text = "Stop Flow Limit Test"
            print("changed the button text and test started")
            if self.dialog:
                self.dialog.dismiss()
            # Note the starting time only at starting time i.e flow_test_time_gap = 0>>
            if flow_test_time_gap == 0:
                self.start_flow_time = time.time()
            # as user gives in min and we use in sec >>                               \/\/
            self.start_flow_time_gap = flow_test_time_gap  # get time gap

            # Start clock >>

            if self.flow_test_time_gap < 25:  # 25 min
                self.flow_test_clock = Clock.schedule_once(self.flow_test_dialog, 25 * 60)

            elif 25 <= self.flow_test_time_gap < 90:  # 90 min
                if moderate == "Moderate":  # moderate or not
                    self.flow_test_clock = Clock.schedule_once(self.flow_test_dialog, (25 * 60) / 2)
                elif moderate == "Continue":
                    self.flow_test_clock = Clock.schedule_once(self.flow_test_dialog, 25 * 60)
                else:
                    self.dialog = MDDialog(text="""An unknown error occurred while checking flow_test_time_gap
                    Please contact the developer explaining the issue at sgsonu132@gmail.com""")
                    self.dialog.open()

            else:
                self.flow_test_tired()

    # Flow test start >>

    # Notification clock definition
    def notify(self, *args):
        beep(sound=6)

    # Flow Start here >>
    def flow_test_dialog(self, *args):
        # Play sound every 5 sec to call the user

        notification_clock = Clock.schedule_interval(self.notify, 10)

        self.dialog = MDDialog(title="Flow Test User Input",
                               text="Do you feel like continuing the work ?",
                               buttons=[
                                   MDRectangleFlatButton(text="No, I am tired", font_size=20,
                                                         on_press=self.flow_test_tired),
                                   MDRectangleFlatButton(text="Moderate", font_size=20,
                                                         on_press=self.flow_test_moderate),
                                   MDRectangleFlatButton(text="Yes, of course", font_size=20,
                                                         on_press=self.flow_test_continue)

                               ])
        self.dialog.open()

    def flow_test_tired(self, *args):

        Clock.unschedule(self.notify)  # Stop notification sound

        if self.dialog:
            self.dialog.dismiss()
        self.start_flow_time_gap = (time.time() - self.start_flow_time) / 60  # get time gap
        # Tired dialog >>
        if self.start_flow_time_gap < 25:
            self.dialog_text = """ Nice work ! Your flow state lies in the 'Normal' range: 
            < 25 min 
            and it will improve with the 'Performance Score'\n 
            """
        elif 25 < self.start_flow_time_gap < 50:
            self.dialog_text = """ Great work ! Your flow state lies in the 'Good' range: 
            25 min to 50 min 
            and it will improve with the 'Performance Score'\n 
            """
        elif 50 < self.start_flow_time_gap < 90:
            self.dialog_text = """ Super work ! Your flow state lies in the 'Excellent' range: 
            50 min to 90 min
            and it will improve with t
            he 'Performance Score'\n 
            """
        else:
            self.dialog_text = """ Super Human work ! Your flow state lies in the 'Outstanding' range: 
            90 min < 
            and it will improve with the 'Performance Score'\n 
            """
        # Changing the variable linked with the Flow Limit label in MainWindow Class
        global flow_test_result  # global change (min)
        flow_test_result = self.start_flow_time_gap  # this is the user's Flow Time
        # End Dialog
        self.dialog = MDDialog(title="Flow Test Result",
                               text=self.dialog_text + f"\nYour 'Flow State' is estimated to be\n near about {flow_test_result} min",
                               buttons=[
                                   MDRectangleFlatButton(text=" OK", font_size=20,
                                                         on_press=lambda x: self.dialog.dismiss())
                               ])

    def flow_test_moderate(self, *args):

        Clock.unschedule(self.notify)  # Stop notification sound

        if self.dialog:
            self.dialog.dismiss()
        self.start_flow_time_gap = (time.time() - self.start_flow_time) / 60  # in min
        self.moderate = "Moderate"
        self.start_flow_test(self.moderate, int(self.start_flow_time_gap))  # flow_test_time_gap should be in min

    def flow_test_continue(self, *args):

        Clock.unschedule(self.notify)  # Stop notification sound

        if self.dialog:
            self.dialog.dismiss()
        self.start_flow_time_gap = (time.time() - self.start_flow_time) / 60  # in min
        self.moderate = "Continue"
        self.start_flow_test(self.moderate, int(self.start_flow_time_gap))  # flow_test_time_gap should be in min


"""

    # Code Only For Android (MDFileManger related) 
    
    def select_path(self, path):
        self.ids.song_address_id.text = str(path)
        print(path)

    def exit_manager(self, *args):
        self.file_chooser.close()

        # **Look for error here in Android
"""


class Records_Tab(MDBottomNavigationItem):
    # Defining >>
    # user data of progress managing option
    measure_limit_var = StringProperty(str(set_data_get['week_measure_limit']))
    measure_option_var = StringProperty(str(set_data_get['week_measure_option']))
    progress_since_date = StringProperty(str(week_date_var))
    flow_test_result_show = StringProperty(str(float(flow_test_result)))
    pc_mobile_var = StringProperty((rec_list['pc_mobile']))
    study_var = StringProperty(str(rec_list['study']))
    limited_time_var = StringProperty(str(rec_list['limited_time_task']))
    pomo_var = StringProperty(str(rec_list['pomo']))
    mind_wandering_var = StringProperty(str(rec_list['mind_wandering']))
    # Exhaustion limit variables :
    # Making avg >>
    mild_limit_avg = make_avg(mark_exh_dict_var['mild'])
    moderate_limit_avg = make_avg(mark_exh_dict_var['moderate'])
    extreme_limit_avg = make_avg(mark_exh_dict_var['extreme'])
    # Putting avg values >>
    mild_limit = StringProperty(str(mild_limit_avg))
    moderate_limit = StringProperty(str(moderate_limit_avg))
    extreme_limit = StringProperty(str(extreme_limit_avg))


    def on_pre_enter(self, *args):
        print("Updating the Progress ON_ENTRY TO RECORDS TAB ")
        # NOTE for Developer :The values in the rec_list are all in sec , so we convert them to hr by / 3600

        # Progress Status Update :

        self.pc_mobile_var = str(float(rec_list['pc_mobile']) / 3600)
        self.ids.screen_progress_label_id.text = "PC, Mobile Tasks: " + str(
            round(float(self.pc_mobile_var) / 3600, 4)) + "hr/" + str(self.measure_limit_var) + " hr"

        self.study_var = str(float(rec_list['study']) / 3600)
        self.ids.study_progress_label_id.text = "Study Tasks:" + str(
            round(float(self.study_var) / 3600, 4)) + "hr/" + str(self.measure_limit_var) + " hr"

        self.limited_time_var = str(float(rec_list['limited_time_task']) / 3600)
        self.ids.timedtask_progress_label_id.text = "Limited Time Tasks:" + str(
            round(float(self.limited_time_var) / 3600, 4)) + "hr/" + str(self.measure_limit_var) + " hr"

        self.pomo_var = str(float(rec_list['pomo']) / 3600)
        self.ids.pomo_progress_label_id.text = "Pomodoro Tasks:" + str(
            round(float(self.pomo_var) / 3600, 4)) + "hr/" + str(self.measure_limit_var) + " hr"

        self.mind_wandering_var = str(rec_list['mind_wandering'])
        self.ids.mindwandering_progress_label_id.text = "60/10 Method Tasks:" + str(
            round(float(self.mind_wandering_var) / 3600, 4
                  )) + "hr/" + str(self.measure_limit_var) + " hr"
        # For debugging :
        print("Progress bar status :", self.pc_mobile_var, self.study_var, self.limited_time_var, self.pomo_var, self.mind_wandering_var)

        # Exhaustion Limit Status Update:

        self.mild_limit_avg = make_avg(mark_exh_dict_var['mild'])
        self.moderate_limit_avg = make_avg(mark_exh_dict_var['moderate'])
        self.extreme_limit_avg = make_avg(mark_exh_dict_var['extreme'])

        self.mild_limit = str(round(float(self.mild_limit_avg),3))
        self.moderate_limit = str(round(float(self.moderate_limit_avg),3))
        self.extreme_limit = str(round(float(self.extreme_limit_avg),3))

        print("Updated Exhaustion Limit :", self.mild_limit , self.extreme_limit, self.extreme_limit)

    def set_custom_limit(self, instance):
        if len(self.ids.progress_limit_textfield_id.text) == 0:
            MDDialog(
                title="No input given to Custom Limit Text Box! Please give input or change to other modes.").open()
            self.ids.progress_limit_textfield_id.focus = True
            self.snackbar_custom_limit.open()
        else:
            self.snackbar_custom_limit.dismiss()
            set_data_get['week_measure_limit'] = str(self.ids.progress_limit_textfield_id.text)  # For global change
            self.measure_limit_var = str(self.ids.progress_limit_textfield_id.text)  # For local change
            print(self.ids.progress_limit_textfield_id.text, set_data_get['week_measure_limit'], self.measure_limit_var,
                  "Progress_bar values (for testing):", self.ids.screen_progress_id.max)
            self.ids.progress_limit_textfield_id.disabled = True

    def when_measure_limit_change(self, spinner_text):

        if spinner_text == "Custom":

            self.ids.progress_limit_textfield_id.disabled = False
            self.ids.progress_limit_textfield_id.focus = True
            self.snackbar_custom_limit = Snackbar(buttons=[
                MDRectangleFlatButton(text="SET", size_hint=(0.5, 0.9), font_size=25, on_press=self.set_custom_limit)],
                text="Press SET after setting custom limit :-", font_size=15, auto_dismiss=False,
            )
            self.snackbar_custom_limit.open()

        else:
            try:
                if self.snackbar_custom_limit:
                    self.snackbar_custom_limit.dismiss()
            except:
                pass
            set_data_get['week_measure_limit'] = str(spinner_text)  # For global change
            self.measure_limit_var = str(spinner_text)  # For local change
            print(spinner_text, set_data_get['week_measure_limit'], self.measure_limit_var)
            self.ids.progress_limit_textfield_id.disabled = True

    def when_measure_progress_change(self, spinner_text):

        set_data_get['week_measure_option'] = str(spinner_text)


class WindowManager(ScreenManager):
    pass


# Loading kv file
"""kv file should be loaded at the end so that classes
can be read """


# Main app blueprint


class NewApp(MDApp):
    """ Remember Anything you keep in App Class is accessible everywhere but this is not true for other classes """
    # Main requirements - Reading uses saved pickled file
    set_data_get = app_manager.On_Start_Settings()
    set_get_records = app_manager.Get_Records()

    def on_start(self):
        # Build file UI using KV file
        Builder.load_file('New.kv')
        # Applying the user theme
        self.theme_cls.primary_palette = self.set_data_get['primary_palette']
        self.theme_cls.theme_style = self.set_data_get['theme_style']
        self.theme_cls.accent_palette = self.set_data_get['accent_palette']
        Options_tab().ids.song_address_id.text = set_data_get['song_address']
        # Get today's date and test to update current day's use time : -
        self.today_date = datetime.date.today()
        if self.today_date != self.set_get_records['date']:  # Set the label to 0 hr and 0 min if diff. date
            with open("records.dat", "rb+") as records_rec:
                record_dict = pickle.load(records_rec)
                record_dict['today_hr'] = 0
                record_dict['date'] = self.today_date
                pickle.dump(record_dict, records_rec)
                print("Date Changed ! ...", records_rec)  # <<...........................date changed new today's timing

    def build(self):
        pass

    def on_stop(self):
        # pp= primary_palette , ts = theme_style , ap =accent_palette
        pp = self.theme_cls.primary_palette
        ts = self.theme_cls.theme_style
        ap = self.theme_cls.accent_palette
        sd = song_addresss_var
        fl = flow_test_result
        fl_bool = flow_time_boolean
        b = blink_test_result
        weeK_measure_option = set_data_get['week_measure_option']
        week_measure_limit = set_data_get['week_measure_limit']
        mark_exh_dict = mark_exh_dict_var
        mark_exh_bool_save = mark_exh_bool
        print(pp, ts, ap, sd, fl, fl_bool, b, weeK_measure_option, week_measure_limit)

        # Writing user data into pickled file
        app_manager.On_Stop_Settings(pp, ts, ap, sd, fl, fl_bool, b, weeK_measure_option, week_measure_limit,
                                     mark_exh_dict, mark_exh_bool_save)


# Adding more stuffs ................................

LabelBase.register(name='normal_font', fn_regular='normal_font.otf')
LabelBase.register(name='digital_font', fn_regular='digital_font.ttf')

NewApp().run()
