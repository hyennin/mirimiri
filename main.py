import cx_Oracle
import traceback
from order_management.order_management import process_order, insert_order, get_orders, get_order_statistics, describe_table
from inventory_management.inventory_management import insert_product, get_products_by_name, get_products

connection = cx_Oracle.connect("mirimiri/mirim@127.0.0.1:1521/XE")

def table_exists(table_name):
    # 테이블 존재 여부 확인
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM USER_TABLES WHERE table_name = :1", (table_name.upper(),))
        result = cursor.fetchone()
        return result[0] > 0

def drop_sequences():
    # products 테이블을 위한 시퀀스 삭제
    with connection.cursor() as cursor:
        cursor.execute("DROP SEQUENCE product_id_seq")

    # orders 테이블을 위한 시퀀스 삭제
    with connection.cursor() as cursor:
        cursor.execute("DROP SEQUENCE order_id_seq")

def drop_tables():
    # products 테이블 삭제
    if table_exists("PRODUCTS"):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE products")

    # orders 테이블 삭제
    if table_exists("ORDERS"):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE orders")
            
    connection.commit()

def create_tables():
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

    # 상품명에 대한 인덱스 생성 (새로 추가한 부분)
    create_index(connection)

def create_sequences():
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

def display_menu():
    print("=== 메뉴 ===")
    print("1. 상품 정보 조회")
    print("2. 주문 정보 조회")
    print("3. 주문 통계 조회")
    print("4. 상품 정보 추가")
    print("5. 주문 정보 추가")
    print("6. 특정 상품 정보 조회")
    print("7. 주문 처리")
    print("8. 테이블 구조 조회")
    print("0. 종료")
    print("===========")

def main():
    try:
        while True:
            display_menu()

            choice = input("원하는 기능의 번호를 입력하세요: ")

            if choice == "1":
                try:
                    # 상품 정보 조회
                    print("=== 상품 정보 ===")
                    products = get_products(connection)
                    if not products:
                        print("등록된 상품이 없습니다.")
                    else:
                        print("상품 ID | 상품명 | 가격 | 재고량")
                        print("--------------------------")
                        for product in products:
                            print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")
                except Exception as e:
                    print("상품 정보 조회 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "2":
                try:
                    # 주문 정보 조회
                    print("=== 주문 정보 ===")
                    orders = get_orders(connection)
                    if not orders:
                        print("등록된 주문이 없습니다.")
                    else:
                        print("주문 ID | 고객명 | 주문일자 | 상품 ID | 수량 | 총 가격 | 상태")
                        print("----------------------------------------------")
                        for order in orders:
                            print(f"{order[0]} | {order[1]} | {order[2]} | {order[3]} | {order[4]} | {order[5]} | {order[6]}")
                except Exception as e:
                    print("주문 정보 조회 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "3":
                try:
                    # 상품별 주문 통계 조회
                    print("=== 상품별 주문 통계 ===")
                    order_statistics = get_order_statistics(connection)
                    if not order_statistics:
                        print("주문 통계 정보가 없습니다.")
                    else:
                        print("상품 ID | 상품명 | 주문 수 | 총 수량 | 평균 가격")
                        print("--------------------------------")
                        for stats in order_statistics:
                            product_id = stats[0]
                            product_name = stats[1]
                            num_orders = stats[2] if stats[2] else 0
                            total_quantity = stats[3] if stats[3] else 0
                            avg_price = stats[4] if stats[4] else 0.0
                            print(f"{product_id} | {product_name} | {num_orders} | {total_quantity} | {avg_price:.2f}")
                except Exception as e:
                    print("상품별 주문 통계 조회 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "4":
                try:
                    # 상품 정보 추가
                    print("=== 상품 정보 추가 ===")
                    product_name = input("상품명을 입력하세요: ")
                    price = float(input("가격을 입력하세요: "))
                    stock_quantity = int(input("재고량을 입력하세요: "))
                    insert_product(connection, product_name, price, stock_quantity)
                    print("상품이 성공적으로 추가되었습니다.")
                except Exception as e:
                    print("상품 정보 추가 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "5":
                try:
                    # 주문 정보 추가
                    print("=== 주문 정보 추가 ===")
                    customer_name = input("고객명을 입력하세요: ")
                    order_date = input("주문 일자를 입력하세요 (yyyy-mm-dd): ")
                    product_id = int(input("상품 ID를 입력하세요: "))
                    quantity = int(input("수량을 입력하세요: "))
                    total_price = float(input("총 가격을 입력하세요: "))
                    insert_order(connection, customer_name, order_date, product_id, quantity, total_price)
                    print("주문이 성공적으로 추가되었습니다.")
                except Exception as e:
                    print("주문 정보 추가 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "6":
                try:
                    # 상품명으로 상품 조회
                    print("=== 특정 상품 정보 조회 ===")
                    product_name = input("조회할 상품명을 입력하세요: ")
                    products = get_products_by_name(connection, product_name)
                    if not products:
                        print("해당 상품이 없습니다.")
                    else:
                        print("상품 ID | 상품명 | 가격 | 재고량")
                        print("--------------------------")
                        for product in products:
                            print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")
                except Exception as e:
                    print("특정 상품 정보 조회 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "7":
                try:
                    # 주문 처리
                    print("=== 주문 처리 ===")
                    order_id = int(input("처리할 주문의 ID를 입력하세요: "))
                    process_order(connection, order_id)
                except Exception as e:
                    print("주문 처리 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "8":
                try:
                    # 테이블 구조 조회
                    print("=== 테이블 구조 조회 ===")
                    table_name = input("조회할 테이블의 이름을 입력하세요: ")
                    describe_table(connection, table_name)
                except Exception as e:
                    print("테이블 구조 조회 중 오류가 발생했습니다.")
                    traceback.print_exc()

            elif choice == "0":
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 입력입니다. 다시 입력해주세요.")

    except Exception as e:
        print("프로그램 실행 중 오류가 발생했습니다.")
        traceback.print_exc()
    finally:
        connection.close()

if __name__ == "__main__":
    # drop_sequences()
    # create_sequences()
    # drop_tables()
    # create_tables()
    main()