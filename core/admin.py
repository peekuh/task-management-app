from django.contrib import admin
from django.core.mail import send_mail
from .models import Invitation
from django.conf import settings

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'expires_at', 'is_used', 'invited_by')
    search_fields = ('email',)
    readonly_fields = ('token', 'invited_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new invitations
            obj.invited_by = request.user
        obj.save()
        
        # Send invitation email
        invitation_url = f"{settings.SITE_URL}/register/{obj.token}"
        email_body = f"""
        Hello!

        You've been invited to join our task management application.
        Click the link below to create your account:

        {invitation_url}

        This invitation will expire on {obj.expires_at.strftime('%Y-%m-%d')}.

        Best regards,
        Your App Team
        """
        
        send_mail(
            subject="Invitation to Join Task Management App",
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[obj.email],
            fail_silently=False,
        )