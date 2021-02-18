# vaccine_appt
## Requirements

<ul>
<li>Selenium and geckdriver setup for firefox</li>
<li>Python 3.6 or greater</li>
<li>Pandas for python</li>
<li>BS4 for python</li>
<li>Selenium for python</li>
</ul>
<br><br>

## Setup
Fill in csv file.  It is case and word sensitive.  Some values have the choices listed in the choice column of the csv.  The priority group will need to be found in the dropdown menu and filled in exactly how it occurs on the website.  Also your exact insurance company will need to be put in here.  It may not matter, and you can try keeping what I already put in there, as they may ask for your insurance ID later anyways.  Otherwise, fill in this section exactly as you see it when you get to the insurance page.
<br><br>

## Variables to change
Within the main function<br>
`data = read_csv(<vaccine_info.csv location>)`<br>
`search_website` This is the website it is currently setup for.  Should work with all maimmunization
searchs.  Just replace your search website within this variable.<br>

## Run
To have it stop at the last page and have you manually selet the appointment<br>
`$ python vaccine_appt.py`<br>
To have the program select the earliest available appointment so that you don't miss your chance<br>
`$ python vaccine_appt.py --schedule`
