import cx_Oracle
import traceback
from setting import *
from order_management import *
from inventory_management import *

def main():
	try:
		admin_connection = cx_Oracle.connect("system/1234@127.0.0.1:1521/XE")
		disconnect_user(admin_connection, 'mirimiri')
		delete_user(admin_connection, 'mirimiri')
		create_user(admin_connection, 'mirimiri', 'mirim')
		grant_create_view_privilege_to_user(admin_connection, 'mirimiri')
		admin_connection.close()

		connection = cx_Oracle.connect("mirimiri/mirim@127.0.0.1:1521/XE")

		drop_tables(connection)
		create_tables(connection)
		drop_sequences(connection)
		create_sequences(connection)
		create_view(connection)

		display_main()

		choice = input("시작하시려면 아무 키나 입력하세요(종료는 0): ")
		if choice == "0":
			exit()
		else:
			while True:
				display_menu()

				choice = input("원하는 기능의 번호를 입력하세요: ")

				if choice == "1":
					try:
						# 상품 정보 조회
						print("========== 상품 정보 ==========")
						products = get_products(connection)
						if not products:
							print("등록된 상품이 없습니다.")
						else:
							print("상품 ID | 상품명 | 가격 | 재고량")
							print("----------------------------------")
							for product in products:
								print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")
					except Exception as e:
						print("상품 정보 조회 중 오류가 발생했습니다.")
						traceback.print_exc()

				elif choice == "2":
					try:
						# 주문 정보 조회
						print("================== 주문 정보 ==================")
						orders = get_orders(connection)
						if not orders:
							print("등록된 주문이 없습니다.")
						else:
							print("주문 ID | 고객명 | 주문일자 | 상품 ID | 수량 | 총 가격 | 상태")
							print("--------------------------------------------------------------")
							for order in orders:
								print(f"{order[0]} | {order[1]} | {order[2]} | {order[3]} | {order[4]} | {order[5]} | {order[6]}")
					except Exception as e:
						print("주문 정보 조회 중 오류가 발생했습니다.")
						traceback.print_exc()

				elif choice == "3":
					try:
						# 상품별 주문 통계 조회
						print("=========== 상품별 주문 통계 ===========")
						order_statistics = get_order_statistics(connection)
						if not order_statistics:
							print("주문 통계 정보가 없습니다.")
						else:
							print("상품 ID | 상품명 | 주문 수 | 총 수량 | 총 가격")
							print("-----------------------------------------------")
							for stats in order_statistics:
								product_id = stats[0]
								product_name = stats[1]
								num_orders = stats[2] if stats[2] else 0
								total_quantity = stats[3] if stats[3] else 0
								total_price = stats[4] if stats[4] else 0.0
								print(f"{product_id} | {product_name} | {num_orders} | {total_quantity} | {total_price}")
					except Exception as e:
							print("상품별 주문 통계 조회 중 오류가 발생했습니다.")
							traceback.print_exc()

				elif choice == "4":
					try:
						# 상품 정보 추가
						print("========== 상품 정보 추가 =========")
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
						print("========== 주문 정보 추가 ==========")
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
						print("========== 특정 상품 정보 조회 ==========")
						product_name = input("조회할 상품명을 입력하세요: ")
						products = get_products_by_name(connection, product_name)
						if not products:
							print("해당 상품이 없습니다.")
						else:
							print("상품 ID | 상품명 | 가격 | 재고량")
							print("----------------------------------")
							for product in products:
								print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")
					except Exception as e:
						print("특정 상품 정보 조회 중 오류가 발생했습니다.")
						traceback.print_exc()

				elif choice == "7":
					try:
						# 주문 처리
						print("========== 주문 처리 ==========")
						order_id = int(input("처리할 주문의 ID를 입력하세요: "))
						process_order(connection, order_id)
					except Exception as e:
						print("주문 처리 중 오류가 발생했습니다.")
						traceback.print_exc()

				elif choice == "8":
					try:
						# 총 주문 통계 조회
						print("========== 총 주문 통계 ==========")
						statistics = all_order(connection)
						if statistics:
							for stat in statistics:
								product_id = stat[0]
								product_name = stat[1]
								num_orders = stat[2]
								total_quantity = stat[3]
								total_price = stat[4]
								if product_id is None and product_name is None:
									print("총 상품 전체 합계")
								elif product_id is None:
									print(f"상품명: {product_name} (전체 합계)")
								elif product_name is None:
									print(f"상품 ID: {product_id} (전체 합계)")
								else:
									print(f"상품 ID: {product_id} | 상품명: {product_name}")
								print("총 주문 수 | 총 주문 수량 | 총 가격")
								print("-------------------------------------")
								print(f"{num_orders} | {total_quantity} | {total_price}")
								print("=====================================")
						else:
							print("주문 통계 정보가 없습니다.")
					except Exception as e:
						print("총 주문 통계 조회 중 오류가 발생했습니다.")
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
		if connection:
			connection.close()

if __name__ == "__main__":
  main()