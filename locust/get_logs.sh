sshpass -p "toxic" scp sw704e18@192.168.1.101:~/logs .
sshpass -p "doggoeyes" scp bottom@192.168.1.100:~/logs .

cat logs/*.dat >> logs/combined.dat