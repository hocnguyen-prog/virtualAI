
import tkinter as tk
from tkinter import ttk
import speedtest
import threading
import matplotlib.pyplot as plt
from datetime import datetime, date

results_history = []
st = None
best_server = None


def format_result(download_speed, upload_speed, ping):
    return f"Download: {download_speed:.2f} Mbps | Upload: {upload_speed:.2f} Mbps | Ping: {ping:.2f} ms"


def run_test():
    btn_test.config(state="disabled")
    status_label.config(text="Probíhá test…")
    threading.Thread(target=test).start()


def test():
    global st, best_server
    try:
        if st is None:
            st = speedtest.Speedtest()
        if best_server is None:
            best_server = st.get_best_server()
            server_text = f"Server: {best_server['host']} ({best_server.get('country', 'unknown')})"
            app.after(0, lambda: server_label.config(text=server_text))

        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping
        timestamp = datetime.now()
        results_history.append((timestamp, download_speed, upload_speed, ping))

        status_text = f"{timestamp:%H:%M:%S} | {format_result(download_speed, upload_speed, ping)}"
        app.after(0, lambda: status_label.config(text=status_text))
    except Exception as e:
        app.after(0, lambda: status_label.config(text=f"Chyba testu: {e}"))
    finally:
        app.after(0, lambda: btn_test.config(state="normal"))


def show_graph():
    if not results_history:
        status_label.config(text="Žádné výsledky pro graf")
        return

    timestamps = [r[0] for r in results_history]
    download_speeds = [r[1] for r in results_history]
    upload_speeds = [r[2] for r in results_history]
    pings = [r[3] for r in results_history]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, download_speeds, marker="o", label="Download (Mbps)")
    plt.plot(timestamps, upload_speeds, marker="o", label="Upload (Mbps)")
    plt.plot(timestamps, pings, marker="o", label="Ping (ms)")
    plt.title("Historie rychlosti Wi-Fi")
    plt.xlabel("Čas")
    plt.ylabel("Hodnota")
    plt.grid(True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()


def save_results():
    if not results_history:
        status_label.config(text="Žádné výsledky k uložení")
        return

    filename = f"wifi_vysledky_{date.today():%Y%m%d}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        for timestamp, download_speed, upload_speed, ping in results_history:
            f.write(f"{timestamp:%Y-%m-%d %H:%M:%S} | Download: {download_speed:.2f} Mbps | Upload: {upload_speed:.2f} Mbps | Ping: {ping:.2f} ms\n")

    status_label.config(text=f"Výsledky uloženy do {filename}")


def clear_history():
    results_history.clear()
    status_label.config(text="Historie vymazána")


# GUI
app = tk.Tk()
app.title("Wi-Fi Speed Test")
app.geometry("420x340")
app.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

title_label = tk.Label(app, text="Wi-Fi Speed Test", font=("Arial", 16), bg="#1e1e1e", fg="#ffffff")
title_label.pack(pady=10)

server_label = tk.Label(app, text="Server: čeká na inicializaci...", font=("Arial", 10), bg="#1e1e1e", fg="#dddddd")
server_label.pack(pady=2)

btn_test = tk.Button(app, text="🚀 Spustit test", command=run_test, bg="#4CAF50", fg="white", font=("Arial", 12), width=18)
btn_test.pack(pady=8)

status_label = tk.Label(app, text="", font=("Arial", 12), bg="#1e1e1e", fg="#ffffff", justify="center")
status_label.pack(pady=6)

btn_graph = tk.Button(app, text="📈 Zobrazit graf", command=show_graph, width=18)
btn_graph.pack(pady=4)

btn_save = tk.Button(app, text="💾 Uložit výsledky", command=save_results, width=18)
btn_save.pack(pady=4)

btn_clear = tk.Button(app, text="🧹 Vymazat historii", command=clear_history, width=18)
btn_clear.pack(pady=4)

app.mainloop()
