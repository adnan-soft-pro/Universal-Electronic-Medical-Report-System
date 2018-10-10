from .xml_utils import (
    chronological_redactable_elements, alphabetical_redactable_elements
)
from .medical_record import MedicalRecord
from .auto_redactable import (
    auto_redact_referrals, auto_redact_consultations, auto_redact_attachments,
    auto_redact_medications, auto_redact_profile_events,
)
from .xml_base import XMLModelBase
from .consultation import Consultation
from .medication import Medication
from .value_event import ValueEvent
from .problem import Problem
from .referral import Referral
from .attachment import Attachment
from instructions.models import Instruction

from typing import List, Dict, TypeVar
T = TypeVar('T')


class MedicalReportDecorator(MedicalRecord):
    # todo: raw_xml type... string or bytes or something else?
    def __init__(self, raw_xml, instruction: Instruction):
        super().__init__(raw_xml)
        self.instruction = instruction

    def consultations(self) -> List[Consultation]:
        return chronological_redactable_elements(
            auto_redact_consultations(
                super().consultations(),
                self.instruction
            )
        )

    def significant_active_problems(self) -> List[Problem]:
        return alphabetical_redactable_elements(
            super().significant_active_problems()
        )

    def significant_past_problems(self) -> List[Problem]:
        return alphabetical_redactable_elements(
            super().significant_past_problems()
        )

    def referrals(self) -> List[Referral]:
        return chronological_redactable_elements(
            auto_redact_referrals(super().referrals())
        )

    def attachments(self) -> List[Attachment]:
        return chronological_redactable_elements(
            auto_redact_attachments(super().attachments())
        )

    def acute_medications(self) -> List[Medication]:
        return chronological_redactable_elements(
            auto_redact_medications(super().acute_medications())
        )

    def repeat_medications(self) -> List[Medication]:
        return chronological_redactable_elements(
            auto_redact_medications(super().repeat_medications())
        )

    def all_allergies(self) -> List[XMLModelBase]:
        return chronological_redactable_elements(super().all_allergies())

    def profile_events_for(self, event_type: str) -> List[XMLModelBase]:
        return self.__table_elements(chronological_redactable_elements(
            auto_redact_profile_events(super().profile_event(event_type))
        ))

    def profile_events_by_type(self) -> Dict[str, List[XMLModelBase]]:
        obj = {}
        for event_type in self.PROFILE_EVENT_TYPES:
            obj[event_type] = self.profile_events_for(event_type)
        return obj

    def bloods_for(self, blood_type: str) -> List[ValueEvent]:
        return self.__table_elements(chronological_redactable_elements(
            super().blood_test(blood_type)
        ))

    def blood_test_results_by_type(self) -> Dict[str, List[ValueEvent]]:
        obj = {}
        for blood_type in ValueEvent.blood_test_types():
            result = self.bloods_for(blood_type)
            if result:
                obj[blood_type] = result
        return obj

    # private
    def __table_elements(self, data: List[T]) -> List[T]:
        max_len = 3
        element_list = data[:max_len]
        element_list += [None] * (max_len - len(element_list))
        return list(reversed(element_list))
