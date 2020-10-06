import datetime
import pytz 

class date_time:

	def tell_date(self):
		current_date = datetime.date.today()
		date = current_date.strftime("%B %d, %Y")
		print(date)
		return date

	def tell_time(self):
		current_time = datetime.datetime.now()
		time = current_time.strftime("%H:%M")
		print(time)
		return time


	def convert_12_hour_format(self,s):
		normal_time = datetime.datetime.strptime(str(s), "%H:%M")
		time = normal_time.strftime("%I:%M %p").lower()
		print(time)
		return time


	def tell_timezones(self):

		cmd = input("Choice of timezone: ")

		if cmd == "UTC" or cmd =="utc":
			self.UTC()
		elif cmd == "PST" or cmd == "pst":
			self.PST()
		elif cmd == "EST" or cmd == "est":
			self.EST()
		elif cmd == "IST" or cmd == "ist":
			self.IST()
		else:
			print("invalid timezone")


	def UTC(self):
		UTC = pytz.utc 
		datetime_utc = datetime.datetime.now(UTC).strftime("%H:%M")
		print(datetime_utc)
		return datetime_utc

	def PST(self):
		PST = pytz.timezone('US/Pacific')
		datetime_pst = datetime.datetime.now(PST).strftime("%H:%M")
		print(datetime_pst)
		return datetime_pst

	def EST(self):
		EST = pytz.timezone('America/New_York')
		datetime_est = datetime.datetime.now(EST).strftime("%H:%M")
		print(datetime_est)
		return datetime_est

	def IST(self):
		IST = pytz.timezone('Asia/Kolkata') 
		datetime_ist = datetime.datetime.now(IST).strftime("%H:%M")
		print(datetime_ist)
		return datetime_ist


# TimeObject = date_time()
# TimeObject.tell_date()
# TimeObject.tell_time()
# TimeObject.convert_12_hour_format(TimeObject.tell_time())
# TimeObject.tell_timezones()