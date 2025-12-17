import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
from discord.ui import Button, View
import json

#I AM NOT GOOD AT CODING, THIS WAS DONE WITH HELP AND IS STILL A WORK IN PROGRESS, if you have suggestions hmu on discord @fynninyoass

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

#Embed Links
embed = discord.Embed(
    title="OST Study Information",
    description="Important links and resources for your studies at OST",
    color=discord.Color.purple()
)
embed.add_field(
    name="Main Platform",
    value="[LOST.University](https://lost.university)\n Plan your Semester",
    inline=False
)
embed.add_field(
    name="Unterricht",
    value="[Unterricht](https://unterricht.ost.ch)\nAdministrative matters, grades, and timetables",
    inline=False
)
embed.add_field(
    name="Studentenportal",
    value="[Studentenportal.ch](https://studentenportal.ch/)\nAlte Prüfungen, zusammenfassungen, Dozentenbewertungen, Events und mehr.",
    inline=False
)
embed.add_field(
    name="Bibliothek",
    value="[Bibliothek](https://www.ost.ch/de/die-ost/bibliothek)\nAlle informationen zur Bibliothek, besonders hilfrech ist Swisscovery und book a librarian.",
    inline=False
)
embed.add_field(
    name="Sportangebote",
    value="[Sports](https://www.ost.ch/de/die-ost/services/sport-an-der-ost)\nAlle Sportangebote der OST",
    inline=False
)
embed.add_field(
    name="OST ICT-Wiki",
    value="[ICT-Wiki](https://wiki.ost.ch/pages/releaseview.action?spaceKey=IOW&title=OST+ICT+Wiki)\nAlle informationen zur OST IT infrastruktur",
    inline=False
)
embed.add_field(
    name="Wohnungsbörse",
    value="[Wohnungsbörse](https://www.ost.ch/de/die-ost/campus/campus-rapperswil-jona/wohnen/wohnungsboerse)",
    inline=False
)
embed.set_footer(text="OST Bot • Your study assistant")
        
#Embed_anleitung
embed_anleitung = discord.Embed(
    title="Schritt-für-Schritt: Modulanmeldung an der OST",
    description="Ein vollständiger Leitfaden.",
    color=discord.Color.purple()
)
embed_anleitung.add_field(
    name="**Schritt 1: Module auswählen**",
    value=(
        "1. Gehe zur **Modulanmeldung**:\n"
        "   Next Semester --> Module --> An/Abmelden\n\n"
        "2. Wähle die Module aus, die du belegen möchtest. Orientiere dich dabei an:\n"
        "   • Dem **Musterstundenplan** für deinen Studiengang:\n"
        "     Nächstes Semester --> Stundenplan --> Musterstundenplan erstellen\n\n"
        "     *IV steht für Informatik Vollzeit, IT für Informatik Teilzeit, usw.*\n\n"
        "**Tipp:** Überprüfe die Voraussetzungen für jedes Modul auf LOST."
    ),
    inline=False
)

embed_anleitung.add_field(
    name="**Schritt 2: Stundenplan erstellen (2. Anmeldephase)**",
    value=(
        "1. Sobald die **zweite Anmeldephase** startet, gehe direkt zu:\n"
        "   Next Semester --> Stundenplan --> Erstellen\n\n"
        "2. Erstelle deinen persönlichen Stundenplan **SO SCHNELL WIE MÖGLICH**.\n"
        "3. Nutze den **Musterstundenplan aus Schritt 1** als Referenz, um Konflikte zu vermeiden.\n\n"
        "**Wichtiger Hinweis:** Viele Kurse haben begrenzte Platzzahlen."
    ),
    inline=False
)

embed_anleitung.set_footer(
    text="Diese Anleitung dient nur der Information. Verbindliche Regelungen findest du in den offiziellen OST Dokumenten."
)

def load_module_data():
    with open('data/modules.json', 'r', encoding='utf-8') as f:
        modules = json.load(f)
    with open('data21/categories.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)
    with open('data21/focuses.json', 'r', encoding='utf-8') as f:
        focuses = json.load(f)
    return modules, categories, focuses

all_modules, all_categories, all_focuses = load_module_data()

class FAQView(View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="Modulanmeldung", style=discord.ButtonStyle.primary)
    async def module_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(embeds=[embed_anleitung], ephemeral=True)
    
    @discord.ui.button(label="Wichtige Links", style=discord.ButtonStyle.primary)
    async def schedule_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(embeds=[embed], ephemeral=True)

@bot.tree.command(name="faq")
async def faq(interaction: discord.Interaction):
    embed = discord.Embed(title="Häufige Fragen (FAQ)", description="Wähle ein Thema:", color=0x7289DA)
    await interaction.response.send_message(embed=embed, view=FAQView(), ephemeral=True)

@bot.tree.command(name="modul_suche", description="Suche nach einem Modul")
@app_commands.describe(modulname="Name oder Kürzel des Moduls")
async def modul_suche(interaction: discord.Interaction, modulname: str):
    modulname_lower = modulname.lower()
    results = []
    
    for module in all_modules:
        if (modulname_lower in module['name'].lower() or 
            modulname_lower in module['id'].lower() or
            modulname_lower in module.get('kuerzel', '').lower()):
            results.append(module)
    
    module = results[0]
    
    embed = discord.Embed(
        title=f"{module['name']} ({module['id']})",
        description=module.get('description'),
        color=discord.Color.blue(),
        url=f"https://studien.ost.ch/{module.get('url', '')}"
    )
    embed.add_field(name="ECTS", value=str(module['ects']), inline=True)
    embed.add_field(name="Semester", value=module['term'], inline=True)
    embed.add_field(name="Voraussetzung", value=module['predecessorModuleId'], inline=True)
    embed.add_field(name="Folgemodul", value=module['successorModuleId'], inline=True)
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="quote", description="Zitiere einen Prof")
@app_commands.describe(
    quote="The quote text",
    professor="Professor's name",
    course="Related course (optional)",
)
async def professor_quote(
    interaction: discord.Interaction,
    quote: str,
    professor: str,
    course: str = None,
):
    embed = discord.Embed(
    title="💬 Professor's Wisdom",
    description=f"\"{quote}\"",
    color=discord.Color.dark_blue(),
    timestamp=datetime.datetime.now()
    )

    zitat_channel = bot.get_channel(1450446958257897555)
    
    if course:
        embed.add_field(name="Course", value=course, inline=True)

        message_content = f"**The Professor said!**"
        message_content += f"\nProfessor **{professor}**"
        await zitat_channel.send(content=message_content, embed=embed)    
    
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

bot.run(DISCORD_TOKEN)