sshpass -p "toxic" scp -r sw704e18@192.168.1.101:~/logs .
sshpass -p "doggoeyes" scp -r bottom@192.168.1.100:~/logs .

cat logs/*.dat >> logs/combined.dat