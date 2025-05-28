# Discord Wake-on-LAN Bot

A Discord bot that first developed as WoL client for my home pc and later expanded to include remote shutdown capabilities, GitHub PR listing, and Discord Active Developer Badge information. This bot allows you to wake your PC remotely, shut it down safely, and manage your GitHub pull requests directly from Discord.

## Features

- **Wake-on-LAN**: Send magic packets to wake your PC remotely
- **Remote Shutdown**: Safely shut down your PC via SSH connection
- **GitHub PR Listing**: View your open GitHub pull requests directly in Discord
- **Discord Active Developer Badge Info**: Command to help users claim their Active Developer Badge

## Requirements

- Python 3.8+
- Discord bot token
- Network with Wake-on-LAN support
- SSH access to target PC for shutdown capability
- GitHub token (optional, for PR listing feature)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/discord-wol-bot.git
   cd discord-wol-bot
   ```

2. Install required dependencies:
   ```bash
   pip install python-dotenv discord.py wakeonlan paramiko requests
   ```

3. Create a `.env` file with your configuration:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   DISCORD_CHANNEL_ID=your_channel_id
   
   TARGET_MAC=your_pc_mac_address
   
   SSH_HOST=your_pc_ip_address
   SSH_USER=your_username
   SSH_PASSWORD=your_password
   
   # Optional for GitHub integration
   GITHUB_TOKEN=your_github_token
   GITHUB_USER=your_github_username
   ```

## Usage

1. Start the bot:
   ```bash
   python discordwol.py
   ```

2. Use the following slash commands in your Discord server:
   - `/wake` - Sends a magic packet to wake your PC
   - `/shutdown` - Shuts down your PC via SSH
   - `/prs [repo]` - Lists your open GitHub PRs (optionally in a specific repo)
   - `/activedevbadge` - Shows information about the Discord Active Developer Badge

## Security Considerations

- The bot only responds to commands in the designated channel specified in `.env`
- Consider using SSH keys instead of passwords for more secure authentication
- Restrict the bot's permissions in your Discord server

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)