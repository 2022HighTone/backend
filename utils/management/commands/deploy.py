from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        os.system('ssh -i "highthon.pem" ubuntu@ec2-52-79-227-119.ap-northeast-2.compute.amazonaws.com')
        os.system('git pull https://github.com/2022HighTone/backend.git master')
        os.system('python manage.py run')
        os.system('exit')