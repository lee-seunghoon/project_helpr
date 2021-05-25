from django.shortcuts import render,redirect
import csv
from django.http import HttpResponse
from .models import User, xyLocation, Message
from django.contrib import messages


# region code insert(xyLocation data db에 넣는 함수)
# 'localhost:8000/insert' url 요청시 실행
def region_code(request):
    f = open('./region_code.csv','r', encoding='UTF-8')
    region_code_data = csv.reader(f)


    for line in region_code_data:
        print('region_code', int(line[2]))
        print('region_1', str(line[3]))
        print('region_2', str(line[4]))
        print('region_3', str(line[5]))
        print('region_x', int(line[6]))
        insert_region = xyLocation(region_code = int(line[2]),
                                    region_1 = str(line[3]),
                                    region_2 = str(line[4]),
                                    region_3 = str(line[5]),
                                    region_x = int(line[6]),
                                    region_y = int(line[7]))
        insert_region.save()

    return HttpResponse('xylocation insert done!!!')


def chart(request):
    return render(request, 'chart.html')

def map(request):
    # 로그인한 아이디
    session_id = request.session.get('user_id')
    return render(request, 'map.html')

def msg(request):
    session_id = request.session.get('user_id')
    messages_list = Message.objects.filter(user_id_id=session_id)
    content_dict={'messages': messages_list}
    print(content_dict)
    if request.method == "POST":
        print('test2')
        print(request.POST)
        print('test2')
        m_title = request.POST.get('massage_title')
        m_content = request.POST.get('message_content')
        message = Message.objects.create(user_id_id= session_id,
                                        title= m_title,
                                        content= m_content)
        message.save()
        # 소켓통신 or mqtt로 pub
        messages.info(request,'메시지가 전송되었습니다.')
    return render(request, 'msg.html', content_dict)

def sign_in(request):
    print("test")
    print(request.POST)
    if request.method == "POST":
        userId = request.POST.get('userId')
        password = request.POST.get('password')
        try: 
            user = User.objects.get(user_id=userId)
        except:
            # 회원이 아닌 경우

            return render(request, 'sign_in.html')
        # 회원인 경우
        if user.user_pw == password:
            request.session['user_id'] = userId
            return redirect('chart')
            # print('비정상 출력')
            # return render(request, 'sign_in.html', {'error': '사용자 아이디 또는 패스워드가 틀립니다.'})
    else:
        return render(request, 'sign_in.html')


