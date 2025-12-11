import requests
import json
import os
import re
import time
from urllib.parse import quote, unquote

# Internationalization Dictionary
LANG = {
    'es': {
        "choose_lang": "Selecciona idioma:",
        "creds_method": "\n[?] ¿Como deseas ingresar las credenciales de Flickr?",
        "manual": "1. Manualmente (Copiar y pegar)",
        "file": "2. Desde archivo (ej: keys.txt)",
        "select_option": "\nSelecciona una opcion (1/2): ",
        "enter_api_key": "Ingresa api_key: ",
        "enter_auth_hash": "Ingresa auth_hash: ",
        "enter_secret": "Ingresa secret: ",
        "enter_file_path": "Ingresa la ruta del archivo (ej: keys.txt): ",
        "file_not_exist": "[!] El archivo {} no existe.",
        "invalid_format": "[!] Formato de archivo invalido. Debe contener api_key=..., auth_hash=... y secret=...",
        "error_reading": "[!] Error leyendo archivo: {}",
        "invalid_option": "[!] Opcion invalida.",
        "enter_email": "[?] Ingresa el email del objetivo: ",
        "starting_search": "\n[*] Iniciando busqueda para: {}",
        "search_error": "[!] Error en busqueda HTTP: {}",
        "jsonp_error": "[!] No se pudo parsear la respuesta JSONP de Flickr.",
        "user_not_found": "[-] Usuario NO encontrado en Flickr.",
        "user_found": "\n[+] Usuario ENCONTRADO! Recopilando informacion completa...",
        "error_user_details": "[!] Error obteniendo detalles del usuario.",
        "profile_info_header": "\n=== INFORMACION DEL PERFIL ===",
        "real_name": "Nombre Real",
        "username": "Nombre de Usuario",
        "nsid": "NSID",
        "dbid": "DBID",
        "date_create": "Fecha Creacion",
        "is_pro": "Es Pro",
        "is_deleted": "Esta Borrado",
        "is_ad_free": "Sin Anuncios",
        "path_alias": "Alias de Ruta",
        "location": "Ubicacion",
        "description": "Descripcion",
        "urls_header": "\n--- URLs ---",
        "profile_url": "URL Perfil",
        "photos_url": "URL Fotos",
        "mobile_url": "URL Movil",
        "stats_header": "\n--- ESTADISTICAS ---",
        "photos_count": "Cantidad de Fotos",
        "has_stats": "Tiene Estadisticas",
        "extras_header": "\n--- EXTRAS ---",
        "gift_eligible": "Elegible para Regalo",
        "media_header": "\n--- MEDIA ---",
        "profile_pic_url": "URL Foto Perfil",
        "banner_url": "URL Banner",
        "banner_not_found": "No encontrado",
        "download_header": "\n=== DESCARGANDO RECURSOS ===",
        "downloading": "[*] Descargando {} desde {}...",
        "saved": "[+] Guardado: {}",
        "download_failed": "[!] Fallo descarga (Status: {})",
        "download_error": "[!] Error descargando imagen: {}",
        "process_finished": "\n[ok] Proceso finalizado.",
        "unexpected_error": "\n[!!!] Ocurrio un error inesperado: {}",
        "yes": "Si",
        "no": "No"
    },
    'en': {
        "choose_lang": "Select language:",
        "creds_method": "\n[?] How do you want to enter Flickr credentials?",
        "manual": "1. Manually (Copy and paste)",
        "file": "2. From file (e.g., keys.txt)",
        "select_option": "\nSelect an option (1/2): ",
        "enter_api_key": "Enter api_key: ",
        "enter_auth_hash": "Enter auth_hash: ",
        "enter_secret": "Enter secret: ",
        "enter_file_path": "Enter file path (e.g., keys.txt): ",
        "file_not_exist": "[!] File {} does not exist.",
        "invalid_format": "[!] Invalid file format. Must contain api_key=..., auth_hash=... and secret=...",
        "error_reading": "[!] Error reading file: {}",
        "invalid_option": "[!] Invalid option.",
        "enter_email": "[?] Enter target email: ",
        "starting_search": "\n[*] Starting search for: {}",
        "search_error": "[!] HTTP Search Error: {}",
        "jsonp_error": "[!] Could not parse JSONP response from Flickr.",
        "user_not_found": "[-] User NOT found on Flickr.",
        "user_found": "\n[+] User FOUND! Collecting full information...",
        "error_user_details": "[!] Error getting user details.",
        "profile_info_header": "\n=== PROFILE INFORMATION ===",
        "real_name": "Real Name",
        "username": "Username",
        "nsid": "NSID",
        "dbid": "DBID",
        "date_create": "Date Created",
        "is_pro": "Is Pro",
        "is_deleted": "Is Deleted",
        "is_ad_free": "Is Ad Free",
        "path_alias": "Path Alias",
        "location": "Location",
        "description": "Description",
        "urls_header": "\n--- URLs ---",
        "profile_url": "Profile URL",
        "photos_url": "Photos URL",
        "mobile_url": "Mobile URL",
        "stats_header": "\n--- STATISTICS ---",
        "photos_count": "Photos Count",
        "has_stats": "Has Stats",
        "extras_header": "\n--- EXTRAS ---",
        "gift_eligible": "Gift Eligible",
        "media_header": "\n--- MEDIA ---",
        "profile_pic_url": "Profile Pic URL",
        "banner_url": "Banner URL",
        "banner_not_found": "Not found",
        "download_header": "\n=== DOWNLOADING RESOURCES ===",
        "downloading": "[*] Downloading {} from {}...",
        "saved": "[+] Saved: {}",
        "download_failed": "[!] Download failed (Status: {})",
        "download_error": "[!] Error downloading image: {}",
        "process_finished": "\n[ok] Process finished.",
        "unexpected_error": "\n[!!!] An unexpected error occurred: {}",
        "yes": "Yes",
        "no": "No"
    }
}

