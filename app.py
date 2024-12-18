from flask import Flask, jsonify, render_template
from pywifi import PyWiFi
import subprocess
import time

app = Flask(__name__)

def get_connected_ssid():
    """
    Obtém o SSID da rede Wi-Fi atualmente conectada.
    """
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], universal_newlines=True)
        for line in result.splitlines():
            if "SSID" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Erro ao obter SSID da rede conectada: {e}")
        return None

def signal_strength_to_percentage(signal):
    """
    Converte a força do sinal de dBm para uma porcentagem entre 0 e 100.
    """
    return max(0, min(100, 100 + signal))  # Ajusta o range de -100 a 0 para 0 a 100

@app.route('/')
def index():
    """
    Renderiza a página inicial.
    """
    return render_template('index.html')

@app.route('/get_networks', methods=['GET'])
def get_networks():
    """
    Obtém as redes Wi-Fi disponíveis e retorna as informações como JSON.
    """
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    try:
        iface.scan()  # Inicia a varredura das redes
        time.sleep(2)  # Adiciona uma pausa para aguardar a conclusão da varredura
        networks = iface.scan_results()  # Obtém os resultados da varredura
    except Exception as e:
        return jsonify({'error': f"Erro ao realizar a varredura de redes Wi-Fi: {str(e)}"}), 500
    
    connected_ssid = get_connected_ssid()  # SSID da rede atualmente conectada
    
    network_list = []
    if networks:
        for network in networks:
            signal_percentage = signal_strength_to_percentage(network.signal)
            # Converte valores de network.akm para strings antes de juntar
            akm_security = 'Open' if not network.akm else ', '.join(map(str, network.akm))
            
            network_info = {
                'ssid': network.ssid,
                'signal': network.signal,
                'signal_percentage': signal_percentage,  # Percentual do sinal para a barra
                'security': akm_security,  # Ajuste aqui
                'connected': network.ssid == connected_ssid
            }
            network_list.append(network_info)
    
    if not network_list:
        return jsonify({'message': 'Nenhuma rede Wi-Fi encontrada'}), 404
    
    return jsonify(network_list)

if __name__ == '__main__':
    app.run(debug=True)
