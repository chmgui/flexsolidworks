# flexlogsw01.py analyzes Solidworks lmgrd.log files and creates a filename.json 
# and filename_denied.json for each of them. It matches each OUT line in a log file 
# to an IN line and output to the filename.json file. The _denied.json file contains
# all the DENIED lines.
# 08/26/2022 CM GUI
#
from datetime import datetime
import zoneinfo
#from zoneinfo import ZoneInfo
from datetime import timezone
from datetime import timedelta
import json
import os
import os.path
import tkinter
from tkinter import filedialog
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from tkinter import messagebox
import collections

def find_dup1(l):
    dupes = []
    flat = [item for sublist in l for item in sublist]
    for f in flat:
        if flat.count(f) > 1:
            if f not in dupes:
                dupes.append(f)
    if dupes:
        return dupes
    else:
        return False


def sort1(sub1):
    sub1.sort(key = lambda x: x[0])
    return sub1
# we sort by out_datetime1
def sortkey1(e):
    return e[2]
# def sortkey0(e):
#     return e[0]




def timezone_win_iana_mapping1(tz1):
    # this maps Windows time zone names to Unix/IANA time zone names used by Python Datetime
    timezone_win_iana1 = [
    {'Dateline Standard Time': 'Etc/GMT+12'} ,
    {'UTC-11': 'Etc/GMT+11'} ,
    {'Aleutian Standard Time': 'America/Adak'} ,
    {'Hawaiian Standard Time': 'Pacific/Honolulu'} ,
    {'Marquesas Standard Time': 'Pacific/Marquesas'} ,
    {'Alaskan Standard Time': 'America/Anchorage'} ,
    {'UTC-09': 'Etc/GMT+9'} ,
    {'Pacific Standard Time (Mexico)': 'America/Tijuana'} ,
    {'UTC-08': 'Etc/GMT+8'} ,
    {'Pacific Standard Time': 'America/Los_Angeles'} ,
    {'US Mountain Standard Time': 'America/Phoenix'} ,
    {'Mountain Standard Time (Mexico)': 'America/Chihuahua'} ,
    {'Mountain Standard Time': 'America/Denver'} ,
    {'Central America Standard Time': 'America/Guatemala'} ,
    {'Central Standard Time': 'America/Chicago'} ,
    {'Easter Island Standard Time': 'Pacific/Easter'} ,
    {'Central Standard Time (Mexico)': 'America/Mexico_City'} ,
    {'Canada Central Standard Time': 'America/Regina'} ,
    {'SA Pacific Standard Time': 'America/Bogota'} ,
    {'Eastern Standard Time (Mexico)': 'America/Cancun'} ,
    {'Eastern Standard Time': 'America/New_York'} ,
    {'Haiti Standard Time': 'America/Port-au-Prince'} ,
    {'Cuba Standard Time': 'America/Havana'} ,
    {'US Eastern Standard Time': 'America/Indiana/Indianapolis'} ,
    {'Turks And Caicos Standard Time': 'America/Grand_Turk'} ,
    {'Paraguay Standard Time': 'America/Asuncion'} ,
    {'Atlantic Standard Time': 'America/Halifax'} ,
    {'Venezuela Standard Time': 'America/Caracas'} ,
    {'Central Brazilian Standard Time': 'America/Cuiaba'} ,
    {'SA Western Standard Time': 'America/La_Paz'} ,
    {'Pacific SA Standard Time': 'America/Santiago'} ,
    {'Newfoundland Standard Time': 'America/St_Johns'} ,
    {'Tocantins Standard Time': 'America/Araguaina'} ,
    {'E. South America Standard Time': 'America/Sao_Paulo'} ,
    {'SA Eastern Standard Time': 'America/Cayenne'} ,
    {'Argentina Standard Time': 'America/Argentina/Buenos_Aires'} ,
    {'Greenland Standard Time': 'America/Godthab'} ,
    {'Montevideo Standard Time': 'America/Montevideo'} ,
    {'Magallanes Standard Time': 'America/Punta_Arenas'} ,
    {'Saint Pierre Standard Time': 'America/Miquelon'} ,
    {'Bahia Standard Time': 'America/Bahia'} ,
    {'UTC-02': 'Etc/GMT+2'} ,
    {'Mid-Atlantic Standard Time': 'Etc/GMT+2'} ,
    {'Azores Standard Time': 'Atlantic/Azores'} ,
    {'Cape Verde Standard Time': 'Atlantic/Cape_Verde'} ,
    {'UTC': 'Etc/UTC'} ,
    {'Morocco Standard Time': 'Africa/Casablanca'} ,
    {'GMT Standard Time': 'Europe/London'} ,
    {'Greenwich Standard Time': 'Atlantic/Reykjavik'} ,
    {'W. Europe Standard Time': 'Europe/Berlin'} ,
    {'Central Europe Standard Time': 'Europe/Budapest'} ,
    {'Romance Standard Time': 'Europe/Paris'} ,
    {'Sao Tome Standard Time': 'Africa/Sao_Tome'} ,
    {'Central European Standard Time': 'Europe/Warsaw'} ,
    {'W. Central Africa Standard Time': 'Africa/Lagos'} ,
    {'Jordan Standard Time': 'Asia/Amman'} ,
    {'GTB Standard Time': 'Europe/Bucharest'} ,
    {'Middle East Standard Time': 'Asia/Beirut'} ,
    {'Egypt Standard Time': 'Africa/Cairo'} ,
    {'E. Europe Standard Time': 'Europe/Chisinau'} ,
    {'Syria Standard Time': 'Asia/Damascus'} ,
    {'West Bank Standard Time': 'Asia/Hebron'} ,
    {'South Africa Standard Time': 'Africa/Johannesburg'} ,
    {'FLE Standard Time': 'Europe/Kiev'} ,
    {'Israel Standard Time': 'Asia/Jerusalem'} ,
    {'Kaliningrad Standard Time': 'Europe/Kaliningrad'} ,
    {'Sudan Standard Time': 'Africa/Khartoum'} ,
    {'Libya Standard Time': 'Africa/Tripoli'} ,
    {'Namibia Standard Time': 'Africa/Windhoek'} ,
    {'Arabic Standard Time': 'Asia/Baghdad'} ,
    {'Turkey Standard Time': 'Europe/Istanbul'} ,
    {'Arab Standard Time': 'Asia/Riyadh'} ,
    {'Belarus Standard Time': 'Europe/Minsk'} ,
    {'Russian Standard Time': 'Europe/Moscow'} ,
    {'E. Africa Standard Time': 'Africa/Nairobi'} ,
    {'Iran Standard Time': 'Asia/Tehran'} ,
    {'Arabian Standard Time': 'Asia/Dubai'} ,
    {'Astrakhan Standard Time': 'Europe/Astrakhan'} ,
    {'Azerbaijan Standard Time': 'Asia/Baku'} ,
    {'Russia Time Zone 3': 'Europe/Samara'} ,
    {'Mauritius Standard Time': 'Indian/Mauritius'} ,
    {'Saratov Standard Time': 'Europe/Saratov'} ,
    {'Georgian Standard Time': 'Asia/Tbilisi'} ,
    {'Caucasus Standard Time': 'Asia/Yerevan'} ,
    {'Afghanistan Standard Time': 'Asia/Kabul'} ,
    {'West Asia Standard Time': 'Asia/Tashkent'} ,
    {'Ekaterinburg Standard Time': 'Asia/Yekaterinburg'} ,
    {'Pakistan Standard Time': 'Asia/Karachi'} ,
    {'India Standard Time': 'Asia/Kolkata'} ,
    {'Sri Lanka Standard Time': 'Asia/Colombo'} ,
    {'Nepal Standard Time': 'Asia/Kathmandu'} ,
    {'Central Asia Standard Time': 'Asia/Almaty'} ,
    {'Bangladesh Standard Time': 'Asia/Dhaka'} ,
    {'Omsk Standard Time': 'Asia/Omsk'} ,
    {'Myanmar Standard Time': 'Asia/Yangon'} ,
    {'SE Asia Standard Time': 'Asia/Bangkok'} ,
    {'Altai Standard Time': 'Asia/Barnaul'} ,
    {'W. Mongolia Standard Time': 'Asia/Hovd'} ,
    {'North Asia Standard Time': 'Asia/Krasnoyarsk'} ,
    {'N. Central Asia Standard Time': 'Asia/Novosibirsk'} ,
    {'Tomsk Standard Time': 'Asia/Tomsk'} ,
    {'China Standard Time': 'Asia/Shanghai'} ,
    {'North Asia East Standard Time': 'Asia/Irkutsk'} ,
    {'Singapore Standard Time': 'Asia/Singapore'} ,
    {'W. Australia Standard Time': 'Australia/Perth'} ,
    {'Taipei Standard Time': 'Asia/Taipei'} ,
    {'Ulaanbaatar Standard Time': 'Asia/Ulaanbaatar'} ,
    {'North Korea Standard Time': 'Asia/Pyongyang'} ,
    {'Aus Central W. Standard Time': 'Australia/Eucla'} ,
    {'Transbaikal Standard Time': 'Asia/Chita'} ,
    {'Tokyo Standard Time': 'Asia/Tokyo'} ,
    {'Korea Standard Time': 'Asia/Seoul'} ,
    {'Yakutsk Standard Time': 'Asia/Yakutsk'} ,
    {'Cen. Australia Standard Time': 'Australia/Adelaide'} ,
    {'AUS Central Standard Time': 'Australia/Darwin'} ,
    {'E. Australia Standard Time': 'Australia/Brisbane'} ,
    {'AUS Eastern Standard Time': 'Australia/Sydney'} ,
    {'West Pacific Standard Time': 'Pacific/Port_Moresby'} ,
    {'Tasmania Standard Time': 'Australia/Hobart'} ,
    {'Vladivostok Standard Time': 'Asia/Vladivostok'} ,
    {'Lord Howe Standard Time': 'Australia/Lord_Howe'} ,
    {'Bougainville Standard Time': 'Pacific/Bougainville'} ,
    {'Russia Time Zone 10': 'Asia/Srednekolymsk'} ,
    {'Magadan Standard Time': 'Asia/Magadan'} ,
    {'Norfolk Standard Time': 'Pacific/Norfolk'} ,
    {'Sakhalin Standard Time': 'Asia/Sakhalin'} ,
    {'Central Pacific Standard Time': 'Pacific/Guadalcanal'} ,
    {'Russia Time Zone 11': 'Asia/Kamchatka'} ,
    {'New Zealand Standard Time': 'Pacific/Auckland'} ,
    {'UTC+12': 'Etc/GMT-12'} ,
    {'Fiji Standard Time': 'Pacific/Fiji'} ,
    {'Kamchatka Standard Time': 'Asia/Kamchatka'} ,
    {'Chatham Islands Standard Time': 'Pacific/Chatham'} ,
    {'UTC+13': 'Etc/GMT-13'} ,
    {'Tonga Standard Time': 'Pacific/Tongatapu'} ,
    {'Samoa Standard Time': 'Pacific/Apia'} ,
    {'Line Islands Standard Time': 'Pacific/Kiritimati'} ,
    ]
    #print( "timezone_win_iana : ", timezone_win_iana)
    #res1 = [ x1 for x1 in timezone_win_iana1.keys() if x1 == tz1 ]
    #list2 = [ x1 for sub1 in list1 for x1 in sub1.items() ]
    #res1 = [ y1 for sub1 in timezone_win_iana1 for x1, y1 in sub1.items() if x1 == tz1 ]
    res1 = [ y1 for sub1 in timezone_win_iana1 for x1, y1 in sub1.items() if x1 == tz1 ]
    if res1:
        return res1[0].strip()
    else:
        # maps Daylight time, e.g., Pacific Daylight Time to be same as Pacific Standard Time
        if tz1.find('Daylight') != -1:
            tz1 = tz1.replace('Daylight','Standard')
            res1 = [ y1 for sub1 in timezone_win_iana1 for x1, y1 in sub1.items() if x1 == tz1 ]
            if res1:
                return res1[0].strip()
            else:
                return(False)
    return(False)

