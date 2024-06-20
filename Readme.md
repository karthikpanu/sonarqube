# Sonarqube Automation
Use the script to generate list of projects on sonarqube server based on a search query and before last analysis date, store it into a csv.

Later use the CSV to delete all the project one by one.

* the project uses one of the best practices for secrets for local desktop execution. (the best would be to make an api call to fetch from vault)
* the project doesn't skip ssl signed cert verification.
