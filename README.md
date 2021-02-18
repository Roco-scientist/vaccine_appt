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
Fill in csv file.  It is case and word sensitive.  Some values have the choices listed in the choice column of the csv.  The priority group will need to be found in the dropdown menu and filled in exactly how it occurs on the website.  Also your exact insurance company will need to be put in here.  It may not matter as they may ask for your insurance ID later anyways.
<br><br>

## Variables to change
Within the main function<br>
`data = read_csv(<vaccine_info.csv location>)`<br>
`search_website` This is the website it is currently setup for.  Should work with all maimmunization
searchs.  Just replace your search website within this variable.<br>
`sec_pause_refresh` If there are no available slots, how many seconds to wait until checking again<br>
`schedule` Boolean for whether or not to finish the scheduling on the last page. Right now it selects the first available appointment but can be set to `False` in order to stop on this page and allow the use to select

## Run
`$ python vaccine_appt.py`
