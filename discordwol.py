import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from wakeonlan import send_magic_packet
import paramiko
import requests

# Load environment variables
load_dotenv()

# Config from .env
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")

TARGET_MAC = os.getenv("TARGET_MAC")

SSH_HOST = os.getenv("SSH_HOST")
SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')
    try:
        await bot.tree.sync()
        print("🎉 Slash commands synced globally!")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

@bot.tree.command(name="wake", description="Sends a magic packet to wake your PC.")
async def wake_pc(interaction: discord.Interaction):
    if interaction.channel_id == CHANNEL_ID:
        send_magic_packet(TARGET_MAC)
        await interaction.response.send_message('📡 Magic packet sent to wake your PC!')
    else:
        await interaction.response.send_message('❌ This command can only be used in the designated channel.', ephemeral=True)

@bot.tree.command(name="shutdown", description="Sends a shutdown command to your PC via SSH.")
async def shutdown_pc(interaction: discord.Interaction):
    if interaction.channel_id == CHANNEL_ID:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
            stdin, stdout, stderr = ssh_client.exec_command('sudo shutdown -h now')
            error_output = stderr.read().decode()
            if error_output:
                await interaction.response.send_message(f'⚠️ Error: {error_output}', ephemeral=True)
            else:
                await interaction.response.send_message('✅ Shutdown command sent.')
            ssh_client.close()
        except Exception as e:
            await interaction.response.send_message(f'❌ SSH error: {e}', ephemeral=True)
    else:
        await interaction.response.send_message('❌ This command can only be used in the designated channel.', ephemeral=True)

@bot.tree.command(name="status", description="Check if your PC is online and get uptime.")
async def status_pc(interaction: discord.Interaction):
    if interaction.channel_id == CHANNEL_ID:
        await interaction.response.defer()
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
            stdin, stdout, stderr = ssh_client.exec_command("uptime -p")
            error_output = stderr.read().decode().strip()
            output = stdout.read().decode().strip()
            ssh_client.close()

            if error_output:
                await interaction.followup.send(f"⚠️ Error fetching uptime: {error_output}")
            else:
                await interaction.followup.send(f"🖥️ PC Uptime: {output}")
        except Exception as e:
            await interaction.followup.send(f"❌ SSH error or PC offline: {e}")
    else:
        await interaction.response.send_message('❌ This command can only be used in the designated channel.', ephemeral=True)

@bot.tree.command(name="restart", description="Restart your PC via SSH.")
async def restart_pc(interaction: discord.Interaction):
    if interaction.channel_id == CHANNEL_ID:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)
            stdin, stdout, stderr = ssh_client.exec_command('sudo reboot')
            error_output = stderr.read().decode()
            if error_output:
                await interaction.response.send_message(f'⚠️ Error: {error_output}', ephemeral=True)
            else:
                await interaction.response.send_message('🔄 Restart command sent.')
            ssh_client.close()
        except Exception as e:
            await interaction.response.send_message(f'❌ SSH error: {e}', ephemeral=True)
    else:
        await interaction.response.send_message('❌ This command can only be used in the designated channel.', ephemeral=True)

@bot.tree.command(name="activedevbadge", description="Info on the Discord Active Developer Badge.")
async def activedevbadge(interaction: discord.Interaction):
    await interaction.response.send_message(
        "✨ You've run an application command! "
        "Check https://discord.com/developers/active-developer in 24h to claim the badge. "
        "Ensure your server is a Community Server and data-sharing is enabled."
    )

@bot.tree.command(name="prs", description="List your open GitHub PRs. Optionally specify a repo.")
async def prs(interaction: discord.Interaction, repo: str = None):
    if interaction.channel_id != CHANNEL_ID:
        await interaction.response.send_message("❌ This command can only be used in the designated channel.", ephemeral=True)
        return
    await interaction.response.defer()
    pr_list = get_github_prs(repo)
    formatted = "\n".join(pr_list)
    await interaction.followup.send(f"📦 **Open PRs{' in ' + repo if repo else ''}:**\n{formatted}")

def get_github_prs(repo=None):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    if repo:
        url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/pulls"
    else:
        url = f"https://api.github.com/search/issues?q=is:pr+author:{GITHUB_USER}+is:open"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return [f"❌ GitHub API error: {response.status_code} - {response.text}"]

    data = response.json()
    items = data if repo else data.get("items", [])
    if not items:
        return ["✅ No open PRs found."]
    return [f"[{pr['title']}]({pr['html_url']})" for pr in items]

# Run the bot
bot.run(TOKEN)
