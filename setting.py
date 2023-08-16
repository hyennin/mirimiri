import cx_Oracle

def disconnect_user(admin_connection, username):
  with admin_connection.cursor() as cursor:
    try:
      # 사용자의 세션 정보 조회
      cursor.execute("SELECT SID, SERIAL# FROM V$SESSION WHERE USERNAME = :1", (username.upper(),))
      session_info = cursor.fetchone()

      if session_info:
        sid, serial = session_info
        # 세션 끊기
        cursor.execute(f"ALTER SYSTEM KILL SESSION '{sid}, {serial}'")
        print(f"사용자 {username}의 세션을 끊었습니다.")
      else:
        print(f"{username} 사용자의 세션을 찾을 수 없습니다.")
    except cx_Oracle.DatabaseError as e:
      print(f"세션 끊기 중 오류 발생: {e}")

def delete_user(admin_connection, username):
  with admin_connection.cursor() as cursor:
    try:
      # 유저가 존재하는지 확인
      cursor.execute("SELECT COUNT(*) FROM ALL_USERS WHERE USERNAME = :1", (username.upper(),))
      result = cursor.fetchone()

      if result[0] > 0:
        # 세션 끊고 사용자 삭제
        disconnect_user(admin_connection, username)
        cursor.execute(f"DROP USER {username} CASCADE")
        print(f"{username} 사용자가 삭제되었습니다.")
      else:
        print(f"{username} 사용자가 존재하지 않습니다.")
    except cx_Oracle.DatabaseError as e:
      print(f"사용자 삭제 중 오류 발생: {e}")

def create_user(admin_connection, username, password):
  with admin_connection.cursor() as cursor:
    try:
      cursor.execute(f"CREATE USER {username} IDENTIFIED BY {password}")
      cursor.execute(f"GRANT CONNECT, RESOURCE TO {username}")  # 필요한 권한 부여
      print(f"{username} 사용자가 생성되었습니다.")
    except cx_Oracle.DatabaseError as e:
      print(f"사용자 생성 중 오류 발생: {e}")

def grant_create_view_privilege_to_user(admin_connection, username):
  with admin_connection.cursor() as cursor:
    try:
      cursor.execute(f"GRANT CREATE VIEW TO {username}")
      print(f"사용자 {username}에게 CREATE VIEW 권한이 부여되었습니다.")
    except cx_Oracle.DatabaseError as e:
      print(f"권한 부여 중 오류가 발생했습니다: {e}")

def table_exists(table_name, connection):
  # 테이블 존재 여부 확인
  with connection.cursor() as cursor:
    cursor.execute("SELECT count(*) FROM USER_TABLES WHERE table_name = :1", (table_name.upper(),))
    result = cursor.fetchone()
    return result[0] > 0

def drop_sequences(connection):
  # products 테이블을 위한 시퀀스 삭제
  with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM USER_SEQUENCES WHERE sequence_name = 'PRODUCT_ID_SEQ'")
    result = cursor.fetchone()
    if result[0] > 0:
      cursor.execute("DROP SEQUENCE product_id_seq")

  # orders 테이블을 위한 시퀀스 삭제
  with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM USER_SEQUENCES WHERE sequence_name = 'ORDER_ID_SEQ'")
    result = cursor.fetchone()
    if result[0] > 0:
      cursor.execute("DROP SEQUENCE order_id_seq")

def drop_tables(connection):
  # products 테이블 삭제
  if table_exists("PRODUCTS", connection):
    with connection.cursor() as cursor:
      cursor.execute("DROP TABLE products")

  # orders 테이블 삭제
  if table_exists("ORDERS", connection):
    with connection.cursor() as cursor:
      cursor.execute("DROP TABLE orders")
            
  connection.commit()

def create_tables(connection):
  # 상품 정보 테이블 생성
  with connection.cursor() as cursor:
    cursor.execute("""
      CREATE TABLE products (
        product_id NUMBER PRIMARY KEY,
        product_name VARCHAR2(100),
        price NUMBER,
        stock_quantity NUMBER
      )
    """)

  # 주문 정보 테이블 생성
  with connection.cursor() as cursor:
    cursor.execute("""
      CREATE TABLE orders (
        order_id NUMBER PRIMARY KEY,
        customer_name VARCHAR2(100),
        order_date DATE,
        product_id NUMBER,
        quantity NUMBER,
        total_price NUMBER,
        status VARCHAR2(20)
      )
    """)

  # 상품명에 대한 인덱스 생성
  create_index(connection)

def create_sequences(connection):
  with connection.cursor() as cursor:
    # products 테이블을 위한 시퀀스 생성
    cursor.execute("""
      CREATE SEQUENCE product_id_seq
        START WITH 1
        INCREMENT BY 1
        NOMAXVALUE
    """)

    # orders 테이블을 위한 시퀀스 생성
    cursor.execute("""
      CREATE SEQUENCE order_id_seq
        START WITH 1
        INCREMENT BY 1
        NOMAXVALUE
      """)

def create_index(connection):
  # 상품명에 대한 인덱스 생성
  with connection.cursor() as cursor:
    cursor.execute("CREATE INDEX idx_product_name ON products(product_name)")
  connection.commit()

def create_view(connection):
  with connection.cursor() as cursor:
    try:
      cursor.execute("""
        CREATE OR REPLACE VIEW order_statistics_view AS
        SELECT p.product_id, p.product_name, COUNT(o.order_id) AS num_orders, SUM(o.quantity) AS total_quantity, SUM(o.total_price) AS total_price
        FROM products p
        LEFT JOIN orders o ON p.product_id = o.product_id
        GROUP BY ROLLUP(p.product_id, p.product_name)
      """)
      print("뷰가 성공적으로 생성되었습니다.")
    except cx_Oracle.DatabaseError as e:
      print(f"뷰 생성 중 오류가 발생했습니다: {e}")

def display_main():
  print("----------------------------------------------")
  print("|     __ __  _       _  __ __  _       _     |")
  print("|    |  \  \<_> _ _ <_>|  \  \<_> _ _ <_>    |")
  print("|    |     || || '_>| ||     || || '_>| |    |")
  print("|    |_|_|_||_||_|  |_||_|_|_||_||_|  |_|    |")
  print("----------------------------------------------")

def display_menu():
  print("============== 메뉴 ==============")
  print("1. 상품 정보 조회")
  print("2. 주문 정보 조회")
  print("3. 상품별 주문 통계 조회")
  print("4. 상품 정보 추가")
  print("5. 주문 정보 추가")
  print("6. 특정 상품 정보 조회")
  print("7. 주문 처리")
  print("8. 총 주문 통계 조회")
  print("0. 종료")
  print("==================================")