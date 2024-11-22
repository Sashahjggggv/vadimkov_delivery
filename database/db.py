import asyncpg as sql


class DataBase:
    def __init__(self, host: str, database: str, password: str, user: str = 'postgres', port: str = '5432'):
        self.host = 'database-1-instance-1.c3auqueak6y4.eu-central-1.rds.amazonaws.com'
        self.port = 5432
        self.database = 'database-1'
        self.user = 'postgres'
        self.password = 'Vadimkov_Delivery_Bot'

    async def create_db(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        await con.execute("CREATE TABLE IF NOT EXISTS users("
                          "id BIGINT,"
                          "bucket BIGINT[] default Null)")

        await con.execute("CREATE TABLE IF NOT EXISTS settings("
                          "work_time INT[],"
                          "price REAL)")

        await con.execute("CREATE TABLE IF NOT EXISTS categories("
                          "category_name VARCHAR,"
                          "category_id SERIAL)")

        await con.execute("CREATE TABLE IF NOT EXISTS goods("
                          "good_name VARCHAR,"
                          "good_id SERIAL,"
                          "description VARCHAR default 'Немає опису',"
                          "price BIGINT,"
                          "amount BIGINT,"
                          "category_id BIGINT)")

        await con.execute("CREATE TABLE IF NOT EXISTS orders("
                          "user_id BIGINT,"
                          "order_id SERIAL,"
                          "courier BIGINT DEFAULT Null,"
                          "address VARCHAR,"
                          "comment VARCHAR,"
                          "contact VARCHAR,"
                          "bucket BIGINT[],"
                          "price BIGINT,"
                          "status INT,"
                          "delivered_time TIMESTAMP DEFAULT Null)")

        await con.execute("CREATE TABLE IF NOT EXISTS couriers("
                          "id BIGINT,"
                          "orders_completed BIGINT DEFAULT 0,"
                          "earned REAL DEFAULT 0)")

        await con.execute("CREATE TABLE IF NOT EXISTS stats("
                          "earned REAL DEFAULT 0)")

    async def insert_settings(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        data = await con.fetch("SELECT price FROM settings")
        if len(data) == 0:
            await con.execute("INSERT INTO settings(work_time, price) VALUES($1, $2)", [10, 22], 0)
            await con.execute("INSERT INTO stats(earned) VALUES($1)", 0)

        await con.close()

    async def fetch(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch(query, *args)
        await con.close()
        return data

    async def insert(self, user_id, username):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("INSERT INTO users(id, username) VALUES($1, $2)", user_id, username)
        await con.close()
        return data

    async def fetch_all(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM users")
        await con.close()
        return data

    async def check_user(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM users WHERE id = $1", user_id)
        await con.close()
        if len(data) == 0:
            await self.add_user(user_id)
            return True
        else:
            return False


    async def add_user(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        await con.execute("INSERT INTO users(id) VALUES($1)", user_id)
        await con.close()

    async def delete_user(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        await con.execute("DELETE FROM users WHERE id = $1", user_id)
        await con.close()

    async def get_user(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        info = await con.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return info

    async def get_all_users(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT id FROM users")
        await con.close()
        return data

    async def get_price(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT price FROM settings")
        await con.close()
        return data['price']


    async def change_price(self, price):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute(f"UPDATE settings SET price = $1", price)
        await con.close()

    async def get_work_time(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow(f"SELECT work_time FROM settings")
        await con.close()
        return data['work_time']

    async def add_order(self,
                        user_id: int,
                        address: str,
                        contact: str,
                        comment: str,
                        bucket: list,
                        price: str,
                        courier: int = None,
                        status: int = 0):

        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute(f"INSERT INTO orders(user_id, courier, address, comment, contact, bucket, price, status) "
                          f"VALUES($1, $2, $3, $4, $5, $6, $7, $8)",
                          user_id, courier, address, comment, contact, bucket, price, status)

        order_id = await con.fetchrow("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1")
        await con.close()
        print(order_id)
        return order_id['order_id']


    async def get_order_by_id(self, order_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM orders WHERE order_id = $1", order_id)
        await con.close()
        return data

    async def get_payed_order_by_user_id(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM orders WHERE user_id = $1 AND status != 0", user_id)
        await con.close()
        return data

    async def execute(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute(query, *args)
        await con.close()

    async def fetchrow(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow(query, *args)
        await con.close()
        return data

    async def set_order_time(self, order_id, time):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("UPDATE orders SET delivered_time = $1 WHERE order_id = $2", time, order_id)
        await con.close()
        return data

    async def get_orders_by_date(self, d, m, y, courier=None):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        if courier is None:
            data = await con.fetch("SELECT * FROM orders WHERE "
                                   "EXTRACT(DAY FROM delivered_time) = $1 AND "
                                   "EXTRACT(MONTH FROM delivered_time) = $2 AND "
                                   "EXTRACT(YEAR FROM delivered_time) = $3 AND status = 3", int(d), int(m), int(y))
        else:
            data = await con.fetch("SELECT * FROM orders WHERE "
                                   "EXTRACT(DAY FROM delivered_time) = $1 AND "
                                   "EXTRACT(MONTH FROM delivered_time) = $2 AND "
                                   "EXTRACT(YEAR FROM delivered_time) = $3 AND "
                                   "courier = $4 AND status = 3", int(d), int(m), int(y), courier)

        await con.close()
        return data

    async def set_courier_for_order(self, order_id, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE orders SET courier = $1 WHERE order_id = $2", courier_id, order_id)
        await con.close()

    async def get_random_addr(self):
        """
        Роялті було хорошим варіантом.
        :return:
        """
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT address FROM orders")
        await con.close()
        return data

    async def check_if_courier(self, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM couriers WHERE id = $1", courier_id)
        await con.close()
        if len(data) == 0:
            return False
        else:
            return True

    async def add_earn_courier(self, earned, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE couriers SET earned = earned + $1 WHERE id = $2", earned, courier_id)
        await con.close()

    async def get_free_tasks(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM orders WHERE status = 1")
        await con.close()
        return data

    async def if_courier_is_available(self, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT order_id FROM orders WHERE status = 2 AND courier = $1", courier_id)
        await con.close()
        return data

    async def get_orders_by_user_id(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM orders WHERE user_id = $1", user_id)
        await con.close()
        return data

    async def get_good_by_good_id(self, good_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM goods WHERE good_id = $1", good_id)
        await con.close()
        return data

    async def get_orders(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM orders")
        await con.close()
        return data

    async def add_earn_stat(self, earned):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE stats SET earned = earned + $1", earned)
        await con.close()

    async def add_completed(self, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE couriers SET orders_completed = orders_completed + 1 WHERE id = $1", courier_id)
        await con.close()

    async def get_all_categories(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM categories")
        await con.close()
        return data

    async def change_order_status(self, order_id, status):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("UPDATE orders SET status = $1 WHERE order_id = $2", status, order_id)
        await con.close()
        return data


    async def get_delivered_orders(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM orders WHERE status = 3")
        await con.close()
        return data

    async def recover_orders(self, good_id, amount):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("UPDATE goods SET amount = amount + $1 WHERE good_id = $2", amount, good_id)
        await con.close()
        return data

    async def set_time(self, start: int, end: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("UPDATE settings SET work_time = ARRAY[$1::int, $2::int]", start, end)
        await con.close()
        return data

    async def get_category_by_category_id(self, cat_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT category_name FROM categories WHERE category_id = $1", cat_id)
        await con.close()
        return data

    async def get_goods_by_category_id(self, cat_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM goods WHERE category_id = $1", cat_id)
        await con.close()
        return data

    async def add_good_to_bucket(self, cat_id: int, good_id: int, amount: int, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE users SET bucket = bucket || ARRAY[ARRAY[$1::bigint, $2::bigint, $3::bigint]] WHERE id = $4",
                          cat_id, good_id, amount, user_id)
        await con.close()

    async def subtract_amount_goods(self, good_id, value: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET amount = amount - $1 WHERE good_id = $2", value, good_id)
        await con.close()

    async def add_amount_goods(self, good_id, value: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET amount = amount + $1 WHERE good_id = $2", value, good_id)
        await con.close()

    async def get_courier(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM couriers WHERE id = $1", user_id)
        await con.close()
        return data

    async def get_couriers(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM couriers")
        await con.close()
        return data

    async def change_good_name(self, good_id, name):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET good_name = $1 WHERE good_id = $2", name,  good_id)
        await con.close()

    async def change_good_description(self, good_id, description):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET description = $1 WHERE good_id = $2", description, good_id)
        await con.close()

    async def change_good_price(self, good_id, price: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET price = $1 WHERE good_id = $2", price, good_id)
        await con.close()

    async def change_good_amount(self, good_id, amount: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE goods SET amount = $1 WHERE good_id = $2", amount, good_id)
        await con.close()

    async def delete_good(self, good_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("DELETE FROM goods WHERE good_id = $1", good_id)
        await con.close()

    """MY BUCKET"""


    async def get_bucket(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT bucket FROM users where id = $1", user_id)
        await con.close()
        return data

    async def clear_bucket(self, user_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE users SET bucket = Null WHERE id = $1", user_id)
        await con.close()

    async def add_good(self, name, description, price, amount, category_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("INSERT INTO goods(good_name, description, price, amount, category_id) VALUES($1, $2, $3, $4, $5)",
                          name, description, price, amount, category_id)
        await con.close()

    async def change_category_name(self, cat_id, name):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("UPDATE categories SET category_name = $1 WHERE category_id = $2", name, cat_id)
        await con.close()

    async def delete_category(self, cat_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("DELETE FROM categories WHERE category_id = $1", cat_id)
        await con.execute("DELETE FROM goods WHERE category_id = $1", cat_id)
        await con.close()

    async def add_category(self, name):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("INSERT INTO categories(category_name) VALUES($1)", name)
        await con.close()

    async def delete_courier(self, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("DELETE FROM couriers WHERE id = $1", courier_id)
        await con.close()

    async def add_courier(self, courier_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("INSERT INTO couriers(id, orders_completed, earned) VALUES($1, $2, $3)", courier_id, 0, 0)
        await con.close()

    async def get_stat(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM stats")
        await con.close()
        return data

    async def delete_order(self, order_id):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.execute("DELETE FROM orders WHERE order_id = $1", order_id)
        await con.close()
        return data

    async def get_settings(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM settings")
        await con.close()
        return data
