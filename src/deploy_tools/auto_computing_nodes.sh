#!/bin/sh
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: auto_computing_nodes.sh 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  4, 2015
 #  Time: 22:58:08
 #  Description: 
###############################################################################

if [ "$EUID" -ne 0 ]; then
    echo Not root.
    exit 1
fi

if (($# != 4)); then
    exit 1
fi


NODE_ADDR=$1
NODE_NUM_PORTS=$2
MASTER_ADDR=$3
MASTER_PORT=$4

# ssh key
rm -rf /root/.ssh
mkdir /root/.ssh
echo '-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA5lkM0KM/6jI/JSbO2OYbD+tT7RDRGTMGqBy7V2vFKP4Jf9fq
nY7VruuSD/0a7vJPTEGGFPk3oEMiIqwAv6wokseHcUz9nRG06RfQ4KM4eLz5MBKg
dACrwCH1kZQa1GpySfuSU8tp1qjHplthCxd0X9WkntHJw+6J2kBpf49j4r/wLbSR
lG15+ggteI1NjjnLzPXV4p7LG0uDX+lvcUabPzi4eYH14XI8dh6Ln2ACS0QBVBLc
s9buU2KZ6WfAQJUIB6BzvIIKRG5PVFRuPf91esREv4mfgeA2BD/sWz7ITNivr3h+
3yTramhQ9Gjjeki4sM7DWmd3sndp2KqMwI+5DQIBIwKCAQATvn1w+AzK7l0vEfR4
/cfOKh0i8tAYGlEHGGfUSxDmQakK9T/+4Ft1ZKYeoKqJgnvTVhLOmQTEmAo9fHUX
vkye3ecJtiRd65Mp7Bk303nedpkEHtqNmahSTA28BWFiqgnL07wVz5tbis9IxgEA
82G/Ek/wWx/sOQSAa+vJGutN8wgpNBebgXpEyhDCsqOkNxLEALlzui6s53opQK5d
hgDoTMBJR6Y6adv9jKiXcq+AcszDZ++JOC3FZOFpF7ciPd4/vZrVYcOghUMRzaud
t9Og0i9MSvo4x3zLG+XpUdElt12/+X/j0DcqgwGRxVcs3qDX/G2oZQhkmC0e9JG8
LDfLAoGBAP+Fq5vv6PC0IsMtCEDETTNvoex0cjZND4YOBIaGn8tnHT/dkGylfgAl
X/i+B9cPG7vJIUWkqoocOQO5mtNw77FVdhZYzdxoTGt1tPRE/7gJJ1A7hGIqCPGG
gcdHTDQzTGE6w1tILkRJ9IHAjk9sKhvdenr9WHUEKn1T4v5Sj4pxAoGBAObHU+I4
80wjWqbBYOz4v2gZS3XSsHRCWhbF8kv84MVB8V/vraCSdosYADlPyNZhl5tN36x4
8k44O1BluD7q04sf26RU6kOLZIAO6qfI9G3ICMy0moDBapSReKrHOAwMMQi1APo1
JCOF0LzkhvBX+UhQ00kFyaDDXYjGTOov/E5dAoGBAK83FpbQZTdW80QBn0JauJhM
jEpeejPdEfWF9HmA4poa0jpsC0MvptuHV8CCToTXKPXLvwsvFdsMCdarKFZ5U+dQ
i30Jsbu1O7dmp/f0zJtz/bNcAwF76OAhuBOemqdzohbJNYBsAnf4MqIdo2mpQXIx
eI7Zm730OmSRSzIMujMLAoGAVbfAEjJo/wXRNp+ZB4+XjRC1oMqZT8Dfog8COXsu
6i5vmKl7ASB1LFlfKzrkMl7DSFAf4Pm5Fb0dWGBLv5kMvqVu1qMycNwAwdmnnWfl
wmA9yGBWpNogRc+h2QgqwqVxTGB8tLSnBeE+5xMNjHhyiJMMphgXsL2XxRZ0Vvvh
Xu8CgYEAiLuclHOycFD0H1YP6dXmyVDdTRq5a5Kzd5thtdXnrW93nlUXrTJpOhBe
DWLkck0oBYEbOgGlUEobS16ZxEc3xoT2F7Xy+eyHaNb6hxLl2HZVh1CtSEyFsXgP
EC8ulbi8hoXSChPHHGPyClwA6yzyAI4vZvmXkEZw3PQdcbAaD5Y=
-----END RSA PRIVATE KEY----- 
' > /root/.ssh/id_rsa

echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA5lkM0KM/6jI/JSbO2OYbD+tT7RDRGTMGqBy7V2vFKP4Jf9fqnY7VruuSD/0a7vJPTEGGFPk3oEMiIqwAv6wokseHcUz9nRG06RfQ4KM4eLz5MBKgdACrwCH1kZQa1GpySfuSU8tp1qjHplthCxd0X9WkntHJw+6J2kBpf49j4r/wLbSRlG15+ggteI1NjjnLzPXV4p7LG0uDX+lvcUabPzi4eYH14XI8dh6Ln2ACS0QBVBLcs9buU2KZ6WfAQJUIB6BzvIIKRG5PVFRuPf91esREv4mfgeA2BD/sWz7ITNivr3h+3yTramhQ9Gjjeki4sM7DWmd3sndp2KqMwI+5DQ== root@iZ25t4aq69iZ' > /root/.ssh/id_rsa.pub

echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCj/55YC9PSsKaIQ6xY/oSMEj38N2xayvUj+Em1Kv5BtSibERNZzSOF3VYtYArvnMcN2aYJ0xd3PLuPCXfulEffU7bEJB5lsg9UUTAR5Kt6ScA2hD4KIhUNzmH1Kdq/4YR1cGesioegZH5uwKSLX5OwdsUqeSfu03sIrQtBbCeeq7ZsJpnNc8IJ49skZ+c0fHtOuiSm8HOBlReAO1b9md6HyrtoNj27iL7kKRbysvNGiBAjo/GL8vpq3ajNJBBUcsQEzQvR+35kRw5n0cR+4O6TB7iy/DxG1C7+55haspqTOcVVLpWpuGh+vaLZh7AfJTJtUWh2glh/0NIgWLJ2SzrZ jamis@Jamiss-MacBook-Air.local' > /root/.ssh/authorized_keys

cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

chmod 600 /root/.ssh/authorized_keys



# install python3 and node.js
yum -y install readline-devel sqlite-devel zlib-devel openssl-devel nodejs tmux > /dev/null
wget http://test-10001818.file.myqcloud.com/Python-3.4.3.tar.xz
tar xvf Python-3.4.3.tar.xz > /dev/null
cd Python-3.4.3
./configure > /dev/null
make > /dev/null
make altinstall > /dev/null
ln -s /usr/local/bin/python3.4 /usr/local/bin/python3
cd ..
rm -rf Python-3.4.3
rm -f Python-3.4.3.tar.xz

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm -f get-pip.py 

# install computing node
wget http://test-10001818.file.myqcloud.com/Distributed-Image-Search-Engine-ds.zip
unzip Distributed-Image-Search-Engine-ds.zip > /dev/null
rm Distributed-Image-Search-Engine-ds.zip

cd Distributed-Image-Search-Engine-ds/src/computing_node/
wget http://test-10001818.file.myqcloud.com/index

# substitude computing node running parameters
line_no=$(grep -n "local_addr = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/local_addr\ =\ \\\"${NODE_ADDR}\\\"/" computing_node.py

line_no=$(grep -n "master_addr = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/master_addr\ =\ \\\"${MASTER_ADDR}\\\"/" computing_node.py

line_no=$(grep -n "master_port = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/master_port\ =\ ${MASTER_PORT}/" computing_node.py

START_PORT=10001
PORTS=""
for ((i = 0; i < $NODE_NUM_PORTS; ++i)); do
    PORTS="$PORTS$((START_PORT + i)), "
done
PORTS="[ $PORTS ]"

echo $PORTS

line_no=$(grep -n "http_ports = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/http_ports\ =\ ${PORTS}/" computing_node.py


