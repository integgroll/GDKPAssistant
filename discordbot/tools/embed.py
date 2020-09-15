import discord
import datetime


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

    embed.add_field(name="🤔", value=f"ICO {len(signups)}", inline=True)
    embed.add_field(name="😱", value=f"ICO {datetime_handle.strftime('%m-%d-%Y')}", inline=True)
    embed.add_field(name="🙄", value=f"ICO {datetime_handle.strftime('%H:%M')} GMT -7", inline=True)

    embed.add_field(name="🤔", value="ICO _Melee_ ## ICO", inline=True)
    embed.add_field(name="😱", value="ICO _Ranged_ ## ICO", inline=True)
    embed.add_field(name="🙄", value="ICO _Heals_ ## ICO", inline=True)

    for role in ["Tank", "Hunter", "Priest", "Warrior", "Mage", "Paladin", "Rogue", "Warlock", "Druid"]:
        embed.add_field(name="🤔", value=f"ICO*_{role}_* ({len(signups_by_class[role])})\n{output_strings[role]}",
                        inline=True)
    return embed
