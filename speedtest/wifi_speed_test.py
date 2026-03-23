<<<<<<< HEAD
# toto je test pro měření rychlosti Wi-Fi připojení pomocí knihovny speedtest
from turtle import title

import speedtest
def test_wifi_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
if __name__ == "__main__":
    test_wifi_speed()
print ("Test rychlosti Wi-Fi připojení dokončen.")
import tkinter as tk
import speedtest
import threading
def test_wifi_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    result_label.config(text=f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps")
def start_test():
    threading.Thread(target=test_wifi_speed).start()
root = tk.Tk()
root.title("Wi-Fi Speed Test")
test_button = tk.Button(root, text="Start Wi-Fi Speed Test", command=start_test)
test_button.pack(pady=20)
result_label = tk.Label(root, text="")
result_label.pack(pady=20)
root.mainloop()

app = tk.Tk()
app.title("Wi-Fi Speed Test")
app.geometry("300x200")
label = tk.Label(app, text="Click the button to test Wi-Fi speed")
label.pack(pady=10)
button = tk.Button(app, text="Test Wi-Fi Speed", command=test_wifi_speed)
button.pack(pady=10)
result_label = tk.Label(app, text="")
result_label.pack(pady=10)
app.mainloop() 

title = "Wi-Fi Speed Test"
title.pack(pady=10)
btn = tk.Button(app, text="Test Wi-Fi Speed", command=test_wifi_speed)
btn.pack(pady=10)

result_label = tk.Label(app, text="")
result_label.pack(pady=10)

=======
# toto je test pro měření rychlosti Wi-Fi připojení pomocí knihovny speedtest
from turtle import title

import speedtest
def test_wifi_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
if __name__ == "__main__":
    test_wifi_speed()
print ("Test rychlosti Wi-Fi připojení dokončen.")
import tkinter as tk
import speedtest
import threading
def test_wifi_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    result_label.config(text=f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps")
def start_test():
    threading.Thread(target=test_wifi_speed).start()
root = tk.Tk()
root.title("Wi-Fi Speed Test")
test_button = tk.Button(root, text="Start Wi-Fi Speed Test", command=start_test)
test_button.pack(pady=20)
result_label = tk.Label(root, text="")
result_label.pack(pady=20)
root.mainloop()

app = tk.Tk()
app.title("Wi-Fi Speed Test")
app.geometry("300x200")
label = tk.Label(app, text="Click the button to test Wi-Fi speed")
label.pack(pady=10)
button = tk.Button(app, text="Test Wi-Fi Speed", command=test_wifi_speed)
button.pack(pady=10)
result_label = tk.Label(app, text="")
result_label.pack(pady=10)
app.mainloop() 

title = "Wi-Fi Speed Test"
title.pack(pady=10)
btn = tk.Button(app, text="Test Wi-Fi Speed", command=test_wifi_speed)
btn.pack(pady=10)

result_label = tk.Label(app, text="")
result_label.pack(pady=10)

>>>>>>> 9e7ab7b3ef6df452d38f6e299e8638294bc4098e
app.mainloop()