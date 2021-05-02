#!/bin/python3
# Koddunyam.net Chat Uygulamasi
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 23847
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def gelen_mesaj():
    """Gelen mesajlarin kontrolünü saglayan fonksiyon."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s baglandi." % client_address)
        client.send(bytes("Koddunyam.net Chat Uygulamasi!" +
                          "Kullanici adinizi giriniz: ", "utf8"))
        addresses[client] = client_address
        Thread(target=baglan_client, args=(client,)).start()

def baglan_client(client):
    """Client baglantisi saglar"""
    isim = client.recv(BUFFERSIZE).decode("utf8")
    hosgeldin = 'Hosgeldin %s! Cikmak icin {cikis} yaziniz!' %isim
    client.send(bytes(hosgeldin, "utf8"))
    msg = "%s Chat Kanalina baglandi!" %isim
    yayin(bytes(msg, "utf8"))
    clients[client] = isim
    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("{cikis}", "utf8"):
            yayin(msg, isim+": ")
        else:
            client.send(bytes("{cikis", "utf8"))
            client.close()
            del clients[client]
            yayin(bytes("%s Kanaldan cikis yapti." %isim, "utf8"))
            break

def yayin(msg, prefix=""):
    """Mesaj yayinlama fonksiyonu"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(10) # Maximum 10 baglantiya izin verir! Kullanici Sayisi Lisans vs olusturulabilir
    print("Baglanti bekleniyor...")
    ACCEPT_THREAD = Thread(target=gelen_mesaj)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()