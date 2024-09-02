import sys
from django.shortcuts import render
from modules import scraper
from .models import News
from django.utils import timezone

# Create your views here.
def display(request):
    # title = scraper.Scraper.get_title_newspaper3k(r'https://news.yahoo.co.jp/pickup/6467328')
    sc = scraper.Scraper()
    info = sc.get_info_newspaper3k(r'https://news.yahoo.co.jp/pickup/6467328')
    News.objects.create(url=info[0], title=info[1], text=info[2], publish_date=timezone.now())
    return render(request, 'display_sample/index.html', {'info': info})
    