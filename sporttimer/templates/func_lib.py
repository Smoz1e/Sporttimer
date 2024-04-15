import datetime

        #0 номер порядковый, 1 номер стартовый, 2 время старта, 3 ФИ, 4 клуб, 5 год, 6 разряд
start_inf=[[1,101,datetime.datetime(2024,1,28,11,00,00) , 'Шамшурина', 'Уктусские', 2007,1],[2,102, datetime.datetime(2024,1,28,11,00,15), 'Вшивцева', 'Укт',2008,2]]
        #номер кт, номер участника, время на кт              КТ - контрольная точка
time_inf=[[2,101, datetime.datetime(2024,1,28,11,15,00)], [1,101,datetime.datetime(2024,1,28,11,23,30)], [1,102,datetime.datetime(2024,1,28,11,23,00)],[2,102,datetime.datetime(2024,1,28,11,16,00)]]
        #номер кт, название кт, дистанция
kt_inf=[[1,1, 3000],[2,2, 2000]]
time_inf.sort(key=lambda x:x[0])
n_kt=2
kt=2 #это НЕ порядковый номер точки
n_part=2 #кол-во участников

kt_inf.sort(key=lambda x:x[2])
for i in range(n_kt):
    kt_inf[i][0]=i+1
def finish_tab(start_inf, time_inf, kt):
    result=[]
    for i in range(n_part):
        inf_s=start_inf[i]
        inf_t=time_inf[(kt-1)+n_part+i]
        delta_time=inf_t[2]-inf_s[2]
                #0 место, 1 порядковый номер,2 фи, 3 время, 4 проигрышь, 5 год, 6 разряд, 7 клуб
        res_inf=[0, inf_s[1], inf_s[3], delta_time,0, inf_s[5], inf_s[6], inf_s[4]]
        result.append(res_inf)
    result.sort(key=lambda x:x[3])
    lider=result[0][3]
    for i in range(1,n_part+1):
        result[i-1][0]=i
        result[i-1][4]=result[i-1][3]-lider
    return result
print(finish_tab(start_inf,time_inf, 1))