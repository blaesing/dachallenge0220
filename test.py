import health_policy as hp
import unittest

class TestHolder(unittest.TestCase):
    """Test the PolicyHolder class"""

    def setUp(self):
        self.test_holder = hp.Insured("John Smith","N/A","1994-01-01","111-12-1234",True,["Peanut Butter","Oxygen"],["Fever","Arrythmia"])
    def test_init(self):
        with self.assertRaises(AssertionError):
            # input a bad ssn format
            hp.Insured("John Smith","N/A","1994-01-01","111-112-1234",True,["Peanut Butter","Oxygen"],["Fever","Arrythmia"])
        self.assertEqual(len(self.test_holder.holder_information),1)
        # if we initialize properly, we should have a dataframe of length one

class TestDataBase(unittest.TestCase):
    """Test the DataBase class"""

    def setUp(self):
        self.test_holder = hp.Insured("John Smith","N/A","1994-01-01","111-12-1234",True,["Peanut Butter","Oxygen"],["Fever","Arrythmia"])
        self.new_insured = hp.Insured("Jane Doe","Female","2000-02-14","000-00-0001",False,["Oranges"],[])
        self.test_db = hp.DataBase(self.test_holder)


    def test_init(self):
        self.assertEqual(len(self.test_db.insureds),1)
        new_db = hp.DataBase(self.test_holder,self.new_insured)
        self.assertEqual(len(new_db.insureds),2)
        with self.assertRaises(ValueError):
            # just make everything wrong
            hp.Insured("Jon",1,"14-14-14","120312031",4,[],[])
        #print(self.test_db.insureds,'\n')

    def test_add_insured(self):
        #print("Insured ID is: ",self.test_db.add_insured(self.new_insured),'\n')
        self.test_db.add_insured(self.new_insured)
        self.assertEqual(len(self.test_db.insureds),2)
        with self.assertRaises(AssertionError):
            self.test_db.add_insured(["Thomas Jefferson","Male","1743-04-13","000-00-0001",True,["British Empire"],[]])

    def test_add_loss(self):
        with self.assertRaises(AssertionError):
            self.test_db.add_loss("aaaaaaaaaaaaaa","2012-01-01","Indemnity",100,100)
        self.test_db.add_insured(hp.Insured("Tom Thompson","Male","1987-02-01","367-88-8888","no",[],[]))
        self.test_db.insureds.iloc[1,0] = "891e02a2-65f5-4ee6-918b-cfa64d7a2cac"
        self.assertEqual(len(self.test_db.add_loss("891e02a2-65f5-4ee6-918b-cfa64d7a2cac","2014-01-01","Medical",100,100)),1)

    def test_show_insureds(self):
        self.test_db.add_insured(self.new_insured)
        self.assertEqual(len(self.test_db.show_insureds()),2)
        #print(self.test_db.show_insureds(),'\n')


    def test_list_losses(self):
        self.test_db.add_loss(self.test_holder._id,"2001-04-08","medical",100,90)
        self.test_db.add_loss(self.test_holder._id,"2006-04-08","medical",100,90)
        self.test_db.add_insured(self.new_insured)
        self.test_db.add_loss(self.new_insured._id,"2006-04-08","medical",100,90)
        self.assertEqual(len(self.test_db.list_loss_events(self.test_holder._id)),2)
        self.assertEqual(len(self.test_db.list_loss_events(self.new_insured._id)),1)


    def test_show_loss_summaries(self):
        self.test_db.add_insured(self.new_insured)
        self.test_db.add_loss(self.test_holder._id,"2012-01-01","Medical",150,100)
        self.test_db.add_loss(self.new_insured._id,"2014-01-01","Medical",150,750.49)
        self.test_db.add_loss(self.test_holder._id,"2014-01-01","Medical",0,0)
        self.test_db.add_loss(self.test_holder._id,"2014-01-01","Medical",150,1000)
        self.assertEqual(self.test_db.show_loss_summaries().loc["Summary","Covered Amount"],1850.49)
        self.assertEqual(self.test_db.show_loss_summaries().loc["Summary","Average Age of Claimant"],23)

if __name__ == "__main__":
    unittest.main()
