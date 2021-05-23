# AV_SCANNER

UPDATED: 23-05-2021 (IST)

Dependencies:
```
	Python3.7>above
	pywebview
	python-crontab
	pyinstaller (for freezing only)
	py2app 		(for freezing only)
	vcredit for windows (automatic installation)
	webruntime (automatic installation)
	cron (needs to be installed in linux depending on os used)
```

## Installation
- Windows  : Simply run the setup.exe
	
- Linux : From terminal run the installer.sh,afterwars launch the av_scanner program

## Running from source 
Run `python3 -m pip install -r requirements.txt` to install dependencies
Then `python3 gui.py` will run the application

## Technologies Used
```
	Python3 (main program core)
	Autoit (scheduling tasks in windows)
	Javascript/html/css (Stylization and GUI)
```

By installing the requirements.txt found at src you will be able to start development of the application
For exporting 32 bit binaries please freeze the application on 32bit OS'es.

For periodic scan crontab feature has been integrated with the application but this requires you to install cron on the desired system

- [Linux cron](https://opensource.com/article/17/11/how-use-cron-linux)
- [windows cron](https://blog.e-zest.com/tutorial-setting-up-cron-job-task-scheduler-in-windows)
- [Mac cron](https://betterprogramming.pub/how-to-execute-a-cron-job-on-mac-with-crontab-b2decf2968eb)

	 
## Preparing MACOS executable

For MaCOS since Mac hardware is hard to get the only way to freeze for MAC is ro run the freezer on MAC for this
follow the below steps:

1) Go to src
2) install requirements with `python3 -m pip install -r requirements.txt`
3) run  `py2applet --make-setup av_scanner.py`
4) run `python setup.py py2app`
5) After the successful completion of the following command inside the dist folder there will be our Xcode compiled binary.


## PRE ADDED VIRUS DEFINITIONS:
(All filenames marked with such files will get flagged)
- virus.txt
- malware
- virus
- a.txt

To add more entries to the database open the scan.db file using an sql editor (https://sqlitebrowser.org/)
and add the entries to the InfectedFiles Table and restart the application.

Regards,
Surya

If you have any querys do contact me either at freelancer or mail me
Adios!