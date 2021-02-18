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
    pause_time = random.uniform(0, 0.5)
    sleep(pause_time)


class vaccine_site:
    def __init__(self, driver, user_info):
        self.driver = driver
        self.user_info = user_info

    def page_start(self):
        self.get_apt_num()
        buttons = self.driver.find_elements_by_class_name("button-primary.px-4")
        for opening, max_button in zip(self.openings, buttons):
            if opening == max(self.openings):
                break
        random_pause()
        max_button.click()

    def get_apt_num(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # apt_days = soup.findAll("div", attrs={"class": "field-fullwidth"})
        apt_days = soup.findAll("div", attrs={"class": "md:flex-shrink.text-gray-800"})
        self.openings = []
        for apt in apt_days:
            apt_info = apt.findAll("p")
            for info in apt_info:
                if "Available Appointments" in info.text:
                    apt_op_search = re.search("\d+", info.text)
                    apt_openings = int(apt_op_search.group())
                    self.openings.append(apt_openings)
                    break

    def page_one(self):
        select = Select(self.driver.find_element_by_class_name("form-select.w-full"))
        select.select_by_visible_text(self.user_info["Priority_Group"])
        checkbox = self.driver.find_element_by_class_name("form-checkbox.cursor-pointer")
        checkbox.click()
        save_and_continue =\
            self.driver.find_element_by_class_name(
                "button-action.submit-patient.pre_consent_attestation")
        random_pause()
        save_and_continue.click()

    def page_two(self):
        for fill_field in ("patient_first_name", "patient_middle_initial", "patient_last_name",
                           "patient_email", "patient_email_confirmation", "patient_phone_number",
                           "patient_address", "locality", "postal_code"):
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        for select_field in ("patient_race", "patient_ethnicity", "patient_date_of_birth_1i",
                             "patient_date_of_birth_2i", "patient_date_of_birth_3i", "patient_sex",
                             "patient_phone_number_type", "administrative_area_level_1"):
            select_value = self.user_info[select_field]
            select_web_loc = Select(self.driver.find_element_by_id(select_field))
            select_web_loc.select_by_visible_text(select_value)
        save_and_continue =\
            self.driver.find_element_by_id("submitButton")
        random_pause()
        save_and_continue.click()

    def page_three(self):
        for fill_field in ("patient_insurance_company_name", "patient_member_id_for_insurance",
                           "patient_insured_first_name", "patient_insured_last_name"):
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        for select_field in ("patient_insurance_type", "patient_insured_date_of_birth_1i",
                             "patient_insured_date_of_birth_2i",  "patient_insured_date_of_birth_3i",
                             "patient_relation_to_patient_for_consent"):
            select_value = self.user_info[select_field]
            select_web_loc = Select(self.driver.find_element_by_id(select_field))
            select_web_loc.select_by_visible_text(select_value)
        save_and_continue = self.driver.find_element_by_id("submitButton")
        random_pause()
        save_and_continue.click()

    def additional_first_vax_info(self):
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
        if self.user_info["9"] == "yes":
            fill_field = "patient_patient_question_answers_attributes_2_additional_info"
            fill_value = self.user_info[fill_field]
            fill_web_loc = self.driver.find_element_by_id(fill_field)
            fill_web_loc.send_keys(fill_value)
        random_pause()
        save_and_continue = self.driver.find_element_by_id("skip_add_family")
        save_and_continue.click()

    def page_six(self):
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
        name_button = self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Type My Full Name')]")
        name_button.click()
        first_name_fill = self.driver.find_element_by_id("patient_signatory_first_name")
        last_name_fill = self.driver.find_element_by_id("patient_signatory_last_name")
        first_name_fill.send_keys(self.user_info["patient_first_name"])
        last_name_fill.send_keys(self.user_info["patient_last_name"])
        relationship_select = Select(self.driver.find_element_by_id(
            "patient_relation_to_patient_for_insurance"))
        relationship_select.select_by_visible_text("Self")
        save_and_continue = self.driver.find_element_by_id("submitButton")
        random_pause()
        save_and_continue.click()
        random_pause()
        save_and_continue = self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Save And Continue')]")
        save_and_continue.click()

    def page_seven(self):
        openings_buttons = self.driver.find_elements_by_class_name(
            "form-radio.appointment-radio-btn")
        # Finds the first opening and clicks on it
        openings_buttons[0].click()
        save_and_continue = self.driver.find_element_by_id("submitButton")
        save_and_continue.click()


def main():
    data = read_csv("./vaccine_info.csv")
    search_website = "https://www.maimmunizations.org/clinic/search?commit=Search&location=&q%5Bclinic_date_eq%5D=&q%5Bvaccinations_name_i_cont%5D=&q%5Bvenue_search_name_or_venue_name_i_cont%5D=fenway&search_radius=All#search_results#search_results"
    sec_pause_refresh = 300
    schedule = True
    user_info = {field: value for field, value in zip(data.Field, data.Value)}
    user_info["patient_email_confirmation"] = user_info["patient_email"]
    if len(user_info["postal_code"]) == 4:
        user_info["postal_code"] = f"0{user_info['postal_code']}"
    driver = webdriver.Firefox()
    driver.get(search_website)
    vaccine_page = vaccine_site(driver, user_info)
    vaccine_page.page_start()
    while max(vaccine_page.openings) == 0:
        now = datetime.now()
        print(f"{now}: No openings found")
        sleep(sec_pause_refresh)
        vaccine_page.driver.navigate().refresh()
        vaccine_page.page_start()
    vaccine_page.page_one()
    vaccine_page.page_two()
    vaccine_page.page_three()
    vaccine_page.page_four()
    vaccine_page.page_six()
    if schedule:
        vaccine_page.page_seven()


if __name__ == "__main__":
    main()
