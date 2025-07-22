import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

urls = [
    'https://www.bncr.fi.cr',
    'https://www.baccredomatic.com/es-cr',
    'https://www.hacienda.go.cr',
    'https://www.ucr.ac.cr',
    'https://www.grupoice.com',
    'https://www.bancobcr.com',
    'https://www.popularenlinea.com',
    'https://www.tec.ac.cr',
    'https://www.una.ac.cr',
    'https://www.uned.ac.cr',
    'https://www.cinde.org',
    'https://www.kerwa.ucr.ac.cr',
    'https://www.recope.go.cr',
    'https://www.ccss.sa.cr',
    'https://www.ministeriodesalud.go.cr',
    'https://www.poder-judicial.go.cr',
    'https://www.presidencia.go.cr',
    'https://www.mep.go.cr',
    'https://www.pgr.go.cr',
    'https://www.micit.go.cr',
    'https://www.mopt.go.cr',
    'https://www.bolsacr.com',
    'https://www.ins-cr.com',
    'https://www.sugeval.fi.cr',
    'https://www.sugef.fi.cr',
    'https://www.sugese.fi.cr',
    'https://www.inamu.go.cr',
    'https://www.procomer.com',
    'https://www.protec.go.cr',
    'https://www.tse.go.cr',
    'https://www.imn.ac.cr',
    'https://www.japdeva.go.cr',
    'https://www.fundecooperacion.org',
    'https://www.migracion.go.cr',
    'https://www.uccaep.or.cr',
    'https://www.cne.go.cr',
    'https://www.munialajuela.go.cr',
    'https://www.munisantodomingo.go.cr',
    'https://www.munipavas.go.cr',
    'https://www.munisanjose.go.cr',
    'https://www.munitibas.go.cr',
    'https://www.muniescazu.go.cr',
    'https://www.incofer.go.cr',
    'https://www.ministeriotrabajo.go.cr',
    'https://www.cnp.go.cr',
    'https://www.ministeriodeeconomia.go.cr',
    'https://www.comex.go.cr',
    'https://www.micit.go.cr',
    'https://www.ayase.go.cr',
    'https://www.setena.go.cr',
    'https://www.fodesaf.go.cr',
    'https://www.cenproah.go.cr',
    'https://www.museosdecostarica.go.cr',
    'https://www.cnfl.go.cr',
    'https://www.iica.int',
    'https://www.lanacion.com.cr',
    'https://www.teletica.com',
    'https://www.aldia.cr',
    'https://www.diarioextra.com',
    'https://www.crhoy.com',
    'https://www.elmundo.cr',
    'https://www.nacion.com',
    'https://www.inamu.go.cr',
    'https://www.turismo.go.cr',
    'https://www.fedefutbol.com',
    'https://www.tdmás.cr',
    'https://www.repretel.com',
    'https://www.monumental.co.cr',
    'https://www.larepublica.net',
    'https://www.elpais.cr',
    'https://www.elguardian.cr',
    'https://www.futbolcentroamerica.com',
    'https://www.deputamadre.com',
    'https://www.parqueculturallamolina.go.cr',
    'https://www.apoyatuproyecto.go.cr',
    'https://www.estudiaencostarica.com',
    'https://www.entrecostas.com',
    'https://www.bcrfi.com',
    'https://www.credomatic.com/cr',
    'https://www.tiquetesbaratos.cr',
    'https://www.vuelo.com',
    'https://www.coopeande.cr',
    'https://www.coopeservidores.fi.cr',
    'https://www.bangente.com',
    'https://www.crstar.com',
    'https://www.grupoinsa.com',
    'https://www.scotiabank.fi.cr',
    'https://www.hardrockhotelcr.com',
    'https://www.marriottcr.com',
    'https://www.hotelloslagartos.com',
    'https://www.arenal.com',
    'https://www.costarica.com',
    'https://www.cr-travel.com',
    'https://www.libertadsindicalcr.org',
    'https://www.unafo.com',
    'https://www.conicit.go.cr',
    'https://www.asamblea.go.cr',
    'https://www.inec.go.cr',
    'https://www.icafe.go.cr',
    'https://www.inbio.ac.cr',
]

# Lista donde se almacenarán las URLs con formularios de login
login_sites = []

# Configuración del encabezado para parecer un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}


def check_login_form(url):
    try:
        print(f"Accediendo a: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                # Buscamos un campo de contraseña o de usuario
                if form.find('input', {'type': 'password'}) or form.find('input', {'type': 'email'}) or form.find('input', {'type': 'text'}):
                    print(f"Formulario de login encontrado en: {url}")
                    login_sites.append(url)
                    return True
            print(f"No se encontró formulario de login en: {url}")
        else:
            print(f"No se pudo acceder a {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error accediendo a {url}: {e}")
    return False


for url in urls:
    check_login_form(url)
    sleep(2)  # Pausa entre solicitudes para evitar sobrecargar los servidores

# Convertimos la lista de sitios en un DataFrame de pandas
df_login_sites = pd.DataFrame(login_sites, columns=['URL'])

# Guardamos el dataset en un archivo CSV
df_login_sites.to_csv('login_sites.csv', index=False)

# Mostramos el DataFrame resultante
df_login_sites



count = 0
for url in df_login_sites['URL']:
    response = requests.get(url)
    count += 1
    print("-------------------------------SITIO--------------------------------------------------------")
    print(response)
    print(f"Intento {count}: {url}")

    print("Código de estado:", response.status_code)
    print("Encabezados:", response.headers)
    print("Contenido (HTML):", response.text)
    print("Contenido (binario):", response.content)
    print("URL final:", response.url)
    print("Cookies:", response.cookies)
    print("Tiempo de response:", response.elapsed)
    print("Éxito de la solicitud:", response.ok)
    print("-----------------------------------------------------------------------------------------------------------------------------------------")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        page = "url" + str(count) + ".html"

        with open(page, "w") as file:
          file.write(response.text)

        if soup.title:
            title = soup.title.string
            print(f"Título de la página: {title}")
        else:
            print(f"No se encontró un título en la página: {url}")
    else:
        print(f"Error al acceder a {url}, código de estado: {response.status_code}")
