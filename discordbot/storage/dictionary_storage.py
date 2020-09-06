import datetime
from dynaconf import settings
from loguru import logger
import yaml


class PythonicRecord:
    """
    This is the data option that we are using for connecting to the data services for the GDKP Assistant.
    It is going to start as a "shitty" bag o' dicts with a series of helper functions and work on from there.
    """

    def __init__(self):
        """
        Create the back end data structure that needs to be connected to systems
        """
        self.account_storage = {}
        if settings.get("DICTIONARY_STORAGE", False):
            self.account_storage = yaml.load(open(settings.DICTIONARY_STORAGE, "r"), yaml.BaseLoader)

    def add_account(self, account_number, requesting_account):
        """
        This will add a new account to the storage system and give it an owner
        :param account_number:
        :param requesting_account:
        :return:
        """
        try:
            self.account_storage[account_number] = {"admins": [requesting_account],
                                                    "powerusers": {},
                                                    "raids": {},
                                                    "users": {}}
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_account(self, account_number):
        """
        Delete the storage for an account
        :param account_number:
        :return:
        """
        try:
            del self.account_storage[account_number]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_account(self, account_number):
        """
        Show information in account
        :param account_number:
        :return:
        """
        try:
            return self.account_storage[account_number]
        except Exception as e:
            logger.error(e)
            return False

    def list_accounts(self):
        """
        Return a list of the accounts
        :return:
        """
        try:
            return list(self.account_storage.keys())
        except Exception as e:
            logger.error(e)
            return False

    def add_owner_account(self, account_number, modify_account):
        """
        Add an owner to the account
        :param account_number:
        :param modify_account:
        :return:
        """
        try:
            self.account_storage[account_number]["admins"].append(modify_account)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def remove_owner_account(self, account_number, modify_account):
        """
        Remove an owner from the account
        :param account_number:
        :param modify_account:
        :return:
        """
        try:
            self.account_storage[account_number]["admins"].remove(modify_account)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_owner_account(self, account_number):
        """
        Shows the owners from the account
        :param account_number:
        :return:
        """
        try:
            return self.account_storage[account_number]["admins"]
        except Exception as e:
            logger.error(e)
            return False

    def add_power_user_account(self, account_number, modify_account, account_value):
        """
        Add a power user to the account
        :param account_number:
        :param modify_account:
        :param account_value:
        :return:
        """
        try:
            self.account_storage[account_number]["powerusers"][modify_account] = account_value
            return True
        except Exception as e:
            logger.error(e)
            return False

    def remove_power_user_account(self, account_number, modify_account):
        """
        Remove a power user from the account
        :param account_number:
        :param modify_account:
        :return:
        """
        try:
            del self.account_storage[account_number]["powerusers"][modify_account]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_power_user_account(self, account_number, modify_account, account_value):
        """
        Update a power user from the account
        :param account_number:
        :param modify_account:
        :param account_value:
        :return:
        """
        try:
            self.account_storage[account_number]["powerusers"][modify_account] = account_value
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_power_user_account(self, account_number):
        """
        Update a power user from the account
        :param account_number:
        :return:
        """
        try:
            return self.account_storage[account_number]["powerusers"]
        except Exception as e:
            logger.error(e)
            return False

    def add_raid(self, account_number, raid_instance, start_datetime):
        """
        Create a raid that is attached to the account number, with the instance for the raid.
        :param account_number:
        :param raid_instance:
        :param start_datetime:
        :return:
        """
        try:
            raid_template = {"raid_instance": raid_instance,
                             "signups": [],  # {"user_account":data,"character_name":data,"signup_time":datetime}
                             "roster": [],  # {user_account":data,"character_name":data,"signup_time":datetime}
                             "start_datetime": datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")}
            raid_id = len(self.account_storage[account_number]["raids"]) + 1000
            self.account_storage[account_number]["raids"][raid_id] = raid_template
            return raid_id
        except Exception as e:
            logger.error(e)
            return False

    def delete_raid(self, account_number, raid_id):
        """
        Delete a raid
        :param account_number:
        :param raid_id:
        :return:
        """
        try:
            del self.account_storage[account_number]["raids"][raid_id]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_raid(self, account_number, raid_id, start_datetime):
        """
        Update the Raid's start time
        :param account_number:
        :param raid_id:
        :param start_datetime:
        :return:
        """
        try:
            self.account_storage[account_number]["raids"][raid_id]["start_datetime"] = datetime.datetime.strptime(
                start_datetime, "%Y-%m-%d %H:%M:%S")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_raid(self, account_number, raid_id):
        """
        Gathers the information about the raid in an account
        :param account_number:
        :param raid_id:
        :return:
        """
        try:
            return self.account_storage[account_number]["raids"][raid_id]
        except Exception as e:
            logger.error(e)
            return False

    def list_raids(self, account_number):
        """
        Lists the raids for the account
        :param account_number:
        :return:
        """
        try:
            return self.account_storage[account_number]["raids"]
        except Exception as e:
            logger.error(e)
            return False

    def add_user(self, account_number, user_account):
        """
        Add a user to the account
        :param account_number:
        :param user_account:
        :return:
        """
        try:
            self.account_storage[account_number]["users"][user_account] = {"characters": {}}
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_user(self, account_number, user_account):
        """
        Deletes a user from an account
        :param account_number:
        :param user_account:
        :return:
        """
        try:
            del self.account_storage[account_number]["users"][user_account]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_user(self, account_number, user_account):
        """
        Show the information on the users in the account
        :param account_number:
        :param user_account:
        :return:
        """
        try:
            return self.account_storage[account_number]["users"][user_account]
        except Exception as e:
            logger.error(e)
            return False

    def list_user(self, account_number, user_account):
        """
        Lists the users that are attached to the account
        :param account_number:
        :param user_account:
        :return:
        """
        try:
            return self.account_storage[account_number]["users"]
        except Exception as e:
            logger.error(e)
            return False

    def add_character_to_user(self, account_number, user_account, character_name, character_class, character_spec,
                              character_scores):
        """
        Add a character to a user inside of the provided account
        :param account_number:
        :param user_account:
        :param character_name:
        :param character_class:
        :param character_spec:
        :param character_scores:
        :return:
        """
        try:
            self.account_storage[account_number]["users"][user_account]["characters"][character_name] = {
                "class": character_class, "spec": character_spec, "scores": character_scores}
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_character_to_user(self, account_number, user_account, character_name, character_class, character_spec,
                                 character_scores):
        """
        Update the character record inside of the provided account
        :param account_number:
        :param user_account:
        :param character_name:
        :param character_class:
        :param character_spec:
        :param character_scores:
        :return:
        """
        try:
            self.account_storage[account_number]["users"][user_account]["characters"][character_name] = {
                "class": character_class, "spec": character_spec, "scores": character_scores}
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_character_from_user(self, account_number, user_account, character_name):
        """
        Deletes a character from a users account inside of the provided account
        :param account_number:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            del self.account_storage[account_number]["users"][user_account]["characters"][character_name]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_character_to_raid_signup(self, account_number, raid_id, user_account, character_name):
        """
        Adds a character to the raid signup list
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            self.account_storage[account_number]["raids"][raid_id]["signups"].append(
                {"user_account": user_account,
                 "character_name": character_name,
                 "signup_time": datetime.datetime.now()})
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_character_from_raid_signup(self, account_number, raid_id, user_account, character_name):
        """
        Delete character from the raid signup
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            signup_index = [signup["user_account"] == user_account and signup["character_name"] == character_name for
                            signup in self.account_storage[account_number]["raids"][raid_id]["signups"]].index(True)
            del self.account_storage[account_number]["raids"][raid_id]["signups"][signup_index]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_character_in_raid_setup(self, account_number, raid_id, user_account, character_name):
        """
        Update a character from the raid signup based on the user account
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            signup_index = [signup["user_account"] == user_account for signup in
                            self.account_storage[account_number]["raids"][raid_id]["signups"]].index(True)
            self.account_storage[account_number]["raids"][raid_id]["signups"][signup_index][
                "character_name"] = character_name
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_raid_signup(self, account_number, raid_id):
        """
        Return the characters signed up for a raid
        :param account_number:
        :param raid_id:
        :return:
        """
        try:
            return self.account_storage[account_number]["raids"][raid_id]["signups"]
        except Exception as e:
            logger.error(e)
            return False

    def add_raid_roster(self, account_number, raid_id, user_account, character_name):
        """
        Add a user to the raid roster
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            return self.account_storage[account_number]["raids"][raid_id]["roster"]
        except Exception as e:
            logger.error(e)
            return False

    def delete_raid_roster(self, account_number, raid_id, user_account, character_name):
        """
        Add a user to the raid roster
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            roster_index = [roster["user_account"] == user_account for roster in
                            self.account_storage[account_number]["raids"][raid_id]["roster"]].index(True)
            del self.account_storage[account_number]["raids"][raid_id]["roster"][roster_index]
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_raid_roster(self, account_number, raid_id, user_account, character_name):
        """
        Update a raid roster
        :param account_number:
        :param raid_id:
        :param user_account:
        :param character_name:
        :return:
        """
        try:
            roster_index = [roster["user_account"] == user_account for roster in
                            self.account_storage[account_number]["raids"][raid_id]["roster"]].index(True)
            self.account_storage[account_number]["raids"][raid_id]["roster"][roster_index][
                "character_name"] = character_name
            return True
        except Exception as e:
            logger.error(e)
            return False

    def show_raid_roster(self, account_number, raid_id):
        """
        Return the characters signed up for a raid
        :param account_number:
        :param raid_id:
        :return:
        """
        try:
            return self.account_storage[account_number]["raids"][raid_id]["roster"]
        except Exception as e:
            logger.error(e)
            return False
