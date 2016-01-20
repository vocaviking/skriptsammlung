from django.contrib.auth         import get_user_model
User = get_user_model()
from django.core.files           import File
from django.core.management.base import BaseCommand, CommandError
from django.utils                import timezone
from series.models               import UserProfile

class Command(BaseCommand):
    help = 'Creates the user "Anonymous", used for populating the database with liblist data.'
    def handle(self, *args, **options):
        self.stdout.write('Creating Anonymous User...')
        if User.objects.filter(username='anonymous6115').count() > 0:
            raise CommandError('The anonymous user already exists!')
        profile               = UserProfile()
        profile.title         = ''
        profile.degree        = 'Master of Disaster'
        profile.about_me      = 'Trolling since the beginning...'
        #THIS TOO IS BAD
        profile.image         = File(open('./series/management/commands/anonymous.png','rb'))
        profile.website       = ''
        profile.phone         = ''
        profile.birth_date    = timezone.now()
        profile.show_age      = True
        profile.show_birthday = True
        profile.show_realname = True
        profile.save()

        user             = User()
        user.username    = 'anonymous6115'
        user.first_name  = 'Anon'
        user.last_name   = ''
        user.email       = ''
        user.userprofile = profile
        user.save()
        self.stdout.write('Done')
