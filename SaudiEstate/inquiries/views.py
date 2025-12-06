from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inquiry, InquiryReply
from properties.models import Property


@login_required
def send_inquiry(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        message = request.POST.get("message")

        Inquiry.objects.create(
            sender=request.user,
            property=property_obj,
            message=message,
        )

        messages.success(request, "Your inquiry has been posted.")
        return redirect("properties:detail", pk=pk)


@login_required
def reply_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)

    if request.user != inquiry.property.owner:
        return HttpResponseForbidden("You are not allowed to reply to this inquiry.")

    if request.method == "POST":
        message = request.POST.get("reply")

        if not message.strip():
            return HttpResponse("Reply cannot be empty", status=400)

        InquiryReply.objects.create(
            inquiry=inquiry,
            sender=request.user,
            message=message
        )

    return redirect("properties:detail", inquiry.property.id)


@login_required
def delete_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)

    if request.user == inquiry.sender or request.user == inquiry.property.owner:
        inquiry.delete()

    return redirect('properties:detail', pk=inquiry.property.id)


@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(InquiryReply, id=reply_id)
    inquiry = reply.inquiry

    if request.user == reply.sender:
        reply.delete()

    return redirect('properties:detail', pk=inquiry.property.id)