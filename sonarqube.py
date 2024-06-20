import requests
import csv
import os
import urllib3
from configparser import ConfigParser
urllib3.disable_warnings()


# Set the Sonarqube Environment
env = "sonar-dev"
secrets_file = "/Users/Documents/sonarqube/secrets.ini"

def _get_username():
    config = ConfigParser()
    config.read(secrets_file)
    return config[env]["username"]

def _get_password():
    config = ConfigParser()
    config.read(secrets_file)
    return config[env]["password"]

def _get_url():
    config = ConfigParser()
    config.read(secrets_file)
    return config[env]["url"]

# ----------  Variables  -----------------------------
os.environ['REQUESTS_CA_BUNDLE'] = '/Users/Documents/cert.pem'
url = _get_url()
auth = (_get_username(), _get_password())
searchTag = "aem-aem-develop-feature"
analyzedBefore = "2023-12-01"
projectsFile = "/Users/Documents/projects.csv"

# ----------  Variables  -----------------------------

def get_projects():
    urlp = f"{url}api/projects/search"
    params = {"q": searchTag, "analyzedBefore": analyzedBefore, "ps": 100}
    projects = []
    while True:
        response = requests.get(urlp, auth=auth, params=params)
        response_json = response.json()
        projects.extend(response_json["components"])
        if not response_json["components"]:
            break
        params["p"] = response_json["paging"]["pageIndex"] + 1
    with open(projectsFile, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Project Name", "Project key", "Last Analyzed Date"])
        for project in projects:
            writer.writerow([project["name"], project["key"], project["lastAnalysisDate"]])


def delete_projects(projectsFile):
    urld = f"{url}api/projects/delete"
    with open(projectsFile, "r") as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            project_name = row[0]
            project_key = row[1]
            print(f"Deleting project: {project_name}")
            params = {"project": project_key}
            response = requests.post(urld, auth=auth, params=params)
            if response.status_code == 204:
                print(f"Project '{project_name}' deleted successfully.")
            elif response.status_code == 404:
                print(f"Project '{project_name}' could not be found")
            else:
                print(f"Failed to delete project '{project_name}'. Error message: {response.text}")

get_projects()
delete_projects(projectsFile=projectsFile)
