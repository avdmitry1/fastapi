import random


def retry(n):
	def decorator(func):
		def wrapper(*args, **kwargs):
			for i in range(1, n + 1):
				try:
					print(f'Try {i}')
					result = func(*args, **kwargs)
					return result
				except Exception as e:
					print(f'Error {e}')
			print(f'Func didnt happen after {n} chances')

		return wrapper

	return decorator


@retry(3)
def unstable():
	if random.random() < 0.6:
		raise ValueError('Something wrong')
	print('Everything fine')


unstable()
