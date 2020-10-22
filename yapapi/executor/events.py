"""Representing events in Golem computation."""
import dataclasses
from datetime import timedelta
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Optional, Type, Tuple

from yapapi.props import NodeInfo

ExcInfo = Tuple[Type[BaseException], BaseException, Optional[TracebackType]]


@dataclass(init=False)
class Event:
    """An abstract base class for types of events emitted by `Executor.submit()`."""

    def __init__(self):
        raise NotImplementedError()

    def extract_exc_info(self) -> Tuple[Optional[ExcInfo], "Event"]:
        """Extract exception information from this event.

        Return the extracted exception information
        and a copy of the event without the exception information.
        """
        return None, self


@dataclass(init=False)
class HasExcInfo(Event):
    """A base class for types of events that carry an optional exception info."""

    exc_info: Optional[ExcInfo] = None

    def extract_exc_info(self) -> Tuple[Optional[ExcInfo], "Event"]:
        """Return the `exc_info` field and a copy of this event with the field set to `None`."""

        exc_info = self.exc_info
        me = dataclasses.replace(self, exc_info=None)
        return exc_info, me


@dataclass
class ComputationStarted(Event):
    pass


@dataclass
class ComputationFinished(HasExcInfo):
    """Indicates successful completion if `exc_info` is `None` and a failure otherwise."""


@dataclass
class SubscriptionCreated(Event):
    sub_id: str


@dataclass
class SubscriptionFailed(Event):
    reason: str


@dataclass
class CollectFailed(Event):
    sub_id: str
    reason: str


@dataclass(init=False)
class ProposalEvent(Event):
    prop_id: str


@dataclass
class ProposalReceived(ProposalEvent):
    provider_id: str


@dataclass
class ProposalRejected(ProposalEvent):
    reason: Optional[str] = None


@dataclass
class ProposalResponded(ProposalEvent):
    pass


@dataclass
class ProposalConfirmed(ProposalEvent):
    pass


@dataclass
class ProposalFailed(ProposalEvent):
    reason: str


@dataclass
class NoProposalsConfirmed(Event):
    num_offers: int
    timeout: timedelta


@dataclass(init=False)
class AgreementEvent(Event):
    agr_id: str


@dataclass
class AgreementCreated(AgreementEvent):
    provider_id: NodeInfo


@dataclass
class AgreementConfirmed(AgreementEvent):
    pass


@dataclass
class AgreementRejected(AgreementEvent):
    pass


@dataclass
class PaymentAccepted(AgreementEvent):
    inv_id: str
    amount: str


@dataclass
class PaymentPrepared(AgreementEvent):
    pass


@dataclass
class PaymentQueued(AgreementEvent):
    pass


@dataclass
class InvoiceReceived(AgreementEvent):
    inv_id: str
    amount: str


@dataclass
class WorkerStarted(AgreementEvent):
    pass


@dataclass
class ActivityCreated(AgreementEvent):
    act_id: str


@dataclass
class ActivityCreateFailed(AgreementEvent):
    pass


@dataclass(init=False)
class TaskEvent(Event):
    task_id: str


@dataclass
class TaskStarted(AgreementEvent, TaskEvent):
    task_data: Any


@dataclass
class WorkerFinished(HasExcInfo, AgreementEvent):
    """Indicates successful completion if `exc_info` is `None` and a failure otherwise."""


@dataclass(init=False)
class ScriptEvent(AgreementEvent):
    task_id: Optional[str]


@dataclass
class ScriptSent(ScriptEvent):
    cmds: Any


@dataclass
class CommandExecuted(ScriptEvent):
    success: bool
    cmd_idx: int
    command: Any
    message: str


@dataclass
class GettingResults(ScriptEvent):
    pass


@dataclass
class ScriptFinished(ScriptEvent):
    pass


@dataclass
class TaskAccepted(TaskEvent):
    result: Any


@dataclass
class TaskRejected(TaskEvent):
    reason: Optional[str]


@dataclass
class DownloadStarted(Event):
    path: str


@dataclass
class DownloadFinished(Event):
    path: str