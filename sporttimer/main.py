# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from func_lib import finish_tab
import datetime
#0 номер порядковый, 1 номер стартовый, 2 время старта, 3 ФИ, 4 клуб, 5 год, 6 разряд
start_inf=[[1,101,datetime.datetime(2024,1,28,11,00,00) , 'Шамшурина', 'Уктусские', 2007,1],[2,102, datetime.datetime(2024,1,28,11,00,15), 'Вшивцева', 'Укт',2008,2]]
        #номер кт, номер участника, время на кт              КТ - контрольная точка
time_inf=[[2,101, datetime.datetime(2024,1,28,11,15,00)], [1,101,datetime.datetime(2024,1,28,11,23,30)], [1,102,datetime.datetime(2024,1,28,11,23,00)],[2,102,datetime.datetime(2024,1,28,11,16,00)]]
        #номер кт, название кт, дистанция
kt_inf=[[1,1, 3000],[2,2, 2000]]
time_inf.sort(key=lambda x:x[0])
n_kt=2
kt=1 #это НЕ порядковый номер точки
n_part=2 #кол-во участников
print(finish_tab(start_inf,time_inf, 0))
#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
   # print('Hi,'+ name)  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':

    #test_func('Nastya')

