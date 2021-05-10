cls
Import-Module ActiveDirectory

$check = $args[0] # sAMAccountName Argument from python

#File Log Date
$FileLogdate = (Get-Date -f yyyy-MM-dd)

#File Log Location
$filename = "C:\Disabled Accounts\" + "Disabled-" + $FileLogdate + ".log"

#Checking procedure starts
Write-Host "Checking the user with accountName:" $check
$pager = "AzureSyncedUser"

try {
#Taking properties of the user
$user = Get-ADUser -Filter "sAMAccountName -eq '$check'" -SearchBase "DC=,DC=,DC=" -Properties * 

}catch {
    #Record if the user not found
    Write-Warning -Message "User $($check) does not found." | Out-File -FilePath $filename -encoding ASCII -append
} 

    #Write-Output " $($user.pager) User with accountname: $($user.SAMAccountName) and displayName: $($user.displayName) `n" 
    
    #execute termination of the account if the user is still enabled
    if($user.Enabled = $true){
        #Writing log file
        Write-Output "Disabling user with accountname: $($user.SAMAccountName) and displayName: $($user.displayName) `n" | Out-File -FilePath $filename -encoding ASCII -append 
        #Command that disables the expired account
        Disable-ADAccount -Identity $user.SAMAccountName
    }else {
        #Else Do nothing and write log file
         Write-Output "Already disabled accountname: $($user.SAMAccountName) and displayName: $($user.displayName) `n" | Out-File -FilePath $filename -encoding ASCII -append
    }


#Testing purposes
Start-Sleep -Seconds 10