def get_lastdate1(filename1,tz1):
    # get the last date in the log file. First get date from a line nearest to end of log file
    # containing date info. After that, check if there is a decrease in the time at the 
    # beginning of line from previous line. If yes, add one day to date.
    with open(filename1, 'r') as f1:
        lines1 = f1.readlines()
    for j, line1 in enumerate(lines1[::-1]):
        if line1.find('-SLOG@) Start-Date:') != -1 or line1.find('-SLOG@) Time:') != -1:
            if line1.find('-SLOG@) Start-Date:') != -1: 
                currentdate1 = line1[ line1.find('-SLOG@) Start-Date:') + 23:]
            elif line1.find('-SLOG@) Time:') != -1:
                currentdate1 = line1[ line1.find('-SLOG@) Time:') + 18:]
            if currentdate1.find(':') == -1:
                print("error at line 300: currentdate1.find(':') == -1")
            else:
                currentdate1 = currentdate1[:currentdate1.find(':')-3].strip()
            dt_obj = datetime.strptime(currentdate1 + ' 00:00:00', '%b %d %Y %H:%M:%S')
            origin_tz = zoneinfo.ZoneInfo(tz1)
            dt_obj = datetime( dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=origin_tz)
            break
    hrprev1 = 0
    for line1 in lines1[-j:]:
        #print(line1)
        if line1.find(':') != -1 and line1.find('(') != -1:
            t1 = line1[:line1.find('(')].strip().split(':')
            hr1 = t1[0]
            if hr1.isdigit():
                hr1 = int(hr1)
                if hr1 < 24:
                    if hr1 < hrprev1:
                        if dt_obj:
                            dt_obj = dt_obj + timedelta(hours=24)
                hrprev1 = hr1
    if dt_obj:
        return dt_obj
    else:
        return False

