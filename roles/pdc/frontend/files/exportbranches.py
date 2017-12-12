""" Export component branches.

This is used to drive the pagure-sync-bugzilla script.
"""

import collections
import json

from django.core.management.base import BaseCommand
from pdc.apps.componentbranch.models import ComponentBranch
from pdc.apps.componentbranch.serializers import is_branch_active


class Command(BaseCommand):
    help = 'Export a JSON file with information about all component branches'

    def handle(self, *args, **options):
        all_entries = ComponentBranch.objects.all()
        output = collections.defaultdict(lambda: collections.defaultdict(list))
        for entry in all_entries:
            if not is_branch_active(entry):
                continue
            output[entry.type.name][entry.global_component.name].append(entry.name)
        self.stdout.write(json.dumps(output))
