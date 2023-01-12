from typing import (
    Dict,
    Any
)
from dataclasses import (
    is_dataclass, 
    asdict
)
from settings import default_logger
from client.models import(
    JobOffer,
    NERProcesableJobOffer
)
from client.exceptions import AdapterException


class BaseAdapter:
    
    incoming_data_dataclass = None
    output_data_dataclass = None
    _incoming_instance = None
    _output_instance = None

    def __init__(self) -> None:
        if self.incoming_data_dataclass is None or self.output_data_dataclass is  None:
            raise AdapterException("Incoming dataclass or output dataclass should be defined.")
        if not is_dataclass(self.incoming_data_dataclass) or not is_dataclass(self.output_data_dataclass):
            raise AdapterException("Incoming dataclass or output dataclass classes are not really dataclasses!")
    
    @property
    def incoming_instance(self):
        return self._incoming_instance

    @property
    def output_instance(self):
        return self._output_instance

    def adapt(self, data: Dict[str, Any]):
        self._incoming_instance = self.incoming_data_dataclass(**data)
        self._output_instance = self.output_data_dataclass.from_instance(instance = self.incoming_instance)
        return asdict(self.output_instance)


class JobOfferAdapter(BaseAdapter):
    incoming_data_dataclass = JobOffer
    output_data_dataclass = NERProcesableJobOffer
