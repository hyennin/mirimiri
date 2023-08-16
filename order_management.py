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
			SELECT p.product_id, p.product_name, COUNT(o.order_id) as num_orders, SUM(o.quantity) as total_quantity, SUM(o.total_price) as total_price
			FROM products p
			LEFT JOIN orders o ON p.product_id = o.product_id
			GROUP BY p.product_id, p.product_name
			ORDER BY p.product_id
		""")
		statistics = cursor.fetchall()
	return statistics

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

			# 재고량 업데이트
			cursor.execute("""
				UPDATE products
				SET stock_quantity = stock_quantity - :1
				WHERE product_id = :2
			""", (quantity, product_id))

			# 주문 상태 업데이트
			cursor.execute("""
				UPDATE orders
				SET status = '처리완료'
				WHERE order_id = :1
			""", (order_id,))

			connection.commit()
			print(f"주문(ID: {order_id})이 처리되었습니다.")
		else:
			print("해당 주문이 존재하지 않습니다.")

def all_order(connection):
	# 총 주문 통계 조회
	with connection.cursor() as cursor:
		cursor.execute("""
			SELECT 
				product_id,
				product_name,
				num_orders,
				total_quantity,
				total_price
			FROM order_statistics_view
		""")
		statistics = cursor.fetchall()
	return statistics