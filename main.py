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

def create_sku_id(choices):
    colors = {"紅": "01", "橙": "02", "黃": "03", "粉紅": "04",
              "青": "05", "藍": "06", "紫": "07", "綠": "08",
              "灰": "09", "黑": "10", "白": "11", "咖啡": "12"}
    for c in choices:
        print(colors[c])

def compute(a,b,c):
    if (4*a*c)>b**2:
        return "Your equation has no root"
    elif a==0:
        x = -c/b
        return x
    else:
        d = ((b**2)-(4*a*c))**0.5
        x1 = (-b+d)/(2*a)
        x2 = (-b-d)/(2*a)
        return x1,x2

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    #create_sku_id(['紅', '橙', '青', '藍', '綠', '灰', '黑'])
    #a,b,c = map(float,input("輸入a,b,c: ").split())

    #print(compute(a,b,c))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
