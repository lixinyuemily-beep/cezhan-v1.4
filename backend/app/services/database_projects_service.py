"""
项目域数据库服务 - 项目、单元、完成项目、文本段落
"""
from typing import Dict, List, Optional

from ..config import settings
from .database import DatabaseClientProvider


class ProjectsDatabaseService(DatabaseClientProvider):
    """项目域相关的数据访问能力。"""

    @classmethod
    def get_projects(cls, user_id: Optional[str] = None) -> List[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_projects).select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        return query.order("created_at", desc=True).execute().data or []

    @classmethod
    def get_project(cls, project_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_projects).select("*").eq("id", project_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return result.data[0] if result.data else None

    @classmethod
    def create_project(cls, project_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_projects).insert(project_data).execute()
        return result.data[0] if result.data else None

    @classmethod
    def update_project(
        cls,
        project_id: str,
        project_data: Dict,
        user_id: Optional[str] = None,
    ) -> Optional[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_projects).update(project_data).eq("id", project_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return result.data[0] if result.data else None

    @classmethod
    def delete_project(cls, project_id: str, user_id: Optional[str] = None) -> bool:
        client = cls.get_client()
        query = client.table(settings.table_projects).delete().eq("id", project_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return bool(result.data)

    @classmethod
    def get_units(cls, project_id: str) -> List[Dict]:
        client = cls.get_client()
        result = (
            client.table(settings.table_units)
            .select("*")
            .eq("project_id", project_id)
            .order("order")
            .execute()
        )
        return result.data or []

    @classmethod
    def get_unit(cls, unit_id: str) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_units).select("*").eq("id", unit_id).limit(1).execute()
        return result.data[0] if result.data else None

    @classmethod
    def create_unit(cls, unit_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_units).insert(unit_data).execute()
        return result.data[0] if result.data else None

    @classmethod
    def update_unit(cls, unit_id: str, unit_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_units).update(unit_data).eq("id", unit_id).execute()
        return result.data[0] if result.data else None

    @classmethod
    def delete_unit(cls, unit_id: str) -> bool:
        client = cls.get_client()
        result = client.table(settings.table_units).delete().eq("id", unit_id).execute()
        return bool(result.data)

    @classmethod
    def create_completed_project(cls, project_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_completed_projects).insert(project_data).execute()
        return result.data[0] if result.data else None

    @classmethod
    def get_completed_projects(cls, user_id: Optional[str] = None) -> List[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_completed_projects).select("*")
        if user_id:
            return query.eq("user_id", user_id).order("created_at", desc=True).execute().data or []
        return query.order("created_at", desc=True).execute().data or []

    @classmethod
    def get_completed_project(
        cls,
        project_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_completed_projects).select("*").eq("project_id", project_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return result.data[0] if result.data else None

    @classmethod
    def delete_completed_project(cls, project_id: str, user_id: Optional[str] = None) -> bool:
        client = cls.get_client()
        query = client.table(settings.table_completed_projects).delete().eq("project_id", project_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return bool(result.data)

    @classmethod
    def get_text_sections(cls, project_id: str) -> List[Dict]:
        client = cls.get_client()
        result = (
            client.table(settings.table_text_sections)
            .select("*")
            .eq("project_id", project_id)
            .order("order")
            .execute()
        )
        return result.data or []

    @classmethod
    def get_text_section(cls, section_id: str) -> Optional[Dict]:
        client = cls.get_client()
        result = (
            client.table(settings.table_text_sections)
            .select("*")
            .eq("id", section_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    @classmethod
    def create_text_section(cls, section_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_text_sections).insert(section_data).execute()
        return result.data[0] if result.data else None

    @classmethod
    def update_text_section(cls, section_id: str, section_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_text_sections).update(section_data).eq("id", section_id).execute()
        return result.data[0] if result.data else None

    @classmethod
    def delete_text_section(cls, section_id: str) -> bool:
        client = cls.get_client()
        result = client.table(settings.table_text_sections).delete().eq("id", section_id).execute()
        return bool(result.data)


projects_db = ProjectsDatabaseService()
