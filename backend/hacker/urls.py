from django.urls import path, include
from project.router import base_router, export_router
from . import api, exports, views

""" API """

# Hacker actions
base_router.register("hackers/me/confirm", api.ConfirmPresence, "hacker_me_confirm")
base_router.register("hackers/me/withdraw", api.Withdraw, "hacker_me_withdraw")
base_router.register(
    "hackers/me/undo_withdraw", api.UndoWithdraw, "hacker_me_undo_withdraw"
)
# Staff actions
base_router.register("hackers/admit", api.Admit, "staff_hacker_admit")
base_router.register("hackers/decline", api.Decline, "staff_hacker_decline")
base_router.register("hackers/unwaitlist", api.Unwaitlist, "staff_hacker_unwaitlist")
base_router.register(
    "hackers/checkin/fetch", api.FetchCheckinHacker, "staff_hacker_checkin_fetch"
)
base_router.register("hackers/checkin", api.CheckinHacker, "staff_hacker_checkin")
# Admin actions
base_router.register("hackers/toggle", api.ToggleIsHacker, "admin_hacker_toggle")


""" Export """

export_router.register(
    "hackers/scanned", exports.ExportScannedHackers, "hacker_scanned"
)
export_router.register("hackers/all", exports.ExportAllHackers, "hacker_all")

apipatterns = []
urlpatterns = []

app_name = "hacker"
payment_urlpatterns = [
    path("pagseguro/checkout/", views.PaymentView.as_view(), name="pagseguro_checkout"),
    path(
        "pagseguro/notifications/",
        include(("pagseguro.urls", "pagseguro"), namespace="pagseguro_notifications"),
    ),
]
