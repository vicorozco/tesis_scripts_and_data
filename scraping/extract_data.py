import requests
import ssl
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

def obtener_features_sitio(url):
    features = {
        "tiene_ssl": False,
        "ssl_valido": False,
        "longitud_url": 0,
        "url_sospechosa": False,
        "longitud_texto": 0,
        "caracteres_extranos": 0,
        "num_imagenes": 0,
        "tiene_favicon": False,
        "hsts": False,
        "x_frame_options": False,
        "x_content_type_options": False,
        "referrer_policy": False,
        "csp": False,
        "dominio_gobierno_edu": False,
        "nro_guiones": 0,
        "cookies_seguras": False
    }

    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        features["longitud_url"] = len(url)
        features["nro_guiones"] = url.count('-')
        features["url_sospechosa"] = "@" in url or "//" in url[8:]
        features["dominio_gobierno_edu"] = any(tld in hostname for tld in [".gob", ".gov", ".edu"])

        if url.startswith("https://"):
            features["tiene_ssl"] = True
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                    s.settimeout(3.0)
                    s.connect((hostname, 443))
                    cert = s.getpeercert()
                    if cert:
                        features["ssl_valido"] = True
            except Exception:
                pass

        response = requests.get(url, timeout=5)
        headers = response.headers
        content = response.text

        # Metadata del sitio
        features["hsts"] = 'strict-transport-security' in headers
        features["x_frame_options"] = 'x-frame-options' in headers
        features["x_content_type_options"] = 'x-content-type-options' in headers
        features["referrer_policy"] = 'referrer-policy' in headers
        features["csp"] = 'content-security-policy' in headers

        soup = BeautifulSoup(content, 'html.parser')
        features["longitud_texto"] = len(soup.get_text())
        features["num_imagenes"] = len(soup.find_all("img"))
        features["caracteres_extranos"] = len(re.findall(r'[\x80-\xff]', content))
        features["tiene_favicon"] = bool(soup.find("link", rel=lambda x: x and 'icon' in x.lower()))

        features["cookies_seguras"] = any(
            'secure' in c.lower() for c in headers.get('Set-Cookie', '').split(';')
        )

    except Exception as e:
        print(f" Error procesando {url}: {e}")

    return features

if __name__ == "__main__":
    sitio = "http://localhost:8001/"
    features = obtener_features_sitio(sitio)

    print("\n Metadatos:")
    for clave, valor in features.items():
        print(f"{clave:25}: {valor}")



