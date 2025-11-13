import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1437560433551872112  # 🧠 Remplace par l’ID du canal cible
TIMEZONE = "Europe/Paris"  # Ton fuseau horaire
MESSAGE = "@everyone Voc aujourd'hui ? 👍 si présent, 👎 sinon"

# Initialisation du bot
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

# Planificateur de tâches
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

    # Démarrage du planificateur
    scheduler.start()
    print("🕓 Planificateur activé")

    # Planifie l’envoi du message chaque semaine
    scheduler.add_job(send_weekly_message, "cron", day_of_week="thu", hour=19, minute=5)
    print("📅 Tâche planifiée pour chaque vendredi à 9h00")

async def send_weekly_message():
    """Envoie le message et ajoute les réactions 👍👎"""
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = await channel.send(MESSAGE)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        print(f"✅ Message envoyé dans #{channel.name} ({datetime.now(pytz.timezone(TIMEZONE))})")
    else:
        print("❌ Canal introuvable ! Vérifie l’ID du canal.")

bot.run(TOKEN)
