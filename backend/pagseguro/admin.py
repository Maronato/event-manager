# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from pagseguro.models import Checkout, Transaction, TransactionHistory


class CheckoutAdmin(admin.ModelAdmin):

    list_display = ("id", "code", "date", "success")
    list_display_links = ("id",)
    search_fields = ["code"]
    list_filter = ("date", "success")


class TransactionHistoryInline(admin.TabularInline):

    list_display = ("id", "transaction", "status", "date")
    list_display_links = ("id",)
    search_fields = ["transaction__code"]
    list_filter = ("status", "date")
    model = TransactionHistory
    extra = 0


class TransactionAdmin(admin.ModelAdmin):

    list_display = ("code", "reference", "status", "date", "last_event_date")
    list_display_links = ("code",)
    search_fields = ["code", "reference"]
    list_filter = ("status", "date", "last_event_date")
    inlines = [TransactionHistoryInline]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(
            hacker__profile__user__email__icontains=search_term
        )
        return queryset, use_distinct


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Transaction, TransactionAdmin)
