import os
import discord

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Token não encontrado no arquivo .env")


intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# COLOQUE AQUI O ID DO CANAL DE DIVULGAÇÃO
CANAL_TIKTOK_ID = 1514836009785884773


class BotaoTikTok(discord.ui.View):
    def __init__(self, link):
        super().__init__(timeout=None)

        botao = discord.ui.Button(
            label="Assistir no TikTok",
            emoji="🎵",
            style=discord.ButtonStyle.link,
            url=link
        )

        self.add_item(botao)


@bot.event
async def on_ready():
    try:
        comandos = await bot.tree.sync()

        print("--------------------------------")
        print(f"Bot conectado como: {bot.user}")
        print(f"Comandos carregados: {len(comandos)}")
        print("--------------------------------")

    except Exception as erro:
        print(f"Erro ao carregar os comandos: {erro}")


@bot.tree.command(
    name="tiktok",
    description="Divulga um vídeo novo do TikTok"
)
@app_commands.describe(
    link="Cole o link do vídeo do TikTok",
    descricao="Escreva uma descrição para o vídeo"
)
async def tiktok(
    interaction: discord.Interaction,
    link: str,
    descricao: str = "Vídeo novo disponível!"
):
    if "tiktok.com" not in link.lower():
        await interaction.response.send_message(
            "❌ Esse link não parece ser do TikTok.",
            ephemeral=True
        )
        return

    canal = bot.get_channel(CANAL_TIKTOK_ID)

    if canal is None:
        await interaction.response.send_message(
            "❌ Não encontrei o canal. Confira o ID configurado.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🎬 VÍDEO NOVO NO TIKTOK!",
        description=(
            f"{descricao}\n\n"
            "❤️ Deixe seu like\n"
            "💬 Comente no vídeo\n"
            "🔄 Compartilhe com seus amigos"
        ),
        color=discord.Color.from_rgb(0, 0, 0)
    )

    embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url
    )

    embed.set_footer(
        text="Obrigado pelo apoio! ⭐"
    )

    await canal.send(
        content=link,
        embed=embed,
        view=BotaoTikTok(link)
    )

    await interaction.response.send_message(
        f"✅ Vídeo enviado em {canal.mention}.",
        ephemeral=True
    )


bot.run(TOKEN)