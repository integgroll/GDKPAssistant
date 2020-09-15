import discord
import datetime
from loguru import logger


def generate_embed(raid_id, raid_instance, start_datetime, signups=[]):
    """
    Generate the embed for the raid message, before all those lovely emotes and all.
    :param raid_handle:
    :return:
    """

    datetime_handle = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")

    # Signup Data Structure
    # {"user_id":data,"character_name":data, "character_class":data, "character_role",:data, "total_funds": int, "min_bids":[],"signup_time":datetime}
    signups_by_class = {"Tank": [], "Hunter": [], "Priest": [], "Warrior": [], "Mage": [], "Paladin": [], "Rogue": [],
                        "Warlock": [], "Druid": []}
    role_count = {"melee": 0, "ranged": 0, "heals": 0}
    # Sort the signups by their signup time
    signups.sort(key=lambda s: s.get('signup_time'))
    signup_order = 0
    for signup in signups:
        signup_order += 1
        if signup['character_role'] == 'tank':
            signups_by_class["Tank"].append(f"_{signup_order}_ {signup['character_name']}")
        else:
            role_count[signup['character_role']] += 1
            signups_by_class[signup['character_class']].append(f"_{signup_order}_ {signup['character_name']}")

    output_strings = dict([(key, '\n'.join(signups)) for key, signups in signups_by_class.items()])

    embed = discord.Embed(colour=discord.Colour(0x252325), url="https://discordapp.com")

    embed.set_author(name="GDKP Assistant", url="https://discordapp.com",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name=f"ICO {len(signups)}", value=f"ICO _Melee_ {role_count['melee']} ICO", inline=True)
    embed.add_field(name=f"ICO {datetime_handle.strftime('%m-%d-%Y')}",
                    value=f"ICO _Ranged_ {role_count['ranged']} ICO", inline=True)
    embed.add_field(name=f"ICO {datetime_handle.strftime('%H:%M')} GMT -7",
                    value=f"ICO _Heals_ {role_count['heals']} ICO", inline=True)

    for role in ["Tank", "Hunter", "Priest", "Warrior", "Mage", "Paladin", "Rogue", "Warlock", "Druid"]:
        logger.info(output_strings[role])
        embed.add_field(name=f"ICO {role} {len(signups_by_class[role])}", value=f"{output_strings[role] or 'none'}",
                        inline=True)
    return embed
