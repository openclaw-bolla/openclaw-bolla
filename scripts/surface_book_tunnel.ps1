Start-Sleep -Seconds 30
while ($true) {
    ssh -N -R 2222:localhost:22 -p 2200 bolla@192.168.178.29 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3
    Start-Sleep -Seconds 15
}
