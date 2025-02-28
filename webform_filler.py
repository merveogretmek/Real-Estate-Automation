# Real Estate Web Form Automated Filling

## Libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

import time
import numpy as np
import pandas as pd

## Driver and Wait Time

chrome_options = Options()

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

wait_time = 10

wait = WebDriverWait(driver, wait_time)

## Functions

def wait_for_section_title(title):
    title_locator = (By.XPATH, '//*[@id="container"]/div[2]/div[1]/div/div/h1')
    WebDriverWait(driver, wait_time).until(
        EC.text_to_be_present_in_element(title_locator, title)
    )

def navigate_to_section(xpath):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def select_dropdown_text(xpath, text):
    select = Select(driver.find_element(By.XPATH, xpath))
    select.select_by_visible_text(text)

def select_dropdown_value(xpath, value):
    select = Select(driver.find_element(By.XPATH, xpath))
    select.select_by_value(value)

def enter_text(xpath, text):
    field = driver.find_element(By.XPATH, xpath)
    field.clear()
    field.send_keys(text)

def click_button(xpath):
    WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()

def click_checkbox(xpath, condition):
    checkbox = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    if condition == 'Yes':
        checkbox.click()
    
def handle_exceptions(func, *args):
    try:
        func(*args)
    except ElementClickInterceptedException:
        click_button('/html/body/div[7]/div[1]/div/div[2]/ul/li/a')
        func(*args)
    except NoSuchElementException:
        time.sleep(5)
        func(*args)
    except StaleElementReferenceException:
        time.sleep(5)
        func(*args)

## Login

def login():
    # Credentials for login
    username = 'username_here'
    password = 'password_here'

    # Navigate to the URL
    
    url = "https://iqenergy-live.quidossoftware.co.uk/passport/login"
    driver.get(url)
    
    # Login process
    
    # username
    username_locator = '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/fieldset/p[1]/input'
    navigate_to_section(username_locator)
    enter_text(username_locator, username)
    
    # password
    password_locator = '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/form/fieldset/p[2]/input'
    navigate_to_section(password_locator)
    enter_text(password_locator, password)
    
    # login
    login_button_locator = '//*[@id="container"]/div[1]/div[2]/div[1]/form/fieldset/div/div/div/button'
    click_button(login_button_locator)

    # Navigate to the relevant part of the website

    # rdsap sidepanel
    rdsap_sidepanel_button_locator = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[2]/div'
    click_button(rdsap_sidepanel_button_locator)
    
    # rdsap
    rdsap_button_locator = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/ul/li[2]/ul/li[1]/a' 
    click_button(rdsap_button_locator)

### New Entry

def add_new_entry(i):
    entry_button_locator = '//*[@id="container"]/div/div[1]/div/button'
    navigate_to_section(entry_button_locator)
    click_button(entry_button_locator) 

### Building Details

def enter_building_details(i):
    
    # Data-----------------
    country = data['All Countries'].iloc[i]
    postcode = data['Postcode'].iloc[i]
    assess_date = data['Assessment Date'].iloc[i]
    rpd = data['Related Party Disclosure'].iloc[i]
    ex_epc = data['Property has existing EPC?'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Building Details")
    
    # Entry-----------------
    
    # all_countries
    all_countries_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="countryId"]')))
    Select(all_countries_field).select_by_visible_text(country)

    # postcode - the entry field changes depending on the country
    if country == 'Scotland':
        postcode_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="findPostcodeSCT"]')))
        postcode_field.clear()
        postcode_field.send_keys(postcode)

    # Click on find address
    find_address_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="SCT"]/p/button[1]')))
    find_address_button.click()

    # Choose first address
    address = wait.until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="addressSeleter"]/option[{i+1}]')))
    address.click()

    # assess_date
    assess_date_field = wait.until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[1]/div/p[6]/input')))
    assess_date_field.clear()
    assess_date_field.send_keys('03/11/2023')  # Example date

    # rpd
    rpd_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="reportForm"]/div[1]/div/p[8]/select')))
    Select(rpd_field).select_by_visible_text(rpd)

    # ex_epc
    ex_epc_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="existingEpc"]')))
    Select(ex_epc_field).select_by_visible_text(ex_epc)

    # Move to next section
    
    next_button_locator = '//*[@id="reportForm"]/div[2]/div/div[1]/div/button'
    click_button(next_button_locator)

### Classification