def detect_timezone_startdate1(filename1):
    # Returns the IANA Time Zone and the starting date of the log file
    with open(filename1, 'r') as f1:
        lines1 = f1.readlines()
    for line1 in lines1:
        if line1.find('-SLOG@) Start-Date: ') != -1 or line1.find('-SLOG@) Time:') != -1:
            tz1 = line1[line1.rfind(':')+3:].strip()
            if line1.find('-SLOG@) Start-Date:') != -1: 
                currentdate1 = line1[ line1.find('-SLOG@) Start-Date:') + 23:]
            elif line1.find('-SLOG@) Time:') != -1:
                currentdate1 = line1[ line1.find('-SLOG@) Time:') + 18:]
            if currentdate1.find(':') == -1:
                print("error at line 200: currentdate1.find(':') == -1")
            else:
                currentdate1 = currentdate1[:currentdate1.find(':')-3].strip()
            dt_obj = datetime.strptime(currentdate1 + ' 00:00:00', '%b %d %Y %H:%M:%S')
            origin_tz = zoneinfo.ZoneInfo(timezone_win_iana_mapping1(tz1))
            dt_obj = datetime( dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=origin_tz)
            return timezone_win_iana_mapping1(tz1), dt_obj
            break
    return(False)


# This creates a list containing all the lines in the log file with 
# " (ptc_d) IN: " 
# so that we can mark a row in the list as Closed when we find an IN 
# corresponding to an OUT in the find_in_time1 function below
# so that an IN will only be associated with a single OUT.
# Note we assume that if user OUT at 1:01 and again at 1:05,
# and IN at 1:11 and 1:15, then 1:01 OUT is matched with 1:11 and 
# 1:05 with 1:15.
def create_out_in_list1(filename1):
    with open(filename1, 'r') as f1:
        lines1 = f1.readlines()
    list1 = []
    for line1 in lines1:
        #if line1.find('(ptc_d) OUT: "') != -1 or line1.find('(ptc_d) IN: "') != -1:
        if line1.find(') IN: "') != -1:
            list2 = [ line1, False ]
            list1.append(list2)
    print("Number of IN (return of license to server) in ", filename1[filename1.rfind("/")+1:], ": ", len(list1))
    return list1


# this find_in_time1 function finds the IN time following an OUT
def find_in_time1(list1, feat1, user1, out_in_list1):
    i = 0
    #print('inside find_in_time1 function', feat1, user1)
    #print('out_in_list1', out_in_list1)
    # list1 is the section of original list1 after current row, i.e, list1[current row:end]
    # as we only search lines after current line in log file to look for IN.
    if list1:
        #print('inside find_in_time1 function list1[0]= ', list1[0])
        #len1 = list1.len()
        closed1 = False
        for line1 in list1:
            #print('for loop = ', '(ptc_d) IN: "' + feat1 + '" ' + user1)
            # if user1 == 'ana@SF125-Guest':
            #     if line1.find('19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)') != -1:
            #         pass
            #         #print(" MMM line1 ", line1)
            if line1.find('(SW_D) IN: "' + feat1 + '" ' + user1) != -1:
                #print('found line1 = ', line1)  
                for i, line2 in enumerate(out_in_list1):
                    # out_in_list1 contains all the IN lines with a second field with False default
                    # value to indicate whether this IN line has been used to 'close' an earlier OUT.
                    # We search in out_in_list1 for a line1 containing an IN and then check if it 
                    # has been marked as 'closed' and then exit the loop. closed1 contains the status.
                    #pass
                    #print('line1, line2 = ', line1,line2)
                    #print(line2[1])
                    # PROBLEM in NO log file, we have two IN lines which are exactly the same
                    #19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)  line 7666
                    #19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)  line 7667
                    #So the inner loop will always break with closed1 equals to True
                    #during the attempt to match the second row line 7667.
                    #below is just a 'patch' to fix 2 same IN lines. We need to rewrite to check 
                    #for duplicates IN lines in the out_in_list1 and then handle according.
                    # In PA log file
                    #15:22:47 (ptc_d) IN: "PROE_EssentialsIIM" ethan@AT105-Ethan    line 16734
                    #15:22:47 (ptc_d) IN: "PROE_EssentialsIIM" ethan@AT105-Ethan    line 36750
                    #the patch does not work for PA log file because the lines are not contiguous.
                    #the permanent solution would be to associate each line in log file with 
                    #a Unix timestamp. Get time zone and then time for each line at the start of 
                    #script before doing the rest.
                    # UPDATE 08/26/2022 - In new version of script, we will use real copy of 
                    # the out_in_list ([:]) and do a pop or remove to remove the line instead 
                    # of using a "closed" field.  
                    # if line2[0].find(line1) != -1 and not line2[1]:
                    #     break
                    # below is a mess... 
                    if line2[0].find(line1) != -1:
                        #print('line1, line2 = ', line1,line2)
                        closed1 = line2[1]
                        if not closed1:
                            break
                        else:
                            if out_in_list1[i+1][0].find(line1) != -1:
                                closed1 = out_in_list1[i+1][1]
                                out_in_list1[i+1][1] = True
                                if not closed1:
                                    break

                            #above patch works only if the identical lines are contiguous
                            j = i + 1
                            #print('iii = ', i)
                            while j < len(out_in_list1):
                                #print('j + 1 ', j)
                                #print(out_in_list1[j])
                                if out_in_list1[j][0].find(line1) != -1:
                                    closed1 = out_in_list1[j][1]
                                    out_in_list1[j][1] = True
                                    if not closed1:
                                        break
                                j += 1


                # if user1 == 'ana@SF125-Guest':
                #     if line1.find('19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)') != -1:
                #         pass
                #         #print(" LLL line1 i ", line1, closed1, i)
                  
                if not closed1 and len(out_in_list1) > 0:
                    # NOTE !!!
                    line2[1] = True
                    # above marks the row as Closed
                    if line1.find('(INACTIVE)') != -1:
                        # if user1 == 'ana@SF125-Guest':
                        #     if line1.find('19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)') != -1:
                        #         print(" ZZZ line1 ", line1)
                        #         input('???')

                        return line1[:line1.find('(SW_D)')-1].strip(), True, line1
                    else:
                        return line1[:line1.find('(SW_D)')-1].strip(), False, line1

    return None, False, None        
                        

def get_filenames1():
    # Prompts user to select a log file via Windows Explorer browser
    currdir = os.getcwd()
    root1 = tkinter.Tk()
    root1.withdraw()
    #file_path1 = filedialog.askopenfilename()
    # note that tkinter.filedialog does not work. Need to have from tkinter import filedialog
    root1.filename =  filedialog.askopenfilenames(initialdir = os.getcwd(),title = "Select one of more Solidworks log file",filetypes = (("log files","*.log"),("all files","*.*")))
    #root1.filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select a log file or multiple log files",filetypes = (("log files","*.log"),("all files","*.*")))
    return(root1.filename)

