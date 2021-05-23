import os,zipfile,io,sys,re,sqlite3
import hashlib,datetime,psutil,time,math,logging
from queue import Queue
logging.basicConfig(filename='scan.log', encoding='utf-8', level=logging.DEBUG)

def listpartitions():
	logging.info('Listing Partitions')
	drps = psutil.disk_partitions()
	drives = [(dp.device,dp.mountpoint) for dp in drps if dp.fstype == 'NTFS' or dp.fstype == 'ext4' or dp.fstype == 'FAT32']
	logging.debug('Found '+str(len(drives))+' Usable Partitions')
	return drives


def walk(directory,q,window = ''):
	connection = sqlite3.connect("scan.db")
	cursor = connection.cursor()
	zip_files = []
	files_count = 0
	vuln_count = 0
	scn_dte = str(datetime.date.today())
	dtime = str(datetime.datetime.now().time())
	scn_type = "folder"
	vuln_files = []

	
	rows = cursor.execute("SELECT COUNT(*) FROM Scan_Reports").fetchall()
	print(rows)
	if (len(rows) == 0):
		scan_id = 1
	else:
		scan_id = int(rows[0][0])+1

	print(scan_id)
	time.sleep(3)

	for p, d, f in os.walk(directory):
		for file in f:
			files_count += 1

			if window:
				try:
					if files_count%math.pow(2,(len(list(map(int, str(files_count))))-1)) == 0:
						window.evaluate_js('document.getElementById("display_scan_stat").innerHTML = "Scanning: '+ str(os.path.join(p[0:10]+"~/", file[0:10]))+'<br> '+str(files_count)+' Scanned</p>";')
				except:
					pass

			if q.qsize() > 0 :
				proc = q.get()
				if proc['info'] == "scan_start":
					scn_type = proc['data']['type']
					print("Started scanning....")
					logging.debug('Starting Scan of :'+ str(directory))

				elif proc['info'] == "scan_pause":
					print("Scan Paused..")
					logging.debug('Scan Paused for :'+ str(directory))

					while True:
						curfew = q.get()
						if curfew['info'] =='scan_resume':
							print("Scan Resuming...")
							logging.debug('Resuming Scan for :'+ str(directory))
							break
						elif curfew['info'] == "scan_stop":
							print("Scan terminated...")
							logging.debug('Scan Terminated :'+ str(directory))
							return

						time.sleep(100)

				elif proc['info'] == "scan_stop":
					print("Scan terminated...")
					logging.debug('Scan Terminated :'+ str(directory))
					return


			if file.endswith('.zip'):
				zip_files.append(os.path.join(p, file))
			else:
				if checkifmalicious(file,cursor):
					print("flagged:" + os.path.join(p, file))
					vuln_count += 1
					vuln_files.append(os.path.join(p, file))
	
	for x in zip_files:
		y = getzipfiles(x)
		for z in y:
			if checkifmalicious((os.path.split(z)[-1]),cursor):
				print("flagged:" + z)
				vuln_count += 1
				vuln_files.append(z)

	for x in vuln_files:
		cursor.execute('INSERT INTO InfectedScannedFiles(ScanID,Filename) VALUES(?,?)',(scan_id, x,))
		connection.commit()

	etime = str(datetime.datetime.now().time())
	sql = 'INSERT INTO Scan_Reports(ScanID,ScanDate,ScanType,ScanLocation,TimeStart,TimeEnd,NumberScanned,NumberInfected) VALUES(?,?,?,?,?,?,?,?)'
	cursor.execute(sql,(scan_id,scn_dte,scn_type,directory,dtime,etime,str(files_count),str(vuln_count),))
	connection.commit()


	logging.info('Scan Finished :'+ str(directory))
	
	if window:
		window.evaluate_js("""
					swal({
		  title: 'Complete!',
		  text: 'Scan Complete',
		  icon: 'success',
		  button: 'Return',
		}).then(function(){location.href='home.html'});
			""")



def checkifmalicious(filename,cursor):
	rows = cursor.execute("SELECT * FROM InfectedFiles WHERE Filename = ?",(filename,)).fetchall()
	if (len(rows) > 0):
		logging.info('Found Virus :'+ str(filename))
		return True

	return False


def getzipfiles(zipname):
	zips = uz(open(zipname, "rb"), [zipname])
	return zips

def uz(f, parent=[]):
	result = []
	try:
		zf = zipfile.ZipFile(f)
		for e in zf.namelist():
			path=parent+[e]
			if e.lower().endswith(".zip"):
				result += uz(io.BytesIO(zf.open(e).read()), path)
			else:
				result.append("/".join(path))

	except Exception as ex:
		return result

	return result