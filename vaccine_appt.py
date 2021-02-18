from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from pandas import read_csv
from bs4 import BeautifulSoup
from time import sleep
import re
import random
from datetime import datetime


def random_pause():
    """
    Function used to have a random pause to mimic human pauses
    """
    pause_time = random.uniform(0, 0.5)
    sleep(pause_time)


class vaccine_site:
    def __init__(self, driver, user_info):
        self.driver = driver
        self.user_info = user_info

    def page_start(self, sec_pause_refresh, search_website):
        # Get how many open appointments per day/site
        self.get_apt_num()
        # If there are none, refresh after ever sec_pause_refresh and check again
        while max(self.openings) == 0:
            now = datetime.now()
            next_page = ""
            while max(self.openings) == 0 and next_page is not None:
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                next_page = soup.find(attrs={"class": "page next"})
                breakpoint()
                if next_page is not None:
                    next_page_button = self.driver.find_element_by_class_name("next.page")
                    next_page_button.click()
                    random_pause()
                    self.get_apt_num()
            if max(self.openings) == 0:
                print(f"{now}: No openings found")
                sleep(sec_pause_refresh)
                self.driver.get(search_website)
                self.get_apt_num()
        # Find the continue buttons for the sites
        buttons = self.driver.find_elements_by_class_name("button-primary.px-4")
        # Find the button with the maximum appointments
        for opening, max_button in zip(self.openings, buttons):
            if opening == max(self.openings):
                break
        # Pause then continue
        max_button.click()
        random_pause()

    def get_apt_num(self):
        """
        Searches the webpage for appointments numbers.  Errors happen here usually.  The class for
        appointment days changes sometimes.  Inspect and change if needed
        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # apt_days = soup.findAll("div", attrs={"class": "field-fullwidth"})
        apt_days = soup.findAll("div", attrs={"class": "md:flex-shrink text-gray-800"})
        # Start a new list for appointments
        self.openings = []
        for apt in apt_days:
            apt_info = apt.findAll("p")
            for info in apt_info:
                # If the text available appointments is witihin then pull the number
                if "Available Appointments" in info.text:
                    apt_op_search = re.search("\d+", info.text)
                    apt_openings = int(apt_op_search.group())
                    self.openings.append(apt_openings)
                    break

    def page_one(self):
        # only continue if it does not put you on an already taken page
        self.continue_next = False
        if "Clinic+does+not+have+any+appointment+slots+available" not in self.driver.current_url:
            self.continue_next = True
            # Find the priority group select box
            select = Select(self.driver.find_element_by_class_name("form-select.w-full"))
            # Select the priority group
            select.select_by_index(int(self.user_info["Priority_Group"]))
            # Check the checkbox to continue
            checkbox = self.driver.find_element_by_class_name("form-checkbox.cursor-pointer")
            checkbox.click()
            # Find the save button
            save_and_continue =\
                self.driver.find_element_by_class_name(
                    "button-action.submit-patient.pre_consent_attestation")
            # Pause and click the button
            save_and_continue.click()
            random_pause()

    def page_two(self):
        # Fill in the following fields with the provided user info
        for fill_field in ("patient_first_name", "patient_middle_initial", "patient_last_name",
                           "patient_email", "patient_email_confirmation", "patient_phone_number",
                           "patient_address", "locality", "postal_code"):
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        # Select the folowing fields with the user info
        for select_field in ("patient_race", "patient_ethnicity", "patient_date_of_birth_1i",
                             "patient_date_of_birth_2i", "patient_date_of_birth_3i", "patient_sex",
                             "patient_phone_number_type", "administrative_area_level_1"):
            select_value = self.user_info[select_field]
            select_web_loc = Select(self.driver.find_element_by_id(select_field))
            select_web_loc.select_by_visible_text(select_value)
        # Puase and continue
        save_and_continue =\
            self.driver.find_element_by_id("submitButton")
        save_and_continue.click()
        random_pause()

    def page_three(self):
        # Fill in the user fields
        for fill_field in ("patient_member_id_for_insurance",
                           "patient_insured_first_name", "patient_insured_last_name"):
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        # Select the user fields
        for select_field in ("patient_insurance_type", "patient_insured_date_of_birth_1i",
                             "patient_insured_date_of_birth_2i",  "patient_insured_date_of_birth_3i",
                             "patient_relation_to_patient_for_consent"):
            select_value = self.user_info[select_field]
            select_web_loc = Select(self.driver.find_element_by_id(select_field))
            select_web_loc.select_by_visible_text(select_value)
        insurance_select =\
            self.driver.find_element_by_id("select2-patient_insurance_company_name-container")
        insurance_select.click()
        other_select =\
            self.driver.find_element_by_id(
                "select2-patient_insurance_company_name-container-result-6sc3-OTHER.(PLEASE.SPECIFY):")
        other_select.click()
        fill_value = self.user_info["patient_insurance_company_name"]
        insurance_field = driver.find_element_by_id("patient_other_insurance")
        insurance_field.send_keys(fill_value)
        # Pause and continue
        save_and_continue = self.driver.find_element_by_id("submitButton")
        save_and_continue.click()
        random_pause()

    def additional_first_vax_info(self):
        """
        If this is the second vaccine, fill in the first vaccine fields
        """
        for click_field in ("first_vaccine_brand"):
            click_value = self.user_info[click_field]
            click_field_final = f"{click_field}_{click_value}"
            checkbox = self.driver.find_element_by_id(click_field_final)
            checkbox.click()
        for fill_field in ("patient_patient_question_answers_attributes_1_additional_info"):
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)

    def page_four(self):
        """
        Answer the questions
        """
        # Click yes or no on all of the questions
        for click_field in ("7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
                            "17", "covid_vaccine_number"):
            click_value = self.user_info[click_field]
            click_field_final = f"{click_field}_{click_value}"
            if click_field == "covid_vaccine_number":
                click_field_start = f"{click_field_final}_time"
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                inputs = soup.findAll("input")
                for input_field in inputs:
                    try:
                        input_field["id"]
                        if click_field_start in input_field["id"]:
                            click_field_final = input_field["id"]
                    except KeyError:
                        pass
                checkbox = self.driver.find_element_by_id(click_field_final)
                checkbox.click()
                if click_value == "second":
                    additional_first_vax_info(self.driver, self.user_info)
            else:
                checkbox = self.driver.find_element_by_id(click_field_final)
                checkbox.click()
        # Fill in field if 9 is a yes
        if self.user_info["9"] == "yes":
            fill_field = "patient_patient_question_answers_attributes_2_additional_info"
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        # Pause and continue
        save_and_continue = self.driver.find_element_by_id("skip_add_family")
        save_and_continue.click()
        random_pause()

    def page_six(self):
        """
        Select the vaccine
        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        vaccines = soup.findAll("label", {"class": "text-lg"})
        vaccine_button_connect = [(vaccine["for"], vaccine.text.lower()) for vaccine in vaccines]
        if str(self.user_info["first_vaccine_brand"]) != "nan":
            first_vaccine = self.user_info["first_vaccine_brand"]
            button_ids = [but_id for but_id, vaccine in vaccine_button_connect
                          if first_vaccine in vaccine]
            if len(button_ids) == 1:
                button_id = button_ids[0]
            else:
                raise SystemExit(
                    f"Site did not have needed vaccine\nVaccines: {vaccine_button_connect}")
        else:
            button_id = vaccines[0]["for"]
        vaccine_button = self.driver.find_element_by_id(button_id)
        vaccine_button.click()
        # Go to type in name field so that a signature is not needed
        name_button = self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Type My Full Name')]")
        name_button.click()
        # Fill in the name
        first_name_fill = self.driver.find_element_by_id("patient_signatory_first_name")
        last_name_fill = self.driver.find_element_by_id("patient_signatory_last_name")
        first_name_fill.send_keys(self.user_info["patient_first_name"])
        last_name_fill.send_keys(self.user_info["patient_last_name"])
        relationship_select = Select(self.driver.find_element_by_id(
            "patient_relation_to_patient_for_insurance"))
        # Fill in as self
        relationship_select.select_by_visible_text("Self")
        # Continue
        save_and_continue = self.driver.find_element_by_id("submitButton")
        save_and_continue.click()
        random_pause()
        # Continue on the next page
        save_and_continue = self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Save And Continue')]")
        save_and_continue.click()
        random_pause()

    def page_seven(self):
        openings_buttons = self.driver.find_elements_by_class_name(
            "form-radio.appointment-radio-btn")
        # Finds the first opening and clicks on it
        openings_buttons[0].click()
        save_and_continue = self.driver.find_element_by_id("submitButton")
        save_and_continue.click()


