# YouTube Video İndirici Başlatıcı
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
python youtube_downloader.py
Read-Host "Çıkmak için Enter'a basın"



