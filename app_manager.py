import datetime
import pickle
import random
import time
import os

# ........................BREAK MANAGER.................................................................................
import pygame as pygame
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from playsound import playsound

# Global variables declaration :

pomo_break_option = 0


def Get_Records():
    if not os.path.exists("records.dat"):
        with open("records.dat", "wb+") as records_rec:
            rec_list = {'pc_mobile': 0, 'study': 0, 'limited_time_task': 0, 'mind_wandering': 0,
                        'pomo': 0}  # everything in sec
            pickle.dump({'hr': 0, 'min': 0, 'today_hr': "0", 'today_min': "0", 'record_list': rec_list,
                         'date': datetime.date.today(), 'week_date': datetime.date.today()},
                        records_rec)
            record_dict = {'hr': 0, 'min': 0, 'today_hr': "0", 'today_min': "0", 'record_list': rec_list,
                           'date': datetime.date.today(), 'week_date': datetime.date.today()}
            return record_dict
    else:
        with open("records.dat", "rb") as records_rec:
            record_dict = pickle.load(records_rec)

    return record_dict


def Update_Records(count_sec, rec_list, week_date):
    # if file do not exists, create it
    if not os.path.exists("records.dat"):
        with open("records.dat", "wb") as records_rec:
            pickle.dump({'hr': 0, 'today_hr': 0, 'record_list': rec_list,
                         'date': datetime.date.today(), 'week_date': datetime.date.today()},
                        records_rec)

    with open("records.dat", "rb") as records_rec:
        record_dict = pickle.load(records_rec)
        # Today's day time addition >>
        today_hour_time = float(count_sec / 3600) + float(record_dict['today_hr'])
        # Total time addition >>
        total_hour_time = float(count_sec / 3600) + float(record_dict['hr'])

    with open("records.dat", "wb") as records_rec:
        # write into the file ( both today use ... total use and progress)
        pickle.dump(
            {'hr': total_hour_time, 'today_hr': today_hour_time, 'record_list': rec_list, 'date': datetime.date.today(),
             'week_date': week_date}, records_rec)

        print({'hr': total_hour_time, 'today_hr': today_hour_time, 'record_list': rec_list,
               'date': datetime.date.today(), 'week_date': week_date})  # <<-------------------------- to debug
        # also writing today's day

    # Returning today's time to the app in the form of hr (Today's use)
    return today_hour_time


# Special Function - Exhaustion Limit Checker :

def exh_limit_checker(mild, moderate, extreme, today_use, break_time_exh):

    if float(today_use) > float(mild):

        break_time_exh = break_time_exh + ((2/5)*break_time_exh)

        pass

    elif float(today_use) > float(moderate):

        break_time_exh = break_time_exh + ((3/5)*break_time_exh)
        pass

    elif float(today_use) > float(extreme):

        break_time_exh = break_time_exh + ((5/5)*break_time_exh)
        pass

    else:
        MDDialog(title="Error", text="An error occured while handling exh_limit_checker() \n "
                                     "Please contact at sgsonu132@gmail.com with the error statement").open()
        break_time_exh = 0  # Just not to make it undefined

    return break_time_exh