def sign_up(request):
    context = {
        "region1_list": ['강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시', '대전광역시', '부산광역시', '서울특별시', '세종특별자치시', '울산광역시', '이어도', '인천광역시', '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도'],
        "region2_list": ['가평군', '강남구', '강동구', '강릉시', '강북구', '강서구', '강진군', '강화군', '거제시', '거창군', '경산시', '경주시', '계룡시', '계양구', '고령군', '고성군', '고양시덕양구',
                         '고양시일산동구', '고양시일산서구', '고창군', '고흥군', '곡성군', '공주시', '과천시', '관악구', '광명시', '광산구', '광양시', '광주시', '광진구', '괴산군', '구례군',
                          '구로구', '구리시', '구미시', '군산시', '군위군', '군포시', '금산군', '금정구', '금천구', '기장군', '김제시', '김천시', '김포시', '김해시', '나주시', '남구', '남동구',
                           '남양주시', '남원시', '남해군', '노원구', '논산시', '단양군', '달서구', '달성군', '담양군', '당진시', '대덕구', '도봉구', '동구', '동대문구', '동두천시', '동래구',
                           '동작구', '동해시', '마포구', '목포시', '무안군', '무주군', '문경시', '미추홀구', '밀양시', '보령시', '보성군', '보은군', '봉화군', '부산진구', '부안군', '부여군',
                           '부천시', '부평구', '북구', '사상구', '사천시', '사하구', '산청군', '삼척시', '상주시', '서구', '서귀포시', '서대문구', '서산시', '서천군', '서초구', '성남시분당구',
                           '성남시수정구', '성남시중원구', '성동구', '성북구', '성주군', '세종특별자치시', '속초시', '송파구', '수성구', '수영구', '수원시 권선구', '수원시권선구', '수원시영통구',
                           '수원시장안구', '수원시팔달구', '순창군', '순천시', '시흥시', '신안군', '아산시', '안동시', '안산시단원구', '안산시상록구', '안성시', '안양시동안구', '안양시만안구', 
                           '양구군', '양산시', '양양군', '양주시', '양천구', '양평군', '여수시', '여주시', '연수구', '연제구', '연천군', '영광군', '영덕군', '영도구', '영동군', '영등포구', '영암군', 
                           '영양군', '영월군', '영주시', '영천시', '예산군', '예천군', '오산시', '옥천군', '옹진군', '완도군', '완주군', '용산구', '용인시기흥구', '용인시수지구', '용인시처인구', '울릉군', 
                           '울주군', '울진군', '원주시', '유성구', '은평구', '음성군', '의령군', '의성군', '의왕시', '의정부시', '이천시', '익산시', '인제군', '임실군', '장성군', '장수군', '장흥군', 
                           '전주시덕진구', '전주시완산구', '정선군', '정읍시', '제주시', '제천시', '종로구', '중구', '중랑구', '증평군', '진도군', '진안군', '진주시', '진천군', '창녕군', '창원시 마산합포구', 
                           '창원시 마산회원구', '창원시 성산구', '창원시 의창구', '창원시 진해구', '천안시동남구', '천안시서북구', '철원군', '청도군', '청송군', '청양군', '청주시상당구', '청주시서원구', 
                           '청주시청원구', '청주시흥덕구', '춘천시', '충주시', '칠곡군', '태백시', '태안군', '통영시', '파주시', '평창군', '평택시', '포천시', '포항시남구', '포항시북구', '하남시', '하동군', 
                           '함안군', '함양군', '함평군', '합천군', '해남군', '해운대구', '홍성군', '홍천군', '화성시', '화순군', '화천군', '횡성군'],
        "region3_list": ["가경동", "가곡동", "가곡면", "가남읍", "가능동", "가덕도동", "가덕면", "가락1동", "가락2동", "가락동", "가락본동", "가례면", "가리봉동", "가북면", "가사문학면", "가산동", "가산면", "가수원동", "가야곡면", "가야면", "가야읍", "가야제1동", "가야제2동", "가양1동", "가양2동", "가양제1동", "가양제2동", "가양제3동", "가은읍", "가음면", "가음정동", "가장동", "가정1동", "가정2동", "가정3동", "가조면", "가좌1동", "가좌2동", "가좌3동", "가좌4동", "가창면", "가천면", "가평읍", "가포동", "가호동", "가회동", "가회면", "가흥1동", "가흥2동", "각남면", "각북면", "간동면", "간석1동", "간석2동", "간석3동", "간석4동", "간성읍", "간전면", "갈마1동", "갈마2동", "갈말읍", "갈매동", "갈산1동", "갈산2동", "갈산동", "갈산면", "갈현동", "갈현제1동", "갈현제2동", "감곡면", "감만제1동", "감만제2동", "감문면", "감물면", "감북동", "감삼동", "감일동", "감전동", "감천면", "감천제1동", "감천제2동", "감포읍", "갑천면", "강경읍", "강구면", "강남동", "강내면", "강동동", "강동면", "강림면", "강상면", "강서동", "강서제1동", "강서제2동", "강일동", "강진면", "강진읍", "강천면", "강하면", "강현면", "강화읍", "개군면", "개금제1동", "개금제2동", "개금제3동", "개령면", "개봉제1동", "개봉제2동", "개봉제3동", "개운동", "개정동", "개정면", "개진면", "개천면", "개포1동", "개포2동", "개포4동", "개포면", "거류면", "거여1동", "거여2동", "거제면", "거제제1동", "거제제2동", "거제제3동", "거제제4동", "거진읍", "거창읍", "건국동", "건입동", "건천읍", "검단동", "검산동", "검암경서동", "결성면", "겸면", "겸백면", "경안동", "경암동", "경천면", "경포동", "경화동", "계곡면", "계남면", "계룡면", "계림1동", "계림2동", "계림동", "계북면", "계산1동", "계산2동", "계산3동", "계산4동", "계성면", "계양1동", "계양2동", "계양3동", "계화면", "고경면", "고군면", "고금면", "고남면", "고달면", "고대면", "고덕면", "고덕제1동", "고덕제2동", "고등동", "고봉동", "고부면", "고북면", "고산1동", "고산2동", "고산3동", "고산면", "고삼면", "고서면", "고성동", "고성읍", "고수면", "고아읍", "고암면", "고양동", "고운동", "고잔동", "고전면", "고제면", "고창읍", "고척제1동", "고척제2동", "고천동", "고촌읍", "고한읍", "고현동", "고현면", "고흥읍", "곡선동", "곡성읍", "곤명면", "곤양면", "곤지암읍", "골약동", "공검면", "공근면", "공단동", "공덕동", "공덕면", "공도읍", "공릉1동", "공릉2동", "공산동", "공산면", "공성면", "공음면", "공항동", "과림동", "과역면", "과천동", "관고동", "관교동", "관문동", "관산동", "관산읍", "관양1동", "관양2동", "관음동", "관인면", "관저1동", "관저2동", "관촌면", "관평동", "광교1동", "광교2동", "광남1동", "광남2동", "광덕면", "광도면", "광림동", "광명1동", "광명2동", "광명3동", "광명4동", "광명5동", "광명6동", "광명7동", "광복동", "광석면", "광시면", "광안제1동", 
                         "광안제2동", "광안제3동", "광안제4동", "광양읍", "광영동", "광의면", "광장동", "광적면", "광정동", "광천동", "광천읍", "광탄면", "광평동", "광혜원면", "광활면", "광희동", "괘법동", "괴산읍", "괴정동", "괴정제1동", "괴정제2동", "괴정제3동", "괴정제4동", "교1동", "교2동", "교남동", "교동", "교동면", "교문1동", "교문2동", "교방동", "교월동", "교하동", "교현.안림동", "교현2동", "구갈동", "구래동", "구례읍", "구로제1동", "구로제2동", "구로제3동", "구로제4동", "구로제5동", "구룡면", "구룡포읍", "구림면", "구만면", "구문소동", "구미1동", "구미동", "구산동", "구산면", "구서제1동", "구서제2동", "구성동", "구성면", "구암1동", "구암2동", "구암동", "구운동", "구월1동", "구월2동", "구월3동", "구월4동", "구의제1동", "구의제2동", "구의제3동", "구이면", "구정면", "구좌읍", "구즉동", "구지면", "구천면", "구평동", "구포제1동", "구포제2동", "구포제3동", "구항면", "국동", "국우동", "국토정중앙면", "군남면", "군내면", "군동면", "군북면", "군서면", "군외면", "군위읍", "군자동", "군포1동", "군포2동", "궁내동", "궁류면", "권선1동", "권선2동", "귀래면", "귀인동", "규암면", "근남면", "근덕면", "근동면", "근북면", "근화동", "근흥면", "금가면", "금강송면", "금곡동", "금곡면", "금과면", "금광1동", "금광2동", "금광면", "금구면", "금남동", "금남면", "금당면", "금동", "금마면", "금사면", "금사회동동", "금산면", "금산읍", "금서면", "금성동", "금성면", "금수면", "금암1동", "금암2동", "금암동", "금왕읍", "금일읍", "금정동", "금정면", "금지면", "금창동", "금천동", "금천면", "금촌1동", "금촌2동", "금촌3동", "금학동", "금호1가동", "금호1동", "금호2.3가동", "금호2동", "금호4가동", "금호동", "금호읍", "기계면", "기린면", "기배동", "기북면", "기산면", "기성동", "기성면", "기장읍", "기흥동", "길곡면", "길동", "길상면", "길안면", "길음제1동", "길음제2동", "김삿갓면", "김포본동", "김화읍", "나산면", "나운1동", "나운2동", "나운3동", "나포면", "낙동면", "낙서면", "낙성대동", "낙안면", "낙월면", "난곡동", "난향동", "남가좌제1동", "남가좌제2동", "남면", "남목1동", "남목2동", "남목3동", "남부동", "남부면", "남부민제1동", "남부민제2동", "남사읍", "남산1동", "남산2동", "남산3동", "남산4동", "남산동", "남산면", "남상면", "남선면", "남양동", "남양면", "남양읍", "남영동", "남원동", "남원읍", "남이면", "남일면", "남정면", "남제동", "남종면", "남중동", "남지읍", "남천면", "남천제1동", "남천제2동", "남촌도림동", "남촌동", "남평읍", "남포동", "남포면", "남하면", "남한산성면", "남항동", "남해읍", "남현동", "남후면", "낭산면", "낭성면", "내가면", "내곡동", "내남면", "내당1동", "내당2.3동", "내당4동", "내덕1동", "내덕2동", "내동", "내동면", "내면", "내북면", "내산면", "내서면", "내서읍", "내손1동", "내손2동", "내수읍", "내외동", "내이동", "내일동", "내장상동", 
                         "내촌면", "노곡면", "노동면", "노량진제1동", "노량진제2동", "노성면", "노송동", "노안면", "노암동", "노원동", "노은1동", "노은2동", "노은3동", "노은면", "노학동", "노형동", "노화읍", "녹번동", "녹산동", "녹양동", "녹전면", "논공읍", "논현1동", "논현2동", "논현고잔동", "농성1동", "농성2동", "농소1동", "농소2동", "농소3동", "농소동", "농소면", "농암면", "능곡동", "능동", "능서면", "능주면", "능포동", "다대제1동", "다대제2동", "다도면", "다사읍", "다산1동", "다산2동", "다산동", "다산면", "다시면", "다압면", "다운동", "다인면", "다정동", "단계동", "단구동", "단대동", "단밀면", "단북면", "단산면", "단성면", "단양읍", "단월면", "단장면", "단촌면", "달동", "달산면", "달안동", "달천동", "담양읍", "답십리제1동", "답십리제2동", "당감제1동", "당감제2동", "당감제4동", "당리동", "당산제1동", "당산제2동", "당진1동", "당진2동", "당진3동", "당하동", "대가면", "대가야읍", "대강면", "대곡동", "대곡면", "대곶면", "대관령면", "대교동", "대구면", "대덕동", "대덕면", "대덕읍", "대동", "대동면", "대륜동", "대림제1동", "대림제2동", "대림제3동", "대마면", "대명10동", "대명11동", "대명1동", "대명2동", "대명3동", "대명4동", "대명5동", "대명6동", "대명9동", "대방동", "대병면", "대봉1동", "대봉2동", "대부동", "대사동", "대산동", "대산면", "대산읍", "대서면", "대성동", "대소면", "대소원면", "대송동", "대송면", "대술면", "대신동", "대신면", "대야동", "대야면", "대양면", "대연제1동", "대연제3동", "대연제4동", "대연제5동", "대연제6동", "대원동", "대월면", "대의면", "대이동", "대저1동", "대저2동", "대전면", "대정읍/마라도포함", "대조동", "대지면", "대창면", "대천1동", "대천2동", "대천3동", "대천4동", "대천5동", "대천동", "대청동", "대청면", "대촌동", "대치1동", "대치2동", "대치4동", "대치면", "대평동", "대평면", "대포동", "대학동", "대합면", "대항면", "대현동", "대호지면", "대화동", "대화면", "대흥동", "대흥면", "덕계동", "덕곡면", "덕과면", "덕산동", "덕산면", "덕산읍", "덕암동", "덕연동", "덕적면", "덕진동", "덕진면", "덕천면", "덕천제1동", "덕천제2동", "덕천제3동", "덕치면", "덕포제1동", "덕포제2동", "덕풍1동", "덕풍2동", "덕풍3동", "도개면", "도계읍", "도고면", "도곡1동", "도곡2동", "도곡면", "도담동", "도덕면", "도두동", "도량동", "도림동", "도마1동", "도마2동", "도봉제1동", "도봉제2동", "도사동", "도산동", "도산면", "도안면", "도암면", "도양읍", "도원동", "도척면", "도천동", "도천면", "도초면", "도촌동", "도통동", "도평동", "도포면", "도화1동", "도화2,3동", "도화동", "도화면", "독도", "독산제1동", "독산제2동", "독산제3동", "독산제4동", "돈암제1동", "돈암제2동", "돌산읍", "동강면", "동계면", "동곡동", "동광동", "동구동", "동내면", "동대신제1동", "동대신제2동", "동대신제3동", "동량면", "동로면", "동림동", "동면", "동명동", "동명면", 
                         "동문1동", "동문2동", "동문동", "동백1동", "동백2동", "동백3동", "동백동", "동복면", "동부동", "동부면", "동산동", "동산면", "동삼제1동", "동삼제2동", "동삼제3동", "동상동", "동상면", "동서금동", "동서동", "동서학동", "동선동", "동성동", "동송읍", "동읍", "동이면", "동인동", "동인천동", "동일면", "동진면", "동천동", "동촌동", "동춘1동", "동춘2동", "동춘3동", "동충동", "동탄1동", "동탄2동", "동탄3동", "동탄4동", "동탄5동", "동탄6동", "동탄7동", "동탄8동", "동해면", "동향면", "동호동", "동홍동", "동화동", "동화면", "두동면", "두류1.2동", "두류3동", "두마면", "두산동", "두서면", "두암1동", "두암2동", "두암3동", "두원면", "두촌면", "두호동", "둔내면", "둔덕동", "둔덕면", "둔산1동", "둔산2동", "둔산3동", "둔촌제1동", "둔촌제2동", "둔포면", "득량면", "등촌제1동", "등촌제2동", "등촌제3동", "마도면", "마동", "마두1동", "마두2동", "마량면", "마령면", "마로면", "마리면", "마북동", "마산동", "마산면", "마서면", "마성면", "마암면", "마장동", "마장면", "마전동", "마천1동", "마천2동", "마천면", "만경읍", "만년동", "만덕동", "만덕제1동", "만덕제2동", "만덕제3동", "만석동", "만수1동", "만수2동", "만수3동", "만수4동", "만수5동", "만수6동", "만촌1동", "만촌2동", "만촌3동", "만호동", "망미제1동", "망미제2동", "망상동", "망성면", "망우본동", "망우제3동", "망운면", "망원제1동", "망원제2동", "망포1동", "망포2동", "매곡동", "매곡면", "매교동", "매산동", "매송면", "매전면", "매탄1동", "매탄2동", "매탄3동", "매탄4동", "매포읍", "매화동", "매화면", "맹동면", "면목본동", "면목제2동", "면목제3.8동", "면목제4동", "면목제5동", "면목제7동", "면천면", "명곡동", "명동", "명륜1동", "명륜2동", "명륜동", "명석면", "명일제1동", "명일제2동", "명장제1동", "명장제2동", "명정동", "명지1동", "명지2동", "명호면", "모가면", "모동면", "모라제1동", "모라제3동", "모서면", "모충동", "모현동", "모현읍", "목1동", "목2동", "목3동", "목4동", "목5동", "목감동", "목동", "목면", "목사동면", "목상동", "목원동", "목천읍", "목행.용탄동", "몽탄면", "묘도동", "묘량면", "묘산면", "무거동", "무릉도원면", "무실동", "무악동", "무안면", "무안읍", "무을면", "무장면", "무전동", "무정면", "무주읍", "무태조야동", "무풍면", "묵제1동", "묵제2동", "묵호동", "문경읍", "문곡소도동", "문광면", "문내면", "문덕면", "문래동", "문막읍", "문무대왕면", "문백면", "문산면", "문산읍", "문성동", "문수동", "문수면", "문원동", "문의면", "문정1동", "문정2동", "문창동", "문척면", "문평면", "문학동", "문현제1동", "문현제2동", "문현제3동", "문현제4동", "문화1동", "문화2동", "문화동", "문흥1동", "문흥2동", "물금읍", "물야면", "미력면", "미로면", "미사1동", "미사2동", "미산면", "미성동", "미수동", "미아동", "미암면", "미양면", "미원면", "미조면", "미천면", "미탄면", "미평동", "민락동", "박달1동", 
                         "박달2동", "반곡관설동", "반구1동", "반구2동", "반남면", "반송동", "반송제1동", "반송제2동", "반여제1동", "반여제2동", "반여제3동", "반여제4동", "반월동", "반포1동", "반포2동", "반포3동", "반포4동", "반포면", "반포본동", "발산제1동", "발한동", "방림1동", "방림2동", "방림면", "방배1동", "방배2동", "방배3동", "방배4동", "방배본동", "방산면", "방어동", "방이1동", "방이2동", "방촌동", "방학제1동", "방학제2동", "방학제3동", "방화제1동", "방화제2동", "방화제3동", "배곧동", "배방읍", "백곡면", "백구면", "백령면", "백사면", "백산면", "백석1동", "백석2동", "백석동", "백석읍", "백수읍", "백아면", "백암면", "백운1동", "백운2동", "백운동", "백운면", "백전면", "백학면", "백현동", "번1동", "번2동", "번3동", "번암면", "벌곡면", "벌교읍", "벌용동", "범계동", "범물1동", "범물2동", "범서읍", "범안동", "범어1동", "범어2동", "범어3동", "범어4동", "범일제1동", "범일제2동", "범일제5동", "범천제1동", "범천제2동", "법1동", "법2동", "법성면", "법수면", "법원읍", "법전면", "벽진면", "변동", "변산면", "별내동", "별내면", "별량면", "별양동", "병곡면", "병암동", "병영1동", "병영2동", "병영면", "병점1동", "병점2동", "병천면", "보개면", "보광동", "보길면", "보덕동", "보라동", "보라매동", "보람동", "보문동", "보문면", "보산동", "보성읍", "보수동", "보안면", "보은읍", "보절면", "보정동", "복내면", "복대1동", "복대2동", "복산1동", "복산2동", "복산동", "복수동", "복수면", "복정동", "복현1동", "복현2동", "복흥면", "본동", "본량동", "본리동", "본오1동", "본오2동", "본오3동", "봉강면", "봉개동", "봉남면", "봉담읍", "봉덕1동", "봉덕2동", "봉덕3동", "봉동읍", "봉래면", "봉래제1동", "봉래제2동", "봉림동", "봉명1동", "봉명2.송정동", "봉명동", "봉방동", "봉산동", "봉산면", "봉선1동", "봉선2동", "봉성면", "봉수면", "봉암동", "봉양면", "봉양읍", "봉평동", "봉평면", "봉현면", "봉화읍", "봉황면", "부강면", "부개1동", "부개2동", "부개3동", "부계면", "부곡동", "부곡면", "부곡제1동", "부곡제2동", "부곡제3동", "부곡제4동", "부귀면", "부남면", "부량면", "부론면", "부리면", "부림동", "부림면", "부민동", "부발읍", "부북면", "부사동", "부산면", "부석면", "부성1동", "부성2동", "부안면", "부안읍", "부암동", "부암제1동", "부암제3동", "부여읍", "부원동", "부적면", "부전제1동", "부전제2동", "부주동", "부창동", "부천동", "부춘동", "부평1동", "부평2동", "부평3동", "부평4동", "부평5동", "부평6동", "부평동", "부항면", "부흥동", "북가좌제1동", "북가좌제2동", "북내면", "북도면", "북면", "북문동", "북방면", "북부동", "북산면", "북삼동", "북삼읍", "북상면", "북성동", "북신동", "북아현동", "북안면", "북이면", "북일면", "북천면", "북평동", "북평면", "북하면", "북항동", "북후면", "분당동", "분평동", "불갑면", "불광제1동", "불광제2동", "불국동", "불당동", "불로.봉무동", 
                         "불로대곡동", "불암동", "불은면", "불정면", "불현동", "비금면", "비래동", "비봉면", "비산1동", "비산2.3동", "비산2동", "비산3동", "비산4동", "비산5동", "비산6동", "비산7동", "비산동", "비아동", "비안면", "비인면", "비전1동", "비전2동", "빛가람동", "사곡면", "사근동", "사남면", "사내면", "사당제1동", "사당제2동", "사당제3동", "사당제4동", "사당제5동", "사동", "사등면", "사량면", "사리면", "사매면", "사벌국면", "사봉면", "사북면", "사북읍", "사우동", "사이동", "사직1동", "사직2동", "사직동", "사직제1동", "사직제2동", "사직제3동", "사창동", "사천면", "사천읍", "사파동", "사평면", "산격1동", "산격2동", "산격3동", "산격4동", "산곡1동", "산곡2동", "산곡3동", "산곡4동", "산남동", "산내동", "산내면", "산동면", "산동읍", "산본1동", "산본2동", "산북면", "산서면", "산성동", "산성면", "산수1동", "산수2동", "산양면", "산양읍", "산외면", "산이면", "산인면", "산정동", "산척면", "산청읍", "산포면", "산호동", "살미면", 
                         "삼가면", "삼각동", "삼각산동", "삼계면", "삼국유사면", "삼기면", "삼남읍", "삼덕동", "삼도1동", "삼도2동", "삼도동", "삼동면", "삼락동", "삼랑진읍", "삼례읍", "삼문동", "삼산1동", "삼산2동", "삼산동", "삼산면", "삼서면", "삼선동", "삼성1동", "삼성2동", "삼성동", "삼성면", "삼송동", "삼수동", "삼승면", "삼안동", "삼양동", "삼일동", "삼장면", "삼전동", "삼죽면", "삼천1동", "삼천2동", "삼천3동", "삼청동", "삼평동", "삼학동", "삼향동", "삼향읍", "삼호동", "삼호읍", "삼화동", "삽교읍", "상갈동", "상계10동", "상계1동", "상계2동", "상계3.4동", "상계5동", "상계6.7동", "상계8동", "상계9동", "상관면", "상교동", "상남동", "상남면", "상대동", "상대원1동", "상대원2동", "상대원3동", "상도제1동", "상도제2동", "상도제3동", "상도제4동", "상동", "상동면", "상동읍", "상리면", "상망동", "상면", "상모사곡동", "상무1동", "상무2동", "상문동", "상봉동", "상봉제1동", "상봉제2동", "상북면", "상사면", "상서면", "상암동", "상운면", "상월면", "상인1동", "상인2동", "상인3동", "상일동", "상장동", "상전면", "상주면", "상중이동", "상촌면", "상패동", "상평동", "상하동", "상하면", "상현1동", "상현2동", "새롬동", "새솔동", "생극면", "생림면", "생비량면", "생연1동", "생연2동", "생일면", "생초면", "서강동", "서교동", "서구동", "서남동", "서농동", "서대신제1동", "서대신제3동", "서대신제4동", "서도면", "서둔동", "서림동", "서면", "서부1동", "서부2동", "서부동", "서부면", "서빙고동", "서삼면", "서상면", "서생면", "서서학동", "서석면", "서수면", "서신동", "서신면", "서운면", "서원동", "서원면", "서정동", "서제1동", "서제2동", "서제3동", "서종면", "서창2동", "서창동", "서천읍", "서초1동", "서초2동", "서초3동", "서초4동", "서탄면", "서포면", "서하면", "서현1동", "서현2동", "서호면", "서홍동", "서화면", "서후면", "석곡동", "석곡면", "석관동", "석교동", "석남1동", "석남2동", "석남3동", "석남동", "석동", "석문면", "석보면", "석봉동", "석사동", "석성면", "석수1동", "석수2동", "석수3동", "석적읍", "석전동", "석촌동", "석포면", "선구동", "선남면", "선단동", "선도동", "선두구동", "선부1동", "선부2동", "선부3동", "선산읍", "선암동", "선원면", "선장면", "선주원남동", "선학동", "설성면", "설악면", "설천면", "성거읍", "성건동", "성곡동", "성남동", "성남면", "성내.충인동", "성내1동", "성내2동", "성내3동", "성내동", "성내면", "성내제1동", "성내제2동", "성내제3동", "성당동", "성당면", "성덕동", "성덕면", "성동면", "성복동", "성북동", "성사1동", "성사2동", "성산면", "성산읍", "성산제1동", "성산제2동", "성송면", "성수1가제1동", "성수1가제2동", "성수2가제1동", "성수2가제3동", "성수면", "성안동", "성연면", "성전면", "성정1동", "성정2동", "성주동", "성주면", "성주읍", "성포동", "성현동", "성화.개신.죽림동", "성환읍", "세곡동", "세교동", "세도면", "세류1동", "세류2동", 
                         "세류3동", "세마동", "세지면", "소공동", "소담동", "소라면", "소룡동", "소보면", "소사본동", "소성면", "소수면", "소안면", "소양동", "소양면", "소요동", "소원면", "소이면", "소정면", "소주동", "소천면", "소초면", "소태면", "소하1동", "소하2동", "소흘읍", "속리산면", "손불면", "손양면", "송광면", "송내동", "송도1동", "송도2동", "송도3동", "송도4동", "송도5동", "송도동", "송동면", "송라면", "송림1동", "송림2동", "송림3.5동", "송림4동", "송림6동", "송북동", "송산1동", "송산2동", "송산3동", "송산동", "송산면", "송악면", "송악읍", "송암동", "송월동", "송정1동", "송정2동", "송정동", "송죽동", "송중동", "송지면", "송천1동", "송천2동", "송천동", "송촌동", "송탄동", "송파1동", "송파2동", "송포동", "송하동", "송학동", "송학면", "송해면", "송현1.2동", "송현1동", "송현2동", "송현3동", "수곡1동", "수곡2동", "수곡면", "수궁동", "수내1동", "수내2동", "수내3동", "수동면", "수륜면", "수리동", "수민동", "수북면", "수비면", "수산면", "수색동", "수서동", "수석동", "수성1가동", "수성2.3가동", "수성4가동", "수성동", "수송동", "수신면", "수안보면", "수암동", "수양동", "수영동", "수완동", "수유1동", "수유2동", "수유3동", "수정제1동", "수정제2동", "수정제4동", "수정제5동", "수지면", "수진1동", "수진2동", "수택1동", "수택2동", "수택3동", "수한면", "순성면", "순창읍", "순흥면", "숭의1,3동", "숭의2동", "숭의4동", "숭인제1동", "숭인제2동", "승주읍", "시기동", "시전동", "시종면", "시천면", "시초면", "시흥동", "시흥제1동", "시흥제2동", "시흥제3동", "시흥제4동", "시흥제5동", "식사동", "신가동", "신갈동", "신곡1동", "신곡2동", "신관동", "신광면", "신기면", "신길동", "신길제1동", "신길제3동", "신길제4동", "신길제5동", "신길제6동", "신길제7동", "신내1동", "신내2동", "신녕면", "신니면", "신당동", "신당제5동", "신대방제1동", "신대방제2동", "신덕면", "신도림동", "신도안면", "신동", "신동면", "신동읍", "신둔면", "신등면", "신림동", "신림면", "신방동", "신백동", "신봉동", "신북면", "신북읍", "신사동", "신사우동", "신사제1동", "신사제2동", "신서면", "신선동", "신성동", "신수동", "신안동", "신안면", "신암1동", "신암2동", "신암3동", "신암4동", "신암5동", "신암면", "신양면", "신용동", "신원동", "신원면", "신월1동", "신월2동", "신월3동", "신월4동", "신월5동", "신월6동", "신월7동", "신의면", "신인동", "신장1동", "신장2동", "신장동", "신전면", "신정1동", "신정2동", "신정3동", "신정4동", "신정5동", "신정6동", "신정7동", "신중동", "신지면", "신창동", "신창면", "신천1.2동", "신천3동", "신천4동", "신천동", "신촌동", "신탄진동", "신태인읍", "신평1동", "신평2동", "신평동", "신평면", "신평제1동", "신평제2동", "신포동", "신풍동", "신풍면", "신현동", "신현원창동", "신흥1동", "신흥2동", "신흥3동", "신흥동", "심곡동", "심원면", "심천면", "십정1동", "십정2동", "쌍령동", 
                         "쌍림면", "쌍문제1동", "쌍문제2동", "쌍문제3동", "쌍문제4동", "쌍백면", "쌍봉동", "쌍용1동", "쌍용2동", "쌍용3동", "쌍책면", "쌍치면", "아라동", "아름동", "아미동", "아산면", "아영면", "아주동", "아포읍", "아현동", "악양면", "안강읍", "안계면", "안기동", "안남면", "안내면", "안덕면", "안락제1동", "안락제2동", "안면읍", "안사면", "안산동", "안성1동", "안성2동", "안성3동", "안성면", "안심1동", "안심2동", "안심3.4동", "안심3동", "안심4동", "안암동", "안양1동", "안양2동", "안양3동", "안양4동", "안양5동", "안양6동", "안양7동", "안양8동", "안양9동", "안양면", "안의면", "안정면", "안좌면", "안중읍", "안천면", "안평면", "안흥면", "암남동", "암사제1동", "암사제2동", "암사제3동", "암태면", "압구정동", "압량읍", "압해읍", "앙성면", "애월읍", "야로면", "야음장생포동", "야탑1동", "야탑2동", "야탑3동", "약목면", "약사동", "약사명동", "약산면", "약수동", "양3동", "양감면", "양강면", "양구읍", "양금동", "양남면", "양덕1동", "양덕2동", "양도면", "양동", "양동면", "양림동", "양보면", "양사면", "양산동", "양산면", "양서면", "양성면", "양양읍", "양재1동", "양재2동", "양정동", "양정제1동", "양정제2동", "양주1동", "양주2동", "양주동", "양지동", "양지면", "양촌면", "양촌읍", "양평읍", "양평제1동", "양평제2동", "양포동", "양학동", "양화면", "어룡동", "어모면", "어상천면", "어양동", "언양읍", "엄궁동", "엄다면", "엄사면", "엄정면", "여량면", "여산면", "여서동", "여의동", "여좌동", "여천동", "여항면", "여흥동", "역삼1동", "역삼2동", "역삼동", "역촌동", "연곡면", "연기면", "연남동", "연동", "연동면", "연무동", "연무읍", "연산동", "연산면", "연산제1동", "연산제2동", "연산제3동", "연산제4동", "연산제5동", "연산제6동", "연산제8동", "연산제9동", "연서면", "연성동", "연수1동", "연수2동", "연수3동", "연수동", "연안동", "연일읍", "연지동", "연천읍", "연초면", "연평면", "연풍면", "연희동", "염리동", "염산면", "염창동", "염치읍", "염포동", "영강동", "영광읍", "영남면", "영덕1동", "영덕2동", "영덕동", "영덕읍", "영동읍", "영등1동", "영등2동", "영등포동", "영등포본동", "영랑동", "영북면", "영산동", "영산면", "영서동", "영선제1동", "영선제2동", "영순면", "영암읍", "영양읍", "영오면", "영운동", "영원면", "영월읍", "영인면", "영종1동", "영종동", "영주1동", "영주2동", "영주제1동", "영주제2동", "영중면", "영천동", "영춘면", "영통1동", "영통2동", "영통3동", "영해면", "영현면", "영화동", "영흥면", "예래동", "예산읍", "예안면", "예천읍", "오가면", "오곡면", "오근장동", "오금동", "오남읍", "오동동", "오라동", "오류동", "오류왕길동", "오류제1동", "오류제2동", "오륜동", "오부면", "오산면", "오성면", "오송읍", "오수면", "오전동", "오정동", "오창읍", "오천면", "오천읍", "오치1동", "오치2동", "오포읍", "오학동", "옥계면", "옥곡면", "옥과면", "옥구읍", "옥도면", 
                         "옥동", "옥련1동", "옥련2동", "옥룡동", "옥룡면", "옥산면", "옥서면", "옥성면", "옥수동", "옥암동", "옥종면", "옥천동", "옥천면", "옥천읍", "옥포1동", "옥포2동", "옥포읍", "온산읍", "온양1동", "온양2동", "온양3동", "온양4동", "온양5동", "온양6동", "온양읍", "온정면", "온천1동", "온천2동", "온천제1동", "온천제2동", "온천제3동", "옴천면", "옹동면", "와동", "와룡면", "와부읍", "와촌면", "완도읍", "완산동", "완월동", "왕곡면", "왕궁면", "왕산면", "왕십리도선동", "왕십리제2동", "왕정동", "왕조1동", "왕조2동", "왕징면", "왜관읍", "외남면", "외도동", "외동읍", "외산면", "외서면", "요촌동", "욕지면", "용강동", "용궁면", "용남면", "용담.명암.산성동", "용담1동", "용담2동", "용담면", "용답동", "용당1동", "용당2동", "용당동", "용덕면", "용동면", "용두동", "용면", "용문동", "용문면", "용방면", "용봉동", "용산1동", "용산2가동", "용산2동", "용산동", "용산면", "용상동", "용성면", "용신동", "용안면", "용암1동", "용암2동", "용암면", "용운동", "용유동", "용이동", "용전동", "용주면", "용지동", "용지면", "용진읍", "용평면", "용해동", "용현1,4동", "용현2동", "용현3동", "용현5동", "용현면", "용호제1동", "용호제2동", "용호제3동", "용호제4동", "용화면", "용흥동", "우강면", "우곡면", "우도면", "우만1동", "우만2동", "우보면", "우산동", "우성면", "우아1동", "우아2동", "우암동", "우이동", "우장산동", "우정동", "우정읍", "우제1동", "우제2동", "우제3동", "우창동", "우천면", "운곡면", "운남동", "운남면", "운문면", "운봉읍", "운산면", "운서동", "운수면", "운암1동", "운암2동", "운암3동", "운암면", "운양동", "운정1동", "운정2동", "운정3동", "운주면", "운중동", "운천.신봉동", "울릉읍", "울진읍", "웅남동", "웅동1동", "웅동2동", "웅양면", "웅진동", "웅천동", "웅천읍", "웅촌면", "웅치면", "웅포면", "원곡동", "원곡면", "원남면", "원당동", "원대동", "원덕읍", "원동면", "원북면", "원산도출장소", "원산동", "원삼면", "원성1동", "원성2동", "원신동", "원신흥동", "원인동", "원천동", "원평1동", "원평2동", "원평동", "원효로제1동", "원효로제2동", "월계1동", "월계2동", "월계3동", "월곡1동", "월곡2동", "월곡제1동", "월곡제2동", "월곶동", "월곶면", "월등면", "월롱면", "월명동", "월산4동", "월산5동", "월산동", "월산면", "월성1동", "월성2동", "월성동", "월송동", "월야면", "월영동", "월평1동", "월평2동", "월평3동", "월피동", "월항면", "월호동", "위도면", "위례동", "위천면", "유가읍", "유곡면", "유구읍", "유달동", "유덕동", "유등면", "유림동", "유림면", "유어면", "유천1동", "유천2동", "유천면", "유치면", "율곡동", "율곡면", "율량.사천동", "율면", "율목동", "율어면", "율천동", "율촌면", "은산면", "은진면", "은척면", "은천동", "은풍면", "은하면", "은행1동", "은행2동", "은행동", "은행선화동", "은현면", "을지로동", "음봉면", "음성읍", "음암면", "읍내동", "응봉동",
                         "응봉면", "응암제1동", "응암제2동", "응암제3동", "의당면", "의령읍", "의림지동", "의성읍", "의신면", "의정부1동", "의정부2동", "의창동", "의흥면", "이곡1동", "이곡2동", "이도1동", "이도2동", "이동", "이동면", "이동읍", "이로동", "이매1동", "이매2동", "이문제1동", "이문제2동", "이반성면", "이방면", "이백면", "이산면", "이서면", "이안면", "이양면", "이원면", "이월면", "이인면", "이창동", "이천동", "이촌제1동", "이촌제2동", "이태원제1동", "이태원제2동", "이평면", "이현동", "이호동", "이화동", "인계동", "인계면", "인동동", "인수동", "인월면", "인제읍", "인주면", "인지면", "인창동", "인헌동", "인화동", "인후1동", "인후2동", "인후3동", "일곡동", "일광면", "일도1동", "일도2동", "일동", "일동면", "일로읍", "일반성면", "일봉동", "일산1동", "일산2동", "일산3동", "일산동", "일신동", "일운면", "일원1동", "일원2동", "일원본동", "일월면", "일죽면", "일직면", "임계면", "임고면", "임곡동", "임남면", "임동", "임동면", "임실읍", "임오동", "임자면", "임천면", "임피면", "임하면", "임회면", "입면", "입북동", "입암면", "입장면", "자금동", "자산동", "자양동", "자양면", "자양제1동", "자양제2동", "자양제3동", "자양제4동", "자월면", "자은동", "자은면", "자인면", "작전1동", "작전2동", "작전서운동", "작천면", "잠실2동", "잠실3동", "잠실4동", "잠실6동", "잠실7동", "잠실본동", "잠원동", "장계면", "장곡동", "장곡면", "장군면", "장기동", "장기면", "장기본동", "장남면", "장단면", "장동면", "장량동", "장림제1동", "장림제2동", "장마면", "장명동", "장목면", "장산면", "장성동", "장성읍", "장수면", "장수서창동", "장수읍", "장승포동", "장안면", "장안읍", "장안제1동", "장안제2동", "장암동", "장암면", "장연면", "장위제1동", "장위제2동", "장위제3동", "장유1동", "장유2동", "장유3동", "장전제1동", "장전제2동", "장지동", "장천동", "장천면", "장충동", "장평동", "장평면", "장항1동", "장항2동", "장항읍", "장호원읍", "장흥면", "장흥읍", "재궁동", "재산면", "재송제1동", "재송제2동", "저전동", "적량면", "적상면", "적성면", "적중면", "전곡읍", "전농제1동", "전농제2동", "전동면", "전민동", "전의면", "전포제1동", "전포제2동", "전하1동", "전하2동", "점곡면", "점동면", "점암면", "점촌1동", "점촌2동", "점촌3동", "점촌4동", "점촌5동", "정곡면", "정관읍", "정남면", "정동면", "정라동", "정량동", "정릉제1동", "정릉제2동", "정릉제3동", "정릉제4동", "정림동", "정미면", "정발산동", "정방동", "정산면", "정선읍", "정안면", "정왕1동", "정왕2동", "정왕3동", "정왕4동", "정왕본동", "정우면", "정자1동", "정자2동", "정자3동", "정자동", "정천면", "정촌면", "제기동", "제원면", "제철동", "조곡동", "조도면", "조리읍", "조마면", "조성면", "조안면", "조양동", "조운동", "조원1동", "조원2동", "조원동", "조종면", "조천읍", "조촌동", "조치원읍", "종로1.2.3.4가동", "종로5.6가동", "종암동", "종천면", "종촌동", "좌제1동", "좌제2동", "좌제3동", "좌제4동", "좌천동", "주교동", "주교면", "주덕읍", "주례제1동", "주례제2동", "주례제3동", "주문진읍", "주산면", "주삼동", "주상면", "주생면", "주안1동", "주안2동", "주안3동", "주안4동", "주안5동", "주안6동", "주안7동", "주안8동", "주암면", "주엽1동", "주엽2동", "주왕산면", "주월1동", "주월2동", "주천면", "주촌면", "주포면", "죽곡면", "죽교동", "죽도동", "죽변면", "죽산면", "죽왕면", "죽장면", "죽전1동", "죽전2동", "죽전동", "죽항동", "줄포면", "중계1동", "중계2.3동", "중계4동", "중계본동", "중곡제1동", "중곡제2동", "중곡제3동", "중곡제4동", "중구동", "중동", "중동면", "중리동", "중림동", "중마동", "중면", "중문동", "중방동", "중부동", "중산동", "중앙동", "중앙탑면", "중제1동", "중제2동", "중촌동", "중학동", "중화산1동", "중화산2동", "중화제1동", "중화제2동", "중흥1동", "중흥2동", "중흥3동", "증도면", "증산동", 
                         "증산면", "증평읍", "증포동", "지곡면", "지도읍", "지동", "지례면", "지보면", "지사면", "지산1동", "지산2동", "지산동", "지산면", "지수면", "지원1동", "지원2동", "지저동", "지정면", "지좌동", "지천면", "지평면", "지품면", "지현동", "직산읍", "진건읍", "진관동", "진교면", "진도읍", "진동면", "진량읍", "진례면", "진미동", "진보면", "진봉면", "진부면", "진북동", "진북면", "진산면", "진상면", "진서면", "진성면", "진안동", "진안읍", "진영읍", "진원면", "진월면", "진위면", "진잠동", "진전면", "진접읍", "진천동", "진천읍", "집현면", "차황면", "창녕읍", "창릉동", "창선면", "창수면", "창신제1동", "창신제2동", "창신제3동", "창전동", "창제1동", "창제2동", "창제3동", "창제4동", "창제5동", "창평면", "채운면", "천곡동", "천북면", "천연동", "천전동", "천지동", "천천면", "천현동", "천호제1동", "천호제2동", "천호제3동", "철마면", "철산1동", "철산2동", "철산3동", "철산4동", "철암동", "철원읍", "첨단1동", "첨단2동", "청계동", "청계면", "청구동", "청기면", "청남면", "청담동", "청덕면", "청도면", "청도읍", "청라1동", "청라2동", "청라3동", "청라면", "청량리동", "청량읍", "청룡노포동", "청룡동", "청리면", "청림동", "청북읍", "청산면", "청성면", "청소면", "청송읍", "청안면", "청암면", "청양읍", "청운면", "청운효자동", "청웅면", "청일면", "청전동", "청천1동", "청천2동", "청천면", "청통면", "청파동", "청평면", "청풍면", "청하면", "청학동", "청학제1동", "청학제2동", "청호동", "초계면", "초당동", "초동면", "초량제1동", "초량제2동", "초량제3동", "초량제6동", "초산동", "초월읍", "초읍동", "초이동", "초장동", "초전면", "초지동", "초촌면", "초평동", "초평면", "추부면", "추자면", "추풍령면", "축동면", "축산면", "춘궁동", "춘산면", "춘양면", "춘포면", "충무공동", "충무동", "충장동", "충현동", "충화면", "취암동", "치평동", "칠곡면", "칠금.금릉동", "칠량면", "칠보면", "칠북면", "칠산서부동", "칠서면", "칠성동", "칠성면", "칠원읍", "침산1동", "침산2동", "침산3동", "탄방동", "탄벌동", "탄부면", "탄천면", "탄현동", "탄현면", "탑대성동", "탕정면", "태백동", "태안읍", "태인동", "태인면", "태장1동", "태장2동", "태전1동", "태전2동", "태평1동", "태평2동", "태평3동", "태평4동", "태화동", "토성면", "토지면", "통복동", "통진읍", "퇴계동", "퇴계원읍", "퇴촌면", "파동", "파장동", "파주읍", "파천면", "파평면", "판교동", "판교면", "판문동", "판부면", "판암1동", "판암2동", "팔금면", "팔덕면", "팔룡동", "팔복동", "팔봉동", "팔봉면", "팔탄면", "팽성읍", "평거동", "평내동", "평동", "평리1동", "평리2동", "평리3동", "평리4동", "평리5동", "평리6동", "평산동", "평안동", "평은면", "평창동", "평창읍", "평촌동", "평해읍", "평화1동", "평화2동", "평화남산동", "평화동", "포곡읍", "포남1동", "포남2동", "포두면", "포승읍", "포천동", "표선면", "풍각면", "풍기읍", "풍남동", "풍납1동", "풍납2동", "풍덕동", "풍덕천1동", "풍덕천2동", "풍무동", "풍산동", "풍산면", "풍산읍", "풍세면", "풍암동", "풍양면", "풍천면", "풍향동", "풍호동", "필동", "하계1동", "하계2동", "하남동", "하남면", "하남읍", "하단제1동", "하단제2동", "하당동", "하대동", "하대원동", "하동읍", "하망동", "하북면", "하빈면", "하서면", "하성면", "하안1동", "하안2동", "하안3동", "하안4동", "하양읍", "하의면", "하이면", "하일면", "하장면", "하점면", "하청면", "학교면", "학동", "학산면", "학성동", "학온동", "학운동", "학익1동", "학익2동", "학장동", "한강로동", "한경면", "한남동", "한려동", "한림면", "한림읍", "한반도면", "한산면", "한솔동", "한수면", "한천면", "함라면", "함안면", "함양읍", "함열읍", "함창읍", "함평읍", "합덕읍", "합성1동", "합성2동", "합정동", "합천읍", "합포동", "항동", "해남읍", "해도동", "해룡면", "해리면", "해미면", "해보면", "해신동", "해안동", "해안면", "해양동", "해제면", "해평면", "행구동", "행궁동", "행당제1동", "행당제2동", "행신1동", "행신2동", "행신3동", "행안면", "행운동", "행주동", "향교동", "향남읍", "향동", "향촌동", "혁신동", "현경면", "현곡면", "현남면", "현내면", "현덕면", "현도면", "현동", "현동면", "현북면", "현산면", "현서면", "현풍읍", "형곡1동", "형곡2동", "혜화동", "호계1동", "호계2동", "호계3동", "호계면", "호매실동", "호명면", "호미곶면", "호법면", "호성동", "호수동", "호암.직동", "호원1동", "호원2동", "호저면", "호평동", "홍농읍", "홍도동", "홍동면", "홍북읍", "홍산면", "홍성읍", "홍은제1동", "홍은제2동", "홍제동", "홍제제1동", "홍제제2동", "홍제제3동", "홍천읍", "화개면", "화곡본동", "화곡제1동", "화곡제2동", "화곡제3동", "화곡제4동", "화곡제6동", "화곡제8동", "화남면", "화도면", "화도읍", "화동면", "화명제1동", "화명제2동", "화명제3동", "화북동", "화북면", "화산동", "화산면", "화서1동", "화서2동", "화서면", "화성면", "화수1.화평동", "화수2동", "화순읍", "화암면", "화양동", "화양면", "화양읍", "화원면", "화원읍", "화전동", "화정1동", "화정2동", "화정3동", "화정4동", "화정동", "화정면", "화천읍", "화촌면", "화현면", "환여동", "활천동", "황간면", "황금1동", "황금2동", "황남동", "황등면", "황룡면", "황산면", "황성동", "황연동", "황오동", "황전면", "황지동", "황학동", "회기동", "회남면", "회덕동", "회성동", "회원1동", "회원2동", "회인면", "회진면", "회천1동", "회천2동", "회천3동", "회천4동", "회천면", "회현동", "회현면", "회화면", "횡성읍", "횡천면", "효곡동", "효덕동", "효돈동", "효동", "효령면", "효목1동", "효목2동", "효문동", "효성1동", "효성2동", "효자1동", "효자2동", "효자3동", "효자4동", "효자5동", "효자동", "효자면", "효창동", "후암동", "후평1동", "후평2동", "후평3동", "후포면", "휘경제1동", "휘경제2동", "휴천1동", "휴천2동", "휴천3동", "휴천면", "흑산면", "흑석동", "흥남동", "흥덕면", "흥도동", "흥선동", "흥업면", "흥천면", "흥해읍"]
                    }
    if request.method == "POST":
        print(request.POST)
        userID = request.POST.get('userId')
        userEmail = request.POST.get("userEmail")
        password = request.POST.get("password")
        passwordCheck = request.POST.get("confirm_password")
        region1 = request.POST.get("region_1")
        region2 = request.POST.get("region_2")
        region3 = request.POST.get("region_3")


        if password == passwordCheck:
            print("test")
            xy = xyLocation.objects.filter(region_3= region3,
                                            region_2= region2,
                                            region_1 = region1)
            regionX = int(xy[0].region_x)
            regionY = int(xy[0].region_y)

            try:
                user = User.objects.create(user_id= userID,
                                            user_pw= password,
                                            user_email= userEmail,
                                            region_1= region1,
                                            region_2 = region2,
                                            region_3= region3,
                                            region_x= regionX,
                                            region_y= regionY)
                user.save()
                messages.info(request,'회원가입이 완료되었습니다.')
                return redirect("sign_in")
            except:
                messages.warning(request,'다시 입력해주세요.')
                return redirect("sign_up")
        # else:
        #     return render(request, "sign_up.html", context)
    return render(request, "sign_up.html", context)



def logout(request):
    del request.session['user_id']
    request.session.clear()
    return redirect("sign_in")

# def only_member(request):
#     context = None
#     if request.user.is_authenticated:
#         context = {'loginUser': request.user.user_name}
#     return render(request, 'member.html', context)