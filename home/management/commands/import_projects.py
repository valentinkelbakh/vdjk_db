import json

from django.core.management.base import BaseCommand

from home.models import Project


class Command(BaseCommand):
    help = "Import data from JSON file into the database"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        json_file = options["json_file"]
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                project = Project(
                    name=item["name"],
                    description=item["description"],
                    img_link=item["img_link"],
                    apply_link=item["apply_link"],
                )
                project.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Imported project: {project.name}")
                )
