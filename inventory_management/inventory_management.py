def get_next_product_id(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT product_id_seq.NEXTVAL FROM DUAL")
        result = cursor.fetchone()
        return result[0]

def insert_product(connection, product_name, price, stock_quantity):
    product_id = get_next_product_id(connection)
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO products (product_id, product_name, price, stock_quantity)
            VALUES (:1, :2, :3, :4)
        """, (product_id, product_name, price, stock_quantity))
    connection.commit()

def update_stock(connection, product_id, quantity):
    # 재고량 업데이트
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - :1
            WHERE product_id = :2
        """, (quantity, product_id))
    connection.commit()

def get_products(connection):
    # 상품 정보 조회
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    return products

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