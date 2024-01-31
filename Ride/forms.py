from django import forms
from django.utils import timezone

from Ride.models import Ride


class DuberRideRequestForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Ride
        fields = ['dst_addr', 'owner_desired_arrival_time', 'num_passengers_owner_party', 'owner_desired_vehicle_type',
                  'is_shareable', 'special_requests']
        widgets = {
            'owner_desired_arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(DuberRideRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'owner_desired_arrival_time':
                self.fields[field].widget.attrs['placeholder'] = 'yyyy-mm-dd hh:mm:ss'
            elif field == 'is_shareable':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            elif field == 'special_requests':
                self.fields[field].widget.attrs['rows'] = '5'
                self.fields[field].widget.attrs['placeholder'] = 'Any special requests?'
            elif field == 'num_passengers_owner_party':
                self.fields[field].widget.attrs['min'] = '1'
                self.fields[field].widget.attrs['placeholder'] = '1'

    def clean(self):
        if self.cleaned_data['num_passengers_owner_party'] < 1:
            raise forms.ValidationError("Number of passengers cannot be less than 1!")
        if self.cleaned_data['owner_desired_arrival_time'] < timezone.now():
            raise forms.ValidationError("Desired arrival time cannot be in the past!")