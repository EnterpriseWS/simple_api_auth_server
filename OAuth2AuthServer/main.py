import controller

# ------------------------------------------------------
# Use main.py to run on any ASGI server
# Example for manually run hypercorn with shell command:
#   $ hypercorn main:app --bind 127.0.0.1:8080
# ------------------------------------------------------
app = controller.app
