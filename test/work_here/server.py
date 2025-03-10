import socket

# ตั้งค่าพอร์ตและโฮสต์ของ SIP Server
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5060

# สร้าง UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_HOST, SERVER_PORT))

print(f"📡 SIP Server is running on {SERVER_HOST}:{SERVER_PORT}")

while True:
    try:
        # รับข้อมูลจาก client (SIP request)
        data, addr = sock.recvfrom(1024)
        request = data.decode()
        print(f"📥 Received SIP request from {addr}:\n{request}")

        if request.startswith("REGISTER"):
            # ตอบกลับ 200 OK
            response = f"""SIP/2.0 200 OK
Via: SIP/2.0/UDP {addr[0]}:{addr[1]}
From: <sip:jeng@{addr[0]}>
To: <sip:jeng@{addr[0]}>;tag=12345
Call-ID: 12345678@{addr[0]}
CSeq: 1 REGISTER
Contact: <sip:jeng@{addr[0]}>
Expires: 3600
Content-Length: 0

"""
            sock.sendto(response.encode(), addr)
            print("✅ Sent SIP 200 OK response")

    except Exception as e:
        print(f"❌ Error: {e}")
