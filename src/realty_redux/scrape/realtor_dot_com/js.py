import os

for script in os.scandir(os.path.join(os.path.dirname(__file__), "js")):
    with open(script.path, "r") as f:
        name = os.path.splitext(script.name)[0]
        locals()[name] = f"{f.read()};return {name}();"