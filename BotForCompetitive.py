import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

ListBratMaps = ["de_inferno_2x2", "de_dust2_2x2", "de_dust"]
ListMMMaps = ["de_inferno", "de_dust2", "cs_estate", "de_prodigy", "de_nuke"]
ListMM = []
ListBrat = []
ListForNameAndPassword = []

ListForNameAndPassword.extend([chr(x) for x in range(ord('a'), ord('z')+1)])
ListForNameAndPassword.extend([chr(x) for x in range(ord('A'), ord('Z')+1)])

@bot.command()
async def start(ctx, *args):
    await ctx.send("Выберите режим.", view=ChooseGameMode())

@bot.command()
async def start_wingman(interaction, *args):
    if interaction.user.id in ListBrat:
        await interaction.response.send_message("Вы уже в поиске")
    else:
        ListBrat.append(interaction.user.id)

    if len(ListBrat) != 4:
        await interaction.response.send_message("В поиске " + str(len(ListBrat)) + " из 4", view=CancelFindMatchWingman())
    else:
        map = random.randint(0, (len(ListBratMaps) - 1))
        host: int = random.randint(0, (len(ListBrat) - 1))
        await interaction.response.send_message("Игра найдена! Игроки в матче:\n 1. <@" + str(ListBrat[0]) +  ">\n2. <@" + str(ListBrat[2]) + ">\n## VS \n1. <@" + str(ListBrat[1]) + ">\n2. <@" + str(ListBrat[3]) + ">\n\nHOST: <@" + str(ListBrat[host]) +"> \nMAP: " + str(ListBratMaps[map]))
        channel = await bot.fetch_user(ListBrat[host])
        NameLobby = "CSO2 #"
        Password = ""
        for i in range(10):
            c = random.randint(0, (len(ListForNameAndPassword) - 1))
            NameLobby += ListForNameAndPassword[c]
        for n in range(7):
            c = random.randint(0, (len(ListForNameAndPassword) - 1))
            Password += ListForNameAndPassword[c]

        await channel.send("ВЫ ХОСТ!\n 1. Сделайте комнату с режимом Competitive на 9 раундов c картой " + str(ListBratMaps[map]) +"\n2. Сделайте название комнаты ||" + NameLobby + "||\n3. Поставьте пароль ||" + Password + "||")
        for b in range(len(ListBrat)):
            if ListBrat[b] != ListBrat[host]:
                user = await bot.fetch_user(ListBrat[b])
                await user.send("Название комнаты: ||" + NameLobby + "||\nПароль: ||" + Password + "||")

        ListBrat.clear()

@bot.command()
async def start_competitive(interaction, *args):
    if interaction.user.id in ListMM:
        await interaction.response.send_message("Вы уже в поиске")
    else:
        ListMM.append(interaction.user.id)

    if len(ListMM) != 10:
        await interaction.response.send_message("В поиске " + str(len(ListMM)) + " из 10", view=CancelFindMatchCompetitve())
    else:
        map = random.randint(0, (len(ListMMMaps) - 1))
        host: int = random.randint(0, (len(ListMM) - 1))
        await interaction.response.send_message("Игра найдена! Игроки в матче:\n 1. <@" + str(ListMM[0]) +  ">\n2. <@" + str(ListMM[2]) + ">\n3. <@" + str(ListMM[4]) + ">\n4. <@"  + str(ListMM[6]) + ">\n5. <@" + str(ListMM[8]) + ">\n## VS\n1. <@" + str(ListMM[1]) + ">\n2. <@" + str(ListMM[3]) + ">\n3. <@" + str(ListMM[5]) + ">\n4. <@" + str(ListMM[7]) + ">\n5. <@" + str(ListMM[9]) + ">\n\nHOST: <@" + str(ListMM[host]) +"> \nMAP: " + str(ListMMMaps[map]))
        channel = await bot.fetch_user(ListMM[host])
        NameLobby = "CSO2 #"
        Password = ""
        for i in range(10):
            c = random.randint(0, (len(ListForNameAndPassword) - 1))
            NameLobby += ListForNameAndPassword[c]
        for n in range(7):
            c = random.randint(0, (len(ListForNameAndPassword) - 1))
            Password += ListForNameAndPassword[c]

        await channel.send("ВЫ ХОСТ!\n1. Сделайте комнату с режимом Competitive на 16 раундов c картой " + str(ListMMMaps[map]) +"\n2. Сделайте название комнаты ||" + NameLobby + "||\n3. Поставьте пароль ||" + Password + "||")
        for b in range(len(ListMM)):
            if ListMM[b] != ListMM[host]:
                user = await bot.fetch_user(ListMM[b])
                await user.send("Название комнаты: ||" + NameLobby + "||\nПароль: ||" + Password + "||")

        ListMM.clear()


class CancelFindMatchWingman(discord.ui.View):
    @discord.ui.button(label="Выйти из поиска", style=discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, button):
        if interaction.user.id in ListBrat:
            ListBrat.remove(interaction.user.id)
            await interaction.response.send_message("Вы вышли из поиска матча")
        else:
            await interaction.response.send_message("Вы не начали поиск матча")


class CancelFindMatchCompetitve(discord.ui.View):
    @discord.ui.button(label="Выйти из поиска", style=discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, button):
        if interaction.user.id in ListMM:
            ListMM.remove(interaction.user.id)
            await interaction.response.send_message("Вы вышли из поиска матча")
        else:
            await interaction.response.send_message("Вы не начали поиск матча")

class ChooseGameMode(discord.ui.View):
    @discord.ui.button(label="Wingman", style=discord.ButtonStyle.primary)
    async def buttonWingman_callback(self, interaction: discord.Interaction, button):
        await start_wingman(interaction)
    @discord.ui.button(label="Competitive", style=discord.ButtonStyle.primary)
    async def buttonCompetitive_callback(self, interaction: discord.Interaction, button):
        await start_competitive(interaction)

bot.run("put your bot token")