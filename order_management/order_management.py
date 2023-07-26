import cx_Oracle

connection = cx_Oracle.connect("mirimiri/mirim@localhost:1521/mirimstore")

def insert_order(order_id, customer_name, order_date, product_id, quantity, total_price, status):
    # 주문 정보 삽입
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO orders (order_id, customer_name, order_date, product_id, quantity, total_price, status)
            VALUES (:1, :2, TO_DATE(:3, 'yyyy-mm-dd'), :4, :5, :6, :7)
        """, (order_id, customer_name, order_date, product_id, quantity, total_price, status))
    connection.commit()
    connection.close()

def get_orders():
    # 주문 정보 조회
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
    connection.close()
    return orders

def update_order_status(order_id, status):
    # 주문 상태 업데이트
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE orders
            SET status = :1
            WHERE order_id = :2
        """, (status, order_id))
    connection.commit()
    
def get_order_statistics():
    # 상품별 주문 통계 조회
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.product_id, p.product_name, COUNT(o.order_id) as num_orders, SUM(o.quantity) as total_quantity, AVG(o.total_price) as avg_price
            FROM products p
            LEFT JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.product_id, p.product_name
        """)
        statistics = cursor.fetchall()
    connection.close()
    return statistics

def get_products_by_name(name):
    # 상품명으로 상품 조회 (인덱스를 활용하여 검색)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM products
            WHERE product_name = :1
        """, (name,))
        products = cursor.fetchall()
    connection.close()
    return products

def describe_table(table_name):
    # 테이블 구조 조회
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, NULLABLE FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table_name.upper()}'")
        columns = cursor.fetchall()

    if columns:
        print(f"=== {table_name.upper()} 테이블 구조 ===")
        print("컬럼 이름 | 데이터 타입 | NULL 허용 여부")
        print("--------------------------")
        for col in columns:
            print(f"{col[0]} | {col[1]} | {'O' if col[2] == 'Y' else 'X'}")
    else:
        print("해당 테이블이 존재하지 않습니다.")

    connection.close()