def enter_classification(i):
    # Data-----------------
    tenure = data['Tenure'].iloc[i]
    trans_type = data['Transaction Type'].iloc[i]
    built_form = data['Built Form'].iloc[i]
    detach_pos = data['Detatchment/Position'].iloc[i]
    main_prop1 = data['Main Property'].iloc[i]
    ext1 = data['Extension 1'].iloc[i]
    main_prop_ab = data['Main Property (Age Band)'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Classification")

    # Entry----------------- 
    
    # tenure
    if pd.notna(tenure):
        tenure_locator = '//*[@id="reportForm"]/div[2]/div/p[1]/select'
        navigate_to_section(tenure_locator)
        select_dropdown_text(tenure_locator, tenure)
        
    time.sleep(1) # page loading
    
    # trans_type
    if pd.notna(trans_type):
        trans_type_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(trans_type_locator)
        select_dropdown_text(trans_type_locator, trans_type)
    
    time.sleep(1) # page loading
    
    # built_form
    if pd.notna(built_form):
        built_form_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(built_form_locator)
        select_dropdown_text(built_form_locator, built_form)
    
    time.sleep(1) # page loading
    
    # detach_pos
    if pd.notna(detach_pos):
        detach_pos_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/select'
        navigate_to_section(detach_pos_locator)
        select_dropdown_text(detach_pos_locator, detach_pos)
    
    time.sleep(1) # page loading
    
    # main_prop1
    if pd.notna(main_prop1):
        main_prop1_locator = '//*[@id="reportForm"]/div[2]/div/p[8]/select'
        navigate_to_section(main_prop1_locator)
        select_dropdown_text(main_prop1_locator, main_prop1)
    
    time.sleep(1) # page loading
    
    # ext1
    if pd.notna(ext1):
        ext1_locator = '//*[@id="reportForm"]/div[2]/div/p[9]/select'
        navigate_to_section(ext1_locator)
        select_dropdown_text(ext1_locator, ext1)
    
    time.sleep(1) # page loading
    
    # main_prop_ab
    if pd.notna(main_prop_ab):
        main_prop_ab_locator = '//*[@id="reportForm"]/div[2]/div/p[15]/select'
        navigate_to_section(main_prop_ab_locator)
        select_dropdown_text(main_prop_ab_locator, main_prop_ab)

    # Move to next section
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### General

def enter_general(i):
    # Data-----------------
    num_of = data['Number of Open Fireplaces'].iloc[i]
    num_hr = data['Number of Habitable Rooms'].iloc[i]
    num_hhr = data['Number of Heated Habitable Rooms'].iloc[i]
    heat_base = data['Heated Basement'].iloc[i]
    cons_type = data['Conservatory Type'].iloc[i]
    wh_vent_type = data['Whole-house Ventiliation Type'].iloc[i]
    ter_type = data['Terrain Type'].iloc[i]
    scs_pres = data['Space Cooling System Present'].iloc[i]
    perc_dp = data['Percentage of Draught Proofed(%)'].iloc[i]
    main_prop2 = data['Main Property.1'].iloc[i]
    num_flo = data['Total Number of Fixed Lighting Outlets'].iloc[i]
    num_le_flo = data['Total Number of Low-EnergyFixed Lighting Outlets'].iloc[i]
    ph_known = data['Photovoltaic Unit details known'].iloc[i]
    wind_turb = data['Wind Turbine'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("General")
    
    # Entry-----------------
    
    # num_of
    if pd.notna(num_of):
        num_of_locator = '//*[@id="reportForm"]/div[2]/div/p[1]/select'
        navigate_to_section(num_of_locator)
        select_dropdown_text(num_of_locator, str(num_of))
        
    time.sleep(1) # page loading
    
    # num_hr
    if pd.notna(num_hr):
        num_hr_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(num_hr_locator)
        select_dropdown_text(num_hr_locator, str(num_hr))
        
    time.sleep(1) # page loading
    
    # num_hhr
    if pd.notna(num_hhr):
        num_hhr_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(num_hhr_locator)
        select_dropdown_text(num_hhr_locator, str(num_hhr))
    
    time.sleep(1) # page loading
    
    # heat_base 
    heat_base_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/input[2]'
    click_checkbox(heat_base_locator, heat_base)
    
    time.sleep(1) # page loading
    
    # cons_type
    if pd.notna(cons_type):
        cons_type_locator = '//*[@id="reportForm"]/div[2]/div/p[5]/select'
        navigate_to_section(cons_type_locator)
        select_dropdown_text(cons_type_locator, cons_type)
    
    time.sleep(1) # page loading
    
    # wh_vent_type
    if pd.notna(wh_vent_type):
        wh_vent_type_locator = '//*[@id="reportForm"]/div[2]/div/p[6]/select'
        navigate_to_section(wh_vent_type_locator)
        select_dropdown_text(wh_vent_type_locator, wh_vent_type)
    
    time.sleep(1) # page loading
    
    # ter_type
    if pd.notna(ter_type):
        ter_type_locator = '//*[@id="reportForm"]/div[2]/div/p[7]/select'
        navigate_to_section(ter_type_locator)
        select_dropdown_text(ter_type_locator, ter_type)
    
    time.sleep(1) # page loading
    
    # scs_pres
    scs_pres_locator = '//*[@id="reportForm"]/div[2]/div/p[8]/input[2]'
    click_checkbox(scs_pres_locator, scs_pres)
    
    time.sleep(1) # page loading
    
    # perc_dp
    perc_dp_locator = '//*[@id="reportForm"]/div[2]/div/p[9]/input'
    navigate_to_section(perc_dp_locator)
    enter_text(perc_dp_locator, str(int(perc_dp)))
    
    time.sleep(1) # page loading
    
    # main_prop2
    if pd.notna(main_prop2):
        main_prop2_locator = '//*[@id="reportForm"]/div[2]/div/p[12]/select'
        navigate_to_section(main_prop2_locator)
        select_dropdown_text(main_prop2_locator, str(int(main_prop2)))
    
    time.sleep(1) # page loading
    
    # num_flo
    if pd.notna(num_flo):
        num_flo_locator = '//*[@id="reportForm"]/div[2]/div/p[19]/select'
        navigate_to_section(num_flo_locator)
        select_dropdown_text(num_flo_locator, str(int(num_flo)))
        
    time.sleep(5) # page loading
    
    # num_le_flo
    if pd.notna(num_le_flo):
        num_le_flo_locator = '//*[@id="reportForm"]/div[2]/div/p[20]/select'
        navigate_to_section(num_le_flo_locator)
        select_dropdown_text(num_le_flo_locator, str(int(num_le_flo)))
    
    time.sleep(1) # page loading
    
    # ph_known
    ph_known_locator = '//*[@id="reportForm"]/div[2]/div/p[23]/input[2]'
    click_checkbox(ph_known_locator, ph_known)
    
    time.sleep(1) # page loading
    
    # wind_turb
    wind_turb_locator = '//*[@id="reportForm"]/div[2]/div/p[28]/input[2]'
    click_checkbox(wind_turb_locator, wind_turb)
    
    # Move to the next section
    
    time.sleep(5) # wait for page to load
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Dimension

def enter_dimension(i):
    # Data-----------------
    dim_type = data['Dimension Type'].iloc[i]
    fl_area_gr = data['Floor Area (m2) Ground'].iloc[i]
    ro_height_gr = data['Room Height (m) Ground'].iloc[i]
    lo_perim_gr = data['Loss Perimiter (m) Ground'].iloc[i]
    pa_wa_length_gr = data['Party Wall Length (m) Ground'].iloc[i]
    fl_area_1st = data['Floor Area (m2) 1st'].iloc[i]
    ro_height_1st = data['Room Height (m) 1st'].iloc[i]
    lo_perim_1st = data['Loss Perimiter (m) 1st'].iloc[i]
    pa_wa_length_1st = data['Party Wall Length (m) 1st'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Dimension")

    # dim_type
    if pd.notna(dim_type):
        dim_type_locator = '//*[@id="reportForm"]/div[2]/div/p[1]/select'
        navigate_to_section(dim_type_locator)
        select_dropdown_text(dim_type_locator, dim_type)

    # fl_area_gr
    if pd.notna(fl_area_gr):
        fl_area_gr_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[2]/input'
        navigate_to_section(fl_area_gr_locator)
        enter_text(fl_area_gr_locator, str(fl_area_gr))

    # ro_height_gr
    if pd.notna(ro_height_gr):
        ro_height_gr_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[3]/input'
        navigate_to_section(ro_height_gr_locator)
        enter_text(ro_height_gr_locator, str(ro_height_gr))

    # lo_perim_gr
    if pd.notna(lo_perim_gr):
        lo_perim_gr_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[4]/input'
        navigate_to_section(lo_perim_gr_locator)
        enter_text(lo_perim_gr_locator, str(lo_perim_gr))

    # pa_wa_length_gr
    if pd.notna(pa_wa_length_gr):
        pa_wa_length_gr_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[2]/td[5]/input'
        navigate_to_section(pa_wa_length_gr_locator)
        enter_text(pa_wa_length_gr_locator, str(pa_wa_length_gr))

    # fl_area_1st
    if pd.notna(fl_area_1st):
        fl_area_1st_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[2]/input'
        navigate_to_section(fl_area_1st_locator)
        enter_text(fl_area_1st_locator, str(fl_area_1st))

    # ro_height_1st
    if pd.notna(ro_height_1st):
        ro_height_1st_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[3]/input'
        navigate_to_section(ro_height_1st_locator)
        enter_text(ro_height_1st_locator, str(ro_height_1st))

    # lo_perim_1st
    if pd.notna(lo_perim_1st):
        lo_perim_1st_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[4]/input'
        navigate_to_section(lo_perim_1st_locator)
        enter_text(lo_perim_1st_locator, str(lo_perim_1st))

    # pa_wa_length_1st 
    if pd.notna(pa_wa_length_1st):
        pa_wa_length_1st_locator = '//*[@id="reportForm"]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[5]/input'
        navigate_to_section(pa_wa_length_1st_locator)
        enter_text(pa_wa_length_1st_locator, str(pa_wa_length_1st))
        
    # Move to the next section
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Flats and Maisonettes

def enter_flats_maisonettes(i):
    # Data-----------------
    heat_lo_ct = data['Heat Loss Corridor Type'].iloc[i]
    build_part = data['Which building part does this apply to?'].iloc[i]
    le_bt_fc = data['Length of Wall Between Flat and Corridor (m)'].iloc[i]
    flo_level = data['Floor Level'].iloc[i]
    pos = data['Position'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Flats and Maisonettes")
    
    # Initialize a default value
    flo_level_adj = np.nan
    pos_adj = np.nan
    
    # Adjustment for the inconsistency in flo_level
    if flo_level == 0:
        flo_level_adj = "376"
    if flo_level == 1:
        flo_level_adj = "377"
    if flo_level == 2:
        flo_level_adj = "378"
    if flo_level == 3:
        flo_level_adj = "379"
    if flo_level == 4:
        flo_level_adj = "380"
    if flo_level == 5:
        flo_level_adj = "381"
    if flo_level == 6:
        flo_level_adj = "382"
    if flo_level == 7:
        flo_level_adj = "383"
    if flo_level == 8:
        flo_level_adj = "384"
    if flo_level == 9:
        flo_level_adj = "385"
    if flo_level == 10:
        flo_level_adj = "386"
        
    # Adjustment for the inconsistency in pos
    if pos == "Basement":
        pos_adj = "404"
    if pos == "Top-floor":
        pos_adj = "244"
    if pos == "Mid-floor":
        pos_adj = "243"
    if pos == "Ground-floor":
        pos_adj = "242"
    
    # Entry-----------------
    
    # heat_lo_ct
    if pd.notna(heat_lo_ct):
        heat_lo_ct_locator = '//*[@id="reportForm"]/div[2]/div/p[1]/select'
        navigate_to_section(heat_lo_ct_locator)
        select_dropdown_text(heat_lo_ct_locator, heat_lo_ct)
        
    time.sleep(1) # page loading
    
    # build_part
    if pd.notna(build_part):
        build_part_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(build_part_locator)
        select_dropdown_text(build_part_locator, build_part)
        
    time.sleep(1)

    # le_bt_fc
    if pd.notna(le_bt_fc):
        le_bt_fc_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/input'
        navigate_to_section(le_bt_fc_locator)
        enter_text(le_bt_fc_locator, str(le_bt_fc))
        
    time.sleep(1) # page loading

    # flo_level
    if pd.notna(flo_level):
        flo_level_locator = '//*[@id="reportForm"]/div[2]/div/p[5]/select'
        navigate_to_section(flo_level_locator)
        select_dropdown_value(flo_level_locator, flo_level_adj)
        
    time.sleep(1) # page loading

    # pos
    if pd.notna(pos):
        pos_locator = '//*[@id="reportForm"]/div[2]/div/p[6]/select'
        navigate_to_section(pos_locator)
        select_dropdown_value(pos_locator, pos_adj)

    # Move to the next section
    
    time.sleep(5) # page loading
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Walls

def enter_walls(i):
    # Data-----------------
    construction = data['Construction'].iloc[i]
    insulation = data['Insulation'].iloc[i]
    ins_th = data['Insulation Thickness (mm)'].iloc[i]
    wt_me = data['Wall Thickness Measured'].iloc[i]
    uv_known = data['U-value known?'].iloc[i]
    dry_lin = data['Dry-lining?'].iloc[i]
    pa_wa_cons = data['Party Wall Consutrction'].iloc[i]
    construction2 = data['Construction.1'].iloc[i]
    insulation2 = data['Insulation.1'].iloc[i]
    ins_th2 = data['Insulation Thickness (mm).1'].iloc[i]
    wt_me2 = data['Wall Thickness Measured.1'].iloc[i]
    uv_known2 = data['U-value known?.1'].iloc[i]
    dry_lin2 = data['Dry-lining?.1'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Walls")
    
    # Entry-----------------
    
    # construction
    if pd.notna(construction):
        construction_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(construction_locator)
        select_dropdown_text(construction_locator, construction)
        
    time.sleep(1) # page loading

    # insulation
    if pd.notna(insulation):
        insulation_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(insulation_locator)
        select_dropdown_text(insulation_locator, insulation)
    
    time.sleep(1) # page loading
    
    # ins_th 
    if pd.notna(ins_th):
        ins_th_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/select'
        navigate_to_section(ins_th_locator)
        select_dropdown_text(ins_th_locator, ins_th)
    
    time.sleep(1) # page loading
    
    # wt_me
    if pd.notna(wt_me):
        wt_me_locator = '//*[@id="thickness_measured_checkbox"]'
        click_checkbox(wt_me_locator, wt_me)
    
    time.sleep(1) # page loading
    
    # uv_known
    if pd.notna(uv_known):
        uv_known_locator = '//*[@id="reportForm"]/div[2]/div/p[7]/input[2]'
        click_checkbox(uv_known_locator, uv_known)
    
    time.sleep(1) # page loading
    
    # dry_lin
    if pd.notna(dry_lin):
        dry_lin_locator = '//*[@id="reportForm"]/div[2]/div/p[9]/input[2]'
        click_checkbox(dry_lin_locator, dry_lin)
    
    time.sleep(1) # page loading
    
    # pa_wa_cons
    if pd.notna(pa_wa_cons):
        pa_wa_cons_locator = '//*[@id="reportForm"]/div[2]/div/p[10]/select'
        navigate_to_section(pa_wa_cons_locator)
        select_dropdown_text(pa_wa_cons_locator, pa_wa_cons)
        
    time.sleep(1) # page loading

    # construction2
    if pd.notna(construction2):
        construction2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[3]/select'
        navigate_to_section(construction2_locator)
        select_dropdown_text(construction2_locator, construction2)
    
    time.sleep(1) # page loading
    
    # insulation2
    if pd.notna(insulation2):
        insulation2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[4]/select'
        navigate_to_section(insulation2_locator)
        select_dropdown_text(insulation2_locator, insulation2)
    
    time.sleep(1) # page loading
    
    # ins_th2
    if pd.notna(ins_th2):
        ins_th2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[5]/select'
        navigate_to_section(ins_th2_locator)
        select_dropdown_text(ins_th2_locator, ins_th2)
    
    time.sleep(1) # page loading
    
    # wt_me2
    if pd.notna(wt_me2):
        wt_me2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[6]/input[2]'
        click_checkbox(wt_me2_locator, wt_me2)
    
    time.sleep(1) # page loading
    
    # uv_known2
    if pd.notna(uv_known2):
        uv_known2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[8]/input[2]'
        click_checkbox(uv_known2_locator, uv_known2)
            
    time.sleep(1) # page loading
    
    # dry_lin2
    if pd.notna(dry_lin2):
        dry_lin2_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/fieldset/p[10]/input[2]'
        click_checkbox(dry_lin2_locator, dry_lin2)

    # Move to the next section
    
    time.sleep(5) # wait for the page to load
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Windows

def enter_windows(i):
    # Data-----------------
    area_type = data['Area Type'].iloc[i]
    perc_mg = data['Percent Multiple Glazed'].iloc[i]
    mg_type = data['Multiple Glazing Type'].iloc[i]
    pvc_wf = data['PVC Window Frames'].iloc[i]
    gla_gap = data['Glazing Gap'].iloc[i]
    
    time.sleep(15) # this page takes long
    
    # Page Loading----------
    
    wait_for_section_title("Windows")
    
    # Entry-----------------
    
    # area_type  
    if pd.notna(area_type):
        area_type_locator = '//*[@id="reportForm"]/div[2]/div/p[1]/select'
        navigate_to_section(area_type_locator)
        select_dropdown_text(area_type_locator, area_type)
        
    time.sleep(5) # page loading

    # perc_mg
    if pd.notna(perc_mg):
        perc_mg_locator = '//*[@id="percent"]'
        navigate_to_section(perc_mg_locator)
        enter_text(perc_mg_locator, str(perc_mg))
    
    time.sleep(5) # page loading

    # mg_type
    if pd.notna(mg_type):
        mg_type_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(mg_type_locator)
        select_dropdown_text(mg_type_locator, mg_type)
        
    time.sleep(5) # page loading
    
     # pvc_wf
    pvc_wf_element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, 
                                         '//*[@id="reportForm"]/div[2]/div/p[4]/input[2]')))
    if pd.notna(pvc_wf):
        pvc_wf_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/input[2]'
        click_checkbox(pvc_wf_locator, pvc_wf)
            
    time.sleep(5) # page loading
    
    # gla_gap
    if pd.notna(gla_gap):
        gla_gap_locator = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[5]/select'
        navigate_to_section(gla_gap_locator)
        select_dropdown_text(gla_gap_locator, gla_gap)
    
# Move to the next section

    time.sleep(5) # page loading
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Doors

def enter_doors(i):
    # Data-----------------
    num_door = data['Number of Doors'].iloc[i]
    num_idoor = data['Number of Insulated Doors'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Doors")
    
    # Entry-----------------
    
    # num_door
    if pd.notna(num_door):
        num_door_locator = '//*[@id="doorNum"]'
        navigate_to_section(num_door_locator)
        enter_text(num_door_locator, str(int(num_door)))

    # num_idoor
    if pd.notna(num_idoor):
        num_idoor_locator = '//*[@id="doorInsulatedNum"]'
        navigate_to_section(num_idoor_locator)
        enter_text(num_idoor_locator, str(int(num_idoor)))
    
    # Move to the next section
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Floors

def enter_floors(i):
    # Data-----------------
    flo_type = data['Floor Type'].iloc[i]
    gr_flo_cons = data['Ground Floor Construction'].iloc[i]
    gr_flo_insu = data['Ground Floor Insulation Type'].iloc[i]
    
    time.sleep(15)
    
    # Page Loading----------
    
    wait_for_section_title("Floors")
    
    # Entry-----------------
    
    # flo_type
    if pd.notna(flo_type):
        flo_type_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(flo_type_locator)
        select_dropdown_text(flo_type_locator, flo_type)
        
    time.sleep(5) # page loading
    
    # gr_flo_cons
    if gr_flo_cons == "Unknown":
        gr_flo_cons_adj = "70"
    if gr_flo_cons == "Solid":
        gr_flo_cons_adj = "71"
    if gr_flo_cons == "Suspended Timber":
        gr_flo_cons_adj = "72"
    if gr_flo_cons == "Suspended not Timber":
        gr_flo_cons_adj = "73"
    
    if pd.notna(gr_flo_cons):
        gr_flo_cons_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(gr_flo_cons_locator)
        select_dropdown_value(gr_flo_cons_locator, gr_flo_cons_adj)
        
    time.sleep(5) # page loading

    # gr_flo_insu
    if pd.notna(gr_flo_insu):
        if gr_flo_insu == "Unknown":
            gr_flo_insu_adj = "63"
        if gr_flo_insu == "As Built":
            gr_flo_insu_adj = "64"
        if gr_flo_insu == "Retro Fitted":
            gr_flo_insu_adj = "65"
            
        gr_flo_insu_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/select'
        navigate_to_section(gr_flo_insu_locator)
        select_dropdown_value(gr_flo_insu_locator, gr_flo_insu_adj)

    # Move to the next section
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Roofs

def enter_roofs(i):
    # Data-----------------
    construction3 = data['Construction.2'].iloc[i]
    insu_type = data['Insulation Type'].iloc[i]
    insu_th3 = data['Insulation Thickness (mm).2'].iloc[i]
    uv_known3 = data['U-value known?.2'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Roofs")
    
    # Entry-----------------
    
   # construction3
    if pd.notna(construction3):
        construction3_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(construction3_locator)
        select_dropdown_text(construction3_locator, construction3)
        
    time.sleep(1) # page loading

    # insu_type
    if pd.notna(insu_type):
        insu_type_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(insu_type_locator)
        select_dropdown_text(insu_type_locator, insu_type)

    time.sleep(1) # page loading

    # insu_th3
    if pd.notna(insu_th3):
        insu_th3_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/select'
        navigate_to_section(insu_th3_locator)
        select_dropdown_text(insu_th3_locator, insu_th3)
        
    time.sleep(1) # page loading

    # uv_known3
    if pd.notna(uv_known3):
        uv_known3_locator = '//*[@id="reportForm"]/div[2]/div/p[5]/input[2]'
        click_checkbox(uv_known3_locator, uv_known3)
    
    # Move to the next section
    
    time.sleep(5)  # page loading
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Rooms in Roof

def enter_rooms_in_roof(i):
    
    # Page Loading----------
    
    wait_for_section_title("Rooms in Roof")

    # Move to the next section
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Non-Separated Conservatory

def enter_non_separated_conservatory(i):
    
    # Page Loading----------
    
    wait_for_section_title("Non-Separated Conservatory")
    
    # Move to the next section
    
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Main Heating System

def enter_main_heating_system(i):
    # Data-----------------
    
    heat_source = data['Heating Source'].iloc[i]
    eff_source = data['Effiency Source'].iloc[i]
    heat_fuel = data['Heating Fuel'].iloc[i]
    heat_type = data['Heating Type'].iloc[i]
    heat_desc = data['Heating Description'].iloc[i]
    cont_type = data['Control Type'].iloc[i]
    comp_cont = data['Compensating Controller'].iloc[i]
    flue_type = data['Flu Type'].iloc[i]
    faf = data['Fan assisted Flue'].iloc[i]
    mcs_inst = data['MCS Installation of heat pump'].iloc[i]
    heat_em_type = data['Heat Emitter Type'].iloc[i]
    pump_age = data['Pump Age'].iloc[i]
    flow_temp = data['Flow temp of heat generator'].iloc[i]
    elec_met_type = data['Electricity Meter Type'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Main Heating System")
    
    # Entry-----------------
    
    # heat_source
    if pd.notna(heat_source):
        heat_source_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(heat_source_locator)
        select_dropdown_text(heat_source_locator, heat_source)
        
    time.sleep(3) # page loading

    # eff_source
    if pd.notna(eff_source):
        eff_source_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(eff_source_locator)
        select_dropdown_text(eff_source_locator, eff_source)
        
    time.sleep(3) # page loading

    # heat_fuel
    if pd.notna(heat_fuel):
        heat_fuel_locator = '//*[@id="reportForm"]/div[2]/div/p[4]/select'
        navigate_to_section(heat_fuel_locator)
        select_dropdown_text(heat_fuel_locator, heat_fuel)
        
    time.sleep(3) # page loading
    
    # heat_type
    if pd.notna(heat_type):
        heat_type_locator = '//*[@id="reportForm"]/div[2]/div/p[7]/select'
        navigate_to_section(heat_type_locator)
        select_dropdown_text(heat_type_locator, heat_type)
        
    time.sleep(3) # page loading
    
    # page is different for "SAP 2012 Table 4a/4b"
    if eff_source == "SAP 2012 Table 4a/4b":
        # cont_type 
        if pd.notna(cont_type):
            cont_type_locator = '//*[@id="reportForm"]/div[2]/div/p[11]/select'
            navigate_to_section(cont_type_locator)
            select_dropdown_text(cont_type_locator, cont_type)
            
        time.sleep(3) # page loading
            
        # heat_desc
        if pd.notna(heat_desc):
            heat_desc_locator = '//*[@id="reportForm"]/div[2]/div/p[8]/select'
            navigate_to_section(heat_desc_locator)
            select_dropdown_text(heat_desc_locator, heat_desc)
            
        time.sleep(3) # page loading
        
        # comp_cont
        if pd.notna(comp_cont):
            comp_cont_locator = '//*[@id="reportForm"]/div[2]/div/p[13]/input[2]'
            click_checkbox(comp_cont_locator, comp_cont)
                
        time.sleep(3) # page loading
        
        # flue_type
        if pd.notna(flue_type):
            flue_type_locator = '//*[@id="fluetypeInput"]'
            navigate_to_section(flue_type_locator)
            select_dropdown_text(flue_type_locator, flue_type)
            
        time.sleep(3) # page loading
        
        # faf
        if pd.notna(faf):
            faf_locator = '//*[@id="fanAssistanceCheckbox"]'
            click_checkbox(faf_locator, faf)
                
        time.sleep(3) # page loading
        
        # mcs_inst
        if pd.notna(mcs_inst):
            mcs_inst_locator = '//*[@id="mcsInstallationCheckbox"]'
            click_checkbox(mcs_inst_locator, mcs_inst)
                
        time.sleep(3) # page loading
        
        # heat_em_type
        if pd.notna(heat_em_type):
            heat_em_type_locator = '//*[@id="reportForm"]/div[2]/div/p[19]/select'
            navigate_to_section(heat_em_type_locator)
            select_dropdown_text(heat_em_type_locator, heat_em_type)
            
        time.sleep(3) # page loading
        
        # pump_age
        if pd.notna(pump_age):
            pump_age_locator = '//*[@id="reportForm"]/div[2]/div/p[20]/select'
            navigate_to_section(pump_age_locator)
            select_dropdown_text(pump_age_locator, pump_age)
            
        time.sleep(3) # page loading
        
        # flow_temp
        if pd.notna(flow_temp):
            flow_temp_locator = '//*[@id="reportForm"]/div[2]/div/p[21]/select'
            navigate_to_section(flow_temp_locator)
            select_dropdown_text(flow_temp_locator, flow_temp)
        
        # elec_met_type
        if pd.notna(elec_met_type):
            elec_met_type_locator = '//*[@id="MAIHS_O_4"]'
            navigate_to_section(elec_met_type_locator)
            select_dropdown_text(elec_met_type_locator, elec_met_type)
            
        time.sleep(3) # page loading
        
    else:
        # heat_desc
        if pd.notna(heat_desc):
            heat_desc_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[8]/select'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, heat_desc_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            heat_desc_field = Select(driver.find_element(By.XPATH, heat_desc_selector))
            heat_desc_field.select_by_visible_text(heat_desc)
            
        # cont_type 
        if pd.notna(cont_type):
            cont_type_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[13]/input[2]'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, cont_type_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            cont_type_field = Select(driver.find_element(By.XPATH, cont_type_selector))
            cont_type_field.select_by_visible_text(cont_type)
        
        # comp_cont
        if pd.notna(comp_cont):
            comp_cont_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[13]/input[2]'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, comp_cont_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            comp_cont_checkbox = driver.find_element(By.XPATH, comp_cont_selector)
            if comp_cont == 'Yes':
                comp_cont_checkbox.click()
        
        # flue_type
        if pd.notna(flue_type):
            flue_type_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[16]/select'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, flue_type_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            flue_type_field = Select(driver.find_element(By.XPATH, flue_type_selector))
            flue_type_field.select_by_visible_text(flue_type)
        
        # faf
        if pd.notna(faf):
            faf_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[17]/input[2]'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, faf_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            faf_checkbox = driver.find_element(By.XPATH, faf_selector)
            if faf == 'Yes':
                faf_checkbox.click()
        
        # mcs_inst
        if pd.notna(mcs_inst):
            mcs_inst_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[17]/input[2]'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, mcs_inst_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            mcs_inst_checkbox = driver.find_element(By.XPATH, mcs_inst_selector)
            if mcs_inst == 'Yes':
                mcs_inst_checkbox.click()
        
        # heat_em_type
        if pd.notna(heat_em_type):
            heat_em_type_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[19]/select'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, heat_em_type_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            heat_em_type_field = Select(driver.find_element(By.XPATH, heat_em_type_selector))
            heat_em_type_field.select_by_visible_text(heat_em_type)
        
        # pump_age
        if pd.notna(pump_age):
            pump_age_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[20]/select'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, pump_age_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            pump_age_field = Select(driver.find_element(By.XPATH, pump_age_selector))
            pump_age_field.select_by_visible_text(pump_age)
        
        # elec_met_type
        if pd.notna(elec_met_type):
            elec_met_type_selector = '/html/body/div[1]/div[2]/div[2]/div[2]/div/div/form/div[2]/div/p[22]/select'
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, elec_met_type_selector)))
            time.sleep(2)  # Short sleep for dynamic content
            elec_met_type_field = Select(driver.find_element(By.XPATH, elec_met_type_selector))
            elec_met_type_field.select_by_visible_text(elec_met_type)

    # Move to the next section
    
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Second Main Heating System

def enter_second_main_heating_system(i):
    
    # Page Loading----------
    
    wait_for_section_title("Second Main Heating System")
    
    # Move to the next section
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

    time.sleep(5)

### Secondary Heating System

def enter_secondary_heating_system(i):
    # Data
    heat_fuel2 = data['Heating Fuel'].iloc[i]
    heat_type2 = data['Heating Type.1'].iloc[i]
    
    # Page Loading----------
    
    wait_for_section_title("Secondary Heating System")
    
    # Entry
    # heat_fuel2
    if pd.notna(heat_fuel2):
        heat_fuel2_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(heat_fuel2_locator)
        select_dropdown_text(heat_fuel2_locator, heat_fuel2)
        
    time.sleep(5) # page loading

    # heat_type2
    if pd.notna(heat_type2):
        heat_type2_locator = '//*[@id="reportForm"]/div[2]/div/p[3]/select'
        navigate_to_section(heat_type2_locator)
        select_dropdown_text(heat_type2_locator, heat_type2)

    # Move to the next section
    
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

    ### Water Heating System

def enter_water_heating_system(i):
    # Data
    heat_type3 = data['Heating Type.2'].iloc[i]
    volume = data['Volume'].iloc[i]
    sw_hp = data['Solar Water Heating Panel'].iloc[i]
    fghrs = data['FGHRS Present?'].iloc[i]
    num_ro_bs = data['Number of Rooms with Bath and/or Shower'].iloc[i]
    num_ro_msnb = data['Number of Rooms with Mixer Shower and no Bath'].iloc[i]
    num_ro_msb = data['Number of Rooms with Mixer Shower and Bath'].iloc[i]

    # Page Loading----------
    
    wait_for_section_title("Water Heating System")
    
    # Entry
    
    # heat_type3
    if pd.notna(heat_type3):
        heat_type3_locator = '//*[@id="reportForm"]/div[2]/div/p[2]/select'
        navigate_to_section(heat_type3_locator)
        select_dropdown_text(heat_type3_locator, heat_type3)
        
    time.sleep(1) # page loading

    # volume 
    if pd.notna(volume):
        volume_locator = '//*[@id="reportForm"]/div[2]/div/p[6]/select'
        navigate_to_section(volume_locator)
        select_dropdown_text(volume_locator, volume)
        
    time.sleep(1) # page loading

    # sw_hp
    if pd.notna(sw_hp):
        sw_hp_locator = '//*[@id="reportForm"]/div[2]/div/p[12]/input[2]'
        click_checkbox(sw_hp_locator, sw_hp)
            
    time.sleep(1) # page loading

    # fghrs
    if pd.notna(fghrs):
        fghrs_locator = '//*[@id="reportForm"]/div[2]/div/p[16]/input[2]'
        click_checkbox(fghrs_locator, fghrs)
            
    time.sleep(1) # page loading

    # num_ro_bs
    if pd.notna(num_ro_bs):
        num_ro_bs_locator = '//*[@id="reportForm"]/div[2]/div/p[19]/input'
        navigate_to_section(num_ro_bs_locator)
        enter_text(num_ro_bs_locator, str(int(num_ro_bs)))
        
    time.sleep(1) # page loading

    # num_ro_msnb
    if pd.notna(num_ro_msnb):
        num_ro_msnb_locator = '//*[@id="reportForm"]/div[2]/div/p[20]/input'
        navigate_to_section(num_ro_msnb_locator)
        enter_text(num_ro_msnb_locator, str(int(num_ro_msnb)))
    
    time.sleep(1) # page loading

    # num_ro_msb
    if pd.notna(num_ro_msb):
        num_ro_msb_locator = '//*[@id="reportForm"]/div[2]/div/p[21]/input'
        navigate_to_section(num_ro_msb_locator)
        enter_text(num_ro_msb_locator, str(int(num_ro_msb)))
    
    # Move to the next section
    
    time.sleep(5) # page loading
    
    dropdown = driver.find_element(By.XPATH, '//*[@id="assessmentsBox"]/a')
    dropdown.click()

    time.sleep(1)

    special_features_option = driver.find_element(By.XPATH, '//*[@id="assessmentsBox"]/ul/li[17]/a')
    special_features_option.click()

### Special Features Appendix Q

def enter_special_features(i):
    
    # Page Loading----------
    
    wait_for_section_title("Special Features Appendix Q")
    
    # Move to the next section
    
    time.sleep(5)
    
    next_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[3]/div/button'
    click_button(next_button_locator)

### Save and Exit

def save_exit():
    
    # Page Loading----------
    
    wait_for_section_title("Improvement Measures")
    
    # Save
    save_button_locator = '//*[@id="submit"]'
    click_button(save_button_locator)

    time.sleep(5) # page loads
    
    # Close
    close_button_locator = '//*[@id="reportForm"]/div[3]/div[1]/div[5]/div/button'
    click_button(close_button_locator)

    time.sleep(5) # page loads
    
    # Ok 
    ok_button_locator = '//*[@id="alertMsgBox"]/div[1]/div/div[2]/ul/li[1]/a/span'
    click_button(ok_button_locator)

    time.sleep(5) # page loads

## Automation

# Login
login()

for i in range(len(data)):
    print(f"Entry {i + 1} started.")
    add_new_entry(i)
    
    print("New entry ended.")
    print("Building details started.")
    handle_exceptions(enter_building_details, i)
    print("Building details ended.")
    print("Classification started.")
    handle_exceptions(enter_classification, i)
    print("Classification ended.")
    print("General started.")
    handle_exceptions(enter_general, i)
    print("General ended.")
    print("Dimension started.")
    handle_exceptions(enter_dimension, i)
    print("Dimension ended.")
    print("Flats and Maisonettes started.")
    handle_exceptions(enter_flats_maisonettes, i)
    print("Flats and Maisonettes ended.")
    print("Walls started.")
    handle_exceptions(enter_walls, i)
    print("Walls ended.")    
    print("Windows started.")
    handle_exceptions(enter_windows, i)
    print("Windows ended.")
    print("Doors started.")
    handle_exceptions(enter_doors, i)
    print("Doors ended.")
    print("Floors started.")   
    handle_exceptions(enter_floors, i)
    print("Floors ended.")     
    print("Roofs started.") 
    handle_exceptions(enter_roofs, i)
    print("Roofs ended.")    
    print("Rooms in roof started.") 
    handle_exceptions(enter_rooms_in_roof, i)
    print("Rooms in roof ended.")
    print("NSC started.")
    handle_exceptions(enter_non_separated_conservatory, i)
    print("NSC ended.")    
    print("Main heating started.")
    handle_exceptions(enter_main_heating_system, i)
    print("Main heating ended.")
    print("Second main heating started.")
    handle_exceptions(enter_second_main_heating_system, i)
    print("Second main heating ended.")
    print("Secondary heating started.")
    handle_exceptions(enter_secondary_heating_system, i)
    print("Secondary heating ended.")
    print("Water heating started.")
    handle_exceptions(enter_water_heating_system, i)
    print("Water heating ended.")
    print("Special features started.")  
    handle_exceptions(enter_special_features, i)
    print("Special features ended.") 
    print("Save-exit started.")
    handle_exceptions(save_exit, )
    print("Save-exit ended.") 
    
    end_time = time.time()
    # Calculate total runtime
    runtime = end_time - start_time
    print(runtime)
    
    time.sleep(5)