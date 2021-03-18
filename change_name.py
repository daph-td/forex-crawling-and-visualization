import os

path = '/Users/admin/Environments/currencypairs/official/'

num = 0
for i in os.listdir(path):
    if '0 copy' in i:
        position = i.index('0')
    
    old_name = path + i
    new_name = i[:position] + str(num) + '.py'
    print(old_name)
    print(new_name)
    num = num + 1

    os.rename(old_name, new_name)