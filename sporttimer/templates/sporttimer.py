from flask import Flask
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import render_template
from flask import request
import datetime
import time


try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="sporttime",
                                  # пароль, который указали при установке PostgreSQL
                                  password="SportRus12!",
                                  host="127.0.0.1",
                                  port="5432",
                                database="sporttime_db")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    #sql_create_database = 'create database sporttime_db'
    #cursor.execute(sql_create_database)
    sql = '''
        DROP TABLE competitions
        '''
    #cursor.execute(sql)

    sql='''
    CREATE TABLE IF NOT EXISTS competitions (
    id serial,
    competitionName varchar(100),
    groupNumber int2,
    interval int2,
    numberOfParticipant int2,
    firstNumber int2,
    date timestamp
        );
    '''
    cursor.execute(sql)
    sql = '''
            DROP TABLE kps
            '''
    #cursor.execute(sql)
    sql='''
    CREATE TABLE IF NOT EXISTS kps (
    id serial,
    competitionID int2,
    kpName varchar(100),
    kpDistance int2
        );
    '''
    cursor.execute(sql)
    sql = '''
                DROP TABLE participant
                '''
    #cursor.execute(sql)
    sql='''
    CREATE TABLE IF NOT EXISTS participant (
    id serial,
    competitionID int2,
    startNumber int2,
    participantName varchar(100),
    startTime time
        );
    '''
    cursor.execute(sql)
    sql = '''
                    DROP TABLE results
                    '''
    #cursor.execute(sql)
    sql='''
    CREATE TABLE IF NOT EXISTS results (
    id serial,
    competitionID int2,
    kpID int2,
    finishNumber int2,
    startNumber int2,
    participantName varchar(100),
    result interval,
    delta interval
    );
    '''
    cursor.execute(sql)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", sql, error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
def sendCompetitionToDataBase(сompetitionName,groupNumber,interval,numberOfParticipant,firstNumber, date,distance):
    result=0
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result=-1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params =(сompetitionName,groupNumber,interval,numberOfParticipant,firstNumber,date)
    sql='''
    INSERT INTO competitions
    (competitionname,
    groupNumber,
    interval,
    numberOfParticipant,
    firstNumber,
    date) 
    VALUES (%s,%s,%s,%s,%s,%s);
    '''
    try:
        cursor.execute(sql,params)

    except (Exception, Error) as error:
        result=-2
        print(params)
        print("Ошибка при добавлении данных PostgreSQL 1: sendCompetitionToDataBase(сompetitionName,groupNumber,interval,numberOfParticipant,firstNumber, date) ", error)
    param=[сompetitionName]
    sql='''
    SELECT max(id)
    FROM competitions
    WHERE competitionname = %s
    '''
    try:
        cursor.execute(sql,param)
        res=cursor.fetchone()
        #print('1111111111111111111111111111111111111111111111111111111111111111111111')
        #print(res[0])
    except (Exception, Error) as error:
        res=1
        print("Ошибка при добавлении данных PostgreSQL 2: ", error)
    a="финиш"
    b=res[0]
    params=(b,a,distance)
    sql='''
    INSERT INTO kps (
    competitionID,
    kpName,
    kpDistance)
    VALUES (%s,%s,%s);
    '''
    try:
        cursor.execute(sql,params)
    except (Exception, Error) as error:
        result = {'res': -2, 'error': error}
        print("Ошибка при добавлении данных PostgreSQL 3: ", error)



    sql = '''
        SELECT * FROM competitions;
        '''
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
        #print(rows)


    except (Exception, Error) as error:
        result = -2
        print("Ошибка при добавлении данных PostgreSQL 4: ", error)

    sql = '''
                SELECT
        column_name,
        data_type
    FROM
        information_schema.columns
    WHERE
        table_name = 'kps';
                '''
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print('*******************************')
        #print(rows)
        #print('****************************************')


    except (Exception, Error) as error:
        result = -2
        print("Ошибка при добавлении данных PostgreSQL 5: ", error)
    if connection:
        cursor.close()
        connection.close()
    return b


