import os
import discord
import psutil
import time
import winsound
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} içeri intikal etti ve sistemi izlemeye hazır!')

@bot.command(name="cpu")
async def cpu_durumu(ctx):
    mesaj = await ctx.send("10 saniyelik işlemci izleme sürece koyuldu!!")
    islemci_yuku = psutil.cpu_percent(interval=10)
    mantiksal = psutil.cpu_count(logical=True)
    fiziksel = psutil.cpu_count(logical=False)

    rapor = (
        f" **10 Saniyelik CPU Raporu**\n"
        f"• **Ortalama İşlemci Yükü:** %{islemci_yuku}\n"
        f"• **Çekirdek Bilgisi:** {fiziksel} Fiziksel / {mantiksal} Mantıksal"
    )
    await mesaj.edit(content=rapor)

@bot.command(name="ram")
async def ram_durumu(ctx):
    mesaj = await ctx.send("10 saniyelik ram dikizleme işlemi başlatılmıştır 0<0")

    toplam_yuzde = 0
    olcumsayisi = 5  
    yuksek_kullanim_tespit_edildi = False
    
    for _ in range(olcumsayisi):
        bellek = psutil.virtual_memory()
        ram_orani = bellek.percent
        toplam_yuzde += ram_orani
        
        if ram_orani > 60:
            yuksek_kullanim_tespit_edildi = True
            try:
                winsound.Beep(1000, 1000)
            except RuntimeError:
                pass
                
        time.sleep(2) 
        
    ortalama_ram = toplam_yuzde / olcumsayisi
    bellek_bilgi = psutil.virtual_memory()
    toplam_gb = bellek_bilgi.total / (1024 ** 3)
    kullanilan_gb = bellek_bilgi.used / (1024 ** 3)

    rapor = (
        f" **10 Saniyelik RAM Raporu**\n"
        f"• **10 Saniyelik Ortalama Kullanım:** %{ortalama_ram:.2f}\n"
        f"• **Anlık Kullanılan RAM:** {kullanilan_gb:.2f} GB / {toplam_gb:.2f} GB\n"
    )
    if yuksek_kullanim_tespit_edildi:
        rapor += "\n *Uyarı: Test sırasında RAM kullanımı %60 sınırını aştı!*"
        
    await mesaj.edit(content=rapor)

@bot.command(name="disk")
async def disk_durumu(ctx):
    mesaj = await ctx.send("10 saniyelik disk yan gözle kesme başladı!! 00__00")

    toplam_disk_yuzdesi = 0
    for i in range(5):
        disk = psutil.disk_usage("/")
        toplam_disk_yuzdesi += disk.percent
        time.sleep(2)

    ortalama_disk = toplam_disk_yuzdesi / 5
    disk_son = psutil.disk_usage('/')
    toplam_disk_gb = disk_son.total / (1024 ** 3)
    kullanilan_disk_gb = disk_son.used / (1024 ** 3)

    rapor = (
        f" **Disk Durum Raporu**\n"
        f"• **Toplam Disk Alanı:** {toplam_disk_gb:.2f} GB\n"
        f"• **Kullanılan Alan:** {kullanilan_disk_gb:.2f} GB\n"
        f"• **Disk Doluluk Oranı:** %{disk_son.percent} (10 sn test ortalaması: %{ortalama_disk:.2f})"
    )
    await mesaj.edit(content=rapor)

bot.run(TOKEN)