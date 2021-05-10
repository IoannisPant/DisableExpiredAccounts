import pyodbc
import subprocess


# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

#Connection to DB
server = '' 
database = '' 
username = '' 
password = '' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Get expired accounts for Docenti 
cursor.execute("SELECT [sAMAccountName] ,CONVERT(DATE, left([accountExpires],16), 102) as accountExpires, GETDATE(),[pager] FROM [].[dbo].[] where [accountExpires] not like '1601%' and CONVERT(DATE, left([accountExpires],16),102) < GETDATE() and [pager] = 'AzureSyncedUser'  ORDER BY accountExpires;") 

#Get all rows of the query
docenti = cursor.fetchall()


#Break counter
i=0

for row in docenti :
    print(row[0])
    #row = cursor.fetchone()
    subprocess.run(['powershell.exe', '-noprofile' ,'-c', '.\Disable_expired_accounts.ps1 @("'+row[0]+'")'])

    i+=1
    #Safety first
    if i == 2:
        break

#Get expired accounts for Alumni 
cursor.execute("SELECT [sAMAccountName] ,CONVERT(DATE, left([accountExpires],16), 102) as accountExpires, GETDATE(),[pager] FROM [].[dbo].[] where [accountExpires] not like '1601%' and CONVERT(DATE, left([accountExpires],16),102) < GETDATE() and [pager] = 'AzureSyncedUser'  ORDER BY accountExpires;") 
    
#Get all rows of the query
alumni = cursor.fetchall()

#Break counter
i=0

for row in alumni :
    print(row[0])
    subprocess.run(['powershell.exe', '-noprofile' ,'-c', '.\Disable_expired_accounts.ps1 @("'+row[0]+'")'])
    i+=1
    #Safety first
    if i == 2:
        break
