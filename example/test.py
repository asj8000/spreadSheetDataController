from oauth2client.service_account import ServiceAccountCredentials
import gspread
import random


scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './pjst.json', scope)
spread_data = gspread.authorize(credentials)

#메뉴 DB 가져옴
alldata = spread_data.open("Bot_DB").worksheet('Lunch_DB')
lunch_db_data = alldata.get_all_values()

#랜덤 변수 생성용. 메뉴 DB 최대 개수 출력
DB_length = len(lunch_db_data) - 1

#마지막에 추천한 메뉴 제거용
#마지막 메뉴 체크 DB 가져옴
last_menu_check_data = spread_data.open("Bot_DB").worksheet('Lunch_last_menu_check')
last_menu_check_array = last_menu_check_data.get_all_values()
#기록되어있는 값들을 array로 불러옴
latest_record = last_menu_check_array[0]


#랜덤으로 변수 생성(최근 추천한 메뉴는 제외)
state = 0;
while state < 1:
    random_data = str(random.randrange(0,DB_length))
    if random_data in latest_record: 
        state = 0;
    else:
        state = 1;
    random_int = int(random_data)


#마지막 등록한 위치 데이터
last_record_location = last_menu_check_array[1][0]

#마지막 식당 추천 내역을 입력할 셀 찾기.
int_to_eng_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
int_to_eng = int_to_eng_array[int(last_record_location)]
#해당 위치에 랜덤 추천값을 입력.
location = str(int_to_eng+'1')
last_menu_check_data.update_acell(location, random_int)

#A2셀(마지막 변경 위치)의 데이터를 가져와 +1해서 업데이트
record_last = int(last_record_location)+1
if record_last >= 21:
    record_last = 0
last_menu_check_data.update_acell('A2', record_last)

#Lunch_DB 시트 랜덤열의 B셀 데이터(url) 리턴
print(lunch_db_data[random_int][1])