filenames1 = []
filenames1 = get_filenames1()
for filename1 in filenames1:  
#for filename1 in ['ptc_d_no_072822.log']: 
#for filename1 in ['ptc_d_at_072822.log']: 
    out_in_list1 = create_out_in_list1(filename1)
    # tem1 = find_dup1(out_in_list1)
    # if tem1:
    #     print('tem1 = ', tem1)
    # print('len of out_in_list1 = ',len(out_in_list1))
    #print(out_in_list1[0])
    #print(out_in_list1[0:10])
    with open(filename1, 'r') as f1:
        lines1 = f1.readlines()
    origin_tz = zoneinfo.ZoneInfo('US/Pacific')
    dt_obj = datetime.strptime('01:01:1000' + ' 00:00:00', '%m:%d:%Y %H:%M:%S')
    dt_obj2 = datetime( dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=origin_tz)
    dt_obj3 = dt_obj2

    #print('dt_obj2 = ', dt_obj2)
    #for line1 in lines1:
    #    print(line1.rstrip())

    # to count the no. of rows in the new feature_use1 list and we add this in the first col.
    rowno1 = 0
    rowdenied1 = 0
    # the code below finds out the features in the log file   
    found1 = 0
    i = 0
    len1 = len(lines1)
    while (not found1) and i < len1:
        line1 = lines1[i]
    #    print("i = " , i, " xxx ", line1)
        i += 1 
        if line1.find('(SW_D) Server started on') != -1:
            found1 = 1
            features1 = line1[line1.rfind(':') + 1:].strip()
    #        print(' features1 = ', features1)
            line2 = lines1[i]
    #        print(" here found1 = ", found1, line2)
    #        print(line2.find('(ptc_d) EXTERNAL FILTERS are OFF'))
            # The features are in the lines starting from (SW_D) Server started on pa016 for:   snlcore
            # and ending in the line (SW_D) EXTERNAL FILTERS are OFF
            while (i < len1) and (line2.find('(SW_D) EXTERNAL FILTERS are OFF') == -1):
    #            print(" here2")
                temp1 = line2[ line2.find('(SW_D)') + 8: ]
                temp1 = temp1.replace('\t', ' ')
                features1 += ' ' + temp1.strip()
                #            print(' features1 = ', features1)
                i += 1
                line2 = lines1[i]
    #            print(" here i = ", i)
                
    features1 = features1.split(' ')
    # the loop below removes empty items in the features1 list
    while True:
        try:
            temp1 = features1.index('')
        except ValueError:
    #        print('error!')
            break
        else:
            features1.pop(temp1)
        
    #print('features1 = ', features1)

    features_interested1 = ['cae_cosmosfloworkspe','cae_cwadvpro','camstd','solidworks','swofficepremium','swofficepro','swpdmstd_cadeditor','visustd']
    feature_use1 = []
    denied_use1 = []

    # get the last time - the last row time in the log file
    # don't use for line1 in reversed(lines1) because that is not efficient
    j = len1 - 1
    line1 = lines1[j]
    time1 = line1[ 0:lines1[j].find('(')-1]
    while True:
        line1 = lines1[j]
        temp1 = line1.find('(SW_D) (@SW_D-SLOG@) Start-Date:')
        temp2 = line1.find('(SW_D) (@SW_D-SLOG@) Time:')
        j -= 1
        if temp1 != -1 or temp2 != -1:
            if temp1 != -1:
                currentdate1 = line1[ temp1 + 36:]
                #print(' 1 currentdate1 ', currentdate1)
                # NOTE !!!
            else:
                currentdate1 = line1[ temp2 + 31:]
                #print('temp2, currentdate1, line1 = ', temp2, currentdate1, line1)
                # NOTE !!!
            pos1 = currentdate1.find(':')
            if pos1 == -1:
                print('error! no :')
            else:        
                pos2 = currentdate1.rfind(':')
                tzone1 = currentdate1[pos2+3:].strip()
                currentdate1 = currentdate1[0:pos1-3].strip()
                #print(currentdate1)
                #exit()
            dt_obj = datetime.strptime(currentdate1 + ' 00:00:00', '%b %d %Y %H:%M:%S')
            if tzone1 == 'Pacific Standard Time' or tzone1 == 'Pacific Daylight Time':
                tzone1 = 'US/Pacific'
            elif tzone1 == 'Eastern Standard Time' or tzone1 == 'Eastern Daylight Time':
                tzone1 = 'US/Eastern'
            elif tzone1 == 'Central Standard Time' or tzone1 == 'Central Daylight Time':
                tzone1 = 'US/Central'   
            origin_tz = zoneinfo.ZoneInfo(tzone1)
            dt_obj2 = datetime( dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=origin_tz)
            origin_tz = zoneinfo.ZoneInfo('US/Pacific')
            dt_obj2 = dt_obj2.astimezone(origin_tz)
            break

    t1 = time1.split(':')
    #print('t1 = ', t1)
    last_time1 = dt_obj2 + timedelta(seconds=int(t1[2])+1, minutes=int(t1[1]), hours=int(t1[0]))
    #print('xxx dt_obj2 = ', dt_obj2.tzname())
    #print('last_time = ', last_time1)
    # we add one second to the time on the last line of the log file
    # in case the last line has is a OUT license line
    #exit()

    #i = 0  
    # we will use the i value from previous loop to save some time
    hrprev1 = 0 #hrprev1 = 24
    count_out1 = 0
    count_denial1 = 0
    while i < len1:  
        line1 = lines1[i]

        # we compare the time with previous line time
        # there are two types of line without time: Socket disconnected by remote. and Exiting.
        if (
        line1[:30] != 'Socket disconnected by remote.'
        and line1[:8] != 'Exiting.'
        ):
            if line1.find(':') != -1 and line1.find('(') != -1:
                #tem1 = line1[:line1.find('(')]
                t1 = line1[:line1.find('(')].strip().split(':')
                #print('t1 = ', t1)
                hr1 = t1[0]
        else:
            #print('&&& line1 = ', line1)
            pass
        # if the hour on the current line is less than the hour on the previous line
        # we add 24 hours to the current date object dt_obj2 (which has time zone info)
        #if t1 == [ '2','58','36']:
            #print('hr1, hrprev1, dt_obj2 = ', hr1, hrprev1, dt_obj2)
            #print('line1 = ', line1)
        if int(hr1) < hrprev1:
            #print('dt_obj2 = ', dt_obj2)
            #print('dt_obj3 = ', dt_obj3)
            #print('t1 = ', t1)
            if dt_obj2 > dt_obj3:
                #print(" Kilroy1 dt_obj2 = ", dt_obj2)
                dt_obj2 = dt_obj2 + timedelta(hours=24)
                #print(" Kilroy2 dt_obj2 = ", dt_obj2)
        hrprev1 = int(hr1)

        #temp1 = line1.find('(ptc_d) TIMESTAMP')
        # TIMESTAMP line does not have time zone.  temp2 is frequent enough
        temp1 = line1.find('(SW_D) (@SW_D-SLOG@) Start-Date:')
        temp2 = line1.find('(SW_D) (@SW_D-SLOG@) Time:')
        temp3 = line1.find('(SW_D) OUT:')
        temp4 = line1.find('(SW_D) DENIED: "')
        i += 1
    #    if temp1 != -1:
            #currentdate1 = line1[ temp1 + 18:].strip()
            #print('1 i, currentdate1 = ', i, currentdate1)
            #dt_obj = datetime.strptime(currentdate1 + ' 00:00:00 UTC', '%m/%d/%Y %H:%M:%S %Z')
            #dt_obj = datetime.strptime('01/02/22 00:00:00', '%m/%d/%y %H:%M:%S')
            #print("The type of the date is now",  type(dt_obj))
            #print("The date is", dt_obj)
    #    elif temp2 != -1:
        if temp1 != -1 or temp2 != -1:
            if temp1 != -1:
                currentdate1 = line1[ temp1 + 36:]
                # NOTE!!!
            else:
                currentdate1 = line1[ temp2 + 31:]
                # NOTE!!!
                #print('temp2, currentdate1, line1 = ', temp2, currentdate1, line1)
            pos1 = currentdate1.find(':')
            if pos1 == -1:
                print('error! no :')
            else:        
                pos2 = currentdate1.rfind(':')
                tzone1 = currentdate1[pos2+3:].strip()
                currentdate1 = currentdate1[0:pos1-3].strip()
            #print('2 i, currentdate1 = ', i, currentdate1)
            #dt_obj = datetime.strptime(currentdate1 + ' 00:00:00 UTC', '%b %d %Y %H:%M:%S %Z')
            dt_obj = datetime.strptime(currentdate1 + ' 00:00:00', '%b %d %Y %H:%M:%S')
            #print("The type of the date is now",  type(dt_obj))
            #print("The date is", dt_obj)
            #print('tzone1 = ', tzone1)
            if tzone1 == 'Pacific Standard Time' or tzone1 == 'Pacific Daylight Time':
                tzone1 = 'US/Pacific'
            elif tzone1 == 'Eastern Standard Time' or tzone1 == 'Eastern Daylight Time':
                tzone1 = 'US/Eastern'
            elif tzone1 == 'Central Standard Time' or tzone1 == 'Central Daylight Time':
                tzone1 = 'US/Central'   
            #print('tzone1 = ', tzone1)
            #print('xxx dt_obj = ', dt_obj.tzname())
            origin_tz = zoneinfo.ZoneInfo(tzone1)
            #print(origin_tz)
            #dt_obj = datetime.strptime(currentdate1 + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
            dt_obj2 = datetime( dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=origin_tz)
            #print('xxx dt_obj = ', dt_obj2.tzname())
            #print("The date is", dt_obj2)
            origin_tz = zoneinfo.ZoneInfo('US/Pacific')
            dt_obj2 = dt_obj2.astimezone(origin_tz)
            #print('2xxx dt_obj = ', dt_obj2.tzname())
            #print("2The date is", dt_obj2)
            #dt_obj2.replace(tzinfo=origin_tz)
            #dt_obj.replace(tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles"))
            #dt_obj.replace(tzinfo=timezone.utc)
            #print('xxx dt_obj = ', dt_obj2.tzname())
            #print("The date is", dt_obj2)
            #dt_obj.tzinfo=origin_tz
            # AttributeError: attribute 'tzinfo' of 'datetime.datetime' objects is not writable
            # 23:31:10 (ptc_d) TIMESTAMP 3/21/2022
            # 0:49:18 (ptc_d) IN: "PROE_EssentialsIIM" vicky@TW103-Vicky  
            # 2:22:25 (ptc_d) OUT: "PROE_EssentialsIIM" Mike@DESKTOP-TLFC9MD  
            # 3:14:49 (ptc_d) (@ptc_d-SLOG@) ===============================================
            # 3:14:49 (ptc_d) (@ptc_d-SLOG@) === Last 10 Client Requests Processing Time (in ms) ===
            # 3:14:49 (ptc_d) (@ptc_d-SLOG@) Time: Tue Mar 22 2022 03:14:49 Central Daylight Time
            # above is from NO log file, time cross to the next day without a Time: or Start-Date line
            # for us to get the new day date.
        elif temp3 != -1:
            count_out1 += 1
            feature1 = line1[ line1.find('"')+1:line1.rfind('"')].strip()
            #print('feature1 = ', feature1)
            # PA license server has a perpetual Creo 3 MECBASICENG license which is indistinguishable
            # from the subscription MECBASICENG.  We want to exclude it as we are only interested in 
            # subscription licenses.
            # Only AT has adv simulation subscription license MECBASICENG_License
            # if (
            # feature1 in features_interested1 
            # and not ((feature1=='MECBASICENG_License' or feature1=='MECBASICUI_License')
            # and filename1=='ptc_d_pa_072722.log')
            # ):
            # if (
            # feature1 in features_interested1 
            # and not ((feature1=='MECBASICENG_License' or feature1=='MECBASICUI_License')
            # and filename1!='ptc_d_at_072822.log')
            # ):
            if feature1 in features_interested1:
                time1 = line1[ 0:line1.find('(')-1]
                #print( time1 )
                if not dt_obj2:
                    print("Error: no currentdate1 dt_obj2 when we come to a OUT line")
                else:
                    #hr1 = int(time1[0:time1.find(':')])
                    #min1 = int(time1[time1.find(':')+1:time1.rfind(':')])
                    #sec1 = int(time1[time1.rfind(':')+1:])
                    t1 = time1.split(':')
                    #print('t1 = ', t1)
                    #print('hr1 = ', hr1, ' min1 = ', min1, ' sec1 = ', sec1)
                    #out_datetime1 = dt_obj2 + timedelta(seconds=sec1, minutes=min1, hours=hr1)
                    out_datetime1 = dt_obj2 + timedelta(seconds=int(t1[2]), minutes=int(t1[1]), hours=int(t1[0]))
                    #print('out_datetime1 =', out_datetime1)
                    #print('xxx out_datetime1.tzname = ', out_datetime1.tzname())
                    # note out_datetime1 is in PDT because dt_obj2 has been converted to PDT
                    user1 = line1[line1.rfind('"')+2:].strip()
                    #print('user1 = ', user1)
                    in_time1, inactive1, in_time_line1 = find_in_time1(lines1[i-1:],feature1,user1,out_in_list1)
                    # if there is no IN time associated with the OUT, we assign it to last_time1 if
                    # the OUT time is less than 24 hours from the last_time1 else...
                    if in_time1 is None:
                        if (last_time1 - out_datetime1).total_seconds()/3600 < 24:  
                            in_datetime1 = last_time1
                        else:
                            in_datetime1 = out_datetime1 + timedelta(hours=24)
                    else:
                        t1 = in_time1.split(':')
                        in_datetime1 = dt_obj2 + timedelta(seconds=int(t1[2]), minutes=int(t1[1]), hours=int(t1[0]))
                        if in_datetime1 < out_datetime1:
                            in_datetime1 = dt_obj2 + timedelta(seconds=int(t1[2]), minutes=int(t1[1]), hours=int(t1[0])+24)
                        else:
                            in_datetime1 = dt_obj2 + timedelta(seconds=int(t1[2]), minutes=int(t1[1]), hours=int(t1[0]))

                    #print('in_time1 = ', in_time1)
                    #print('i = ', i)
                    #origin_tz = zoneinfo.ZoneInfo('US/Pacific')         
                    #templist1 = [ feature1, int(out_datetime1.timestamp()), out_datetime1, time1,
                    #datetime.fromtimestamp(int(out_datetime1.timestamp())),
                    #datetime.fromtimestamp(int(out_datetime1.timestamp())).astimezone(origin_tz),
                    #int(in_datetime1.timestamp()), in_datetime1, in_time1,
                    #datetime.fromtimestamp(int(in_datetime1.timestamp())).astimezone(origin_tz),
                    #inactive1, user1 ]
                    #print('filename1 === ', filename1)
                    #if user1 == 'alla@MV123-Alla':
                        #print(" YYY i, line1 ", i, line1, in_time_line1)
                        # if line1.find('15:56:10 (ptc_d) OUT: "PROE_EssentialsIIM" ana@SF125-Guest') != -1:
                        #     print(" YYY i, line1 ", i, line1, in_time_line1)

                    templist1 = [ rowno1, feature1, int(out_datetime1.timestamp()), 
                    int(in_datetime1.timestamp()), 
                    inactive1, user1,
                    line1, in_time_line1, filename1
                    ]
                    rowno1 += 1
                    feature_use1.append( templist1 )
        elif temp4 == 9:
            count_denial1 += 1
            # for Denied
            feature1 = line1[ line1.find('"')+1:line1.rfind('"')].strip()
            # if (
            # feature1 in features_interested1 
            # and not ((feature1=='MECBASICENG_License' or feature1=='MECBASICUI_License')
            # and filename1=='ptc_d_pa_072722.log')
            # ):
            if feature1 in features_interested1:
                time1 = line1[ 0:line1.find('(')-1].strip()
                #print( " xxx time1 = ", time1 )
                if not dt_obj2:
                    print("Error: no currentdate1 dt_obj2 when we come to a DENIED line")
                else:
                    t1 = time1.split(':')
                    denied_datetime1 = dt_obj2 + timedelta(seconds=int(t1[2]), minutes=int(t1[1]), hours=int(t1[0]))
                    user1 = line1[line1.rfind('"')+2:line1.find(' ',line1.rfind('"')+2)].strip()    
                    errorno1 = line1[line1.rfind('(')+1:line1.rfind('))')]            
                    #print("XXX temp4 line1 ", temp4, line1)
                    templist1 = [ rowdenied1, feature1, int(denied_datetime1.timestamp()), user1,
                    errorno1, line1, filename1
                    ]
                    rowdenied1 += 1
                    denied_use1.append( templist1 )
                    #print("&&& templist1 ", templist1)
    print("Number of OUT (getting license from server) in ", filename1[filename1.rfind("/")+1:], ": ", count_out1)
    print("Number of DENIAL in ", filename1[filename1.rfind("/")+1:], ": ", count_denial1)
    print("The number of denials shown in graph can be lesser than above number ")
    print("because some denials to the same user can happen at the same time.")

    tz4, dt_obj4 = detect_timezone_startdate1(filename1)
    print("Start date in ",filename1[filename1.rfind("/")+1:], ": ", dt_obj4.strftime('%m/%d/%Y %Z') )
    dt_obj5 = get_lastdate1(filename1, tz4)
    print("End date in ",filename1[filename1.rfind("/")+1:], ": ", dt_obj5.strftime('%m/%d/%Y %Z') )
    #print(feature_use1)
    filename2 = filename1[:filename1.rfind('.')] + '.json'
    with open(filename2, 'w') as f2:
        json.dump(feature_use1,f2)
        #print( filename2, " created.")
    filename2 = filename1[:filename1.rfind('.')] + '_denied.json'
    with open(filename2, 'w') as f2:
        json.dump(denied_use1,f2)
        #print( filename2, " created.")
    #print(denied_use1)
    #input("???")
    #print('out_in_list1 ', out_in_list1)
    # tem1, tem2 = 0, 0
    # for m1, line1 in enumerate(out_in_list1):
    #     #if line1[0].find('19:54:27 (ptc_d) IN: "PROE_EssentialsIIM" ana@SF125-Guest  (INACTIVE)') != -1:
    #     if line1[0].find('15:22:47 (ptc_d) IN: "PROE_EssentialsIIM" ethan@AT105-Ethan') != -1:
    #         #pass
    #         print('line1 m1', line1, m1)

    #     if line1[1]: 
    #         tem1 += 1
    #     else:
    #         tem2 +=1
    #print('true = ', tem1)
    #print('false = ', tem2)


