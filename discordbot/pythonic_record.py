import datetime
from loguru import logger


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

    def add_account(self, account_number, requesting_account):
        """
        This will add a new account to the storage system and give it an owner
        :param account_number:
        :param owner_information:
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

    def add_owner_account(self, account_number, modify_account):
        """
        Add an owner to the account
        :param account_number:
        :param modifying_account:
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
        :param modifying_account:
        :return:
        """
        try:
            self.account_storage[account_number]["admins"].remove(modify_account)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_power_user_account(self, account_number, modify_account, account_value):
        """
        Add a power user to the account
        :param account_number:
        :param modifying_account:
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
        :param modifying_account:
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
        :param modifying_account:
        :param account_value:
        :return:
        """
        try:
            self.account_storage[account_number]["powerusers"][modify_account] = account_value
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_raid(self, account_number, raid_instance, start_datetime):
        """
        Create a raid that is attached to the account number, with the instance for the raid.
        :param account_number:
        :param instance:
        :return:
        """
        raid_template = {"raid_instance": raid_instance,
                         "signup_queue": [],
                         "approved_list": [],
                         "start_datetime": datetime.datetime.strptime(start_datetime,"%Y-%m-%d %H:%M:%S")}

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
            self.account_storage[account_number]["raids"][raid_id]["start_datetime"] = datetime.datetime.strptime(start_datetime,"%Y-%m-%d %H:%M:%S")
            return True
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
            self.account_storage[account_number]["users"][user_account] = {"characters":{}}
            return True
        except Exception as e:
            return False