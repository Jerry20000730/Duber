from django import forms

from Ride.models import Ride


class DuberRideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['dst_addr', 'owner_desired_arrival_time', 'num_passengers_owner_party', 'owner_desired_vehicle_type', 'is_shareable', 'special_requests']

    def __init__(self, *args, **kwargs):
        super(DuberRideRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'