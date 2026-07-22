"""
展品域数据库服务 - 展品知识库与项目展品
"""
from typing import Dict, List, Optional

from ..config import settings
from .database import DatabaseClientProvider


class ExhibitsDatabaseService(DatabaseClientProvider):
    """展品域相关的数据访问能力。"""

    @classmethod
    def get_exhibits(
        cls,
        project_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> List[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        if project_id:
            query = query.eq("project_id", project_id)
        if unit_id:
            query = query.eq("unit_id", unit_id)
        return query.execute().data or []

    @classmethod
    def get_all_exhibits(cls, user_id: Optional[str] = None) -> List[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        return query.order("created_at", desc=True).execute().data or []

    @classmethod
    def search_exhibits(cls, keyword: str, user_id: Optional[str] = None) -> List[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        return (
            query.or_(
                f"name.ilike.%{keyword}%,time.ilike.%{keyword}%,place.ilike.%{keyword}%,"
                f"material.ilike.%{keyword}%,introduction.ilike.%{keyword}%,other.ilike.%{keyword}%"
            ).execute().data or []
        )

    @classmethod
    def get_exhibit(cls, exhibit_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).select("*").eq("id", exhibit_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.limit(1).execute()
        return result.data[0] if result.data else None

    @classmethod
    def create_exhibit(cls, exhibit_data: Dict) -> Optional[Dict]:
        client = cls.get_client()
        result = client.table(settings.table_exhibits).insert(exhibit_data).execute()
        return result.data[0] if result.data else None

    @classmethod
    def update_exhibit(
        cls,
        exhibit_id: str,
        exhibit_data: Dict,
        user_id: Optional[str] = None,
    ) -> Optional[Dict]:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).update(exhibit_data).eq("id", exhibit_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return result.data[0] if result.data else None

    @classmethod
    def delete_exhibit(cls, exhibit_id: str, user_id: Optional[str] = None) -> bool:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).delete().eq("id", exhibit_id)
        if user_id:
            query = query.eq("user_id", user_id)
        result = query.execute()
        return bool(result.data)

    @classmethod
    def delete_all_exhibits(cls, user_id: Optional[str] = None) -> bool:
        client = cls.get_client()
        query = client.table(settings.table_exhibits).delete().neq("id", "00000000-0000-0000-0000-000000000000")
        if user_id:
            query = query.eq("user_id", user_id)
        query.execute()
        return True


exhibits_db = ExhibitsDatabaseService()
