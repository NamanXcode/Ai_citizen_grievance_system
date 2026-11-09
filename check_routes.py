import day54

print("Loaded application from:", day54.__file__)
print("\nRegistered routes:")

for route in day54.app.routes:
    print(
        getattr(route, "methods", None),
        getattr(route, "path", None)
    )