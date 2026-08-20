# pyrefly: ignore [missing-import]
from django.contrib.sitemaps import Sitemap
# pyrefly: ignore [missing-import]
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    protocol = "https"

    priority = 0.8

    changefreq = "weekly"

    def items(self):

        return [

            "home",

            "local_taxi_service",

            "bus_booking",

            "tempo_traveller",

            "outstation_tours",

            "pilgrimage_trips",

            "corporate_travel",

        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):

        priorities = {

            "home": 1.0,

            "local_taxi_service": 0.9,

            "bus_booking": 0.9,

            "tempo_traveller": 0.9,

            "outstation_tours": 0.8,

            "pilgrimage_trips": 0.8,

            "corporate_travel": 0.8,

        }

        return priorities.get(item, 0.7)

    def changefreq(self, item):

        frequencies = {

            "home": "daily",

            "local_taxi_service": "weekly",

            "bus_booking": "weekly",

            "tempo_traveller": "weekly",

            "outstation_tours": "monthly",

            "pilgrimage_trips": "monthly",

            "corporate_travel": "monthly",

        }

        return frequencies.get(item, "monthly")
