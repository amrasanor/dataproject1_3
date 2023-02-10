# module import
import pandas as pd
import folium
import requests
import json
# import IPython

# csv 파일 읽어들이기
df = pd.read_csv("https://github.com/amrasanor/dataproject1_3/raw/master/%EC%A0%84%EA%B5%AD_%EA%B2%B0%EB%B9%99%EC%82%AC%EA%B3%A0%EB%8B%A4%EB%B0%9C%EC%A7%80%EC%97%AD.csv", encoding="CP949")


# 사고 지역 좌표 list화 후 마커(+팝업) 생성 함수 정의
def add_marker(m):
    locations = list(zip(df["지점명"], df["발생건수"], df["사상자수"], df["사망자수"], df["중상자수"], df["경상자수"], df["부상신고자수"], df["위도"], df["경도"]))
  
    for i in locations:
        pp = f"{i[0]}, 사고 {i[1]}건: 사상자 {i[2]}명(사망 {i[3]}, 중상 {i[4]}, 경상 {i[5]}, 부상신고 {i[6]})"
        popup = folium.Popup(pp, max_width=800)
    
        folium.Marker(location=i[7:], popup=popup).add_to(m)


# 사고 지점 구역 표시
def add_area(m):
    for i in range(len(df)):
        polygon_str = df["다발지역폴리곤"][i]
    
        polygon_dict = json.loads(polygon_str)

        coordinates = polygon_dict["coordinates"]

        geo_json = {"type": "Feature",
                    "geometry": {"type": "Polygon",
                                 "coordinates": coordinates}}

    folium.GeoJson(geo_json, style_function=lambda x: {"color": "red"}).add_to(m)


# 국내 행정구역 구분
def add_district(m):
    r = requests.get("https://github.com/amrasanor/dataproject1_3/raw/master/SIDO_MAP_2022.json")
    c = r.content

    district = json.loads(c)
  
    folium.GeoJson(district, style_function=lambda x: {"fillOpacity": 0}).add_to(m)


# 지도와 마커 + 팝업 + 사고 지점 구역, 행정구역 구분 출력, 다운로드함
# colab에서는 폴리곤을 사용한 folium이 잘 출력되지 않아, 지도 html을 다운로드하게 하였음
def map_print(city_input, city):
    m = folium.Map(location=city,
                   zoom_start=10,
                   width=1000,
                   height=1000)
  
    add_marker(m)

    add_area(m)

    add_district(m)

    filename = f"17-21년_{city_input}결빙사고다발지역.html"

    m.save(filename)

    # colab에서의 출력을 위해 html이 저장된 경로를 리턴하였음
    file_name = f"/content/{filename}"

    return file_name


# 확대할 좌표가 담긴 csv 파일
name_list = pd.read_csv("https://github.com/amrasanor/dataproject1_3/raw/master/korea_city_coordinant.csv", encoding="CP949")


# 원하는 지역 확대하여 지도를 다운로드
def map_result():
    input_text = '''
열람을 원하시는 시/도를 입력하세요. 입력하신 시/도가 다음 검색어와 일치해야 합니다.
검색어: 강원, 경기, 경남, 경북, 광주, 대구, 대전, 부산, 서울, 세종, 울산, 인천, 전남, 전북, 제주, 충남, 충북\n
'''

    city_input = input(input_text)

    city = None

    # 입력한 검색어가 데이터에 있다면 해당하는 좌표를 가져온다
    for i in range(len(name_list.name)):
        if city_input == name_list.name[i]:
            city = [name_list.lat[i], name_list.long[i]]
            break

    # 좌표를 가져왔다면 map_print()를 실행하고 지도를 html로 저장한다
    if city:
        print("\n잠시만 기다려 주세요...")

        # html 출력을 위해 map_print()에서 return한 file_name을 return함
        return map_print(city_input, city)

    else:
        print("\n정확히 입력해 주세요.")


# 전체 실행하는 result 정의
result = map_result()

# 전체 실행하면서 html을 colab에 출력
# IPython.display.HTML(filename=result)
