# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import hashlib


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def check_id(str):
    list = [1, 2, 1, 2, 1, 2, 4, 1]
    serial_list = []
    new_list = []

    for c in str:
        serial_list.append(int(c))
        if not c.isnumeric():
            return True
            break

    if len(serial_list) != 8:
        return True

    for i in range(8):
        temp = serial_list[i] * list[i]
        new_list.append(int(temp / 10) + int(temp % 10))

    s = sum(new_list)
    if s % 10 != 0 or (serial_list[6] == 7 and (s - new_list[6] % 10 == 0 or s - new_list[6] % 10 == 9)):
        return True

    return False
def create_productID(brand,i):
    string = bytes(brand + str(i),'utf8')
    return base64.encode(string)
def create_product_id(num):
    try:
        num += 1
        if 9999 > num >= 1000:
            return str(num)
        elif 1000 > num >= 100:
            return '0'+str(num)
        elif 100 > num >= 10:
            return '00'+str(num)
        else:
            return '000'+str(num)
    except:
        return '0001'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #print(check_id("5312539"))
    i=1
    string = "89123456"
    print(create_product_id(0))
    print(create_product_id(123))
    print(1321)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
