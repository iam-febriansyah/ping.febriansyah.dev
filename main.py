import subprocess
import aiofiles
import asyncio
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
load_dotenv()

async def ping_ip():
    while True: 
        try:
            async with aiofiles.open("ip.txt", 'r') as file:
                lines = await file.readlines()
            ips = []
            for line in lines:
                ip_address = line.strip()
                output = subprocess.run(
                    ['ping', '-n', '2', ip_address],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                if output.returncode != 0:
                    ips.append(ip_address)
            if len(ips) > 0 :
                send_webhook(ips=ips, title="IP Intermittent", webhook=os.getenv("DISCORD_WEBHOOK"))
        except Exception as e:
            print(f"An error occurred: {e}")
        
def send_webhook(ips : list, title : str, webhook : str):
    desc = ''
    for ip in ips:
        desc += f"{ip}\n"
    webhook = DiscordWebhook(url=webhook)
    embed = DiscordEmbed(title=title, description=desc)
    webhook.add_embed(embed)
    webhook.execute()

asyncio.run(ping_ip())
