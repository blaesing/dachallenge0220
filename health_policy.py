import pandas as pd, numpy as np, uuid, hashlib, re
from datetime import datetime, date

class Insured():
  """A Policy Holder is a Person who holds unique identifying information pertaining to the, primarily:
  1. A Name
  2. A DOB (which will be parsed into a datetime using YYYY-MM-DD format)
  3. A SSN (which should be hashed for safety purposes. I used SHA-256, but ideally would be paired with a method that has a stored private key for decryption.
  4. Smoking status
  5. Allergies
  6. Current known medical conditions"""

  def __init__(self,name: str,gender: str, dob: str,ssn: str, smoking, allergies: list, conditions: list):

    try:
        self.name = str(name)
        self.gender =str(gender)
        self.dob = datetime.strptime(dob,"%Y-%m-%d")
        assert re.match(r"^\d{3}-\d{2}-\d{4}$",ssn), "Social Security Number is of invalid format"
        self.ssn = hashlib.sha256(str(ssn).encode('utf-8')).hexdigest()
        if str(smoking).lower() in ["true",1,"yes"]:
            self.smoking = True
        else: self.smoking = False
        self.allergies = list(allergies)
        self.conditions = list(conditions)
        self._id = uuid.uuid4() # hold off until we're sure we need it

    except ValueError as e:
        raise e


    # make a dataframe out of the information
    self.holder_information = pd.DataFrame([[self._id,self.name,self.gender,self.dob,self.ssn,self.smoking,self.allergies,self.conditions]],columns = ["_id","Name","Gender","Date of Birth","SSN","Smoking","Allergies","Conditions"])

class DataBase():
    """A Database holds two tables:
    1. A PolicyHolder table, called "insureds"
    2. An Event table, called "losses"
    It takes an Insured as an input and will generate loses from class methods"""

    def __init__(self,*insureds):
        self.insureds = pd.DataFrame(columns = ["_id","Name","Gender","Date of Birth","SSN","Smoking","Allergies","Conditions"])
        self.losses = pd.DataFrame(columns = ["loss_id","insured_id","LossDate","LossType","Total Paid","Covered Amount"])

        for i in insureds:
            assert isinstance(i,Insured), f"Expected an Insured, got {type(i)}"
            self.insureds = self.insureds.append(i.holder_information)

    def add_loss(self,insured_id: str,loss_date: str, loss_type: str, loss_amount: float, amount_covered: float):
        """Adds a loss that inputs policy holder information into a table, it checks to make sure that the holder's name is in the data structure before you can add anything"""

        assert insured_id in self.insureds["_id"].tolist(), f"{insured_id} not found in records!"

        try:
            insured_id = str(insured_id)
            format_date = datetime.strptime(loss_date,"%Y-%m-%d")
            loss_type = str(loss_type)
            format_date = datetime.strptime(loss_date,"%Y-%m-%d")
            amount_covered = float(amount_covered)
        except ValueError as e:
            raise e

        loss_id = uuid.uuid4()
        loss_table = pd.DataFrame([[loss_id,insured_id,format_date,loss_type,loss_amount,amount_covered]],columns = ["loss_id","insured_id","LossDate","LossType","Total Paid","Covered Amount"])
        self.losses = self.losses.append(loss_table)
        return self.losses

    def add_insured(self,insured):
        """Requires an Insured object, adds the insured to the database and returns the unique identifier of the new insured"""

        assert isinstance(insured,Insured), f"Expected Insured, got {type(insured)}"
        self.insureds = self.insureds.append(insured.holder_information)
        return insured._id

    def show_insureds(self):
        table = self.insureds.iloc[:,:2]
        return table

    def list_loss_events(self,insured_id):
        
        losses = self.losses[self.losses["insured_id"]== str(insured_id)]
        return losses

    def show_loss_summaries(self):
        """This function will aggregate all information in the insureds and losses tables and return the following in a dataframe:
        1. Total covered amount for all claims (incurred)
        2. Claims per year 
        3. Average Age of insured"""
        current_year = date.today().year
        losses = self.losses.copy()
        losses["Loss Year"] = losses["LossDate"].map(lambda x: x.year)

        claim_values = pd.DataFrame(losses["Loss Year"].value_counts()).reset_index()
        claim_values.columns = ["Loss Year","Claim Count"]

        ages = [current_year - x.year for x in self.insureds["Date of Birth"]]
        average_age = sum(ages)//len(ages)

        summary_table = losses.groupby("Loss Year").sum()
        summary_table=summary_table.merge(claim_values,on = "Loss Year")
        summary_table.loc["Summary"] = summary_table.sum()
        summary_table.loc["Summary","Loss Year"] = np.nan
        summary_table.loc["Summary", "Average Age of Claimant"] = average_age
        return summary_table
