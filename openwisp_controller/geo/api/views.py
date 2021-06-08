from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework import generics, pagination
from rest_framework.permissions import BasePermission
from rest_framework_gis.pagination import GeoJsonPagination
from swapper import load_model

from openwisp_users.api.mixins import FilterByOrganizationManaged, FilterByParentManaged

from .serializers import (
    FloorPlanSerializer,
    GeoJsonLocationSerializer,
    LocationDeviceSerializer,
    LocationSerializer,
    LocationSerializerNew,
)

Device = load_model('config', 'Device')
Location = load_model('geo', 'Location')
DeviceLocation = load_model('geo', 'DeviceLocation')
FloorPlan = load_model('geo', 'FloorPlan')


class DevicePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.query_params.get('key') == obj.key


class ListViewPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DeviceLocationView(generics.RetrieveUpdateAPIView):
    serializer_class = LocationSerializer
    permission_classes = (DevicePermission,)
    queryset = Device.objects.select_related(
        'devicelocation', 'devicelocation__location'
    )

    def get_location(self, device):
        try:
            return device.devicelocation.location
        except ObjectDoesNotExist:
            return None

    def get_object(self, *args, **kwargs):
        device = super().get_object()
        location = self.get_location(device)
        if location:
            return location
        # if no location present, automatically create it
        return self.create_location(device)

    def create_location(self, device):
        location = Location(
            name=device.name,
            type='outdoor',
            organization=device.organization,
            is_mobile=True,
        )
        location.full_clean()
        location.save()
        dl = DeviceLocation(content_object=device, location=location)
        dl.full_clean()
        dl.save()
        return location


class GeoJsonLocationListPagination(GeoJsonPagination):
    page_size = 1000


class GeoJsonLocationList(FilterByOrganizationManaged, generics.ListAPIView):
    queryset = Location.objects.filter(devicelocation__isnull=False).annotate(
        device_count=Count('devicelocation')
    )
    serializer_class = GeoJsonLocationSerializer
    pagination_class = GeoJsonLocationListPagination


class LocationDeviceList(FilterByParentManaged, generics.ListAPIView):
    serializer_class = LocationDeviceSerializer
    pagination_class = ListViewPagination
    queryset = Device.objects.none()

    def get_parent_queryset(self):
        qs = Location.objects.filter(pk=self.kwargs['pk'])
        return qs

    def get_queryset(self):
        super().get_queryset()
        qs = Device.objects.filter(devicelocation__location_id=self.kwargs['pk'])
        return qs


class FloorPlanListCreateView(generics.ListCreateAPIView):
    serializer_class = FloorPlanSerializer
    queryset = FloorPlan.objects.all()


class FloorPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FloorPlanSerializer
    queryset = FloorPlan.objects.all()


class LocationListCreateView(generics.ListCreateAPIView):
    serializer_class = LocationSerializerNew
    queryset = Location.objects.all()


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializerNew
    queryset = Location.objects.all()


device_location = DeviceLocationView.as_view()
geojson = GeoJsonLocationList.as_view()
location_device_list = LocationDeviceList.as_view()
list_floorplan = FloorPlanListCreateView.as_view()
detail_floorplan = FloorPlanDetailView.as_view()
list_location = LocationListCreateView.as_view()
detail_location = LocationDetailView.as_view()