def On_Stop_Break(spinner_text, task_spinner_text, interval_time, break_count, flow_time, blink_num, flow_time_bool,
                  exh_limit_list, today_use_hr, mark_exh_bool):  # Default
    # Setting up exhaustion limit :
    today_use_hr = float(today_use_hr)

    def make_avg(element_x, element_sum=0):
        for i in element_x:
            element_sum = float(i) + float(element_sum)
        return element_sum / len(element_x)
        # Average of different limits

    mild_limit_avg_2 = make_avg(exh_limit_list['mild'])
    moderate_limit_avg_2 = make_avg(exh_limit_list['moderate'])
    extreme_limit_avg_2 = make_avg(exh_limit_list['extreme'])

    # Setting up Flow Time:
    if flow_time == "0":
        flow_time = 25

    # Check file exists (Done on start up)
    # IMP : Load file data in dictionary and update others (rb) (Done on start up)

    # Some definitions

    def break_over_notify(*args):
        if dialogs:
            dialogs.dismiss()
        x = random.randint(1, 3)
        if x == 1:
            sound_file = "Music/break_over.mp3"
        elif x == 2:
            sound_file = "Music/break_over_1.mp3"
        else:
            sound_file = "Music/break_over_2.mp3"

        playsound(sound_file)

        pygame.mixer.music.load("Music/beep_on.wav")
        pygame.mixer.music.play(loops=-1)

        #  Check if the user has come back
        def stop_beep_call(instance):
            pygame.mixer.music.stop()
            dialogs_stop_call.dismiss()

        dialogs_stop_call = MDDialog(title="Came back ?", buttons=[MDRectangleFlatButton(text="Yes!",
                                                                                         font_size=20,
                                                                                         on_press=stop_beep_call)])
        dialogs_stop_call.open()

    def break_time_notify(*args):
        x = random.randint(1, 3)
        if x == 1:
            source_file = "Music/break_time.mp3"
        elif x == 2:
            source_file = "Music/break_time_1.mp3"
        else:
            source_file = "Music/break_time_2.mp3"
        playsound(source_file)

    def close_button(instance):
        dialogs.dismiss()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    # some useless functions for pomodoro break selection (Why 3.9 python does'nt support lambda assignment !)
    # ????????????????????????????????????????? global/ local issue ??????????????????????????????????????????
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<< AVAILABLE IN THE NEXT VERSION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    global pomo_break_option

    def pomo_break_1(instance):

        pomo_break_option = (2 / 5) * float(interval_time_rounded)
        if dialog:
            dialog.dismiss()

        pass

    def pomo_break_2(instance):

        pomo_break_option = (4 / 5) * float(interval_time_rounded)
        if dialog:
            dialog.dismiss()

        pass

    def pomo_break_3(instance):


        pomo_break_option = float(interval_time_rounded)

        if dialog:
            dialog.dismiss()

        pass

    # Identifying algorithm and running if >> then wise .........................................

    if spinner_text == "AppName Algorithm(RECOMMENDED)":

        if task_spinner_text == "PC or Mobile Related":
            break_count += 1

            # inclusion of flow time logic (YES/NO ; based on flow_time_bool)

            if flow_time_bool:
                interval_time = (float(interval_time) + float(flow_time)) / 2
            else:
                interval_time = float(interval_time)

            required_blink_time = interval_time * (1 / 3) * (1 / 60) * (
                    20 - float(blink_num))  # converting in min
            required_20_20_rule = (1 / 60) * float(interval_time)
            required_moving_time = (1 / 20) * float(interval_time)
            normal_break_time = (1 / 5) * float(interval_time)
            break_time = normal_break_time + required_blink_time + required_20_20_rule + required_moving_time

            if (break_count % 4) == 0:
                break_time = 2 * break_count  # applying pomodoro technique
            break_time_notify()  # .......................................... tell the user that the break has started
            dialogs = MDDialog(text=f"Rest time [color=#42f55a]{float(break_time)} min [/color]",
                               buttons=[MDRectangleFlatButton(text="Okay", on_press=close_button, font_size=20)])
            dialogs.open()

            # Initiating the exhaustion limit checker :
            if ((today_use_hr > mild_limit_avg_2) or (today_use_hr > moderate_limit_avg_2) or (
                    today_use_hr > extreme_limit_avg_2)) and mark_exh_bool == True:
                break_time = exh_limit_checker(mild_limit_avg_2, moderate_limit_avg_2, extreme_limit_avg_2, today_use_hr, break_time)

                pass

            Clock.schedule_once(break_over_notify, break_time * 60)  # in min , start the break timer

        elif task_spinner_text == "Study":

            break_count += 1

            # inclusion of flow time logic (YES/NO ; based on flow_time_bool)

            if flow_time_bool:
                interval_time = (float(interval_time) + float(flow_time)) / 2
            else:
                interval_time = float(interval_time)

            required_moving_time = (1 / 20) * float(interval_time)
            required_pomo_break = (1 / 5) * float(interval_time)
            break_time = required_moving_time + required_pomo_break

            break_time_notify()

            dialogs = MDDialog(text=f"Time for a break of [color=#42f55a]{float(break_time)} min[/color]",
                               buttons=[MDRectangleFlatButton(text="Okay", on_press=close_button, font_size=20)])
            dialogs.open()

            # Clock.schedule_once(quick_revise_notify_close(dialog), 10)
            required_pomo_break = (1 / 5) * float(interval_time)
            # Calculate total break time:
            break_time = required_moving_time + required_pomo_break

            # Initiating exhaustion limit checker :
            if ((today_use_hr > mild_limit_avg_2) or (today_use_hr > moderate_limit_avg_2) or (
                    today_use_hr > extreme_limit_avg_2)) and mark_exh_bool == True:
                break_time = exh_limit_checker(mild_limit_avg_2, moderate_limit_avg_2, extreme_limit_avg_2, today_use_hr, break_time)
                # Break time should be returned !

            Clock.schedule_once(break_over_notify, break_time * 60)  # in min

        elif task_spinner_text == "Limited Time Task":
            # no need to do anything this is a already
            # existing feature of the app in __main__ code
            pass

    elif spinner_text == "Pomodoro Technique":
        print("Entered Pomodoro Technique Break Calculation in Module - app_manager")
        break_count += 1
        global pomo_break_option
        pomo_break_option = (1 / 5) * float(interval_time)  # in case of issues

        if break_count % 1 == 0:
            interval_time_rounded = round(float(interval_time), 4)
            dialog = MDDialog(text="Select Long Break Duration :",
                              buttons=[MDFlatButton(text=str(round((2 / 5) * (float(interval_time_rounded)), 4)),
                                                    on_press=pomo_break_1),
                                       MDFlatButton(text=str(round((4 / 5) * (float(interval_time_rounded)), 4)),
                                                    on_press=pomo_break_2),
                                       MDFlatButton(text=str(round(float(interval_time_rounded), 4)),
                                                    on_press=pomo_break_3)])
            # dialog.open() >> will be available in the next version

        else:
            pass

        break_time = pomo_break_option

        if (break_count % 4) == 0:
            break_time = 2 * break_time  # applying pomodoro technique

        break_time_notify()  # tell the user that the break has started
        dialogs = MDDialog(text=f"Rest time [color=#42f55a]{float(break_time)} min [/color]",
                           buttons=[MDRectangleFlatButton(text="Okay", on_press=close_button, font_size=20)])
        dialogs.open()
        Clock.schedule_once(break_over_notify, break_time * 60)  # in min , start the break timer

    elif spinner_text == "60/10 Method":
        print("Entered 60/10 Method Calculation in module - app_manager")
        # This is straight forward 60 min task followed by 10 min of break
        break_time = 10

        break_time_notify()  # tell the user that the break has started
        dialogs = MDDialog(text=f"Rest time [color=#42f55a]{float(break_time)} min [/color]",
                           buttons=[MDRectangleFlatButton(text="Okay", on_press=close_button, font_size=20)])
        dialogs.open()
        Clock.schedule_once(break_over_notify, break_time * 60)  # in min , start the break timer

        pass