def main():
    # user data input
    data = read_csv("./vaccine_info.csv")
    # website for the search.  This is replaceable with any search from maimmunizations, just do
    # your search and put the site here
    search_website = "https://www.maimmunizations.org/clinic/search?commit=Search&location=&q%5Bclinic_date_eq%5D=&q%5Bvaccinations_name_i_cont%5D=&q%5Bvenue_search_name_or_venue_name_i_cont%5D=fenway&search_radius=All#search_results#search_results"
    # How many seconds to wait if there are no appointments available until checking again
    sec_pause_refresh = 300
    # Whether or not to proceed on the last page.  False if you want to pick your own time,
    # otherwise it picks the first
    schedule = True

    # Creating a dictionary of user variables to put into the website
    user_info = {field: value for field, value in zip(data.Field, data.Value)}
    # Email is needed twice on one page.  Setting that here
    user_info["patient_email_confirmation"] = user_info["patient_email"]
    # Sometimes the initial 0 is left off of the zip code.  Fix
    if len(user_info["postal_code"]) == 4:
        user_info["postal_code"] = f"0{user_info['postal_code']}"
    # Open a web browser
    driver = webdriver.Firefox()
    # Open the webpage
    driver.get(search_website)
    # Setup the class
    vaccine_page = vaccine_site(driver, user_info)
    # Navigate page one and find all open appointments and select the day with the most
    vaccine_page.page_start(sec_pause_refresh, search_website)
    # Navigate the next page which has priority list
    vaccine_page.page_one()
    # If the appt was taken before continuing to next page, go back to the start page
    while not vaccine_page.continue_next:
        vaccine_page.driver.get(search_website)
        vaccine_page.page_start(sec_pause_refresh)
        vaccine_page.page_one()
    # Fill in page 2
    vaccine_page.page_two()
    # Fill in page 3
    vaccine_page.page_three()
    # Fill in page 4 and 5
    vaccine_page.page_four()
    # Fill in page 6
    vaccine_page.page_six()
    if schedule:
        # Schedule appointment
        vaccine_page.page_seven()


if __name__ == "__main__":
    main()
