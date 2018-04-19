import redis
import datetime
import re

class DB:
    def __init__(self,host='localhost',port=6379):
        self.r = redis.Redis(host=host,port=port)
        
    def store_devices(self,devicelist):
        for device in devicelist:
            self.r.rpush('devices',device)

    def decode(self,device):
        return device.decode('utf-8') if device else None
    
    def get_devices(self,devicelist):
        l = []
        for device in self.r.lrange('devices',0,-1):
            d = self.decode(device)
            if d == None :break
            l.append(d)
    
    def get_device_states(self):
        devices_dict = {}
        for device in self.r.lrange('devices',0,-1):
            device = self.decode(device)
            devices_dict[device]={}
            devices_dict[device]['user'] = self.decode(self.r.hget(device,'user'))
            devices_dict[device]['minutes'] = self.decode(self.r.hget(device,'minutes'))
            time = self.decode(self.r.hget(device,'time'))
            if time != None:
                time = time.split(' ')[0]+' '+time.split(' ')[1].split('.')[0]
            devices_dict[device]['time'] = time

        return devices_dict

    def is_reserved(self,device):
        if self.r.hget(device,'user') != None:
            t = self.decode(self.r.hget(device,'time'))
            matcho = re.match(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})\s([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]*)$',t)
            time = []
            for i in range(1,7):
                time.append(int(matcho.group(i)))
            t = datetime.datetime(year=time[0],month=time[1],day=time[2],hour=time[3],minute=time[4],second=time[5])
            tn = datetime.datetime.now()
            minutes = int(self.decode(self.r.hget(device,'minutes')))
            mini,_ = divmod((tn-t).seconds,60)
            r = (minutes - mini )
            return str(r)
        else:
            return False

    def store(self,device,user,minutes):
        time = datetime.datetime.now()
        e_time = time + datetime.timedelta(minutes=int(minutes))
        self.r.hmset(device,{'user':user,'minutes':minutes,'time':time})
        self.r.expireat(name=device,when=e_time)

        
    

            
        
