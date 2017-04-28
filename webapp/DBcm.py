import mysql.connector
class UseDatabase:
	def __init__(self, config:dict)-> None:
		self.configuration = config

	def __enter__(self)->'Cursor':
		self.Conn=mysql.connector.connect(**self.configuration)
		self.Cursor=self.Conn.cursor()
		return self.Cursor

	def __exit__(self, exc_type, exc_value, exc_trace) ->None:
		self.Conn.commit()
		self.Cursor.close()
		self.Conn.close()

