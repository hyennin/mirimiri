def get_next_order_id(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT order_id_seq.NEXTVAL FROM DUAL")
        result = cursor.fetchone()
        return result[0]

def insert_order(connection, customer_name, order_date, product_id, quantity, total_price):
    order_id = get_next_order_id(connection)
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO orders (order_id, customer_name, order_date, product_id, quantity, total_price, status)
            VALUES (:1, :2, TO_DATE(:3, 'yyyy-mm-dd'), :4, :5, :6, '접수완료')
        """, (order_id, customer_name, order_date, product_id, quantity, total_price))
    connection.commit()

def get_orders(connection):
    # 주문 정보 조회
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
    return orders

def update_order_status(connection, order_id, status):
    # 주문 상태 업데이트
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE orders
            SET status = :1
            WHERE order_id = :2
        """, (status, order_id))
    connection.commit()
    
def get_order_statistics(connection):
    # 상품별 주문 통계 조회
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.product_id, p.product_name, COUNT(o.order_id) as num_orders, SUM(o.quantity) as total_quantity, AVG(o.total_price) as avg_price
            FROM products p
            LEFT JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY p.product_id
        """)
        statistics = cursor.fetchall()
    return statistics

def get_products_by_name(connection, name):
    # 상품명으로 상품 조회 (인덱스를 활용하여 검색)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM products
            WHERE product_name = :1
        """, (name,))
        products = cursor.fetchall()
    return products

def process_order(connection, order_id):
    with connection.cursor() as cursor:
        # 주문 정보 조회
        cursor.execute("""
            SELECT * FROM orders
            WHERE order_id = :1
        """, (order_id,))
        order = cursor.fetchone()

        if order:
            product_id = order[3]
            quantity = order[4]
            total_price = order[5]

            # 재고량 업데이트 (기존 테이블에서 처리)
            cursor.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity - :1
                WHERE product_id = :2
            """, (quantity, product_id))

            # 주문 상태 업데이트 (기존 테이블에서 처리)
            cursor.execute("""
                UPDATE orders
                SET status = '처리완료'
                WHERE order_id = :1
            """, (order_id,))

            connection.commit()
            print(f"주문(ID: {order_id})이 처리되었습니다.")
        else:
            print("해당 주문이 존재하지 않습니다.")

def describe_table(connection, table_name):
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