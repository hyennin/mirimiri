import cx_Oracle
from order_management.order_management import process_order, insert_order, get_orders, get_order_statistics, get_products_by_name, describe_table
from inventory_management.inventory_management import insert_product, update_stock, get_products

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
    connection = cx_Oracle.connect("사용자이름/비밀번호@호스트:포트/서비스이름")

    while True:
        display_menu()

        choice = input("원하는 기능의 번호를 입력하세요: ")

        if choice == "1":
            # 상품 정보 조회
            print("=== 상품 정보 ===")
            products = get_products()
            for product in products:
                print(product)

        elif choice == "2":
            # 주문 정보 조회
            print("=== 주문 정보 ===")
            orders = get_orders()
            for order in orders:
                print(order)

        elif choice == "3":
            # 상품별 주문 통계 조회
            print("=== 상품별 주문 통계 ===")
            order_statistics = get_order_statistics()
            for stats in order_statistics:
                print(stats)

        elif choice == "4":
            # 상품 정보 추가
            product_id = int(input("상품 ID를 입력하세요: "))
            product_name = input("상품명을 입력하세요: ")
            price = float(input("가격을 입력하세요: "))
            stock_quantity = int(input("재고량을 입력하세요: "))
            insert_product(product_id, product_name, price, stock_quantity)

        elif choice == "5":
            # 주문 정보 추가
            order_id = int(input("주문 ID를 입력하세요: "))
            customer_name = input("고객명을 입력하세요: ")
            order_date = input("주문 일자를 입력하세요 (yyyy-mm-dd): ")
            product_id = int(input("상품 ID를 입력하세요: "))
            quantity = int(input("수량을 입력하세요: "))
            total_price = float(input("총 가격을 입력하세요: "))
            status = input("주문 상태를 입력하세요: ")
            insert_order(order_id, customer_name, order_date, product_id, quantity, total_price, status)

        elif choice == "6":
            # 상품명으로 상품 조회
            product_name = input("조회할 상품명을 입력하세요: ")
            products = get_products_by_name(product_name)
            if products:
                print("=== 상품 정보 ===")
                for product in products:
                    print(product)
            else:
                print("해당 상품이 없습니다.")

        elif choice == "7":
             # 주문 처리
            order_id = int(input("처리할 주문의 ID를 입력하세요: "))
            process_order(order_id)

        elif choice == "8":
            # 테이블 구조 조회
            table_name = input("조회할 테이블의 이름을 입력하세요: ")
            describe_table(table_name)

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 입력해주세요.")

    connection.close()

if __name__ == "__main__":
    main()
