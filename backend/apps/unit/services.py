from django.utils.translation import get_language

from apps.unit.models import Unit, UnitGroup, UnitGroupTranslation, UnitTranslation


class UnitTranslationService:
    @classmethod
    def get_unit_group_translation(
        cls,
        group: UnitGroup,
        language: str | None = None,
    ) -> UnitGroupTranslation:
        """Возвращает локализованный вариант группы ед. измерений."""
        lang = get_language() if language is None else language

        translation = group.translations.filter(language_code=lang).first()
        if not translation:
            translation = group.translations.filter(language_code='en').first()
        return translation

    @classmethod
    def get_unit_group_translation_by_id(
        cls,
        group_id: int,
        language: str | None = None,
    ) -> UnitGroupTranslation:
        """Возвращает локализованный вариант группы ед. измерений."""
        lang = get_language() if language is None else language
        translation = (
            UnitGroupTranslation.objects.select_related('group')
            .filter(
                language_code=lang,
                group_id=group_id,
            )
            .first()
        )
        if not translation:
            translation = (
                UnitGroupTranslation.objects.select_related('group')
                .filter(
                    group_id=group_id,
                )
                .first()
            )
        return translation

    @classmethod
    def get_unit_translation(
        cls,
        unit: Unit,
        language: str | None = None,
    ) -> UnitTranslation:
        """Возвращает локализованный вариант ед. измерений."""
        lang = get_language() if language is None else language
        translation = unit.translations.filter(language_code=lang).first()
        if not translation:
            translation = unit.translations.filter(language_code='en').first()
        return translation

    @classmethod
    def get_unit_translation_by_id(
        cls,
        unit_id: int,
        language: str | None = None,
    ) -> UnitTranslation:
        """Возвращает локализованный вариант ед. измерений."""
        lang = get_language() if language is None else language
        translation = (
            UnitTranslation.objects.select_related('unit', 'unit__group')
            .filter(
                language_code=lang,
                unit_id=unit_id,
            )
            .first()
        )
        if not translation:
            translation = (
                UnitTranslation.objects.select_related('unit', 'unit__group')
                .filter(
                    unit_id=unit_id,
                )
                .first()
            )
        return translation
