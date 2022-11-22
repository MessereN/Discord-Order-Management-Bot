import sqlite3
import pickle
from queue_sys import Queue


#DATABASE OPERATIONS

def clear_db(queues: str):


	conn = sqlite3.connect("./database_queue/queues.db")

	c = conn.cursor()

	new_q = Queue()
	new_q_obj = pickle.dumps(new_q)


	if queues == "acc":
		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q_obj, 1))

		conn.commit()
		c.close()
		conn.close()

		return new_q.print_()


	elif queues == "div":
		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q_obj, 2))

		conn.commit()
		c.close()
		conn.close()

		return new_q.print_()

	elif queues == "acc_div":
		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q_obj, 3))

		conn.commit()
		c.close()
		conn.close()

		return new_q.print_()


	elif queues == "all":


		new_q2 = Queue()
		new_q2_obj = pickle.dumps(new_q2)

		new_q3 = Queue()
		new_q3_obj = pickle.dumps(new_q3)

		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q_obj, 1))
		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q2_obj, 2))
		c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (new_q3_obj, 3))

		conn.commit()
		c.close()
		conn.close()

		return [new_q.print_(), new_q2.print_(), new_q3.print_()]


	else:
		c.close()
		conn.close()
		return None


def add_to_queue_at_db(queue_num: int, info: list):

	conn = sqlite3.connect("./database_queue/queues.db")
	c = conn.cursor()
	c.execute("""SELECT * FROM queue""")


	for i in range(queue_num):

		row = c.fetchone()

	obj = pickle.loads(row[1])

	obj.enqueue(info)

	insert_obj = pickle.dumps(obj)

	c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (insert_obj, queue_num))

	conn.commit()
	c.close()
	conn.close()

	return obj.print_()



def dequeue_from_queue_at_db(queue_num: int):


	conn = sqlite3.connect("./database_queue/queues.db")
	c = conn.cursor()
	c.execute("""SELECT * FROM queue""")


	for i in range(queue_num):

		row = c.fetchone()

	obj = pickle.loads(row[1])

	element_removed = obj.dequeue()

	insert_obj = pickle.dumps(obj)

	c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (insert_obj, queue_num))

	conn.commit()
	c.close()
	conn.close()

	return [element_removed, obj.print_()]


def look_and_remove_from_queue_at_db(queue_num: int, member: str):


	conn = sqlite3.connect("./database_queue/queues.db")
	c = conn.cursor()
	c.execute("""SELECT * FROM queue""")


	for i in range(queue_num):

		row = c.fetchone()

	obj = pickle.loads(row[1])

	element_look_for = obj.remove_look(member)

	insert_obj = pickle.dumps(obj)

	c.execute("""UPDATE queue SET queue_obj = ? WHERE queue_system = ?""", (insert_obj, queue_num))

	conn.commit()
	c.close()
	conn.close()

	return [element_look_for, obj.print_()]


def display_queue_from_db(queue: str):

	conn = sqlite3.connect("./database_queue/queues.db")
	c = conn.cursor()
	c.execute("""SELECT * FROM queue""")


	if queue == "acc":

		row1 = c.fetchone()
		obj = pickle.loads(row1[1])
		c.close()
		conn.close()
		return obj.print_()



	elif queue == "div":

		for i in range(2):
			row2 = c.fetchone()

		obj = pickle.loads(row2[1])

		c.close()
		conn.close()
		return obj.print_()


	elif queue == "acc_div":

		for i in range(3):
			row3 = c.fetchone()

		obj = pickle.loads(row3[1])

		c.close()
		conn.close()
		return obj.print_()


	else:

		rows = c.fetchall()

		obj = pickle.loads(rows[0][1])
		obj2 = pickle.loads(rows[1][1])
		obj3 = pickle.loads(rows[2][1])

		c.close()
		conn.close()

		return [obj.print_(), obj2.print_(), obj3.print_()]
