# ScholarSpider
This program is a web crawler intended to scrape Google Scholar for recently published papers which include CCMR’s DMR 
number (1719875). It does so by querying Google Scholar for the DMR number and cross-referencing the titles of each of 
the results against a preloaded list of titles of publications already included in the current impact report and previous 
reports. It returns a console output listing all of the results from the query which do not come from preprint aggregators 
(e.g. arxiv) and which have not yet been included in the current or previous report. This output can be copied into a text 
file and used as a curated list of publications to check. However, this output needs to be filtered manually, as the program
will likely return a number of preprints and theses (which should not be included in the report) and potentially papers that
have been uploaded to Zotero but were not properly added to one of the spreadsheets.


# Dependencies:

In order for this program to run properly, the user must first install the selenium and pandas Python packages. This can 
be done easily using either the pip or conda package managers.


# Parameters:

The following parameters may be changed according to the user’s personal setup:

--spreadsheet_1_path: the location of the spreadsheet on the user's computer containing the papers already included in the current report.

--spreadsheet_2_path: the location of the spreadsheet on the user's computer containing papers from the previous year’s report.

--spreadsheet_1_title_col: the column of spreadsheet 1 containing the title of each paper

--spreadsheet_2_title_col: the column of spreadsheet 2 containing the title of each paper.

--dmr: the main Google Scholar search query. Should be set to "DMR-1719875" (CCMR's DMR number)

--to_exclude: sources of Google Scholar hits to be filtered from the search results. Default includes “APS”, “arxiv”, and “chemrxiv”, 
              as these sources consist exclusively of conference talks and preprints, which are not included in the report.
              
--doc_types: list of prefixes Google Scholar appends to some results' titles. Important for title comparisons; add any if missing

--since_year: the year of the last report, as a string. Filters all papers published before said year.


# Troubleshooting:

Some bugs the user may encounter while using this program:

--False positives: The program conducts its search by querying Google Scholar for CCMR’s DMR number, but some papers 
  may include this number for reasons unrelated to funding acknowledgements (DOI, numerical results, etc.). Therefore, a 
  manual verification of each of the results pulled from Google Scholar is necessary.
  
--Blank titles: Since the program filters out non-Latin characters from paper titles to avoid HTML conversion issues, a 
  blank title in the final print statement usually means the program encountered a result whose title was written in a 
  non-Latin alphabet. These are almost always false positives as well, so the user may safely ignore this.
  
--Google captchas: Google policy prohibits web crawlers from using its services, including Google Scholar. Consequently, 
  submitting too many queries in a short period of time will often result in the program getting locked out of Google 
  Scholar and asked to answer a captcha. This should not be a problem for day-to-day use of the program, as running it only 
  a few times does not seem to trip a captcha; however, it has frequently been a problem for tweaking and testing the 
  program. The program has an inbuilt implicit wait which gives the user 60 seconds to solve the captcha, after which the 
  program resumes operating as usual. After 12 to 24 hours, Google Scholar will stop asking for captchas until the next
  time the program is overused.
