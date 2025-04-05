import socket

""" 
Function to get ip address of the app where it is hosted. so to check the connected devices over the network will
recieve the link and the app will be ran on 0.0.0.0:8000 so the connected device can verify link on same network
"""


def get_app_ip_address():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address
