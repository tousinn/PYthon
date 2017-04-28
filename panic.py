phrase = "Dont't panic!"
plist = list(phrase)
print(phrase)
print(plist)

plist.remove('D')
plist.remove("'")
plist.remove(" ")
plist.insert(2," ")
plist.remove("p")
for i in range(6):
    plist.pop()
    
plist.extend(['a','p'])
new_phrase = ''.join(plist)
print(plist)
print(new_phrase)
