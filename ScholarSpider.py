__author__ = "Max Greenberg"
__email__ = "mg957@cornell.edu"
__date__ = "5/4/2022"
__license__ = "MIT"
__version__ = "1.0"


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from math import ceil
import pandas as pd
import re


# Spreadsheet paths and column of titles within sheets
spreadsheet_1_path = '...\\sheet1.xlsx'   # List of publications already included in 2022 report
spreadsheet_2_path = '...\\sheet2.xlsx'   # List of publications included in previous reports
spreadsheet_1_title_col = 'A'
spreadsheet_2_title_col = 'E'


# Google Scholar search parameters
dmr = 'DMR-1719875'                                             # CCMR DMR number as main query
to_exclude = ["APS", "arxiv", "chemrxiv"]                       # Sources to exclude; APS only has conference notes while arxiv and chemrxiv only have preprints
filtered_phrases = ["Data from:", "Data From:", "Correction:"]  # Phrases to filter: we exclude datasets and corrections
doc_types = ["[HTML]", "[BOOK]", "[PDF]", "[CITATION]"]         # Doc types that appear in Google Scholar titles
since_year = "2021"                                             # Ask for no results from before this year (last year)


# Generates the initial url to query based on above parameters
def generate_url():
    to_exclude_str = ""
    for e in to_exclude:
        to_exclude_str += "+-" + e
    return 'https://scholar.google.com/scholar?start=0&q=' + dmr + to_exclude_str + '&hl=en&as_sdt=0,33&as_ylo=' + since_year


# Queries the initial url to grab the number of results
def get_num_pages():
    driver = webdriver.Firefox()
    driver.get(generate_url())
    results_string = driver.find_element_by_xpath("//div[@id='gs_ab_md']/div[@class='gs_ab_mdw']").text
    results = results_string[:results_string.find('(')]         # Obtains number of results
    driver.close()
    return ceil(int(re.sub("\D", "", results)) / 10)            # Converts number of results into number of pages


# Converts titles into standard form. Order is very important!
def reformat(title):
    for d in doc_types:                                         # Filters out all Google Docs document type prefixes
        title = title.replace(d, '')
    title = re.sub('[^a-zA-Z]+', '', title)                     # Filters out everything but alphabetical characters
    title = title[:100]                                         # Trims title to 100 characters to avoid Scholar cutoff
    return title.lower()                                        # Turns title to lowercase and returns it


# Scrapes spreadsheets of previously-included publications, re-formats titles, and collates them into list
def get_already_downloaded():
    added_list = []
    df1 = pd.read_excel(spreadsheet_1_path, usecols=spreadsheet_1_title_col, skiprows=0)
    df2 = pd.read_excel(spreadsheet_2_path, usecols=spreadsheet_2_title_col, skiprows=0)
    for i in range(len(df1)):
        title = reformat(df1.values[i][0])
        added_list.append(title)
    for j in range(len(df2)):
        title = reformat(df2.values[j][0])
        added_list.append(title)
    return added_list


# Cycles through Google Scholar results and grabs all titles not listed in above spreadsheets
def collect_papers():
    added_list = get_already_downloaded()
    to_add_list = []                                            # Creates empty list to populate with new papers
    pages = get_num_pages()                                     # Defines the number of pages to cycle through
    driver = webdriver.Firefox()
    for i in range(pages):                                      # Each iteration is the next page of Scholar results
        url = generate_url().replace("start=0", "start=" + str(10 * i))
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@class='gs_ri']")))
        elements = driver.find_elements_by_xpath("//*[@class='gs_ri']")
        for e in elements:
            title = e.find_element_by_class_name("gs_rt").text  # Grabs all titles on page
            for p in filtered_phrases:                          # Removes papers with phrases to filter
                if p in title:
                    title = ''
            title2 = reformat(title)
            if title2 not in added_list and len(title2) > 1:    # Ensures title is not in spreadsheets and has at least one Latin character
                to_add_list.append([title, i+1])                # Adds title of paper and Scholar page number to list
    driver.close()
    return to_add_list


# Main function. Creates list of new papers then prints said list
def main():
    paper_list = collect_papers()
    for paper in paper_list:
        print(paper)


if __name__ == "__main__":
    main()