def sendKPToDataBase(kpName, kpDistance, competitionID):
    result=0
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result=-1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params =(competitionID, kpName, kpDistance)
    sql='''
    INSERT INTO kps
    (competitionID,
    kpName,
    kpDistance) 
    VALUES (%s,%s,%s);
    '''
    try:
        cursor.execute(sql,params)

    except (Exception, Error) as error:
        result=-2
        print(params)
        print("Ошибка при добавлении данных PostgreSQL sendKPToDataBase: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result



def printTableRows(tableName):

    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result=-1
        print("Ошибка при подключении к базе данных PostgreSQL: printTableRows(tableName) ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    data = [tableName]
    try:
        cursor.execute('Select * FROM "kps" LIMIT 0')
        colnames = [desc[0] for desc in cursor.description]
        #print(colnames)
    except (Exception, Error) as error:
        result=-2
        print(data)
        print("Ошибка при printTableRows(tableName) PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()


def getCompetitionByID(id):
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result=-1
        print("Ошибка при подключении к базе данных PostgreSQL: printTableRows(tableName) ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params = [id]
    try:
        sql='''
        Select 
        competitionName, 
        groupNumber, 
        interval,
        numberOfParticipant, 
        firstNumber,
        date 
        FROM "competitions" 
        where id=%s 
        
        '''
        cursor.execute(sql,params)
        competition=cursor.fetchone()
        #print('************************************************************************************************************************')
        #print(competition)
        result={'competitionName':competition[0], 'groupNumber':competition[1],
                'interval':competition[2],'numberOfParticipant':competition[3], 'firstNumber':competition[4], 'date':competition[5]}

    except (Exception, Error) as error:
        result={'res':-2,'error':error}
        print("Ошибка при getCompetitionByID PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result


def timechange(a,b,c,r):
    c+=r
    b+=c//60
    c=c%60
    a+=b//60
    b=b%60
    a=a%24
    s=[a,b,c]
    return s


def sendStartTimeToDataBase(times,competitionID):
    result = 0
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params = (times,competitionID)
    sql = '''
        UPDATE competitions
        SET date=%s 
        WHERE id=%s;
        '''
    try:
        cursor.execute(sql, params)

    except (Exception, Error) as error:
        result = -2
        print(params)
        print(
            "Ошибка при добавлении данных PostgreSQL 1:  sendStartTimeToDataBase ",
            error)
    if connection:
        cursor.close()
        connection.close()
    return result



def getcompetitionByKPID(kpID):
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: printTableRows(tableName) ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params = (kpID,)
    try:

        sql = '''
        Select 
        competitionID,
        kpName,
        kpDistance
        FROM kps 
        where id=%s;

        '''
        cursor.execute(sql, params)
        competition = cursor.fetchone()
        # print('************************************************************************************************************************')
        # print(competition)
        result = {'competitionID': competition[0],'kpName':competition[1],'kpDistance':competition[2]}

    except (Exception, Error) as error:
        result = {'res': -2, 'error': error}
        print("Ошибка при getCompetitionByID PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result

def getfinishKPID(competiotionID):
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: printTableRows(tableName) ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params = (competiotionID,)
    try:

        sql = '''
        Select 
        id,
        max(kpDistance)
        FROM kps 
        WHERE competitionID=%s
        GROUP BY id;

        '''
        cursor.execute(sql, params)
        competition = cursor.fetchone()
        # print('************************************************************************************************************************')
        # print(competition)
        if competition:
            result = {'kpID': competition[0],'kpDistance':competition[1]}
        else:
            result={'res':-1,'msg':
                   f'kpID не найдено для competiotionid = {competiotionID}'}

    except (Exception, Error) as error:
        result = {'res': -2, 'error': error}
        print("Ошибка при getCompetitionByID PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result
def addResultToDataBase(competitionID,kpID,participantNumber,participantName,finshTime):
    result = 0
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)
    # sql_create_database = 'create database sporttime_db'
    # cursor.execute(sql_create_database)
    params = (competitionID, kpID, participantNumber)
    part_id=0
    sql = '''
            SELECT id FROM results
            WHERE 
            (competitionID=%s) AND 
            (kpID=%s) AND
            (startNumber = %s)
            '''
    try:
        cursor.execute(sql, params)
        row=cursor.fetchone()
        if row:
            part_id=row[0]

    except (Exception, Error) as error:
        result = -2
        print(params)
    if part_id>0:
        print('update')
        params = (participantName, finshTime, finshTime, part_id)
        sql = '''
                    UPDATE results
                    SET 
                        participantName=%s,
                        result=%s,
                        delta=%s
                    WHERE id=%s;
                    '''
        try:
            cursor.execute(sql, params)

        except (Exception, Error) as error:
            result = -2
            print(params)
            print("Ошибка при добавлении данных PostgreSQL 1: UPDATE addResultToDataBase ", error)
    else:

        params = (competitionID, kpID,participantNumber,participantName,finshTime,finshTime)
        sql = '''
            INSERT INTO results
            (competitionID, 
            kpID,
            startNumber,
            participantName,
            result,
            delta) 
            VALUES (%s,%s,%s,%s,%s,%s);
            '''
        try:
            cursor.execute(sql, params)

        except (Exception, Error) as error:
            result = -2
            print(params)
            print("Ошибка при добавлении данных PostgreSQL 1: INSERT INTO addResultToDataBase ",error)
    delta=finshTime
    param=(kpID,)
    sql='''
        SELECT * FROM results
        WHERE kpID=%s;
    '''
    try:
        cursor.execute(sql, param)
        print(cursor.fetchall())

    except (Exception, Error) as error:
        result = -2
        print(params)
        print("Ошибка  PostgreSQL 1: addResultToDataBase ",error)


    result={'delta':delta, 'finshTime':finshTime}
    if connection:
        cursor.close()
        connection.close()
    return result


def getStartTime(competitionID):
    result = 0
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)

    param=(competitionID,)
    sql='''
    SELECT date FROM competitions
    WHERE id=%s;
    
    '''
    try:

        cursor.execute(sql, param)
        start = cursor.fetchone()
        r=start[0]
        print('************************************************************************************************************************')
        print(r)
        result = {'competitionID': competitionID,'start':r}

    except (Exception, Error) as error:
        result = {'res': -2, 'error': error}
        print("Ошибка при getStartTime PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result


def getStartTimeForParticipant(competitionID, participantNumber):
    result ={}
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)

    param = (competitionID,participantNumber,)
    sql = '''
    SELECT startTime FROM participant
    WHERE competitionID=%s AND startNumber=%s;

    '''
    try:

        cursor.execute(sql, param)
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        start = cursor.fetchone()
        r=start[0]
        print('************************************************************************************************************************')
        print(f'r={start[0]}')
        result = {'competitionID': competitionID, 'startParticipantTime': r}

    except (Exception, Error) as error:
        result = {'res': -2, 'error': error,'startParticipantTime':''}
        print("Ошибка при getStartTimeForParticipant PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    return result


def getPartisipantResultsFromDataBase(kpID):
    sql = '''
        CREATE TABLE IF NOT EXISTS results (
        id serial,
        competitionID int2,
        kpID int2,
        finishNumber int2,
        startNumber int2,
        participantName varchar(100),
        result time,
        delta time
        );
        '''
    try:
        connection = psycopg2.connect(user="sporttime",
                                      # пароль, который указали при установке PostgreSQL
                                      password="SportRus12!",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="sporttime_db")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
    except (Exception, Error) as error:
        result = -1
        print("Ошибка при подключении к базе данных PostgreSQL: ", error)
    params=(kpID,)

    sql='''
        SELECT startNumber, result
        FROM results
        WHERE kpID=%s
        ORDER BY result;
     '''
    kpResults = {}
    result = []
    try:

        cursor.execute(sql, params)
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        start = cursor.fetchall()
        if start:

            #print('************************************************************************************************************************')
            #print(start)

            liderTime=start[0][1]

            for i in range(len(start)):
                delta=str(start[i][1]-liderTime)[:9]
                finish_time_td=start[i][1]
                finish_time_s=f'{finish_time_td.seconds//3600}:{(finish_time_td.seconds%3600)//60}:{(finish_time_td.seconds%3600)%60}.{finish_time_td.microseconds//10000}'
                print(f'start_time={start[i][1]} lider_time={liderTime} delta = {delta}')
                print('----------- ',finish_time_s)
                #result_i={'place':i+1,'startNumber':start[i][0],'finshResult':str(start[i][1]),'delta':delta}
                result_i = {'place': i + 1, 'startNumber': start[i][0], 'finshResult': finish_time_s, 'delta': delta}
                kpResults[str(start[i][0])]=i+1


                result.append(result_i)
            #print(f'kpResults = {kpResults}')


    except (Exception, Error) as error:
        result = [{'res': -2, 'error': error,'startParticipantTime':''}]
        print("Ошибка при getPartisipantResultsFromDataBase PostgreSQL: ", error)

    if connection:
        cursor.close()
        connection.close()
    res={'results':result,'kpRating':kpResults}
    return res

app = Flask(__name__)
@app.route('/',methods=['post','get'])
def home():

    return render_template('index.html')
@app.route('/list')
def list():
    context='Hello'
    return render_template('timer.html', context=context)



@app.route('/competitionList',methods=['post','get'])
def competitionList():
    if request.method=='GET':
        competitionName = request.args.get('competitionName', default='empty', type=str)
    else:
        competitionName=request.form.get('competitionName', default='empty',type=str)
    context='Competition: '+competitionName
    #print(context)
    d=datetime.date.today()
    startDate=d.strftime('%Y-%m-%dT11:00')
    return render_template('timer.html', context=context, startDate=startDate)

@app.route('/onlinecomplist',methods=['post','get'])
def onlinecomplist():


    return render_template('onlinecomplist.html')

@app.route('/competition',methods=['post','get'])
def competition():
    if request.method=='GET':
        competitionID = request.args.get('competitionID', default='empty', type=str)
    else:
        competitionID=request.form.get('competitionID', default='empty',type=str)
    a=getCompetitionByID(competitionID)
    context='Название соревнований: '+a['competitionName']
    groupNumber=a['groupNumber']
    interval=a['interval']
    numberOfParticipant=a['numberOfParticipant']
    firstNumber=a['firstNumber']
    date=a['date']
    #print(context)
    return render_template('startPage.html', context=context, groupNumber=groupNumber, interval=interval,
                           numberOfParticipant=numberOfParticipant, firstNumber=firstNumber,date=date, competitionID=competitionID)


@app.route('/kp',methods=['post','get'])
def kp():
    if request.method=='GET':
        kpID = request.args.get('kpID', default='empty', type=str)
    else:
        kpID=request.form.get('kpID', default='empty',type=str)
    a=getcompetitionByKPID(kpID)
    b=getCompetitionByID(a['competitionID'])
    competitionName=b['competitionName']+' '+a['kpName']+' '+'дистанция: '+str(a['kpDistance'])

    return render_template('competition.html', kpID=kpID, competitionName=competitionName)

@app.route('/onlineresults',methods=['post','get'])
def onlineresults():
    if request.method=='GET':
        competitionName = request.args.get('competitionName', default='empty', type=str)
    else:
        competitionName=request.form.get('competitionName', default='empty',type=str)
    context='Competition: '+competitionName
    #print(context)
    d=datetime.date.today()
    startDate=d.strftime('%Y-%m-%d')
    return render_template('timer.html', context=context, startDate=startDate)


@app.route('/sporttimer_api', methods=['post','get'])
def sporttimer_api():
    #printTableRows('competitions')
    result={'result':-1,'description':'Ошибка, ничего не получилось!'}
    req_json=request.get_json()
    try:
        cmd=req_json['cmd']
    except:
        cmd=''
        result = {'result': -1, 'description': 'cmd не найден'}

    if cmd=='addCompetition':
        competitionName = ''
        groupNumber = 0
        interval = 0
        numberOfParticipant = 0
        firstNumber = 0
        date = datetime.datetime.today()
        distance=0
        try:
            competitionName=req_json['competitionName']
            groupNumber=int(req_json['groupNumber'])
            interval=int(req_json['interval'])
            numberOfParticipant=int(req_json['numberOfParticipant'])
            firstNumber=int(req_json['firstNumber'])
            date=datetime.datetime.strptime(req_json['date'], '%Y-%m-%dT%H:%M')
            distance=int(req_json['distance'])
            #print(f'в date содержится: {date}')
        except (Exception, Error) as error:
            print(req_json['date'])
            print('Ошибка получения данных со страницы 556: ',error)

        res=sendCompetitionToDataBase(competitionName, groupNumber, interval, numberOfParticipant, firstNumber, date,distance)

        result = {'result': res, 'description': 'i save the date', 'comprtitionName': competitionName,
                  'groupNumber': groupNumber, 'interval': interval,
                  'numberOfParticipant': numberOfParticipant, 'firstNumber': firstNumber, 'date':date}
        try:
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user="sporttime",
                                          # пароль, который указали при установке PostgreSQL
                                          password="SportRus12!",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="sporttime_db")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL 2", error)
        if connection:
            try:
                s=[0,0,0]
                time2 = datetime.timedelta(hours=0,minutes=0,seconds=0)
                for i in range(numberOfParticipant):
                    params=(res,int(firstNumber+i),'Участник '+str(firstNumber+i)+'     ',time2)
                    sql='''
                    INSERT INTO participant
                    (competitionID,
                    startNumber,
                    participantName,
                    startTime) 
                    VALUES (%s,%s,%s,%s);
                    '''
                    cursor.execute(sql,params)
                    s = timechange(s[0],s[1],s[2],interval)
                    s2=timechange(0,0,30,15)
                    print('chek=',s)
                    time2=datetime.timedelta(hours=s[0],minutes=s[1],seconds=s[2])
            except (Exception, Error) as error:
                print("Ошибка создании списка участников PostgreSQL", error)
            cursor.close()
            connection.close()

    if cmd=='addTime':
        time1 = datetime.datetime.today()
        #print(req_json['startTime'])
        try:
            competitionID=req_json['competitionID']
            a=req_json['startTime']
            b=a.find('.')
            a=a[:b]
            time1 = datetime.datetime.strptime(a, '%Y-%m-%dT%H:%M:%S')
            # print(f'в date содержится: {time}')
        except (Exception, Error) as error:
            print(req_json['startTime'])
            print('Ошибка получения данных со страницы 610: ', error)

        res = sendStartTimeToDataBase(time1,competitionID)

        result = {'result': res, 'description': 'i save the date', 'startTime': time1}

    if cmd=='getCompetitionID':
        kpID=req_json['kpID']
        #print(kpID)
        a=getcompetitionByKPID(kpID)
        #print(a['competitionID'])
        result= {'competitionID':a['competitionID']}

    if cmd=='getCompetitionList':
        result=0
        try:
            connection = psycopg2.connect(user="sporttime",
                                          # пароль, который указали при установке PostgreSQL
                                          password="SportRus12!",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="sporttime_db")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
        except (Exception, Error) as error:
            result = -1
            print("Ошибка при подключении к базе данных PostgreSQL 2: ", error)
        if connection:
            sql = '''
                    SELECT competitionName,
                    date,
                    id
                    FROM competitions;
                    '''
            try:

                cursor.execute(sql)
                rows = cursor.fetchall()
                #print(rows)
                outputCompetitionList=[]

                for i in range(len(rows)):
                    row=rows[i]
                    date=row[1]
                    date_s=date.strftime('%d.%m.%Y')
                    finishKP_res=getfinishKPID(row[2])
                    if 'kpID' in finishKP_res:
                        finishKP=finishKP_res['kpID']
                    else:
                        finishKP=''
                    line={'competitionName':row[0],'date':date_s, 'id':row[2], 'finishKP':finishKP}
                    outputCompetitionList.append(line)
            except (Exception, Error) as error:
                print('Ошибка при получения данных с sql: ',error)

            result = outputCompetitionList
            #print(result)
            cursor.close()
            connection.close()

    if cmd=='addKP':
        kpName=''
        kpDistance=0
        competitionID=0
        try:
            kpName = req_json['kpName']
            kpDistance = req_json['kpDistance']
            competitionID = req_json['competitionID']
            # print(f'в date содержится: {date}')
        except (Exception, Error) as error:
            print('Ошибка получения данных со страницы 675: ', error)

        res = sendKPToDataBase(kpName, kpDistance, competitionID)
        result = {'result': res, 'description': 'i save the date', 'kpName': kpName,
                  'kpDistance': kpDistance, 'competitionID': competitionID,}

    if cmd=='getKPList':
        try:
            competitionID=req_json['competitionID']
        except (Exception, Error) as error:
            competitionID=1
            print('Ошибка при получения competitionID: ',error)
        result = 0
        try:
            connection = psycopg2.connect(user="sporttime",
                                          # пароль, который указали при установке PostgreSQL
                                          password="SportRus12!",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="sporttime_db")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
        except (Exception, Error) as error:
            result = -1
            print("Ошибка при подключении к базе данных PostgreSQL 2: ", error)
        if connection:
            param=(competitionID,)
            sql='''
            SELECT kpname, 
            kpdistance,
            id
            FROM kps
            WhERE competitionid=%s
            ORDER BY kpDistance;
            '''
            try:
                cursor.execute(sql,param)
                rows = cursor.fetchall()
                #print('555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555')
                #print(rows)
                outputKPList = []

                for i in range(len(rows)):
                    row = rows[i]
                    line = {'kpName': row[0], 'kpDistance': row[1],'kpID':row[2]}
                    outputKPList.append(line)
            except (Exception, Error) as error:
                print('Ошибка при получения данных с sql: ', cmd, error)

            result = outputKPList
            #print(result)
            cursor.close()
            connection.close()

    if cmd=='getParticipantList':
        try:
            competitionID=req_json['competitionID']
            kpID=0
            if 'kpID' in req_json:
                kpID=req_json['kpID']
        except (Exception, Error) as error:
            competitionID=1
            print('Ошибка при получения competitionID: ',error)
        result = 0
        try:
            connection = psycopg2.connect(user="sporttime",
                                          # пароль, который указали при установке PostgreSQL
                                          password="SportRus12!",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="sporttime_db")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
        except (Exception, Error) as error:
            result = -1
            print("Ошибка при подключении к базе данных PostgreSQL 2: ", error)
        if connection:
            kpRes = getPartisipantResultsFromDataBase(kpID)
            kpRating=kpRes['kpRating']
            kpResults=kpRes['results']
            param=(competitionID,)
            sql='''
            SELECT startNumber, 
            participantName,
            startTime
            FROM participant
            WhERE competitionid=%s;
            '''
            try:
                cursor.execute(sql,param)
                rows = cursor.fetchall()
                print('555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555')
                #print(rows)
                print(kpResults)
                outputKPList = []
                resultTime=''
                resultDelta=''

                for i in range(len(rows)):
                    row = rows[i]
                    resultTime = ''
                    resultDelta = ''
                    for j in range(len(kpResults)):
                        if kpResults[j]['startNumber']==row[0]:
                            resultTime=kpResults[j]['finshResult']
                            resultDelta=kpResults[j]['delta']
                            break
                    startTime=row[2]
                    place_s=''
                    if str(row[0]) in kpRating:
                        place_s=kpRating[str(row[0])]
                    line = {'startNumber': row[0],'place':place_s,'resultTime':resultTime,'resultDelta':resultDelta, 'participantName': row[1], 'startTime':startTime.strftime('%H:%M:%S')}
                    outputKPList.append(line)
            except (Exception, Error) as error:
                print('Ошибка при получения данных с sql: ', cmd, error)

            result = outputKPList
            #print(result)
            cursor.close()
            connection.close()

    if cmd=='stopParticipant':
        kpID = 0
        competitionID = 0
        participantNumber = 0
        participantName = 0
        finshTime = 0
        try:
            kpID = int(req_json['kpID'])
            competitionID = int(req_json['competitionID'])
            participantNumber = int(req_json['participantNumber'])
            print(req_json)
            participantName = req_json['participantName']
            finshTime = datetime.datetime.strptime(req_json['finshTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

            #print(f'в date содержится: {date}')

        except (Exception, Error) as error:
            #print(req_json['date'])
            print('Ошибка получения данных со страницы 799: ', error)

        a=getStartTime(competitionID)
        startCompetitionTime=a['start']
        b=getStartTimeForParticipant(competitionID,participantNumber)
        startParticipantTime=b['startParticipantTime']
        startParticipantTime = datetime.timedelta(hours=startParticipantTime.hour, minutes=startParticipantTime.minute, seconds=startParticipantTime.second)
        print('aaaaaaaaaa  ',startParticipantTime)

        print(f'startCompetitionTime={startCompetitionTime}')
        print(f'finishTime1={finshTime}')
        #print(startParticipantTime)
        finshTime = finshTime - startParticipantTime - startCompetitionTime
        print(f'finshTime={finshTime}')
        res = addResultToDataBase(competitionID,kpID,participantNumber,participantName,finshTime)
        participantResult=res['finshTime']
        res=0

        finshTime_str=str(finshTime)
        a=finshTime_str.find('.')
        finshTime_str=finshTime_str[:a+2]

        participantResult_str=str(participantResult)
        delta=participantResult_str
        place='X'
        answer_r=getPartisipantResultsFromDataBase(kpID)
        answer=answer_r['results']
        result = {'result': res, 'description': 'i save the date', 'competitionID': competitionID,
                  'kpID': kpID, 'participantNumber': participantNumber,
                  'participantName': participantName, 'finshTime': finshTime_str, 'participantResult':participantResult_str,'delta':delta, 'place':place}
        result=answer
    if cmd=='getParticipantPlace':
        participantNumber=0
        kpID=0

    return result






#printTableRows("competitions")
#printTableRows('kps')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)