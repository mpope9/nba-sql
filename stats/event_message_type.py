
from models import EventMessageType
from constants import event_message_types

class EventMessageTypeBuilder:

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([EventMessageType])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([EventMessageType], safe=True)

    def initialize(self):
        """
        Build table from const mappings.
        """

        EventMessageType.insert_many(event_message_types).execute()
