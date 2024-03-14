from typing import Any
from opentelemetry import metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

class Telemetry:
    def __init__(self) -> None:
        resource = Resource(attributes={
            SERVICE_NAME: "MTG Collector"
        })
        metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics"))
        provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

        # Sets the global default meter provider
        metrics.set_meter_provider(provider)
        meter = metrics.get_meter("Magic.Meter")
        self.request_counter = meter.create_counter("http.client.counter", unit="request", description="Counts number of requests performed")

    def __call__(self):
        return self

telemetry = Telemetry()
