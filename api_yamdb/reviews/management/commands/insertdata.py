from django.core.management.base import BaseCommand, CommandError
from reviews.models import Genre,Category, Title,Review,Comment, TitleGenre
from django.contrib.auth import get_user_model
import csv
User=get_user_model()
class Command(BaseCommand):

    def add_arguments(self, parser) -> None:
        return super().add_arguments(parser)

    #id,title_id,genre_id
    def handle(self, *args, **options):
        genre = "E:/python6/Cпринт_10/02_Итоговый проект курса/api_yamdb-master/api_yamdb-master/api_yamdb/static/data/genre_title.csv"
        with open(file=genre,encoding="utf8") as genre_csv:
            reader=csv.reader(genre_csv,delimiter=',')
            count=0
            for row in reader:
                if count>0:
                    TitleGenre.objects.create(title=Title.objects.get(id=int(row[1])),genre=Genre.objects.get(id=int(row[2])+1))
                count+=1
        
