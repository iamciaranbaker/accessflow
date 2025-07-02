from accessflow.models.activity_event_type import ActivityEventType
from accessflow.models.activity_log import ActivityLog
from accessflow.models.job_log import JobLog
from accessflow.models.job_run import JobRun
from accessflow.models.job import Job
from accessflow.models.permission_group import PermissionGroup
from accessflow.models.permission import Permission
from accessflow.models.pid import PID
from accessflow.models.request_pid import RequestPID
from accessflow.models.request_service import RequestService
from accessflow.models.request import Request
from accessflow.models.service_environment import ServiceEnvironment
from accessflow.models.service_host_group_team import ServiceHostGroupTeam
from accessflow.models.service_host_group import ServiceHostGroup
from accessflow.models.service import Service
from accessflow.models.team import Team
from accessflow.models.user_permission import UserPermission
from accessflow.models.user import User

model_registry = {
    "ActivityEventType": ActivityEventType,
    "ActivityLog": ActivityLog,
    "JobLog": JobLog,
    "JobRun": JobRun,
    "Job": Job,
    "PermissionGroup": PermissionGroup,
    "Permission": Permission,
    "PID": PID,
    "RequestPID": RequestPID,
    "RequestService": RequestService,
    "Request": Request,
    "ServiceEnvironment": ServiceEnvironment,
    "ServiceHostGroupTeam": ServiceHostGroupTeam,
    "ServiceHostGroup": ServiceHostGroup,
    "Service": Service,
    "Team": Team,
    "UserPermission": UserPermission,
    "User": User
}