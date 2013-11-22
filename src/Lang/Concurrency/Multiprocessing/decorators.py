import sys
import traceback
from functools import wraps
from multiprocessing import Process, Queue

def processify(func):
	"""
	Decorator to run a function as a process.
	
	Note that every argument and the return value must be picklable!!
	The created process is joined, so the code does not run in parallel.
	
	Usage:
	
	@processify
	def test_function():
		return os.getpid()
	
	Found at:
	https://gist.github.com/schlamar/2311116
	"""
	
	def process_func(q, *args, **kwargs):
		try:
			ret = func(*args, **kwargs)
		except Exception:
			ex_type, ex_value, tb = sys.exc_info()
			error = ex_type, ex_value, "".join(traceback.format_tb(tb))
			ret = None
		else:
			error = None
		
		q.put((ret, error))
	
	# register original function with different name
	# in sys.modules so it is pickable
	process_func.__name__ = func.__name__ + "processify_func"
	setattr(sys.modules[__name__], process_func.__name__, process_func)
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		q = Queue()
		p = Process(target=process_func, args=[q] + list(args), kwargs=kwargs)
		p.start()
		p.join()
		ret, error = q.get()
		
		if error:
			ex_type, ex_value, tb_str = error
			message = "%s (in subprocess)\n%s" % (ex_value.message, tb_str)
			raise ex_type(message)
		
		return ret
	return wrapper
