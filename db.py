import redis
import datetime
import re

class DB:
    def __init__(self,host='localhost',port=6379):
        self.r = redis.Redis(host=host,port=port)
        
    def store_elements(self,elementlist):
        for element in elementlist:
            self.r.rpush('elements',element)

    def store_element(self,element):
        self.r.rpush('elements',element)
    
    def decode(self,element):
        return element.decode('utf-8') if element else None

    def specialdecode(self,element):
        return element.decode('utf-8').replace('\n','<br>') if element else None
    
    def get_elements(self,elementlist):
        l = []
        for element in self.r.lrange('elements',0,-1):
            d = self.decode(element)
            if d == None :break
            l.append(d)

    def store_eprop(self,element,prop,value):
        self.r.hset(element+'Prop',prop,value)
    
    def get_element_states(self):
        elements_dict = {}
        for element in self.r.lrange('elements',0,-1):
            element = self.decode(element)
            elements_dict[element]={}
            elements_dict[element]['user'] = self.decode(self.r.hget(element,'user'))
            elements_dict[element]['minutes'] = self.decode(self.r.hget(element,'minutes'))
            time = self.decode(self.r.hget(element,'time'))
            if time != None:
                time = time.split(' ')[0]+' '+time.split(' ')[1].split('.')[0]
            elements_dict[element]['time'] = time
            
            elements_dict[element]['Role'] = self.decode(self.r.hget(element+'Prop','Role'))
            elements_dict[element]['IP Address'] = self.specialdecode(self.r.hget(element+'Prop','IP Address'))
            elements_dict[element]['Credentials'] = self.specialdecode(self.r.hget(element+'Prop','Credentials'))
            elements_dict[element]['Device'] = self.specialdecode(self.r.hget(element+'Prop','Device'))
        return elements_dict

    def is_reserved(self,element):
        if self.r.hget(element,'user') != None:
            t = self.decode(self.r.hget(element,'time'))
            matcho = re.match(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})\s([0-9]{2}):([0-9]{2}):([0-9]{2}).([0-9]*)$',t)
            time = []
            for i in range(1,7):
                time.append(int(matcho.group(i)))
            t = datetime.datetime(year=time[0],month=time[1],day=time[2],hour=time[3],minute=time[4],second=time[5])
            tn = datetime.datetime.now()
            minutes = int(self.decode(self.r.hget(element,'minutes')))
            mini,_ = divmod((tn-t).seconds,60)
            r = (minutes - mini )
            return str(r)
        else:
            return False

    def store(self,element,user,minutes):
        time = datetime.datetime.now()
        e_time = time + datetime.timedelta(minutes=int(minutes))
        self.r.hmset(element,{'user':user,'minutes':minutes,'time':time})
        self.r.expireat(name=element,when=e_time)

        
    

            
        
