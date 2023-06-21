import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from threading import Thread

# Função para atualizar a barra de progresso
def update_progress(stream, chunk, bytes_remaining):
    # Calcular o progresso atual em porcentagem
    progress = round((1 - bytes_remaining / stream.filesize) * 100)
    progress_bar['value'] = progress

# Função para baixar o vídeo
def download_video():
    # Obter a URL do vídeo do campo de entrada
    video_url = url_entry.get()

    try:
        # Criar objeto YouTube
        yt = YouTube(video_url, on_progress_callback=update_progress)

        # Obter todas as resoluções disponíveis
        resolutions = yt.streams.filter(progressive=True).all()

        # Obter a resolução selecionada pelo usuário
        selected_resolution = resolution_var.get()
        
        # Encontrar a stream com a resolução selecionada
        stream = next(
            (res for res in resolutions if str(res.resolution) == selected_resolution),
            None
        )

        if stream is None:
            raise ValueError("Resolução selecionada inválida.")

        # Solicitar ao usuário uma pasta de destino
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            return  # Se nenhuma pasta for selecionada, sair da função

        # Definir o nome do arquivo como o título do vídeo com extensão .mp4
        file_name = f"{yt.title}.mp4"

        # Definir o caminho completo para o arquivo de destino
        file_path = os.path.join(destination_folder, file_name)

        # Criar uma thread separada para o download
        download_thread = Thread(
            target=stream.download,
            kwargs={'output_path': destination_folder, 'filename': file_name}
        )
        download_thread.start()

        # Exibir mensagem de download em andamento
        messagebox.showinfo("Download em progresso", 'O Download em andamento, espere a conclusão da barra para apertar "Ok".')

        # Esperar a conclusão do download
        download_thread.join()

        # Exibir uma mensagem de conclusão
        messagebox.showinfo("Download concluído", "O download foi concluído com sucesso!")

        # Resetar a barra de progresso
        progress_bar['value'] = 0

    except RegexMatchError:
        messagebox.showerror("Erro", "URL inválida.")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", "Ocorreu um erro durante o download.")

# Criar a janela principal
window = tk.Tk()
window.title("YouTube Downloader")

# Criar rótulo e campo de entrada para a URL
url_label = tk.Label(window, text="URL do vídeo:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Criar rótulo e caixa de seleção para a qualidade do vídeo
resolution_label = tk.Label(window, text="Qualidade:")
resolution_label.pack()
resolution_var = tk.StringVar(window)
resolution_var.set("720p")  # Valor padrão
resolution_dropdown = tk.OptionMenu(window, resolution_var, "360p", "720p", "1080p")
resolution_dropdown.pack()

# Criar botão de download
download_button = tk.Button(window, text="Baixar", command=download_video)
download_button.pack()

# Criar barra de progresso
progress_bar = Progressbar(window, orient='horizontal', mode='determinate', length=200)
progress_bar.pack()

# Executar a janela principal
window.mainloop()
