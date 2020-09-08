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
        logger.info(self.account_storage)

    def add_account(self, guild_id, requesting_account):
        """
        This will add a new account to the storage system and give it an owner
        :param guild_id:
        :param requesting_account:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id] = {"admins": [requesting_account],
                                          "powerusers": {},
                                          "raids": {},
                                          "users": {}}
        return True

    def delete_account(self, guild_id):
        """
        Delete the storage for an account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        del self.account_storage[guild_id]
        return True

    def show_account(self, guild_id):
        """
        Show information in account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]

    def list_accounts(self):
        """
        Return a list of the accounts
        :return:
        """
        return list(self.account_storage.keys())

    def add_admin(self, guild_id, modify_account):
        """
        Add an admins to the account
        :param guild_id:
        :param modify_account:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["admins"].append(modify_account)
        return True

    def delete_admin(self, guild_id, modify_account):
        """
        Remove an admins from the account
        :param guild_id:
        :param modify_account:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["admins"].delete(modify_account)
        return True

    def show_admin(self, guild_id: str):
        """
        Shows the admin from the account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]["admins"]

    def add_power_user(self, guild_id, modify_account, account_value):
        """
        Add a power user to the account
        :param guild_id:
        :param modify_account:
        :param account_value:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["powerusers"][modify_account] = account_value
        return True

    def delete_power_user(self, guild_id, modify_account):
        """
        Remove a power user from the account
        :param guild_id:
        :param modify_account:
        :return:
        """
        guild_id = str(guild_id)
        del self.account_storage[guild_id]["powerusers"][modify_account]
        return True

    def update_power_user(self, guild_id, modify_account, account_value):
        """
        Update a power user from the account
        :param guild_id:
        :param modify_account:
        :param account_value:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["powerusers"][modify_account] = account_value
        return True

    def show_power_user(self, guild_id):
        """
        Update a power user from the account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]["powerusers"]

    def add_raid(self, guild_id, raid_instance, start_datetime):
        """
        Create a raid that is attached to the account number, with the instance for the raid.
        :param guild_id:
        :param raid_instance:
        :param start_datetime:
        :return:
        """
        guild_id = str(guild_id)
        raid_template = {"raid_instance": raid_instance,
                         "signups": [],  # {"user_id":data,"character_name":data,"signup_time":datetime}
                         "roster": [],  # {user_id":data,"character_name":data,"signup_time":datetime}
                         "start_datetime": datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")}
        raid_id = len(self.account_storage[guild_id]["raids"]) + 1000
        self.account_storage[guild_id]["raids"][raid_id] = raid_template
        return raid_id

    def delete_raid(self, guild_id, raid_id):
        """
        Delete a raid
        :param guild_id:
        :param raid_id:
        :return:
        """
        guild_id = str(guild_id)
        del self.account_storage[guild_id]["raids"][raid_id]
        return True

    def update_raid(self, guild_id, raid_id, start_datetime):
        """
        Update the Raid's start time
        :param guild_id:
        :param raid_id:
        :param start_datetime:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["raids"][raid_id]["start_datetime"] = datetime.datetime.strptime(
            start_datetime, "%Y-%m-%d %H:%M:%S")
        return True

    def show_raid(self, guild_id, raid_id):
        """
        Gathers the information about the raid in an account
        :param guild_id:
        :param raid_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]["raids"][raid_id]

    def list_raids(self, guild_id):
        """
        Lists the raids for the account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]["raids"]

    def add_user(self, guild_id, user_id):
        """
        Add a user to the account
        :param guild_id:
        :param user_id:
        :return:
        """
        guild_id = str(guild_id)
        self.account_storage[guild_id]["users"][user_id] = {"characters": {}}
        return True

    def delete_user(self, guild_id, user_id):
        """
        Deletes a user from an account
        :param guild_id:
        :param user_id:
        :return:
        """
        guild_id = str(guild_id)
        del self.account_storage[guild_id]["users"][user_id]
        return True

    def show_user(self, guild_id, user_id):
        """
        Show the information on the users in the account
        :param guild_id:
        :param user_id:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        return self.account_storage[guild_id]["users"][user_id]

    def list_user(self, guild_id):
        """
        Lists the users that are attached to the account
        :param guild_id:
        :return:
        """
        guild_id = str(guild_id)
        return self.account_storage[guild_id]["users"]

    def add_character_to_user(self, guild_id, user_id, character_name, character_class, character_spec,
                              character_ratings):
        """
        Add a character to a user inside of the provided account
        :param guild_id:
        :param user_id:
        :param character_name:
        :param character_class:
        :param character_spec:
        :param character_ratings:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        self.account_storage[guild_id]["users"][user_id]["characters"].append({"name": character_name,
                                                                               "class": character_class,
                                                                               "spec": character_spec,
                                                                               "ratings": character_ratings})
        return True

    def delete_character_from_user(self, guild_id, user_id, character_name, character_class, character_spec):
        """
        Deletes a character from a users account inside of the provided account
        :param guild_id:
        :param user_id:
        :param character_name:
        :param character_class:
        :param character_spec:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        matching_character = [character for character in self.account_storage[guild_id]["users"][user_id]["characters"]
                              if
                              character["name"] == character_name and character["class"] == character_class and
                              character[
                                  "spec"] == character_spec]
        if matching_character:
            character_index = self.account_storage[guild_id]["users"][user_id]["characters"].index(
                matching_character[0])
            del self.account_storage[guild_id]["users"][user_id]["characters"][character_index]
            return True
        else:
            return False

    def add_character_to_raid_signup(self, guild_id, raid_id, user_id, character_name):
        """
        Adds a character to the raid signup list
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        self.account_storage[guild_id]["raids"][raid_id]["signups"].append(
            {"user_id": user_id,
             "character_name": character_name,
             "signup_time": datetime.datetime.now()})
        return True

    def delete_character_from_raid_signup(self, guild_id, raid_id, user_id, character_name):
        """
        Delete character from the raid signup
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        signup_index = [signup["user_id"] == user_id and signup["character_name"] == character_name for
                        signup in self.account_storage[guild_id]["raids"][raid_id]["signups"]].index(True)
        del self.account_storage[guild_id]["raids"][raid_id]["signups"][signup_index]
        return True

    def update_character_in_raid_setup(self, guild_id, raid_id, user_id, character_name):
        """
        Update a character from the raid signup based on the user account
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        signup_index = [signup["user_id"] == user_id for signup in
                        self.account_storage[guild_id]["raids"][raid_id]["signups"]].index(True)
        self.account_storage[guild_id]["raids"][raid_id]["signups"][signup_index]["character_name"] = character_name
        return True

    def show_raid_signup(self, guild_id, raid_id):
        """
        Return the characters signed up for a raid
        :param guild_id:
        :param raid_id:
        :return:
        """
        guild_id = str(guild_id)
        raid_id = str(raid_id)
        return self.account_storage[guild_id]["raids"][raid_id]["signups"]

    def add_raid_roster(self, guild_id, raid_id, user_id, character_name):
        """
        Add a user to the raid roster
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        raid_id = str(raid_id)
        return self.account_storage[guild_id]["raids"][raid_id]["roster"]

    def delete_raid_roster(self, guild_id, raid_id, user_id, character_name):
        """
        Add a user to the raid roster
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        raid_id = str(raid_id)
        roster_index = [roster["user_id"] == user_id for roster in
                        self.account_storage[guild_id]["raids"][raid_id]["roster"]].index(True)
        del self.account_storage[guild_id]["raids"][raid_id]["roster"][roster_index]
        return True

    def update_raid_roster(self, guild_id, raid_id, user_id, character_name):
        """
        Update a raid roster
        :param guild_id:
        :param raid_id:
        :param user_id:
        :param character_name:
        :return:
        """
        guild_id = str(guild_id)
        user_id = str(user_id)
        raid_id = str(raid_id)
        roster_index = [roster["user_id"] == user_id for roster in
                        self.account_storage[guild_id]["raids"][raid_id]["roster"]].index(True)
        self.account_storage[guild_id]["raids"][raid_id]["roster"][roster_index]["character_name"] = character_name
        return True

    def show_raid_roster(self, guild_id, raid_id):
        """
        Return the characters signed up for a raid
        :param guild_id:
        :param raid_id:
        :return:
        """
        guild_id = str(guild_id)
        raid_id = str(raid_id)
        return self.account_storage[guild_id]["raids"][raid_id]["roster"]
