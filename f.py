#Program for oversikt over foring av fisk i merder.
import pymssql

server = "192.168.15.15\\IT22" # ip adresse eller servernavn og instanse 

user = "sa" # databasebruker 

password = "123QWEr" 

database = "db_ta_T23" 
conn = pymssql.connect(server, user, password) 

conn.autocommit(True) 

cursor = conn.cursor() 

sqlsetning = "use " + database 

cursor.execute(sqlsetning ) 

sqlsetning = "IF OBJECT_ID('dbo.antallForing', 'U') IS NULL CREATE TABLE antallForing (antallForingnr INT NOT NULL IDENTITY PRIMARY KEY, Merder_som_er_matet VARCHAR(8000) )" 
cursor.execute(sqlsetning) 

sqlsetning = "IF OBJECT_ID('dbo.kgForLager', 'U') IS NULL CREATE TABLE kgForLager (kgForLagernr INT NOT NULL IDENTITY PRIMARY KEY, antall VARCHAR(8000))" 
cursor.execute(sqlsetning) 

sqlsetning = "IF OBJECT_ID('dbo.antallForinger', 'U') IS NULL CREATE TABLE antallForinger (antallForingernr INT NOT NULL IDENTITY PRIMARY KEY, antall_foringer_daglig VARCHAR(8000))" 
cursor.execute(sqlsetning) 

sqlsetning = "IF OBJECT_ID('dbo.antallMerder', 'U') IS NULL CREATE TABLE antallMerder (antallMerdernr INT NOT NULL IDENTITY PRIMARY KEY, antall VARCHAR(8000))" 
cursor.execute(sqlsetning) 

sqlsetning = "IF OBJECT_ID('dbo.MerderInfo', 'U') IS NULL CREATE TABLE MerderInfo (Merdenummer INT NOT NULL IDENTITY PRIMARY KEY, merde_nummer VARCHAR (8000), antall_fisker VARCHAR(8000), antall_Foring VARCHAR (8000))" 
cursor.execute(sqlsetning) 


antallForinger = 2
kgForLager = 50000.0
maksKgLager = 70000
prosentGrense = 20
antallMerder = 6
#Listen merder inneholder antall fisk i merden og hvor mye for det er beregnet per fisk per foring
merder = [[200000,0.2],[160000,0.3],[160000,0.3],[130000,0.4],[130000,0.4],[130000,0.4]]

while True:
    print(f'1: Registrer en foring')
    print(f'2: Registrer antall foringer per dag')
    print(f'3: Registrere antall merder')
    print(f'4: Registrering av fisk')

    print(f'8: Justering av forlager')
    print(f'9: List ut informasjon')
    print(f'0: Avslutt')
    print(f'Valg: ')
    valg = input()
    if valg  == '1':
        conn = pymssql.connect(server, user, password, database) 
        foringAntall = conn.cursor(as_dict=True) 
        print(f'Registrering av foring')
        print(f'Hvilken merde er foret 1-{antallMerder}?')
        m =  int(input())
        forBrukt = merder[m-1][0]*merder[m-1][1]
        kgForLager = float(kgForLager) - forBrukt

        sqlsetning = f"INSERT INTO antallForing (Merder_som_er_matet) values ('{m}')"
        foringAntall.execute(sqlsetning) 
        conn.commit() 
        
        if kgForLager <= maksKgLager*prosentGrense:
            print('Lageret for fiskefôr er snart tomt. Du må bestille mer')

            

    if valg == '2':
        print(f'Justering av antall foringer per dag. Antall foringer resigtrert i dag er {antallForinger}.')
        print(f'Nytt antall: ')
        antallForinger = input()
        foringerAntall = conn.cursor(as_dict=True) 
        sqlsetning = f"INSERT INTO antallForinger (antall_foringer_daglig) values ('{antallForinger}')"
        foringerAntall.execute(sqlsetning) 
        conn.commit() 
    if valg == '3':
        print(f'Justering av antall merder i anlegget. Antall merder resigtrert i dag er {antallMerder}.')
        print(f'Nytt antall: ')
        antallMerder = input()
        merderAntall = conn.cursor(as_dict=True) 
        sqlsetning = f"INSERT INTO antallMerder (antall) values ('{antallMerder}')"
        merderAntall.execute(sqlsetning) 
        conn.commit() 
    if valg == '4':

        print(f'Registrering av fisk')
        print('Antall fisk totalt i meren:')
        antallFisk = input()
        print('Mengde i Kg hvor mye for til fisken per foring: ')
        kg = input()
        print(f'Merde nr 1-{antallMerder}:')
        merdeNr = (input())
        #merder[merdeNr-1] = [antallFisk,kg]


       # sql = "UPDATE merdeInfo SET merde_nummer = ('{merderNr}')"
        merderAntall = conn.cursor(as_dict=True) 
        sqlsetning = f"SELECT * from MerderInfo WHERE merde_nummer = '{merdeNr}'"
        #sqlsetning = "SELECT merde_nummer from merderInfo WHERE merde_nummer = ('{merderNr}')" 

        merderAntall.execute(sqlsetning) 
        print (merderAntall.fetchone())
        if merderAntall.fetchone() == None:
            test = conn.cursor(as_dict=True) 
            sqlsetning = f"INSERT INTO MerderInfo (merde_nummer, antall_fisker, antall_Foring) values ('{merdeNr}','{antallFisk}', '{kg}')"
            test.execute(sqlsetning) 

        else:
            teste = conn.cursor(as_dict=True) 
            sqlsetning = f"UPDATE MerderInfo SET antall_fisker = '{antallFisk}', antall_Foring = '{kg}' WHERE merde_nummer = '{merdeNr}'"
            teste.execute(sqlsetning) 

        
       # infomerde = conn.cursor(as_dict=True)                        
        #sqlsetning = f"INSERT INTO MerderInfo (merde_nummer, antall_fisker, antall_Foring) values ('{merdeNr}','{antallFisk}', '{kg}')"
        #infomerde.execute(sqlsetning) 
        #conn.commit() 
    if valg == '8':
        print(f'Justering av for på lager. Antall for resigtrert i dag er {kgForLager} Kg.')
        print(f'Nytt antall: ')
        kgForLager = input()
    if valg == '9':
        print(f'Antall foringer per dag: {antallForinger}')
        print(f'Antall merder : {antallMerder}')
        print(f'Antall kg for på lager: {kgForLager}')
        print(f'Størrelse på lager i Kg: {maksKgLager}')
        print(f'Prosentgrense for bestilling av for: {prosentGrense}')
        input()
    if valg == '0':
        break



conn.close() 
