todo_list = ["Do yoga", 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM']

print("Today:")
i = 1
for item in todo_list:
    print("{}) {}".format(i, item))
    i+=1