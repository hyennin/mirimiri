import cx_Oracle

connection = cx_Oracle.connect("mirimiri/mirim@localhost:1521/mirimstore")

def insert_product(product_id, product_name, price, stock_quantity):
    # 상품 정보 삽입
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO products (product_id, product_name, price, stock_quantity)
            VALUES (:1, :2, :3, :4)
        """, (product_id, product_name, price, stock_quantity))
    connection.commit()
    connection.close()

def update_stock(product_id, quantity):
    # 재고량 업데이트
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - :1
            WHERE product_id = :2
        """, (quantity, product_id))
    connection.commit()
    connection.close()

def get_products():
    # 상품 정보 조회
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
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

# 연결 닫기
connection.close()
