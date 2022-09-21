import socket
from threading import Thread
import random

# Basic Config
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

clients = []

print("Server is currently running...")


q = [
    "What is the mass of the Sun?\n1. 2.433 × 10^28\n2. 1.989 × 10^30 kg\n3. 2.049 × 10^32",
    "Why is the sky blue?\n 1. Water from earth evaporates, condenses to form water droplets that are blue in colour\n 2. short waves of blue light are scattered more than the other colours in the spectrum\n3. Water molecules scatter blue wavelengths by absorbing the light waves, and then rapidly re-emitting the light waves in different directions",
    "What is the correct definition of time?\n1. The indefinite continued progress of existence and events in the present, and future regarded as a whole.\n2. Time is a measure of constant change in our surroundings, mostly from a specific viewpoint.\n3. Time is time which is time (I have no idea of how to answer)",
    "Which word best best the word 'Worthless'?\n1.Pseudopseudohypoparathyroidism\n2.Honorificabilitudinitatibus\n3. Floccinaucinihilipilification"
]

a = [
    "2", "2", "2", "3"
]

def clientthread(conn):
    score = 0
    conn.send("Welcome to Avner's Genius Quiz!".encode('utf-8'))
    conn.send(f"You will receive a question. The answer should be either 1, 2, or 3. There are {len(q)} questions in this quiz.".encode('utf-8'))
    conn.send("Let's see if you can be the NEXT EINSTEIN. All the best!".encode('utf-8'))
    index, qn, ans = get_random_question_answer(conn)

    while 1:
        try:
            msg = conn.recv(2048).decode('utf-8')
            if msg:
                if str(msg) == ans:
                    score += 1
                    conn.send(f"Amazing! Your current score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect Answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
            else:
                remove(conn)
        except: continue

def get_random_question_answer(conn):
    r_index = random.randint(0, len(q) - 1)
    r_qn = q[r_index]
    r_ans = a[r_index]
    conn.send(r_qn.encode('utf-8'))

    return r_index, r_qn, r_ans

def remove_question(i):
    q.pop(i)
    a.pop(i)

def remove(conn):
    if conn in clients:
        clients.remove(conn)

while True:
    conn, addr = server.accept()
    clients.append(conn)

    new_thread = Thread(target=clientthread, args=(conn, addr))
    new_thread.start()