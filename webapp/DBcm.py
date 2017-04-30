import mysql.connector
class ConnectionError(Exception):
	pass

class CredentialsError(Exception):
	pass

class SQLError(Exception):
	pass

class UseDatabase:
	def __init__(self, config:dict)-> None:
		self.configuration = config

	def __enter__(self)->'Cursor':
		try:
			self.Conn=mysql.connector.connect(**self.configuration)
			self.Cursor=self.Conn.cursor()
			return self.Cursor
		except mysql.connector.errors.InterfaceError as e:
			raise ConnectionError(e)
		except mysql.connector.errors.ProgrammingError as e:
			raise CredentialsError(e)


	def __exit__(self, exc_type, exc_value, exc_trace) ->None:
		self.Conn.commit()
		self.Cursor.close()
		self.Conn.close()
		if(exc_type is mysql.connector.errors.ProgrammingError):
			raise SQLError(exc_value)
		elif exc_type:
			raise exc_type(exc_value)

