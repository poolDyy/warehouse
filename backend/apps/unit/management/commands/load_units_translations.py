import json
import os
from argparse import ArgumentParser
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.unit.models import Unit, UnitGroup, UnitGroupTranslation, UnitTranslation


class Command(BaseCommand):
    help = 'Loads units and groups with translations from a JSON file into the database'

    json_file_path = settings.BASE_DIR / 'json_data' / 'units' / 'units.json'

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def _load_json_data(self, file_path: str) -> dict[str, list[dict[str, Any]]]:
        """Читает данные из JSON-файла."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} does not exist')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data: dict[str, list[dict[str, Any]]] = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON format - {e}')
        except Exception as e:
            raise IOError(f'Error reading file: {e}')

    def _process_groups(self, groups_data: list[dict[str, Any]]) -> None:
        """Обрабатывает группы и их переводы."""
        for group_data in groups_data:
            group_id: int = group_data['id']

            # Создаем или получаем группу
            group, created = UnitGroup.objects.get_or_create(id=group_id)
            self.stdout.write(f'{"Created" if created else "Found"} group {group_id}')

            # Обработка переводов группы
            for translation in group_data.get('translations', []):
                language_code: str = translation['language_code']
                title: str = translation['title']
                UnitGroupTranslation.objects.update_or_create(
                    group=group, language_code=language_code, defaults={'title': title}
                )
                self.stdout.write(f'Processed translation for group {group_id} ({language_code}: {title})')

    def _process_units(self, units_data: list[dict[str, Any]]) -> None:
        """Обрабатывает единицы измерения и их переводы."""
        for unit_data in units_data:
            unit_id: int = unit_data['id']
            group_id: int = unit_data['group_id']
            coefficient: float = unit_data['coefficient']

            # Проверяем существование группы
            try:
                group: UnitGroup = UnitGroup.objects.get(id=group_id)
            except UnitGroup.DoesNotExist:
                self.stderr.write(f'Error: Group {group_id} does not exist for unit {unit_id}')
                continue

            # Создаем или получаем единицу измерения
            unit, created = Unit.objects.get_or_create(
                id=unit_id, defaults={'group': group, 'coefficient': Decimal(str(coefficient))}
            )
            if created:
                self.stdout.write(f'Created unit {unit_id}')
            else:
                # Проверяем, совпадают ли существующие данные
                if unit.group_id != group_id or unit.coefficient != Decimal(str(coefficient)):
                    self.stdout.write(f'Warning: Unit {unit_id} has different group_id or coefficient. Updating.')
                    unit.group = group
                    unit.coefficient = Decimal(str(coefficient))
                    unit.save()
                self.stdout.write(f'Unit {unit_id} already exists')

            # Обработка переводов единицы измерения
            for translation in unit_data.get('translations', []):
                language_code: str = translation['language_code']
                title: str = translation['title']
                short_title: str = translation['short_title']
                UnitTranslation.objects.update_or_create(
                    unit=unit, language_code=language_code, defaults={'title': title, 'short_title': short_title}
                )
                self.stdout.write(f'Processed translation for unit {unit_id} ({language_code}: {title})')

    def handle(self, *args: Any, **options: Any) -> None:
        json_file_path: str = options.get('json_file', self.json_file_path)

        try:
            data: dict[str, list[dict[str, Any]]] = self._load_json_data(json_file_path)

            with transaction.atomic():
                self._process_groups(data.get('groups', []))
                self._process_units(data.get('units', []))

            self.stdout.write(self.style.SUCCESS('Successfully loaded units and groups with translations from JSON'))
        except (FileNotFoundError, ValueError, IOError) as e:
            self.stderr.write(str(e))
        except Exception as e:
            self.stderr.write(f'Error processing data: {e}')
            raise
