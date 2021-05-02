#!/bin/python3
"""Görsel Arayüzlü Chat Uygulamasi - Client Baglantisi"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def gelen_mesaj():
    """Mesaj algilama fonksiyonu"""
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            mesaj_listesi.insert(tkinter.END, msg)
        except OSError:
            break # Eger kullanici cikis yaparsa

def gonder(event=None):
    """Mesaj gonderme fonksiyonu"""
    msg = mesajim.get()
    mesajim.set("") # Girdi kismini bosaltacak
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{cikis}":
        client_socket.close()
        app.quit()

def cikis_durumu(event=None):
    """Cikis durumunda 'cikis' mesajinin gönderimini saglayacak olan ek fonksiyon.
    Bu fonksiyon ile cikis yapildiginda cikisin gercekten saglandigi kontrol edilir."""
    mesajim.set("{cikis}")
    gonder()



app = tkinter.Tk()
app.title("Koddunyam.net")

mesaj_alani = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Mesajinizi girin...")
scrollbar = tkinter.Scrollbar(mesaj_alani)
mesaj_listesi = tkinter.Listbox(mesaj_alani, height=20, width=70,
                                yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
mesaj_listesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaj_listesi.see("end")
mesaj_listesi.pack()
mesaj_alani.pack()

giris_alani = tkinter.Entry(app, textvariable=mesajim)
giris_alani.bind("<Return>", gonder)
giris_alani.pack()
gonder_buton = tkinter.Button(app, text="Gonder", command=gonder)
gonder_buton.pack()

app.protocol("WM_DELETE_WINDOW", cikis_durumu)

HOST = '127.0.0.1'
PORT = 23847 #input("Server Portu (OTO:23847): ")



if not PORT:
    PORT = 23847
else:
    PORT = int(PORT)

BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=gelen_mesaj)
receive_thread.start()
tkinter.mainloop()