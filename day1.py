problem =  input("Enter your problem:")
if  problem == "fire" or problem == "gas leak":
    print("priority: Critical")
elif problem == "water supply":
    print("Priority: High")
elif problem == "street light":
    print("Priority: Medium")
else:
    print("Priority: Low")