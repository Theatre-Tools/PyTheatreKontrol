from typing import TYPE_CHECKING
import time

from pyosc import OSCFalse, OSCMessage, OSCString, OSCTrue, OSCInt

from pytk.etc.eos.eos_types.ping import PingResponse
from pytk.etc.eos.eos_types.processor import Processor, ProcResponse
from pytk.etc.eos.eos_validators.ping import PingValidator
from pytk.etc.eos.eos_validators.processor import Processor_Info, numProcessors


from .eos_types import VersionInfo, VersionResponse
from .eos_validators import VersionValidator

if TYPE_CHECKING:
	from .eos import EOS


class Utilities:
	def __init__(self, eos: "EOS") -> None:
		self._eos = eos

	@property
	def version(self) -> VersionResponse | None:
		message = OSCMessage(address="/eos/get/version", args=())
		response = self._eos.instance.call(
			message=message,
			return_address="/eos/out/get/version",
			validator=VersionValidator,
		)
		try:
			if response is None:
				raise RuntimeError("No response received for version message.")
			if isinstance(response, list):
				raise RuntimeError("Multiple responses received for version message. Expected only one.")
			eos_response = VersionInfo(
				major=response.message.eos.major,
				minor=response.message.eos.minor,
				patch=response.message.eos.patch,
				build=response.message.eos.build,
			)
			fixture_lib_response = VersionInfo(
				major=response.message.fixture_lib.major,
				minor=response.message.fixture_lib.minor,
				patch=response.message.fixture_lib.patch,
				build=response.message.fixture_lib.build,
			)
			return VersionResponse(
				eos=eos_response,
				fixture_lib=fixture_lib_response,
				gel_swatch_type=response.message.gel_swatch_type,
			)
		except Exception as e:
			raise RuntimeError(f"Error processing version response: {e}")


	def ping(self, ping_message: str = 'PyShowControl') -> PingResponse | None:
		message = OSCMessage(address="/eos/ping", args=(OSCString(value=ping_message),))
		response = self._eos.instance.call(message=message, return_address="/eos/out/ping", validator=PingValidator)
		try:
			if response is None:
				raise RuntimeError("No response received for ping message.")
			if isinstance(response, list):
				raise RuntimeError("Multiple responses received for ping message. Expected only one.")
			latency = response.latency
			return PingResponse(message=response.message.message, latency=latency)

		except Exception as e:
			raise RuntimeError(f"Error processing ping response: {e}")

	def processors(self) -> ProcResponse | None:
		initial = self._eos.instance.call(
			message=OSCMessage(address="/eos/get/processors", args=()),
			return_address="/eos/out/get/processors",
			validator=numProcessors,
		)
		if initial is not None and not isinstance(initial, list):
			Processors = initial.message.num_processors
			time.sleep(0.2)
			info = self._eos.instance.call(
				message=OSCMessage(address="/eos/get/processors", args=()),
				return_address="/eos/out/get/processors",
				responses=Processors,
				validator=Processor_Info,
				prefix=1
			)
			if info is not None and not isinstance(info, list):
				return ProcResponse(
					count=1,
					processors=Processor(
						id=info.message.processor_id,
						backup_id=info.message.backup_id,
						host_flag=info.message.host_flag,
						health_status=info.message.health_status,
						label=info.message.label,
						name=info.message.name,
						description=info.message.description,
						IP_address=info.message.IP_address,
						universe_string=info.message.universe_string
					)
				)
			elif isinstance(info, list):
				return ProcResponse(
					count=Processors,
					processors=[
						Processor(
							id=item.message.processor_id,
							backup_id=item.message.backup_id,
							host_flag=item.message.host_flag,
							health_status=item.message.health_status,
							label=item.message.label,
							name=item.message.name,
							description=item.message.description,
							IP_address=item.message.IP_address,
							universe_string=item.message.universe_string
						) for item in info
					]
				)
       
			
