
#Basic usage:
from logger import log

log.d("This is a debug message")
log.i("This is an info message")
log.w("This is a warning message")
log.e("This is an error message")
log.c("This is a critical message")

#--------------------------------------------------------------------------------

#Function logging with decorators
@log("debug")
def example_function(x, y):
    return x + y

example_function(5, 10)

#-------------------------------------------------------------------------------

#Error handling
@log("error")
def faulty_function():
    return 1 / 0  # Intentional error

try:
    faulty_function()
except ZeroDivisionError:
    log.e("Handled division by zero error")

#------------------------------------------------------------------------------

#Log files
"""
scriptname_debug.log
scriptname_info.log
scriptname_warning.log
scriptname_error.log
scriptname_critical.log
"""

#------------------------------------------------------------------------------

#Example Code
from logger import log

@log("debug")  # Logs function entry, exit, and errors at DEBUG level
def example_function(x, y):
    log.i("Performing addition")
    return x + y

@log("error")  # Logs at ERROR level
def faulty_function():
    log.w("About to divide by zero")
    return 1 / 0  # Intentional error

# Running the functions
example_function(5, 10)

try:
    faulty_function()
except ZeroDivisionError:
    log.e("Handled division by zero error")

