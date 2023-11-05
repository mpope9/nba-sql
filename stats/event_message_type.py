"""
------------------------------------------------------------------------------
Copyright 2023 Matthew Pope

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------


Initializer for the EventMessageType object.
"""

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
