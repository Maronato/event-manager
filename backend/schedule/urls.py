from project.router import base_router, export_router
from . import api, exports

base_router.register("events/my", api.MyEventViewset, "my_event")
base_router.register("events/registered", api.RegisteredEventViewset, "registered_event")
base_router.register(
    "events/not_registered", api.NotRegisteredEventViewset, "not_registered_event"
)
base_router.register("events/attended", api.AttendedEventViewset, "attended_event")
base_router.register("events/full", api.FullEventViewset, "full_event")
base_router.register("events/checkinable", api.CheckinableEventViewset, "checkinable_events")
base_router.register("events/my_full", api.MyFullEventViewset, "my_full_event")
base_router.register("events/feedback", api.FeedbackViewset)

base_router.register("events/attend", api.AttendEvent, 'event_attend')
base_router.register("events/neglect", api.NeglectEvent, 'event_neglect')
base_router.register("events/checkin/fetch", api.FetchCheckinAttendee, 'event_checkin_fetch')
base_router.register("events/checkin", api.CheckinAttendee, 'event_checkin')

base_router.register("events", api.EventViewset, 'event')

apipatterns = []

export_router.register("events", exports.ExportEventsViewset, "events")

app_name = "schedule"
urlpatterns = []