# Global var for selected language
L = LANG['es']

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
    ███████╗██╗     ██╗ ██████╗██╗  ██╗██████╗ 
    ██╔════╝██║     ██║██╔════╝██║ ██╔╝██╔══██╗
    █████╗  ██║     ██║██║     █████╔╝ ██████╔╝
    ██╔══╝  ██║     ██║██║     ██╔═██╗ ██╔══██╗
    ██║     ███████╗██║╚██████╗██║  ██╗██║  ██║
    ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
             OSINT TOOL - PYTHON EDITION
    """)

def get_language_choice():
    print("\nSelect Language / Selecciona Idioma:")
    print("1. Español")
    print("2. English")
    while True:
        choice = input("\n> ").strip()
        if choice == '1':
            return 'es'
        elif choice == '2':
            return 'en'
        else:
            print("Invalid option / Opcion invalida")

def get_credentials():
    print(L["creds_method"])
    print(L["manual"])
    print(L["file"])
    
    while True:
        choice = input(L["select_option"]).strip()
        
        if choice == '1':
            api_key = input(L["enter_api_key"]).strip()
            auth_hash = input(L["enter_auth_hash"]).strip()
            secret = input(L["enter_secret"]).strip()
            return api_key, auth_hash, secret
            
        elif choice == '2':
            file_path = input(L["enter_file_path"]).strip()
            if not os.path.exists(file_path):
                print(L["file_not_exist"].format(file_path))
                continue
                
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                api_key_match = re.search(r'api_key=(.+)', content)
                auth_hash_match = re.search(r'auth_hash=(.+)', content)
                secret_match = re.search(r'secret=(.+)', content)
                
                if not (api_key_match and auth_hash_match and secret_match):
                    print(L["invalid_format"])
                    continue
                    
                return api_key_match.group(1).strip(), auth_hash_match.group(1).strip(), secret_match.group(1).strip()
            except Exception as e:
                print(L["error_reading"].format(e))
        else:
            print(L["invalid_option"])

def download_image(url, filename):
    if not url:
        return
        
    try:
        print(L["downloading"].format(filename, url))
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(L["saved"].format(filename))
        else:
            print(L["download_failed"].format(response.status_code))
    except Exception as e:
        print(L["download_error"].format(e))

def main():
    global L
    clear_screen()
    print_banner()
    
    lang_code = get_language_choice()
    L = LANG[lang_code]
    
    email = input(L["enter_email"]).strip()
    api_key, auth_hash, secret = get_credentials()
    
    print(L["starting_search"].format(email))
    
    headers = {
        'accept': '*/*',
        'accept-language': 'es,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        search_url = f"https://www.flickr.com/services/rest?format=json&clientType=yui-3-flickrapi-module&api_key={api_key}&auth_hash={auth_hash}&auth_token=&secret={secret}&username={quote(email)}&method=flickr.people.search&jsoncallback=YUI.flickrAPITransactions.flapicb5&cachebust={int(time.time()*1000)}"
        
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(L["search_error"].format(response.status_code))
            return

        text = response.text
        match = re.search(r'YUI\.flickrAPITransactions\.flapicb5\((.+)\);?$', text)
        
        if not match:
            print(L["jsonp_error"])
            return
            
        search_data = json.loads(match.group(1))
        
        if not search_data.get('people') or not search_data['people'].get('person') or len(search_data['people']['person']) == 0:
            print(L["user_not_found"])
            return

        user = search_data['people']['person'][0]
        nsid = user['nsid']
        username = user['username']
        
        # User found message removed as requested

        extras = "ad_eligibility,can_addmeta,can_comment,can_download,can_print,can_share,contact,content_type,count_comments,count_faves,count_views,date_taken,date_upload,description,icon_urls_deep,isfavorite,ispro,license,media,needs_interstitial,owner_name,owner_datecreate,path_alias,perm_print,realname,rotation,safety_level,secret_k,secret_h,url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l,url_h,url_k,url_3k,url_4k,url_f,url_5k,url_6k,url_o,visibility,visibility_source,o_dims,publiceditability,system_moderation"
        profile_url = f"https://api.flickr.com/services/rest?per_page=5&page=1&extras={quote(extras)}&get_user_info=1&jump_to=&user_id={quote(nsid)}&privacy_filter=1&viewerNSID=&method=flickr.people.getPhotos&csrf=&api_key={api_key}&format=json&hermes=1&hermesClient=1&reqId=672e40d8-b662-419f-b2f2-854d495b3c04&nojsoncallback=1"
        
        profile_resp = requests.get(profile_url, headers=headers)
        profile_data = profile_resp.json()
        
        if not profile_data.get('user'):
            print(L["error_user_details"])
        else:
            user_data = profile_data['user']
            icon_urls = user_data.get('iconurls', {})
            profile_pic_url = icon_urls.get('retina') or icon_urls.get('large') or icon_urls.get('medium') or icon_urls.get('small') or icon_urls.get('default')
            
            banner_url_api = f"https://api.flickr.com/services/rest?method=flickr.people.getInfo&api_key={api_key}&user_id={quote(nsid)}&format=json&nojsoncallback=1"
            banner_resp = requests.get(banner_url_api, headers=headers)
            banner_data = banner_resp.json()
            
            person_data = banner_data.get('person', {})
            
            # Print Info
            print(L["profile_info_header"])
            print(f"{L['real_name']}: {user_data.get('realname', 'N/A')}")
            print(f"{L['username']}: {user_data.get('username', 'N/A')}")
            print(f"{L['nsid']}: {user_data.get('nsid', 'N/A')}")
            print(f"{L['dbid']}: {person_data.get('dbid', 'N/A')}")
            print(f"{L['date_create']}: {user_data.get('datecreate', 'N/A')}")
            print(f"{L['is_pro']}: {L['yes'] if user_data.get('ispro') == 1 else L['no']}")
            print(f"{L['is_deleted']}: {L['yes'] if person_data.get('is_deleted') == 1 else L['no']}")
            print(f"{L['is_ad_free']}: {L['yes'] if person_data.get('is_ad_free') == 1 else L['no']}")
            print(f"{L['path_alias']}: {user_data.get('path_alias', 'N/A')}")
            print(f"{L['location']}: {person_data.get('location', {}).get('_content', 'N/A')}")
            print(f"{L['description']}: {person_data.get('description', {}).get('_content', 'N/A')}")
            
            print(f"{L['profile_url']}: {person_data.get('profileurl', {}).get('_content', 'N/A')}")
            print(f"{L['photos_url']}: {person_data.get('photosurl', {}).get('_content', 'N/A')}")
            print(f"{L['mobile_url']}: {person_data.get('mobileurl', {}).get('_content', 'N/A')}")
            
            print(f"{L['photos_count']}: {person_data.get('photos', {}).get('count', {}).get('_content', 'N/A')}")
            print(f"{L['has_stats']}: {L['yes'] if person_data.get('has_stats') == 1 else L['no']}")
            
            print(f"{L['gift_eligible']}: {L['yes'] if person_data.get('gift', {}).get('gift_eligible') else L['no']}")
            
            print(f"{L['profile_pic_url']}: {profile_pic_url}")
            
            banner_pic_url = ""
            if person_data.get('coverphoto_url'):
                cp = person_data['coverphoto_url']
                banner_pic_url = cp.get('l') or cp.get('h') or cp.get('s')
                print(f"{L['banner_url']}: {banner_pic_url}")
            else:
                print(f"{L['banner_url']}: {L['banner_not_found']}")

            print(L["download_header"])
            
            if profile_pic_url:
                if 'http:' in profile_pic_url: 
                   profile_pic_url = profile_pic_url.replace('http:', 'https:')
                download_image(profile_pic_url, f"flickr_profile_{nsid}.jpg")
            
            if banner_pic_url:
                 if 'http:' in banner_pic_url: 
                   banner_pic_url = banner_pic_url.replace('http:', 'https:')
                 download_image(banner_pic_url, f"flickr_banner_{nsid}.jpg")
            
            print(L["process_finished"])

    except Exception as e:
        print(L["unexpected_error"].format(e))

if __name__ == "__main__":
    main()
