from app.core.exceptions import ConflictException, NotFoundException


class TopicNotFoundError(NotFoundException):
    def __init__(self, topic_label: str) -> None:
        super().__init__(f"Тему «{topic_label}» не знайдено")


class TopicHasNoOrganizationsError(ConflictException):
    def __init__(self, topic_label: str) -> None:
        super().__init__(f"Для теми «{topic_label}» немає оцінок з організацією")
