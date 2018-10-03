import sys
import getopt
import socket
import ipaddress
from datetime import datetime
from tkinter import *
import time
target_ip = ""
target_port = ""
def pscan(server,port,s):
    try:
        s.connect((server,port))
        return True
    except:
        return False

def retrieve_ip():
    target_ip = tbox.get("1.0", "end")
    target_ip = target_ip[:-1]
    target_port = tbox1.get("1.0", "end")
    target_port = target_port[:-1]
    print("""
    Checking your ports...
          ,,__
        c''   )?
          ''''    """)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    today = str(datetime.strftime(datetime.today(), '%d %b %Y'))
    #Get the input from cmd
    ###############################Check if it is one or more hosts
    hosts = []
    if "," in target_ip:
        hosts = target_ip.split(",")
    #Checks for a file
    elif ".txt" in target_ip:
        hosts = open("ips.txt").read().splitlines()
        # print(lines)
    elif "/" in target_ip:
        hosts = ipaddress.ip_network(str(target_ip))
        print(hosts)
    else:
        hosts.append(target_ip)
    ###############################Check if the it is one or multiple ports
    #Checks for comma separated ports
    ports = []
    if "," in target_port:
        ports = target_port.split(",")
    #Checks for a range of ports
    elif "-" in target_port:
        s_e = target_port.split("-")
        ports = range(int(s_e[0]), int(s_e[1]))
    #Else it is just one port
    else:
        ports.append(target_port)

    html_list = ["<style>table {font-family: arial, sans-serif;border-collapse: collapse;width:30%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style><h1>Steven's Amazing Port Scan</h1><h3>Run at: " + today + "</h3>"]
    #Scan and print to console
    for h in hosts:
        target_ip = h
        print("Host: " + str(h))
        html_list.append("</table>")
        html_list.append("<table><tr><td style='font-weight:bold'>Host: " + str(h) + "</td></tr>")
        for p in ports:
            q = pscan(target_ip,int(p),s)
            # print(q)
            if q == True:
                status = "Open"
            else:
                status = "Closed"
            print(" Port: " + str(p) + " Status: " +status)
            html_list.append("<tr><td>" + str(p) + "</td><td>" + status+ "</td></tr>")
    f = open("scan_" + today + ".html",'w')
    f.write(''.join(html_list))
    f.close()
    print("______________________FINISHED____________________________")
    print("scan_" + today + ".html created.")
root = Tk()
root.title("Steven's Amazing Scanner")
root.geometry("500x400")
ip_label = Label(text="IP's")
tbox = Text(root, height=2, width=30)
ip_label.pack()
tbox.pack()
port_label = Label(text="Ports")
tbox1 = Text(root, height=2, width=30)
port_label.pack()
tbox1.pack()
buttonCommit=Button(root, height=1, width=10, text="Submit", command=lambda: retrieve_ip())
buttonCommit.pack()
root.mainloop()
