### On init application (after verifying that all scripts work well !)
We want the script on_init.sh to be runned on system init. To do so, there are multiple choices but, as we wanted to keep it simple and lightweight, we are going to change the /etc/rc.local file to execute our file at the begining. 

To do so we only have to add one line to the /etc/rc.local (need sudoers) before the exit 0:

```
sudo /bin/bash /home/pi/solar_pi0_ws_otaa/03-run/raspberry/on_init.sh
```

### TO DO:
### improve the on_init script and, then, push it in bin/bash
### deactivate wifi and every ssh method(more lightweight) at the end and only connect when you want to access the mqtt to read more updates
