import webview,core,os,sqlite3
import sys, getopt,json,logging
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread, Event

logging.basicConfig(filename='info.log', encoding='utf-8', level=logging.DEBUG)
window = 0
api = 0
listdrives = 0
infectedscan = 0

scan_running = False

cur_scanhist = ()
q = Queue()

def set_scan(inparam):
	global q
	if inparam["info"] == "scan_start":
		scan_dir = inparam["data"]["dir"]
		q.put(inparam)
		core.walk(scan_dir,q,window)

	elif inparam["info"] == "scan_pause":
		q.put({'info':'scan_pause'})

	elif inparam["info"] == "scan_resume":
		q.put({'info':'scan_resume'})
		
	elif inparam["info"] == "scan_stop":
		q.put({'info':'scan_stop'})
		
def run_cmd(argv):
	inputfile = ''
	global q
	try:
		opts, args = getopt.getopt(argv,"hi:o:a",["ifile=","ofile="])
	except getopt.GetoptError:
		print ('test.py -i <inputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('test.py -i <inputfile> ;this should be the json file\n Format: {"info":"scan_start","data":{"dir":param,"type":"drive"},"cron":"data_cron"}')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			jsd = json.loads(open(inputfile,"r").read())
			logging.debug("Starting Periodic Scan with input params")
			set_scan(jsd)
			sys.exit()
		elif opt in ("-a","--full_scan"):
			logging.debug("Starting Full System Scan")
			full_scan()
			sys.exit()


def full_scan():
	drivs = core.listpartitions()
	for x in drivs:
		set_scan({"info":"scan_start","data":{"dir":str(x[1]),'type':'drive'}})


class Api3:
	def close(self):
		global infectedscan
		print('killing')
		try:
			infectedscan.destroy()
		except Exception as e:
			print("not found drive")



	def queryscan_full(self):
		connection = sqlite3.connect("scan.db")
		cursor = connection.cursor()
		data_bank = []
		rows = cursor.execute("SELECT ScanID,ScanDate,Scantype,ScanLocation FROM Scan_Reports WHERE ScanDate BETWEEN ? AND ?",cur_scanhist).fetchall()
		for x in rows:
			rows2 = cursor.execute("SELECT Filename FROM InfectedScannedFiles WHERE ScanID =  ?",(x[0],)).fetchall()
			for y in rows2:
				data_bank.append({"name":os.path.split(y[0]) ,"date":x[1],"type":x[2],"loc":x[3]})

		ret =  {"list":data_bank}
		print(ret)
		return ret
	

class Api2:
	def close_listdrv(self):
		print('killing')
		try:
			listdrives.destroy()
		except Exception as e:
			print("not found drive")

	def querydrives(self):
		drivs = core.listpartitions()
		print(drivs) 
		msg = []
		for x in drivs:
			msg.append({"drive": str(x[0]),"mount":str(x[1])})

		strp = {"list":msg}
		print("listdrive_start")
		print(strp)
		print("listdrive_end")
		return strp

	def driveselected(self,param):
		try:
			listdrives.destroy()
		except Exception as e:
			print("not found drive")

		if param:
			window.evaluate_js("location.href = 'scan_running.html'")
			set_scan({"info":"scan_start","data":{"dir":param,'type':'drive'}})



class Api:
	
	def quit(self):
		global q
		q.put({'info':'scan_stop'})
		window.destroy()
		os._exit(1)

	def min(self):
		window.minimize()

	def pausescan(self):
		print("calling pause")
		set_scan({"info":"scan_pause"})

	def resumescan(self):
		print("calling resume")
		set_scan({"info":"scan_resume"})

	def stopscan(self):
		print("Calling abortion")
		set_scan({"info":"scan_stop"})


	def selectfolder(self):
		path = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
		if path:
			print(path[0])
			window.evaluate_js('location.href="scan_running.html";')
			set_scan({"info":"scan_start","data":{"dir":str(path[0]),'type':'folder'}})
			scan_running = True
			return "0"

		return "1"

	def querydrive(self):
		global listdrives
		listdrives = webview.create_window('JVSOFT MALWARE DETECTOR', 'gui/listdrives.html',width=537, height=413,frameless=True,js_api = Api2(),easy_drag=False)

	def pause_scan(self):
		pass

	def terminate_scan(self):
		pass	

	def report_getdates(self):
		connection = sqlite3.connect("scan.db")
		cursor = connection.cursor()
		rows = cursor.execute("SELECT ScanDate,ScanID FROM Scan_Reports").fetchall()
		return rows

	def getscan_data(self,param):
		global cur_scanhist
		connection = sqlite3.connect("scan.db")
		cur_scanhist = param
		cursor = connection.cursor()
		rows = cursor.execute("SELECT NumberScanned,NumberInfected FROM Scan_Reports WHERE ScanID = ?",(param,)).fetchall()
		return {'nscan':str(rows[0][0]),'ninf':str(rows[0][1])}

	def getstat_data(self):
		connection = sqlite3.connect("scan.db")
		cursor = connection.cursor()
		rows = cursor.execute("SELECT COUNT(*) FROM InfectedScannedFiles").fetchall()
		rows2 = cursor.execute("SELECT COUNT(*) FROM InfectedFiles").fetchall()
		print("Scanned data is sent")
		print({'sum':str(rows[0][0]),'files':str(rows2[0][0])})
		print("endmark")
		return {'sum':str(rows[0][0]),'files':str(rows2[0][0])}

	def showinfected(self,param):
		global infectedscan
		connection = sqlite3.connect("scan.db")
		cursor = connection.cursor()
		rows = cursor.execute("SELECT Filename,ID FROM InfectedScannedFiles WHERE ScanID = ?",(param,)).fetchall()
		infectedscan = webview.create_window('JVSOFT MALWARE DETECTOR', 'gui/scannedfiles.html',width=600, height=500,frameless=True,js_api = Api3(),easy_drag=False)

	def fetcha_dates(self,cmd):
		global cur_scanhist
		connection = sqlite3.connect("scan.db")
		cursor = connection.cursor()
		start_date = datetime.today().strftime('%Y-%m-%d')
		if cmd == "tod":
			end_date = (datetime.today() - timedelta(days=0)).strftime('%Y-%m-%d')

		elif cmd == "lwk":
			end_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

		elif cmd == "lmo":
			end_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

		elif cmd == "lyr":
			end_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

		elif cmd == "alt":
			end_date = False


		cur_scanhist = (end_date,start_date,)
		print(start_date,end_date)
		if end_date:
			rows = cursor.execute("SELECT SUM(NumberScanned),SUM(NumberInfected) FROM Scan_Reports WHERE ScanDate BETWEEN ? AND ?",(end_date,start_date,)).fetchall()
		else:
			rows = cursor.execute("SELECT SUM(NumberScanned),SUM(NumberInfected) FROM Scan_Reports").fetchall()

		print(rows)

		return {'nscan':str(rows[0][0]),'ninf':str(rows[0][1])}



	def error(self):
		raise Exception('This is a Python exception')

if len(sys.argv) > 1:
	run_cmd(sys.argv[1:])
	exit(0)

api = Api()
#t1 = Thread(target = set_scan, args =(q, ))
#t1.start()
window = webview.create_window('JVSOFT MALWARE DETECTOR', 'gui/home.html',width=772, height=566,frameless=True, js_api = api,easy_drag=False)
webview.start(http_server=True)


