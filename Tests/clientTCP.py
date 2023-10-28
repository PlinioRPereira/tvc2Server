import socket
import json
import wave
import numpy as np
import threading

def start_recording(server_ip = "10.0.0.106", server_port=5000, output_file_name="output.wav"):
    print("server_ip: ", server_ip)
    print("port: ", server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip.strip(), server_port))

    metadata_bytes = client_socket.recv(1024)
    metadata = json.loads(metadata_bytes.decode('utf-8'))
    RATE = metadata['rate']
    CHANNELS = metadata['channels']
    DTYPE = np.dtype(metadata['dtype'])
    BUFFER_SIZE = metadata['buffer_size']

    wav_file = wave.open(output_file_name, 'wb')
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(DTYPE.itemsize)
    wav_file.setframerate(RATE)

    print(f"Gravando com {RATE} taxa de amostragem, {CHANNELS} canais, buffer de tamanho {BUFFER_SIZE}.")

    try:
        while recording:
            audio_data = client_socket.recv(BUFFER_SIZE)
            if not audio_data:
                break
            wav_file.writeframes(audio_data)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        wav_file.close()
        client_socket.close()


# Variável global para controlar o estado da gravação
recording = False

# Interface de menu
while True:
    print("\nMenu:")
    if not recording:
        print("1. Iniciar gravação")
    else:
        print("2. Parar gravação")
    print("3. Sair")

    choice = input("Escolha uma opção: ")

    if choice == '1':
        if not recording:
            recording = True
            server_ip = input("Informe o endereço IP do servidor: ")
            server_port = int(input("Informe a porta de conexão: "))
            thread = threading.Thread(target=start_recording, args=(server_ip, server_port))
            thread.start()
            print("Gravação iniciada.")
        else:
            print("Gravação já está em andamento.")
    elif choice == '2':
        if recording:
            recording = False
            print("Gravação parada.")
        else:
            print("Nenhuma gravação em andamento.")
    elif choice == '3':
        if recording:
            recording = False
        print("Saindo.")
        break
    else:
        print("Opção inválida.")
