from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from services.emisapiservices import services
from services.xml.medical_report_decorator import MedicalReportDecorator
from services.xml.patient_list import PatientList
from .dummy_models import (DummyInstruction, DummyClient, DummyPatient)
from medicalreport.forms import MedicalReportFinaliseSubmitForm
from .models import Redaction
from instructions.models import Instruction
from .functions import create_or_update_redaction_record


# Create your views here.
def get_matched_patient(patient):
    raw_xml = services.GetPatientList(patient).call()
    patients = PatientList(raw_xml).patients()
    return patients


def get_patient_record(patient_number):
    raw_xml = services.GetMedicalRecord(patient_number).call()
    # redacted = redaction_elements(raw_xml, [".//Event[GUID='{12904CD5-1B75-4BBF-95ED-338EC0C6A5CC}']",
    #     ".//ConsultationElement[Attachment/GUID='{6BC4493F-DB5F-4C74-B585-05B0C3AA53C9}']",
    #     ".//ConsultationElement[Referral/GUID='{1FA96ED4-14F8-4322-B6F5-E00262AE124D}']",
    #     ".//Medication[GUID='{5A786379-97B4-44FD-9726-E3C9C5E34E32}']",
    #     ".//Medication[GUID='{A18F2B49-8ECA-436A-98F8-5C26E4F495DC}']",
    #     ".//Medication[GUID='{A1C57DC5-CCC6-4CD2-871B-C8A07ADC7D06}']",
    #     ".//Event[GUID='{EC323C66-8698-4802-9731-6AC229B11D6D}']",
    #     ".//Event[GUID='{6F058DA7-420E-422A-9CE6-84F3CA9CA246}']"])
    return raw_xml


def reject_request(request, instruction_id):
    instruction = Instruction.objects.get(id=instruction_id)
    instruction.reject(request.POST)
    return redirect('instructions:view_pipeline')


def select_patient(request, instruction_id, patient_emis_number):
    try:
        redaction = Redaction.objects.get(instruction=instruction_id)
    except Redaction.DoesNotExist:
        redaction = Redaction()
        redaction.instruction = instruction

    redaction.patient_emis_number = patient_emis_number
    redaction.save()
    return redirect('medicalreport:edit_report', instruction_id=instruction_id)


def set_patient_emis_number(request, instruction_id):
    instruction = Instruction.objects.get(id=instruction_id)
    dummy_patient = DummyPatient(instruction.patient.user.first_name, instruction.patient.user.last_name, instruction.patient.date_of_birth)
    patient_list = get_matched_patient(dummy_patient)

    return render(request, 'medicalreport/patient_emis_number.html', {
        'patient_list': patient_list,
        'instruction': instruction
    })


def edit_report(request, instruction_id):
    try:
        redaction = Redaction.objects.get(instruction=instruction_id)
        if not redaction.patient_emis_number:
            raise Redaction.DoesNotExist
    except Redaction.DoesNotExist:
        return redirect('medicalreport:set_patient_emis_number', instruction_id=instruction_id)

    instruction = get_object_or_404(Instruction, id=instruction_id)
    raw_xml = services.GetMedicalRecord(redaction.patient_emis_number).call()
    medical_record_decorator = MedicalReportDecorator(raw_xml, instruction)
    dummy_instruction = DummyInstruction(instruction)
    finalise_submit_form = MedicalReportFinaliseSubmitForm(request.user)

    return render(request, 'medicalreport/medicalreport_edit.html', {
        'medical_record': medical_record_decorator,
        'redaction': redaction,
        'instruction': dummy_instruction,
        'finalise_submit_form': finalise_submit_form,
    })


def update_report(request, instruction_id):
    instruction = get_object_or_404(Instruction, id=instruction_id)
    create_or_update_redaction_record(request, instruction)
    return redirect('medicalreport:edit_report', instruction_id=instruction_id)
