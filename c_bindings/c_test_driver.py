import imp
print(imp.find_module("spam"))


import spam
status = spam.system("ls -l")