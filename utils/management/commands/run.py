from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        os.system('docker-compose down')
        os.system('docker rmi $(docker images -a -q)')
        os.system('docker volume rm $(docker volume ls -q)')
        os.system('docker-compose up -d')