from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def chart(request):
    return render(request, 'chart.html')

def map(request):
    return render(request, 'map.html')

def msg(request):
    return render(request, 'msg.html')

def sign_in(request):
    if request.method == "POST":
        userEmail = request.POST['userEmail']
        password = request.POST['password']
        user = authenticate(username=userEmail, password=password)

        if user is not None:
            print('정상 출력')
            return redirect("chart.html")
        else:
            print('비정상 출력')
            return render(request, 'sign_in.html', {'error': '사용자 아이디 또는 패스워드가 틀립니다.'})
    else:
        return render(request, 'sign_in.html')

def sign_up(request):
    if request.method == "POST":
        print(request.POST)
        userName = request.POST("userName")
        userEmail = request.POST("userEmail")
        password = request.POST("password")
        confirm_password = request.POST("confirm_password")

        user = User.objects.create_user(userName, userEmail, password)
        user.save()
        return redirect("sign_in")
    return render(request, "sign_up.html")

    # res_data = None
    # if request.method == 'POST':
    #     userName = request.POST.get('userName', None)
    #     userEmail = request.POST.get('userEmail')
    #     password = request.POST.get('password', None)
    #     confirm_password = request.POST.get('confirm_password', None)
    #
    #     res_data = {}
    #     if User.objects.filter(userEmail=userEmail):
    #         res_data['error'] = '이미 가입된 아이디(이메일주소)입니다.'
    #     elif password != confirm_password:
    #         res_data['error'] = '비밀번호가 다릅니다.'
    #     else:
    #         res_data['error'] = '회원가입이 완료되었습니다.'
    #         user = User.objects.create_user(userEmail=userEmail,
    #                                         password=password)
    #         auth.login(request, user)
    #         redirect("chart.html")
    # return render(request, 'sign_up.html', res_data)

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("sign_in")

# def only_member(request):
#     context = None
#     if request.user.is_authenticated:
#         context = {'loginUser': request.user.user_name}
#     return render(request, 'member.html', context)
