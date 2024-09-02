from django.shortcuts import render
from .models import Person
# from .models import Post

def test(request):
    test_sentences ={
        '中平',
        'なかひら',
        'ナカヒラ',
        'nakahira',
        'NAKAHIRA',
        '1998/03/02',
    }
    
    pp = Person.objects.all()
    
    return render(request, 'sample2/index.html', {'test_sentences': test_sentences, 'pp': pp})