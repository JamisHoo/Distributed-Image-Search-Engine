#!/bin/sh
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: Distributed Image Search Engine
 #  Filename: auto_config.sh
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  4, 2015
 #  Time: 22:58:08
 #  Description: this script does some fundamental installation and settings
###############################################################################

if [ "$EUID" -ne 0 ]; then
    echo Not root.
    exit 1
fi

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

chmod 600 /root/.ssh/id_rsa
chmod 600 /root/.ssh/authorized_keys



# install python3 and node.js
yum -y install readline-devel sqlite-devel zlib-devel openssl-devel nodejs tmux nload > /dev/null
wget http://imagenet.oss-cn-beijing.aliyuncs.com/Python-3.4.3.tar.xz
tar xvf Python-3.4.3.tar.xz > /dev/null
cd Python-3.4.3
./configure > /dev/null
make > /dev/null
make altinstall > /dev/null
ln -s /usr/local/bin/python3.4 /usr/local/bin/python3
cd ..
rm -rf Python-3.4.3
rm -f Python-3.4.3.tar.xz

wget http://imagenet.oss-cn-beijing.aliyuncs.com/get-pip.py
python get-pip.py
rm -f get-pip.py 

rm $0


