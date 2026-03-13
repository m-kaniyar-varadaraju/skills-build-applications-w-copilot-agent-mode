
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Create Users
        tony = User.objects.create(email='tony@stark.com', name='Tony Stark', team=marvel.name)
        steve = User.objects.create(email='steve@rogers.com', name='Steve Rogers', team=marvel.name)
        bruce = User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team=dc.name)
        clark = User.objects.create(email='clark@kent.com', name='Clark Kent', team=dc.name)
        diana = User.objects.create(email='diana@themyscira.com', name='Diana Prince', team=dc.name)
        natasha = User.objects.create(email='natasha@romanoff.com', name='Natasha Romanoff', team=marvel.name)

        # Create Workouts
        pushups = Workout.objects.create(name='Pushups', description='Do pushups', difficulty='easy')
        running = Workout.objects.create(name='Running', description='Run 5km', difficulty='medium')
        flying = Workout.objects.create(name='Flying', description='Fly for 10 minutes', difficulty='hard')
        swimming = Workout.objects.create(name='Swimming', description='Swim 1km', difficulty='medium')

        # Create Activities
        Activity.objects.create(user=tony, type='pushups', duration=20, date=timezone.now().date())
        Activity.objects.create(user=steve, type='running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='pushups', duration=25, date=timezone.now().date())
        Activity.objects.create(user=clark, type='flying', duration=15, date=timezone.now().date())
        Activity.objects.create(user=diana, type='swimming', duration=40, date=timezone.now().date())
        Activity.objects.create(user=natasha, type='running', duration=35, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(user=tony, score=120, rank=1)
        Leaderboard.objects.create(user=steve, score=110, rank=2)
        Leaderboard.objects.create(user=bruce, score=100, rank=3)
        Leaderboard.objects.create(user=clark, score=90, rank=4)
        Leaderboard.objects.create(user=diana, score=85, rank=5)
        Leaderboard.objects.create(user=natasha, score=80, rank=6)

        # Ensure unique index on email for users collection
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
