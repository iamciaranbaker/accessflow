# AccessFlow

AccessFlow is a comprehensive user access management system designed to streamline CIS engineers' workflows by integrating Jira Service Desk and GitLab. The system enables engineers to view, approve, or decline user requests which automatically trigger GitLab pipelines to provision user accounts on requested services and environments.

The system centralizes user data by replacing the current GitLab-based user storage with a robust database-backed API. This allows for dynamic retrieval of user information, ensuring seamless integration with existing Ansible projects. The system enforces structured request submission, prompting users to provide necessary details via Jira and automating feedback for incomplete or improperly formatted requests.

The internal dashboard for CIS engineers includes advanced features such as user and access management, search capabilities, and SC clearance tracking. Engineers can granularly control user access across specific services and environments, ensuring precision and compliance. Audit logging captures all actions for transparency and accountability.