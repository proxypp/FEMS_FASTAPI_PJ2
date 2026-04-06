import socket
import pyodbc

HOST = "211.224.136.28"
PORT = 3308

# 1. 포트 연결 확인
print(f"=== 1. 네트워크 연결 확인 ({HOST}:{PORT}) ===")
try:
    s = socket.create_connection((HOST, PORT), timeout=5)
    print("포트 열림 - 서버 도달 가능")
    s.close()
except Exception as e:
    print(f"포트 연결 실패: {e}")

# 2. pyodbc 직접 연결
print("\n=== 2. pyodbc 연결 테스트 ===")
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={HOST},{PORT};"
    "DATABASE=fems_test;"
    "UID=swit;"
    "PWD=Swit@##!1234;"
    "TrustServerCertificate=yes;"
    "Encrypt=no;"
)
try:
    conn = pyodbc.connect(conn_str, timeout=10)
    print("pyodbc 연결 성공!")
    conn.close()
except Exception as e:
    print(f"pyodbc 연결 실패: {e}")
