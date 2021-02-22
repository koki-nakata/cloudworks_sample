from selenium import webdriver
import json


''' 本番環境の場合コメントアウトを外す '''
# from selenium.webdriver.chrome.options import Options
#
# options = Options()
# options.add_argument('--disable-gpu');
# options.add_argument('--disable-extensions');
# options.add_argument('--proxy-server="direct://"');
# options.add_argument('--proxy-bypass-list=*');
# options.add_argument('--start-maximized');
# options.add_argument('--headless');
# DRIVER_PATH = 'chromedriverのpath'

''' 開発環境の場合コメントアウトを外す '''
DRIVER_PATH = 'chromedriverのpath'


browser = webdriver.Chrome(executable_path=DRIVER_PATH)
browser.get("http://www.asahikawa-med.ac.jp/schedule/index.html") #データ取得先URL

def get_json_file():
    ''' データ取得スタート '''
    main = browser.find_element_by_class_name("table00")
    table_base = main.find_elements_by_tag_name("tr")
    json_base = {}
    num  = 0

    for i in range(1,6):
        week = table_base[0].find_elements_by_tag_name("td")[i].text

        for j in range(1,4):
            if j == 1:
                medical = table_base[1].find_elements_by_tag_name("td")[0].text.replace("\n","")
                attribute = table_base[j].find_elements_by_tag_name("td")[1].text
                apm = table_base[j].find_elements_by_tag_name("td")[2].text.replace("\n","")
                patient_base = table_base[1].find_elements_by_tag_name("td")[2+i]

                for k in range(0,len(patient_base.find_elements_by_tag_name("p"))):
                    doctor = []
                    specialty = []
                    irregular = []
                    reservation = []
                    patient = patient_base.find_elements_by_tag_name("p")[k].text.replace("\u3000"," ").split("\n")
                    doctor.append(patient[0])
                    specialty.append(patient[1].replace("（","").replace("）",""))
                    num += 1
                    json_base["data"+str(num)] = {"Week":week,"Medical":medical,"Attribute":attribute,"Apm":apm,"Docter":doctor,"Specialty":specialty,"Reservation":reservation,"Irregular":irregular}

            elif j == 2:
                medical = table_base[1].find_elements_by_tag_name("td")[0].text.replace("\n","")
                attribute = table_base[j].find_elements_by_tag_name("td")[0].text
                apm = table_base[j].find_elements_by_tag_name("td")[1].text
                patient_base = table_base[j].find_elements_by_tag_name("td")[2+i-1]

                if patient_base.text == " ":
                    pass

                else:
                    try:
                        patient_base = patient_base.text.split("\n")
                        irregular = [s for s in patient_base if '週' in s]
                        base = [s for s in patient_base if '予約'not in s and '週' not in s  and ' ' not in s]
                        doctor = [s.replace("\u3000","") for s in base if '\u3000' in s]
                        specialty = [s.replace("【","").replace("】","") for s in base if '\u3000' not in s]
                        reservation = [s for s in patient_base if '予約' in s]

                    except:
                        pass
                    num += 1
                    json_base["data"+str(num)] = {"Week":week,"Medical":medical,"Attribute":attribute,"Apm":apm,"Docter":doctor,"Specialty":specialty,"Reservation":reservation,"Irregular":irregular}

            else:
                medical = table_base[1].find_elements_by_tag_name("td")[0].text.replace("\n","")
                attribute = table_base[j-1].find_elements_by_tag_name("td")[0].text
                apm = table_base[j-1].find_elements_by_tag_name("td")[1].text
                patient_base = table_base[j].find_elements_by_tag_name("td")[1+i-1]

                if patient_base.text == " ":
                    pass

                else:
                    try:
                        patient_base = patient_base.text.split("\n")
                        irregular = [s for s in patient_base if '週' in s]
                        base = [s for s in patient_base if '予約'not in s and '週' not in s]
                        doctor = [s.replace("\u3000","") for s in base if '\u3000' in s]
                        specialty = [s.replace("【","").replace("】","") for s in base if '\u3000' not in s]
                        reservation = [s for s in patient_base if '予約' in s]

                    except:
                        pass
                    num += 1
                    json_base["data"+str(num)] = {"Week":week,"Medical":medical,"Attribute":attribute,"Apm":apm,"Docter":doctor,"Specialty":specialty,"Reservation":reservation,"Irregular":irregular}
    ''' データ取得終了 '''

    ''' ファイル作成スタート '''
    fw = open('json_sample.json','w') #ファイル名、保存先指定
    json.dump(json_base, fw, ensure_ascii=False, indent=4)
    ''' ファイル作成終了 '''
