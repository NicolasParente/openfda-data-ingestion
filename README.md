# openfda-data-ingestion
A robust Python ETL pipeline to extract, clean, and structure adverse drug event data from the public OpenFDA API.

## Abstract
This project aims to programmatically query and transform complex, nested clinical data regarding adverse drug reactions into a cohesive, highly readable format. The resulting pipeline acts as a robust foundation for Data Science, Machine Learning, or Pandas-based analytical workflows.

## Dataset Description
The data is retrieved dynamically via the **FDA Adverse Event Reporting System (FAERS)** API. 
- **Raw Input:** A deeply nested JSON structure containing detailed patient records, drug information, and reported reactions.
- **Processed Output:** A cleaned, unified dictionary mapped by `safetyreportid` (primary key). Each entry isolates critical clinical features: the medicinal product name, the patient's onset age, and a flattened list of adverse reactions.

## Code Description
The Python script (`safety_report.py`) is logically divided into distinct modular functions to handle the ETL process:
- **Data Extraction (`request_data`):** Connects to the OpenFDA API querying for specific cases (e.g., Ibuprofen). It implements defensive programming via `requests.RequestException` and custom timeouts to prevent the script from hanging during network failures.
- **Data Cleaning (`clean_data`):** Iterates through the raw API response. It safely flattens nested lists (such as the `drug` array) and handles missing or corrupt keys (e.g., missing `reactionmeddrapt` strings or `patientonsetage`) without interrupting the extraction flow.
- **Data Output (`print_save_data`):** Serializes the standardized Python dictionary into a formatted `cleaned_data.json` file for permanent storage and visual inspection.

## Conclusions 
Unlike the raw API response, which features highly variable nesting and unpredictable key absences, the pipeline successfully guarantees a strict, flattened dictionary structure. By actively filtering out corrupted nodes and unifying the data under unique report IDs, the script eliminates the risk of misaligned data indices, making the output immediately suitable for DataFrame conversion and downstream ML applications.

## How to Run
In order to run the program:
1. Clone or download this repository to your
2. Ensure you have Python 3.x installed.
3. Install the required third-party library by running: `pip install requests`
4. Open your terminal in the project directory and run: `python safety_report.py`
5. The processed dataset will be printed to the terminal and saved locally as `cleaned_data.json`.
