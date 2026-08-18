import os

PLAYLIST_NAME = "Radar TV"
LOGO_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/Logo%20RadarTV%203000x3000.jpg"
EPG_URL = "https://raw.githubusercontent.com/althierestm/radartv/main/epg.xml"

CANAL_PRINCIPAL_FCV = "https://video01.logicahost.com.br/fcvtv/fcvtv/playlist.m3u8"


def create_m3u():
    m3u_content = f'#EXTM3U url-tvg="{EPG_URL}" x-tvg-url="{EPG_URL}"\n'
    m3u_content += f'#EXTINF:-1 tvg-id="RadarTV" tvg-name="{PLAYLIST_NAME}" tvg-logo="{LOGO_URL}" group-title="Radar TV", {PLAYLIST_NAME}\n'
    m3u_content += f'{CANAL_PRINCIPAL_FCV}\n'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("✅ Arquivo lista.m3u gerado com suporte total a EPG!")


if __name__ == "__main__":
    create_m3u()
