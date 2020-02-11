# Kevin Blaesing

## Summary of Code
Note: this requires python3 as it uses argument hinting

This project makes use of two classes:
1. **Insured**, which is a person that takes in the following arguments:
	- Name
	- Gender
	- Date of Birth (in YYYY-MM-DD format, which is checked for)
	- A Social Security Number (including dashes: xxx-xx-xxxx), which is then hashed using SHA 256 for security
	- A Smoking status: which takes "yes",1,True or "no",0,False (words can be in any variety of case) and is evaluated to `True` or `False`.
	- A list of allergies
	- A list of current medical Conditions.

2. **Database**, which inputs any number of Insureds on initialization and has the following functions:

- `add_insured`, which asks for a valid **Insured** object to add to the `insureds` table.
- `add_loss`, which requests to be passed an Insured's unique id (which is generated on initialization of the Insured object), a loss date (formatted for YYYY-MM-DD), a Loss Type, a paid amount, and an amount covered by the carrier
- `show_insureds`, which shows all current insureds and their unique identifiers
- `list_loss_events` which will show all loss events pertaining to an insured, requires the insured's unique identifier and returns a list of losses for that insured
- `show_loss_summaries` which returns an aggregate dataframe of total payouts, number of claims per year and overall, and average age of insureds in the database.


## Question 5
To keep information safe, I would use an encryption method with a stored secret key for methods such as AES for two way encoding and decoding.
