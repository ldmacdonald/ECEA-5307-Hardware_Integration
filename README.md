# ECEA-5307-Hardware_Integration

## Setup

Enable the LCD

` sudo raspi-config`

Navigate to 'Interface Options' then 'I2C'
Select 'Yes' to enable then reboot

Documentation: https://rplcd.readthedocs.io/en/stable/getting_started.html


## Python Pip Setup
```

python -m pip install adafruit-circuitpython-matrixkeypad
python -m pip install RPi.GPIO
python -m pip install RPLCD

```
