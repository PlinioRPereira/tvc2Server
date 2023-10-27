import json
import sounddevice as sd
import numpy as np
import socket
import threading

def get_device_info(device_id):
    device_info = sd.query_devices(device_id, 'input')
    return device_info['default_samplerate'], np.int16

def start_streaming(device_id, rate):
    CHANNELS = 2
    DTYPE = np.int16
    BUFFER_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)
    conn, addr = server_socket.accept()

    print(f"Conexão estabelecida com {addr}")

    metadata = {
        'rate': rate,
        'channels': CHANNELS,
        'dtype': 'int16',
        'buffer_size': BUFFER_SIZE
    }
    conn.sendall(json.dumps(metadata).encode('utf-8'))

    try:
        with sd.InputStream(samplerate=rate, channels=CHANNELS, dtype=DTYPE, device=device_id) as stream:
            while streaming:
                audio_chunk, overflowed = stream.read(BUFFER_SIZE)
                audio_bytes = audio_chunk.astype(DTYPE).tobytes()
                conn.sendall(audio_bytes)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        conn.close()
        server_socket.close()

devices = sd.query_devices()

streaming = False

while True:
    print("\nMenu:")
    if not streaming:
        print("1. Iniciar transmissão")
    else:
        print("2. Parar transmissão")
    print("3. Sair")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        if not streaming:
            for i, device in enumerate(devices):
                print(
                    f"ID: {i}, Nome: {device['name']}, Canais: {device['max_input_channels']}, Taxas de amostragem suportadas: {device['default_samplerate']}")

            device_id = int(input("Informe o ID do dispositivo: "))
            rate = int(input("Informe a taxa de amostragem: "))
            streaming = True
            thread = threading.Thread(target=start_streaming, args=(device_id, rate))
            thread.start()
            print("Transmissão iniciada.")
        else:
            print("Transmissão já está em andamento.")
    elif choice == '2':
        if streaming:
            streaming = False
            print("Transmissão parada.")
        else:
            print("Nenhuma transmissão em andamento.")
    elif choice == '3':
        if streaming:
            streaming = False
        print("Saindo.")
        break
    else:
        print("Opção inválida.")