# This is the second script

    list1 = []
    list1 = feature_use1


    # startdate_str1 = '04/14/2022 0:0:0'
    # #startdate_str1 = '05/07/2022 0:0:0'
    # startdate1 = int(datetime.strptime(startdate_str1, '%m/%d/%Y %H:%M:%S').timestamp())
    # enddate_str1 = '08/14/2022 0:0:0'
    # #enddate_str1 = '05/16/2022 0:0:0'
    # enddate1 = int(datetime.strptime(enddate_str1, '%m/%d/%Y %H:%M:%S').timestamp())



    #print(list1)

    #feature1 = 'solidworks'
    #feature1 = 'swofficepremium'
    #feature1 = 'swofficepro'
    for feature1 in ['cae_cosmosfloworkspe','cae_cwadvpro','camstd','solidworks','swofficepremium','swofficepro','swpdmstd_cadeditor','visustd']:

        # we remove all sublists from the list of lists except for 'PROE_EssentialsIIM' feature
        list2 = [ sublist2 for sublist2 in list1 if feature1 in sublist2 ]

        #print(list2[:20])
        #exit()

        #list2 = [ sublist2.extend([False]) for sublist2 in list2 ]
        #above does not work
        for sublist2 in list2:
            sublist2.extend([False])

        #print(list2)
        #print(list2[:10])

        # we sort by out_datetime1
        # def sortkey1(e):
        #     return e[2]

        list2.sort(key=sortkey1)
        #print(list2[:10])
        #print(list2)


        #print('startdate1 = ', startdate1)
        #print('enddate1 = ', enddate1)

        #list2 = [ sublist2 for sublist2 in list2 if int(sublist2[2]) >= startdate1 and int(sublist2[2]) < enddate1 ]
        #print(list2)
        #print('startdate1 = ', startdate1)
        #print('enddate1 = ', enddate1)

        #print(list2)
        #print(list2[:10])
        #exit()
        # Logic: for every license OUT, we add a x point with value equals to the OUT time and increment y by one.
        # At the same time, we look at previous OUT to see if they are now IN (IN time before current OUT time)
        # if yes, we decrement y by one, we will mark the previous OUT as "closed"
        # so that we won't consider them again for the next OUT we process.
        x1 = []
        y1 = []
        coord1 = []
        i = 0
        yprev1 = 0
        #print(list2[:10])
        #list3 = list2[:]
        #print(list3[:10])
        for sublist2 in list2:
            #print('sublist2 OUT IN = ', sublist2[2], sublist2[3])
            #print('sublist2 = ', sublist2)
            # we look at all previous rows and decrement yprev for every IN earlier/equal to current OUT time 
            # and the marker "closed" must be false, i.e., not decremented before
            for sublist3 in list2:
                #print('sublist3 OUT IN closed', sublist3[2], sublist3[3], sublist3[9])
                #print('sublist3, sublist2  = ', sublist3, ' === ', sublist2)
                #print('sublist3 = ', sublist3)
                # if inner for loop reaches current row of outer for loop then exit inner for loop 
                if (sublist3==sublist2):
                    break
                # if sublist3[8] is False (the marker we added to list2, not closed yet) and IN time is earlier or equal to OUT time of current row.
                elif (not sublist3[9]) and (sublist3[3]<=sublist2[2]):
                    yprev1 -= 1
                    sublist3[9] = True
                    x1.append(sublist3[3])
                    y1.append(yprev1)
                    coord1.append([sublist3[3],yprev1])
                    #print('inside decrement yprev1 -= 1 : , sublist3[9] [sublist3[3],yprev1]', yprev1,sublist3[9],[sublist3[3],yprev1])
            # We increment y1 by one for the current OUT, i.e., x1.append(sublist2[1])   
            #print('1yprev1 = ', yprev1)     
            yprev1 += 1    
            # print('after increment 2yprev1 = [sublist2[2],yprev1]', yprev1, [sublist2[2],yprev1])   
            # if yprev1 > 5 and feature1 == 'PROE_EssentialsIIM':
            #     print('??? sublist3, sublist2  = ', sublist3, ' === ', sublist2)
            # elif yprev1 > 8 and feature1 == 'PROE_DesignAdv':
            #     print('+++ sublist3, sublist2  = ', sublist3, ' === ', sublist2)
            # elif yprev1 > 1 and feature1 == 'MECBASICENG_License':
            #     print('+++ sublist3, sublist2  = ', sublist3, ' === ', sublist2)
            # elif yprev1 > 1 and feature1 == 'MECBASICUI_License':
            #     print('+++ sublist3, sublist2  = ', sublist3, ' === ', sublist2)
            x1.append(sublist2[2])
            y1.append(yprev1)
            coord1.append( [sublist2[2],yprev1] )
            i += 1
            #input('???')
            #print( 'x1, y1 = ', x1, y1)

            # OUT and IN time the same - verified this is true in the log file. Verified for MECBASICUI_License
            # MECBASICENG_License
            # for sublist2 in list2:
            #     if sublist2[2] == sublist2[3]:
            #         print(" ==== ", sublist2)
        #print( 'x1, y1 = ', x1, y1)        
        #print( 'coord1 = ', coord1)
                    #         templist1 = [ rowno1, feature1, int(out_datetime1.timestamp()), 
                    # int(in_datetime1.timestamp()), 
                    # inactive1, user1,
                    # line1, in_time_line1, filename1
                    # ]
        if list2:
            yprev1 -= 1
            x1.append(list2[-1][3])
            y1.append(yprev1)
            coord1.append( [list2[-1][3],yprev1] )
        coord1 = sort1(coord1)
        #print( 'coord1 = ', coord1)
        filename2 = feature1 + '.json'
        with open(filename2, 'w') as f2:
          json.dump(coord1,f2)
          #print( filename2, " created.")
            
