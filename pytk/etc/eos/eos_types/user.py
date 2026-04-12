from dataclasses import dataclass
from typing import List


@dataclass
class User:
	"""Represents a single user connected to the Eos show file."""

	id: int
	console_type: str
	console_name: str


@dataclass
class UserListResponse:
	"""Represents the parsed response from /eos/out/get/userlist."""
 
	users: List[User]
	count: int