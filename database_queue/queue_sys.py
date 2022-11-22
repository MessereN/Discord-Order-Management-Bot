import pickle

class Node:

	def __init__(self, data, prev = None, next_one = None):

		self.data = data
		self.prev = prev
		self.next = next_one


class Queue:

	def __init__(self, head = None, tail = None):

		self.head = head
		self.tail = tail
		self.__items = []


	def enqueue(self, new_data):

		if self.head is None:
			self.head = Node(new_data)
			self.tail = self.head
			return

		before_last = self.tail
		self.tail = Node(new_data)
		self.tail.prev = before_last
		before_last.next = self.tail


	def dequeue(self):

		removed = None

		if self.head is None:
			print("Queue is empty")
			return removed

		elif self.head == self.tail:
			removed = self.head.data
			self.head = None
			self.tail = None
			return removed


		else:

			removed = self.head
			self.head = removed.next
			self.head.prev = None

		return removed.data



	def remove_look(self, look_for):

		info = self.head


		while info is not None:

			if look_for in info.data:

				q_order = info.data

				if info == self.head and info == self.tail:
					self.head = None
					self.tail = None

				elif info == self.head:

					info.next.prev = None
					self.head = info.next

				elif info == self.tail:
					self.tail = info.prev
					self.tail.next = None


				else:
					info.prev.next = info.next
					info.next.prev = info.prev

				return q_order

			info = info.next

		return None


	def print_(self):

		info = self.head

		self.__items = []

		while info is not None:

			self.__items.append(info.data)
			info = info.next

		return self.__items