# this is the third script
# drop this - we won't do hourly no of denials as the no of denials in SW log is very low
# actually we should still do hourly but below isn't working
        # list2 = [ sublist2 for sublist2 in denied_use1 if feature1 in sublist2 ]
        # if len(list2) > 0:
        #     # NOTE !!!
        #     list2.sort(key=sortkey1)
        #     x2 = [ [sublist2[2],1] for sublist2 in list2]

        #     x2 = [ [datetime.fromtimestamp(ts[0]), ts[1]] for ts in x2 ]

        #     #print(x2)
        #     #exit()
        #     df = pd.DataFrame(x2, columns=['col1','col2'])

        #     #print("here df ", df)
        #     #input('?')
        #     # df.set_index('col1')
        #     df = df.set_index('col1', drop=False)
        #     hourly = df.resample('1H').sum()
        #     #print(hourly)
        #     #hourly = list(hourly)
        #     #hourly['col1'] = hourly['col1'].apply(str)
        #     #print(hourly.dtypes)
        #     #hourly=hourly.astype(str)
        #     #print(hourly.dtypes)
        #     #hourly['col1'] = hourly['col1'].strftime('%m/%d/%Y %H:%M:%S')
        #     #hourly = hourly.to_json()
        #     #hourly = hourly.values.tolist()
        #     #print(hourly)
            
        #     for index, row in hourly.iterrows():
        #         #print(index, index.timestamp(), row['col2'])
        #         #coord1.append([index.timestamp(),row['col2']])
        #         #print(type(int(index.timestamp())))
        #         coord1.append([int(index.timestamp()),int(row['col2'])])
        #         #print(row[0], row[1])
        #         #print(row)
        #         pass
        #         #print(row[0], row['col2'])
        #     #exit()


        #     #print(hourly.dtypes)
        #     #hourly_df['col1'] = df['col1'].resample('H').count()

        #     #df.groupby([pd.Grouper(key='col1', freq='H')]).count()
        #     #df2 = df.groupby(['col1'])['col1'].count()

        #     #data.groupby([pd.Grouper(key='created_at', freq='M'), 'store_type']).price.sum().head(15)

        #     #print(hourly)

        #     #x1 = [ datetime.fromtimestamp(ts) for ts in x1 ]




        #     #print('feature1, coord1 = ', feature1, coord1)
        #     # print('feature1, len(coord1', feature1, len(coord1))
        #     filename2 = feature1 + '_denied_hourly.json'
        #     with open(filename2, 'w') as f2:
        #       json.dump(coord1,f2)
        #  #     #print( filename2, " created.")
        #  templist1 = [ rowdenied1, feature1, int(denied_datetime1.timestamp()), user1,
        # errorno1, line1, filename1
        # ]
        #list2 = denied_use1
        #list2 = [ sublist2 for sublist2 in denied_use1 if feature1 in sublist2 ]

        list2 = [ sublist2[2] for sublist2 in denied_use1 if feature1 in sublist2 ]
        # print(list2)
        # input("?")
        list2.sort()
        #list2.sort(key=sortkey1)
        #list2.sort(key=sortkey0)
        x1 = []
        y1 = []
        coord1 = []
        i = 0


        # # for sublist2 in list2:
        # #     if i > 1:
        # #         if sublist2[2] == x1[i-1]:
        # #             y1[i-1] = y1[i-1] + 1
        # #             coord1[i-1] = [ coord1[i-1][0], coord1[i-1][1] + 1 ]
        # #         else:
        # #             y1.append(1)
        # #             x1.append(sublist2[2])
        # #             coord1.append([ sublist2[2], 1 ])
        # #             i += 1
        # #     else:
        # #         y1.append(1)
        # #         x1.append(sublist2[2])
        # #         coord1.append([ sublist2[2], 1 ])
        # #         i += 1

        coord1 = ([[item2, count2] for item2, count2 in collections.Counter(list2).items()])
     
        # print(coord1)
        # input("???")
        if coord1:
            #print('feature1, coord1 = ', feature1, coord1)
            #print('feature1, len(coord1', feature1, len(coord1))
            filename2 = feature1 + '_denied.json'
            with open(filename2, 'w') as f2:
              json.dump(coord1,f2)
              #print( filename2, " created")

