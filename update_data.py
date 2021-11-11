from flask_apscheduler import APScheduler

import requests

from models import Center
import db_connect


scheduler = APScheduler()

@scheduler.task('cron', id='update_data', hour=0)
def update_data():
    url = 'https://api.odcloud.kr/api/15077586/v1/centers?page={0}&perPage={1}'
    page, perPage = 1, 10
    authKey = ''
    headers = {'Authorization': 'Infuser {0}'.format(authKey)}

    db = db_connect.MysqlPool()
    cursor = db.cursor()
    
    # 테이블 초기화
    cursor.execute(
        'TRUNCATE center'
    )
    db.commit()
    
    endCount = 0
    while True:
        res = requests.get(url=url.format(page, perPage), headers=headers)
        res.raise_for_status()
        json_res = res.json()
        
        totalCount, currentCount = int(json_res.get('totalCount')), int(json_res.get('currentCount'))
        datas = json_res.get('data', None)
        if datas:            
            # 데이터 삽입
            for data in datas:
                center = Center(data)
                cursor.execute(
                    'INSERT INTO center (centerName, centerType, facilityName, org, phoneNumber, full_address, part_address_1, part_address_2, lat, lng) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (center.centerName, center.centerType, center.facilityName, center.org, center.phoneNumber, center.full_address, center.part_address_1, center.part_address_2, center.lat, center.lng)
                )
                db.commit()
                
            print('데이터 삽입 중...')
        
        if totalCount <= endCount: break
        endCount += currentCount
        page += 1
    
    print('데이터 전처리 완료')
    db.close()
    
    
def start(app):
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()