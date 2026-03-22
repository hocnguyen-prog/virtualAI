import tkinter as tk
from tkinter import ttk
import speedtest
import threading
import matplotlib.pyplot as plt
from datetime import datetime

results_history = []
st = speedtest.Speedtest()
best_server = st.get_best_server()  # Cache server pro rychlejší opakované

def run_test():
    btn_test.config(state="disabled")
    status_label.config(text="testuje se...")

    def test():
        try:
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000 
            ping = st.results.ping

            results_history.append((datetime.now(), download_speed, upload_speed, ping))

            results_test = f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps\nPing: {ping:.2f} ms"
            status_label.config(text=results_test)
        except Exception as e:
            status_label.config(text=f"Chyba testu: {e}")
        finally:
            btn_test.config(state="normal")
        
    threading.Thread(target=test).start()

def show_graph():
    if not results_history:
        status_label.config(text="Žádné výsledky pro graf")
        return

    timestamps = [r[0] for r in results_history]
    download_speeds = [r[1] for r in results_history]
    upload_speeds = [r[2] for r in results_history]

    plt.figure()
    plt.plot(timestamps, download_speeds, label="Download Speed (Mbps)")
    plt.plot(timestamps, upload_speeds, label="Upload Speed (Mbps)")
    plt.title("Historie rychlosti Wi-Fi")
    plt.xlabel("Čas")
    plt.ylabel("Rychlost (Mbps)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def save_results():
    if not results_history:
        status_label.config(text="Žádné výsledky k uložení")
        return

    with open("wifi_vysledky.txt", "a") as f:
        for timestamp, download, upload, ping in results_history:
            f.write(f"{timestamp} | Download: {download:.2f} Mbps | Upload: {upload:.2f} Mbps | Ping: {ping:.2f} ms\n")

    status_label.config(text="Výsledky uloženy do wifi_vysledky.txt")

# GUI
app = tk.Tk()
app.title("Wi-Fi Speed Test")
app.geometry("400x300")
app.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

title_label = tk.Label(app, text="Wi-Fi Speed Test", font=("Arial", 16), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=10)
btn_test = tk.Button(app, text="🚀 Spustit test", command=run_test, bg="#4CAF50", fg="white", font=("Arial", 12))
btn_test.pack(pady=10)
status_label = tk.Label(app, text="", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff")
status_label.pack(pady=10)
btn_graph = tk.Button(app, text="📈 Zobrazit graf", command=show_graph)
btn_graph.pack(pady=10)
btn_save = tk.Button(app, text="💾 Uložit výsledky", command=save_results)
btn_save.pack(pady=10)
app.mainloop()