# .....................SETTINGS_MANAGER.................................................................................


def On_Start_Settings():
    if not os.path.exists("settings.dat"):
        with open("settings.dat", "wb") as settings_rec:
            pickle.dump({'primary_palette': 'Green',
                         'theme_style': 'Dark',
                         'accent_palette': 'Blue',
                         'song_address': '-',
                         'flow_limit': '0',
                         'flow_time_boolean': False,
                         'blinks': [5],
                         'week_measure_option': "Weekly",
                         'week_measure_limit': "8",
                         'mark_exhaustion_dict': {'mild': [5], 'moderate': [8], 'extreme': [12]},
                         'mark_exh_bool': False},
                        settings_rec)

    with open("settings.dat", "rb") as settings_rec:
        set_data = pickle.load(settings_rec)

    return set_data


def On_Stop_Settings(pp, ts, ap, sd, fl, fl_boolean,
                     b, week_measure_option, week_measure_limit,
                     mark_exh_dict, mark_exh_bool_save):  # pp= primary_palette , ts = theme_style ,
    # ap =accent_palette,
    # sd=song_address # week_measure_option : it is to save the week progress method
    # week_measure_limit: it sets the limit in progress
    # fl = flow_limit, b = blinks

    with open("settings.dat", "wb") as settings_rec:
        pickle.dump({"primary_palette": str(pp),
                     'theme_style': str(ts),
                     'accent_palette': str(ap),
                     'song_address': sd,
                     'flow_limit': fl,
                     'flow_time_boolean': fl_boolean,
                     'blinks': b,
                     'week_measure_option': week_measure_option,
                     'week_measure_limit': week_measure_limit,
                     'mark_exhaustion_dict': mark_exh_dict,
                     'mark_exh_bool': mark_exh_bool_save
                     }, settings_rec)


