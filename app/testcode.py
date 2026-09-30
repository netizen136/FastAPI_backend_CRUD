def numbers():
    print("First")
    yield 1

    # print("Second")
    # yield 2

    print("Third")
    yield 3

    print("Fourth")
    return "zindahunyaar"


gen = numbers()
print(gen)
next(gen)  # Output: First
# print(next(gen))  # Output: First, 1  
# print("gen :", gen)
print("//")  
print(next(gen))  # Output: Second, 2
# print(next(gen))  # Output: Third, 3
# print(next(gen))  # Output: Fourth, 4
# print(next(gen))  # Raises StopIteration
next(gen)  
print("//")     
# print(gen)  
