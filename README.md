# vaccine_appt
## Requirements

<ul>
<li>Selenium and geckodriver setup for firefox</li>
<li>Python 3.6 or greater</li>
<li>Pandas for python</li>
<li>BS4 for python</li>
<li>Selenium for python</li>
</ul>
<br><br>

## Setup
Fill in csv file.  It is case and word sensitive.  Some values have the choices listed in the choice column of the csv.
<br><br>

## Variables that are possible to change
Within the main function<br>
`data = read_csv(<vaccine_info.csv location>)`<br>
`search_website` This is the website it is currently setup for.  Should work with all maimmunization
searchs.  Just replace your search website within this variable.<br>

## Run
To have it stop at the last page and have you manually select the appointment<br>
`$ python vaccine_appt.py`<br>
To have the program select the earliest available appointment so that you don't miss your chance<br>
`$ python vaccine_appt.py --schedule`