# ............................................Extra Functions..........................................................

#  For habit maker .....................................
def habit_close_button_text():
    x = random.randint(1, 5)
    if x == 1:
        close_button_text = "I Know it !"
    elif x == 2:
        close_button_text = "Oh ! Okay"
    elif x == 3:
        close_button_text = "I just know it !"
    elif x == 4:
        close_button_text = "Ya, I learnt"
    else:
        close_button_text = "Yes Master :)"

    return close_button_text


def habit_label_text(gif_name):
    label_text = "-"
    if gif_name == "posture":
        x = random.randint(1, 5)
        if x == 1:
            label_text = "Sitting Upright Prevents Back Pain"
        elif x == 2:
            label_text = "Sit Straight to stand tall"
        elif x == 3:
            label_text = "if you are looking at screens,pls.don't bent towards the screen"
        elif x == 4:
            label_text = "A Straight Back Bone Makes Task Easy"
        else:
            label_text = "Mr. Back Bone Straight , Now :)"

    elif gif_name == "drinkwater":

        x = random.randint(1, 5)
        if x == 1:
            label_text = "Drinking water is NOT important, right?"
        elif x == 2:
            label_text = "Drink water to keep yourself growing"
        elif x == 3:
            label_text = "Keep a water bottle near you, always"
        elif x == 4:
            label_text = "Our body is water and it needs it"
        else:
            label_text = "Remember to drink enough water !"

    elif gif_name == "star":

        x = random.randint(1, 5)
        if x == 1:
            label_text = "Please rate us"
        elif x == 2:
            label_text = "Do review me"
        elif x == 3:
            label_text = "Just give it a 5 star if you like me"
        elif x == 4:
            label_text = "I am tired , give me some star rating"
        else:
            label_text = "5 star vs 0 star , rate me"


# For mind wandering (playing youtube video):

def play_mind_wandering_music():
    x = random.randint(1, 10)
    if x == 1:
        wandering_song = "Please rate us"
    elif x == 2:
        wandering_song = "Do review me"
    elif x == 3:
        wandering_song = "Just give it a 5 star if you like me"
    elif x == 4:
        wandering_song = "I am tired , give me some star rating"
    elif x == 5:
        wandering_song = "5 star vs 0 star , rate me"
    elif x == 6:
        wandering_song = "Keep moving while working"
    elif x == 7:
        wandering_song = "Change your position and move"
    elif x == 8:
        wandering_song = "Humans are made to move and work"
    elif x == 9:
        wandering_song = "A break and a walk during a long task is good"
    else:
        wandering_song = "Remember to give your sedentary body a exercise"
