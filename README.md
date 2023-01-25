# Deepsky-Temp-RH-pi

Read Temperature + Relative Humidity from Sensirion SHT20 sensor and publish to MQTT broker


## Instructions

Edit the MQTT parameters in ```main.py```. 

To avoid overlapping cron job execution, use ```flock``` in crontab:

```
* * * * * /usr/bin/flock -w 0 ~/deepsky_temp_rh_pi.lock python3 ~/Deepsky-Temp-RH-pi/main.py
```

To check if your cron job is running:

```
grep CRON /var/log/syslog
```
