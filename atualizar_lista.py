import datetime
import gzip
import os
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ==========================================
# CONFIGURAÇÕES GERAIS E DA LISTA M3U
# ==========================================
PLAYLIST_NAME = "Radar TV"
CHANNEL_ID = "RadarTV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/Radartvplayer/refs/heads/main/logo%20png%20RadarTV.png"
EPG_URL = "https://althierestm.github.io/Lista-RadarTV/epg.xml"
CANAL_PRINCIPAL_RADARTV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"
TIMEZONE = "-0300"  # Horário de Brasília

# ==========================================
# BANCO DE DADOS DA PROGRAMAÇÃO TÍPICA
# ==========================================
PROGRAMAS_BASE = {
    "madrugada": [
        ("Sessão Madrugada", "Filmes clássicos e produções independentes."),
        ("Radar Night", "Música, videoclipes e entrevistas exclusivas."),
        ("Igreja no Ar", "Momento de fé e reflexão."),
    ],
    "manha": [
        ("Bom Dia Região", "As primeiras notícias da manhã e previsão do tempo."),
        ("Radar Rural", "O homem do campo e os destaques do agronegócio regional."),
        ("Manhã Show", "Variedades, culinária e entretenimento."),
        ("Desenhos Animados", "Os melhores desenhos para a criançada."),
    ],
    "almoco": [
        ("Radar Notícias 1ª Edição", "Informação ao vivo e cobertura dos principais fatos da região."),
        ("Radar Esporte Regional", "Destaques esportivos de Muriaé e região."),
        ("Debate Aberto", "Opinião, entrevistas e temas da atualidade."),
    ],
    "tarde": [
        ("Novela da Tarde", "Grandes clássicos e dramas imperdíveis."),
        ("Tarde Total", "Revista eletrônica com prestação de serviços e entretenimento."),
        ("Cinema na Tarde", "Sucessos de bilheteria para toda a família."),
    ],
    "noite": [
        ("Radar Notícias 2ª Edição", "O resumo completo dos fatos mais importantes do dia."),
        ("Radar Esportes", "Tudo sobre o futebol e modalidades esportivas da região."),
        ("Novela das Oito", "A trama que prende a sua atenção."),
        ("Super Tela", "Os melhores filmes em alta definição."),
    ],
}

def format_xmltv_date(dt):
    return dt.strftime("%Y%m%d%H%M%S") + f" {TIMEZONE}"

def get_random_show(hour):
    if 0 <= hour < 6:
        shows = PROGRAMAS_BASE["madrugada"]
    elif 6 <= hour < 11:
        shows = PROGRAMAS_BASE["manha"]
    elif 11 <= hour < 14:
        shows = PROGRAMAS_BASE["almoco"]
    elif 14 <= hour < 18:
        shows = PROGRAMAS_BASE["tarde"]
    else:
        shows = PROGRAMAS_BASE["noite"]
    
    durations = [30, 45, 60, 90, 120]
    title, desc = random.choice(shows)
    duration = random.choice(durations)
    return title, desc, duration

def create_m3u():
    m3u_content = f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"\n'
    m3u_content += f'#EXTINF:-1 tvg-id="{CHANNEL_ID}" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
    m3u_content += f'{CANAL_PRINCIPAL_RADARTV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print("✅ Arquivo lista.m3u gerado com sucesso!")

def generate_epg():
    tv = ET.Element("tv", attrib={"generator-info-name": "RadarTV_EPG_Generator"})
    
    channel = ET.SubElement(tv, "channel", attrib={"id": CHANNEL_ID})
    display_name = ET.SubElement(channel, "display-name")
    display_name.text = PLAYLIST_NAME
    ET.SubElement(channel, "icon", attrib={"src": LOGO_URL})

    agora_brasil = datetime.datetime.utcnow() - datetime.timedelta(hours=3)
    
    start_date = (agora_brasil - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.datetime(2026, 12, 31, 23, 59, 59)
    
    current_time = start_date
    desc_baldanza = "Copa baldanza ao vivo direto do antigo sesc de Muriaé, MG. siga no instagram @RadarTVMG."

    while current_time < end_date:
        current_day = current_time.day
        current_month = current_time.month
        current_year = current_time.year

        # Copa Baldanza: Sábado 05/09/2026 (08:00 às 20:00)
        if current_year == 2026 and current_month == 9 and current_day == 5 and current_time.hour == 8 and current_time.minute == 0:
            prog_start = current_time
            prog_end = current_time.replace(hour=20, minute=0)
            
            prog = ET.SubElement(tv, "programme", attrib={
                "start": format_xmltv_date(prog_start),
                "stop": format_xmltv_date(prog_end),
                "channel": CHANNEL_ID
            })
            ET.SubElement(prog, "title", attrib={"lang": "pt"}).text = "Copa Baldanza de Handebol - Ao Vivo"
            ET.SubElement(prog, "desc", attrib={"lang": "pt"}).text = desc_baldanza
            ET.SubElement(prog, "category", attrib={"lang": "pt"}).text = "Esporte"
            
            current_time = prog_end
            continue

        # Copa Baldanza: Domingo 06/09/2026 (09:00 às 15:00)
        elif current_year == 2026 and current_month == 9 and current_day == 6 and current_time.hour == 9 and current_time.minute == 0:
            prog_start = current_time
            prog_end = current_time.replace(hour=15, minute=0)
            
            prog = ET.SubElement(tv, "programme", attrib={
                "start": format_xmltv_date(prog_start),
                "stop": format_xmltv_date(prog_end),
                "channel": CHANNEL_ID
            })
            ET.SubElement(prog, "title", attrib={"lang": "pt"}).text = "Copa Baldanza de Handebol - Finais"
            ET.SubElement(prog, "desc", attrib={"lang": "pt"}).text = desc_baldanza
            ET.SubElement(prog, "category", attrib={"lang": "pt"}).text = "Esporte"
            
            current_time = prog_end
            continue

        # Programação Normal
        title, desc, duration_min = get_random_show(current_time.hour)
        prog_start = current_time
        prog_end = prog_start + datetime.timedelta(minutes=duration_min)

        if current_year == 2026 and current_month == 9:
            if current_day == 5 and prog_start.hour < 8 and prog_end.hour >= 8:
                prog_end = prog_start.replace(hour=8, minute=0)
            elif current_day == 6 and prog_start.hour < 9 and prog_end.hour >= 9:
                prog_end = prog_start.replace(hour=9, minute=0)

        if prog_end > end_date:
            prog_end = end_date

        prog = ET.SubElement(tv, "programme", attrib={
            "start": format_xmltv_date(prog_start),
            "stop": format_xmltv_date(prog_end),
            "channel": CHANNEL_ID
        })
        ET.SubElement(prog, "title", attrib={"lang": "pt"}).text = title
        ET.SubElement(prog, "desc", attrib={"lang": "pt"}).text = desc

        current_time = prog_end

    xml_str = minidom.parseString(ET.tostring(tv, encoding="utf-8")).toprettyxml(indent="  ", encoding="utf-8")
    
    with open("epg.xml", "wb") as f:
        f.write(xml_str)
    
    with gzip.open("epg.xml.gz", "wb") as f:
        f.write(xml_str)

    print("✅ Arquivos epg.xml e epg.xml.gz gerados com sucesso!")

if __name__ == "__main__":
    create_m3u()
    generate_epg()
