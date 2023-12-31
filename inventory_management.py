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

def get_products_by_name(connection, name):
	# 상품명으로 상품 조회
	with connection.cursor() as cursor:
		cursor.execute("""
			SELECT * FROM products
			WHERE product_name LIKE '%' || :1 || '%'
		""", (name,))
		products = cursor.fetchall()
	return products