f = open('C:/Users/craig/Documents/Atom Projects/XML & Webservices/lab1/updates.txt', 'r')
x = f.readlines()

'''
This for loop will run over the lines in the file and print them to the console.

'''

output = '{'

print(type(x))
print(x)

for item in x:
    #   "line1": "item1",
    output = output + '"line": "'+item + '",'
f.close()

output = output[:-1]

output = output + '}'

print(output)
