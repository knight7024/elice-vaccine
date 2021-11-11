from typing import Dict


class Center:   
    def __init__(self, data):
        if type(data) is dict:
            self.centerName = data['centerName']
            self.centerType = data['centerType']
            self.facilityName = data['facilityName']
            self.org = data['org']
            self.phoneNumber = data['phoneNumber']
            self.full_address = data['address']
            self.part_address_1 = data['sido']
            self.part_address_2 = data['sigungu']
            self.lat = data['lat']
            self.lng = data['lng']
            
    
    def __str__(self):
        return f'{self.full_address}\n{self.centerName}\n'
            
        
    
    