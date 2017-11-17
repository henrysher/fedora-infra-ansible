import json

from django.core.management.base import BaseCommand
from pdc.apps.componentbranch.models import ComponentBranch
from pdc.apps.componentbranch.serializers import is_branch_active

class Command(BaseCommand):
    help = 'Export a JSON file with information about all component branches'

    def handle(self, *args, **options):
        all_entries = ComponentBranch.objects.all()
        exported = [e.export() for e in all_entries]
        for i, entry in enumerate(all_entries):
            exported[i]['active'] = is_branch_active(entry)
        self.stdout.write(json.dumps(exported, indent=2))
