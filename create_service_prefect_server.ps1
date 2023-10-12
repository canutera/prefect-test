New-Service -Name "PrefectServer" -BinaryPathName "start_prefect_server.bat" -DisplayName "Prefect Server" -StartupType "Automatic"
Start-Service "PrefectServer"