# this is the fourth script

features1 = ['cae_cosmosfloworkspe','cae_cwadvpro','camstd','solidworks','swofficepremium','swofficepro','swpdmstd_cadeditor','visustd']
feature_dict1 = {
    'cae_cosmosfloworkspe':'SOLIDWORKS Flow Simulation',
    'cae_cwadvpro':'SOLIDWORKS Simulation Premium',
    'camstd':'SOLIDWORKS CAM Standard',
    'solidworks':'SOLIDWORKS Standard',
    'swofficepremium':'SOLIDWORKS Premium',
    'swofficepro':'SOLIDWORKS Professional',
    'swpdmstd_cadeditor':'SOLIDWORKS PDM Standard CAD Editor',
    'visustd':'SOLIDWORKS Visualize Standard'
}
answer1 = ""
#while answer1 not in ['Q', 'q', '1', '2', '3', '4']:
while True:
    print("Please enter one of the numbers below or Q or q to quit.")
    print("1    SOLIDWORKS Flow Simulation")
    print("2    SOLIDWORKS Simulation Premium")
    print("3    SOLIDWORKS CAM Standard")
    print("4    SOLIDWORKS Standard")
    print("5    SOLIDWORKS Premium")
    print("6    SOLIDWORKS Professional")
    print("7    SOLIDWORKS Flow Simulation Denial")
    print("8    SOLIDWORKS Simulation Premium Denial")
    print("9    SOLIDWORKS CAM Standard Denial")
    print("10   SOLIDWORKS Standard Denial")
    print("11   SOLIDWORKS Premium Denial")
    print("12   SOLIDWORKS Professional Denial")



    print("A graph will pop up if you enter 1 to 12. Close the graph to enter another choice.")
    answer1 = input("Please enter your choice: ")
    if answer1 == 'Q' or answer1 == 'q': 
        break
    if answer1.strip() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
        continue
    if int(answer1) < 7:
        feature1 = features1[int(answer1)-1]
        filename1 = feature1 + '.json'
        if not os.path.exists(filename1):
            print(filename1, " does not exist.")
            messagebox.showinfo('Solidworks license log', 'No data for this feature ' + feature_dict1[feature1])
        else:
            with open(filename1) as f1:
                list1 = json.load(f1)


            # startdate_str1 = '04/14/2022 0:0:0'
            # startdate1 = int(datetime.strptime(startdate_str1, '%m/%d/%Y %H:%M:%S').timestamp())
            # enddate_str1 = '08/14/2022 0:0:0'
            # enddate1 = int(datetime.strptime(enddate_str1, '%m/%d/%Y %H:%M:%S').timestamp())
            # enddate_str2 = '08/13/2022 0:0:0'
            # list2 = [ t1 for t1 in list1 if t1[0] >= startdate1 and t1[0] < enddate1 ]
            list2 = list1

            if len(list2) == 0:
                print('No values for this feature ', feature_dict1[feature1], '. Please select another.')
                messagebox.showinfo('Solidworks license log', 'No data for this feature ' + feature_dict1[feature1])
            else:
                #NOTE !!!
                #print('xxx list2[0:10]', list2[0:10])
                #print(list2)

                #print("what !")

                x1, y1 = (zip(*list2))
                x1 = list(x1)
                y1 = list(y1)
                #x1 = mdates.epoch2num(x1)
                # epoch2num is not useful here. It just converts epoch time to no. of days since 1970.
                x1 = [ datetime.fromtimestamp(ts) for ts in x1 ]
                #print( 'x1,y1 = ', x1, y1)
                #plt.title(feature_dict1[feature1] + " Usage from " + startdate_str1[:startdate_str1.find('0:')-1] + " to " + enddate_str2[:enddate_str1.find('0:')-1])
                plt.title(feature_dict1[feature1] + " Usage ")
                
                plt.xlabel("Time")
                plt.ylabel("No. of licenses in use")
                plt.step(x1,y1,where='post')
                #plt.plot(x1,y1)
                #plt.bar(x1,y1,width=10)
                # https://itecnote.com/tecnote/python-plotting-unix-timestamps-in-matplotlib/
                plt.subplots_adjust(bottom=0.2)
                plt.xticks( rotation=25 )
                ax=plt.gca()
                #xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
                xfmt = mdates.DateFormatter('%m-%d')
                ax.xaxis.set_major_formatter(xfmt)
                plt.show()
    else:
        feature1 = features1[int(answer1)-7]
        filename1 = feature1 + '_denied.json'
        if not os.path.exists(filename1):
            print('No denial for this feature ' + feature_dict1[feature1] + '. Please select another.')
            messagebox.showinfo('Solidworks license log', 'No DENIED data for this feature ' + feature_dict1[feature1])
        else:
            with open(filename1) as f1:
                list1 = json.load(f1)

                # print("start1 list1 ", list1)
                # input("??")
                origin_tz = zoneinfo.ZoneInfo('US/Pacific')
                #dt_obj = datetime.strptime('01:01:1000' + ' 00:00:00', '%m:%d:%Y %H:%M:%S')
                


                # startdate_str1 = '04/14/2022 0:0:0'
                # startdate_obj1 =  datetime.strptime(startdate_str1, '%m/%d/%Y %H:%M:%S')
                # startdate_obj1 = datetime( startdate_obj1.year, startdate_obj1.month, startdate_obj1.day, tzinfo=origin_tz)
                # startdate1 = int(datetime.strptime(startdate_str1, '%m/%d/%Y %H:%M:%S').timestamp())
                # enddate_str1 = '08/14/2022 0:0:0'
                # enddate_obj1 =  datetime.strptime(enddate_str1, '%m/%d/%Y %H:%M:%S')
                # enddate_obj1 = datetime( enddate_obj1.year, enddate_obj1.month, enddate_obj1.day, tzinfo=origin_tz)
                # enddate1 = int(datetime.strptime(enddate_str1, '%m/%d/%Y %H:%M:%S').timestamp())
                # enddate_str2 = '08/13/2022 0:0:0'

                #list2 = [ t1 for t1 in list1 if int(t1[0]) >= startdate1 and int(t1[0]) < enddate1 ]
                #list2 = [ t1 for t1 in list1 if int(float(t1[0])) >= startdate1 and int(float(t1[0])) < enddate1 ]
                #list2 = [ t1 for t1 in list1 if t1[0].astype(float).astype(int)>= startdate1 and t1[0].astype(float).astype(int) < enddate1 ]
                #.astype(float).astype(int)
                #list2 = [ t1 for t1 in list1 if t1[0] >= startdate_obj1 and t1[0] < enddate_obj1 ]
                #print('xxx list2[0:10]', list2[0:10])
                #print(list2)
                list2 = list1
                if len(list2) == 0:
                    print('No values for this feature ', feature_dict1[feature1], '. Please select another.')
                    messagebox.showinfo('Solidworks license log', 'No DENIED data for this feature ' + feature_dict1[feature1])
                else:

                    x1, y1 = (zip(*list2))
                    x1 = list(x1)
                    y1 = list(y1)
                    #print( 'x1,y1 = ', x1, y1)
                    #plt.step(x1,y1)
                    #plt.plot(x1,y1)
                    #plt.bar(x1,y1,width=50)
                    #input("dfff")

                    x1 = [ datetime.fromtimestamp(ts) for ts in x1 ]
                    # print(x1)
                    # print(y1)
                    # input("nn")
                    # plt.stem(x1,y1)
                    #plt.title(feature_dict1[feature1] + " DENIED from " + startdate_str1[:startdate_str1.find('0:')-1] + " to " + enddate_str1[:enddate_str2.find('0:')-1])
                    plt.title(feature_dict1[feature1] + " DENIED ")
                    
                    plt.xlabel("Time")
                    plt.ylabel("No. of Denials")
                    #plt.step(x1,y1)
                    #plt.plot(x1,y1)
                    plt.stem(x1,y1)
                    #plt.bar(x1,y1)
                    # https://itecnote.com/tecnote/python-plotting-unix-timestamps-in-matplotlib/
                    plt.subplots_adjust(bottom=0.2)
                    plt.xticks( rotation=25 )
                    ax=plt.gca()
                    #xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
                    xfmt = mdates.DateFormatter('%m-%d')
                    ax.xaxis.set_major_formatter(xfmt)
                    plt.show()

               
