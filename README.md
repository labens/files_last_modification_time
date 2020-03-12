# Logs Last Modification Time

The idea is to constantly log how long ago were the files modified. This is useful for the LABENS TI to analyse if we have a network or hardware error and act on it.

## Files

- **database.py** defines the commands related to the DB
+ **last_mod_file.py** logs how long ago were the current day files modified

### To do

- warns user (email) if some file is a long time without update
- show and grapth data to the website (django integration)