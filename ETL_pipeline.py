"""This module is responsible for the collection, cleaning and output of the dataset"""
import sys
import json

import requests

def main():
    """Main of the program: collects, cleans and prints the data"""
    data = request_data()
    cleaned_data = clean_data(data)
    print_save_data(cleaned_data)


def request_data():
    """gets the data from the database and returns it"""

    try:
        response = requests.get(
            "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:ibuprofen&limit=10", 
            timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        sys.exit("Could not complete request!")

    content = response.json()

    # The following lines are commented, since they are only used
    # to create a text file allowing the visual analysis of the results

    # with open("analysis.json", "w") as file:
    #    json.dump(content, file, indent=4)

    return content.get("results") # returns a list of dicts, each one is a case


def clean_data(results):
    """cleans and returns the dataset by retaining only:
    - safety report id
    - medicinal product name
    - adverse effects 
    - patient set age"""

    try:
        # empty dict to store the results
        filtered_data = {}

        for result in results:

            # Safety Report extraction
            safety_report_id = result["safetyreportid"]

            # Medicinal product extraction
            patient = result["patient"] # returns a dict
            drug = patient["drug"] # returns a list of dicts
            drug = drug[0] # the product name can be found inside the first dict
            medicinal_product = drug["medicinalproduct"]

            # Adverse reaction effect extraction
            reactions = []
            for reaction in patient["reaction"]:
                if "reactionmeddrapt" in reaction: # Note: some dicts lack the string key
                                                   # reactionmeddrapt, so I check and choose to just ignore them
                    reactions.append(reaction["reactionmeddrapt"])

            # Patient onset age extraction
            if patient.get("patientonsetage") is None:
                patient_set_age = "Not specified"
            else:
                patient_set_age = patient.get("patientonsetage")

            # Creation of the data dict
            case = {"medicinalproduct" : medicinal_product,
                    "reactionmeddrapt" : reactions,
                    "patientonsetage" : patient_set_age,}

            # Creation of the case dict
            filtered_data[safety_report_id] = case

        return filtered_data

    except KeyError:
        sys.exit("Data lacks crucial information")


def print_save_data(dataset):
    """Prints the data to the terminal and writes it to a JSON file"""

    # Print on terminal
    print(json.dumps(dataset, indent=4))

    # Write json file
    with open("cleaned_data.json", "w") as file:
        json.dump(dataset, file, indent=4)


if __name__ == "__main__":
    main()
