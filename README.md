# vaccine_appt
Last tested on 2021-02-21<br>
Script that pings maimmunizations every 30 seconds to check for a vaccine opening.  It then fills in all of your info on the next 7 pages.  This script takes a few seconds to find an opening, fill in your information, and schedule your appointment

## Requirements

<ul>
<li>Firefox</li>
<li>Download Geckodriver and move to a path directory <a href="https://github.com/mozilla/geckodriver/releases/tag/v0.29.0">Download Here</a></li>
<li>Python 3.6 or greater</li>
<li>virtualenv installed for regular python if not using Anaconda</li>
</ul>
<br><br>

## Setup
<li>Create a virtualenvironment and install dependencies
<li>for regular python<br>
```
$ python3 -m venv vaccine
$ source vaccine/bin/acivate
$ pip install -r requirements.txt --user
```
</li>
<li>
for anaconda<br>

```
$ conda create --name vaccine python=3.6
$ conda activate vaccine
$ conda install --file requirements.txt
```
</li></li>
<li>Fill in the csv file
<li>
It is case and word sensitive.  Some values have the choices listed in the choice column of the csv.
</li></li>

## Variables that are possible to change
Within the main function<br>
`data = read_csv(<vaccine_info.csv location>)`<br>
`search_website` This is the website it is currently setup for.  Should work with all maimmunization
searches.  Just replace your search website within this variable.<br>

## Run
To have it stop at the last page and have you manually select the appointment<br>
`$ python vaccine_appt.py`<br><br>
To have the program select the earliest available appointment so that you don't miss your chance.  Otherwise it stops on the last page so you can selecct the appointment time<br>
`$ python vaccine_appt.py --schedule`<br><br>
To search gillette instead of fenway.  The default is fenway.  `search_website` within main can also be changed to any maimmunizations search needed<br>
`$ python vaccine_appt.py --gillette`<br><br>
To check the website every 10 seconds instead of 30.  The default is 30<br>
`$ python vaccine_appt.py --refresh_secs 10`<br><br>
