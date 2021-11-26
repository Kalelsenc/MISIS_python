# Сделайте так, чтобы число секунд отображалось в виде дни:часы:минуты:секунды.
print('Введите количество секунд:')
seconds=int(input())

days=0
hours=0
minutes=0

if (seconds//86400!=0):
    days=seconds//86400
    seconds=seconds-days*86400
    
if (seconds//3600!=0):
    hours=seconds//3600
    seconds=seconds-hours*3600
    
if (seconds//60!=0):
    minutes=seconds//60
    seconds=seconds-minutes*60
    
print('В '+str(days*86400+hours*3600+minutes*60+seconds)+' секундах: '+str(days)+' дней '+str(hours)+' часов '+str(minutes)+' минут '+str(seconds)+' секунд')

#Напишите калькулятор который запрашивает на входе две переменные и знак, и в соответствии с знаком ( + - * / ) выводит результат
print('Введите первое число:')
num1=float(input())
print('Введите второе число:')
num2=float(input())
print('Введите знак')
sign=input()
print('Результат:')

if (sign=='+'):
    print(num1+num2)
elif (sign=='-'):
    print(num1-num2)
elif (sign=='*'):
    print(num1*num2)
elif (sign=='/'):
    print(num1/num2)
else:
    print('Вы ввели что-то не то')