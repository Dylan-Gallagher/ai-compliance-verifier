import json

# Load data from files
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_path.endswith('.py'):
            content = file.read()
            dict_str = content.split('=', 1)[1].strip()
            data = eval(dict_str)
        else:
            data = [json.loads(line) for line in file]
    return data

# Generate compliance checklist from KG rules
def generate_compliance_checklist(kg_rules):
    checklist = {}
    for rule in kg_rules:
        if rule["type"] == "require":
            category = rule["tail_cat"]
            if category not in checklist:
                checklist[category] = []
            checklist[category].append(rule["tail"].lower())
    return checklist

# Score compliance based on factsheet and checklist
def score_compliance(factsheet, checklist):
    #score = 100
    factsheet_str = str(factsheet).lower()
    compliance_details = {"met_requirements": {}, "missing_requirements": {}}
    present = 0
    missing = 0
    for category, requirements in checklist.items():
        for requirement in requirements:
            if requirement in factsheet_str:
                if category not in compliance_details["met_requirements"]:
                    compliance_details["met_requirements"][category] = []
                compliance_details["met_requirements"][category].append(requirement)
                present += 1
            else:
                if category not in compliance_details["missing_requirements"]:
                    compliance_details["missing_requirements"][category] = []
                compliance_details["missing_requirements"][category].append(requirement)
                missing += 1

    #print(f"{present = }")
    #print(f"{missing = }")
    #print(f"total = {present + missing}")
    score = ((min(max(present + 12, 0), present+missing)) / missing) * 100
    # Determine risk level and adjust the score
    if 'high risk' in factsheet_str:
        score = max(min(100, score * 0.682), 0)
    elif 'low risk' in factsheet_str:
        score = max(min(100, score * 1.47), 0)
    else:  # Mid risk or unspecified
        score = max(min(100, score * 1.03), 0)
    
    return round(score), compliance_details

# Generate detailed recommendations based on compliance details
def analyze_documentation(compliance_details):
    recommendations = []
    if compliance_details["missing_requirements"]:
        for category, reqs in compliance_details["missing_requirements"].items():
            req_list = ", ".join(reqs)
            recommendations.append(f"- For {category.upper()} ({expand_acronym(category)}), consider addressing: {req_list}.")
    if not recommendations:
        recommendations.append("Great job! Your AI system meets all compliance requirements. Keep up the good work.")
    return recommendations

# Helper function to expand acronyms for clarity
def expand_acronym(acronym):
    expansions = {
        "ETH": "Ethical Considerations",
        "SYS": "System Characteristics",
        "ACT": "Actions and Processes",
        "DAT": "Data Handling",
        "DOC": "Documentation and Specifications",
        "ORG": "Organizational Aspects",
        "PER": "Personal Data",
        "LOC": "Location Data",
        "SPA": "Space Utilization",
        "STA": "Standards and Regulations",
        "ALG": "Algorithms and Automated Processes",
        "PRO": "Regulatory Processes",
        "HAR": "Harm Prevention",
        "MAR": "Marking and Compliance"
    }
    return expansions.get(acronym, "Unknown Category")

def save_compliance_checklist(kg_rules):
    checklist = generate_compliance_checklist(kg_rules)
    with open("compliance_checklist.json", "w", encoding="utf-8") as file:
        json.dump(checklist, file, indent=4)

def pdf_data_to_rules(factsheet_data):
    with open("compliance_checklist.json", "r") as file:
        checklist = json.load(file)
    compliance_score, compliance_details = score_compliance(factsheet_data, checklist)
    recommendations = analyze_documentation(compliance_details)
    return compliance_score, recommendations


def main():
    factsheet_path = "factsheet_data.py"
    kg_path = "kg_data.jsonl"
    
    factsheet_data = load_data(factsheet_path)
    kg_rules = load_data(kg_path)
    
    checklist = generate_compliance_checklist(kg_rules)
    compliance_score, compliance_details = score_compliance(factsheet_data, checklist)
    recommendations = analyze_documentation(compliance_details)
    
    # Define the output file path
    output_file_path = "compliance_report.txt"
    
    # Open the file in write mode
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(f"Compliance Score: {compliance_score}\n")
        file.write("Recommendations:\n")
        for recommendation in recommendations:
            file.write(recommendation + "\n")
    
    # Notify the user that the report has been saved
    print(f"Compliance report saved to '{output_file_path}'.")

if __name__ == "__main__":
    main()