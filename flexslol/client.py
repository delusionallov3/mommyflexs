from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from .exceptions import (
    APIError,
    AuthError,
    NotAuthenticatedError,
    UserNotFoundError,
)
from .models import Session, User

_BASE_URL = "https://vxlgyofbpljpmtyirohz.supabase.co"
_REST_URL = f"{_BASE_URL}/rest/v1"
_AUTH_URL = f"{_BASE_URL}/auth/v1"

_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ4bGd5b2ZicGxqcG10eWlyb2h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQxODU0NDMsImV4cCI6MjA4OTc2MTQ0M30.IzzrQmSNIVsLCJybgjAKSlvsMBP2y-AfyNGkp4KKksM"


class _Http:
    def __init__(self) -> None:
        self._session_obj: Optional[Session] = None
        self._http = requests.Session()

    def _headers(self, *, auth_required: bool = False) -> Dict[str, str]:
        if auth_required and self._session_obj is None:
            raise NotAuthenticatedError(
                "This action requires authentication. Call client.auth.login() first."
            )

        token = self._session_obj.access_token if self._session_obj else _ANON_KEY
        return {
            "apikey": _ANON_KEY,
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def get(
        self, url: str, *, params: Optional[dict] = None, auth_required: bool = False
    ) -> Any:
        r = self._http.get(
            url, headers=self._headers(auth_required=auth_required), params=params
        )
        return self._raise_for_status(r)

    def post(self, url: str, *, json: dict, auth_required: bool = False) -> Any:
        r = self._http.post(
            url, headers=self._headers(auth_required=auth_required), json=json
        )
        return self._raise_for_status(r)

    def patch(self, url: str, *, json: dict, auth_required: bool = True) -> Any:
        r = self._http.patch(
            url, headers=self._headers(auth_required=auth_required), json=json
        )
        return self._raise_for_status(r)

    @staticmethod
    def _raise_for_status(r: requests.Response) -> Any:
        if r.status_code in (200, 201, 204):
            if r.status_code == 204 or not r.content:
                return None
            return r.json()
        try:
            detail = r.json()
            msg = (
                detail.get("message")
                or detail.get("msg")
                or detail.get("error_description")
                or str(detail)
            )
        except Exception:
            msg = r.text
        raise APIError(r.status_code, msg)


class AuthClient:
    def __init__(self, http: _Http) -> None:
        self._http = http

    @property
    def session(self) -> Optional[Session]:
        """Return the current active session, or None if not logged in"""
        return self._http._session_obj

    @property
    def is_authenticated(self) -> bool:
        """Return True if a session is active"""
        return self._http._session_obj is not None

    def signup(self, email: str, password: str, *, username: str) -> Session:
        """
        Create a new mew account :3

        Parameters
        ----------
        email:    Email address
        password: pass baby
        username: Desired username (unique btw)

        Returns
        -------
        Session object, the user is automatically logged in after signup
        """
        try:
            data = self._http.post(
                f"{_AUTH_URL}/signup",
                json={
                    "email": email,
                    "password": password,
                    "data": {"username": username},
                    "gotrue_meta_security": {},
                },
            )
        except APIError as e:
            raise AuthError(str(e)) from e

        session = Session.from_dict(data)
        self._http._session_obj = session
        return session

    def login(self, email: str, password: str) -> Session:
        """
        Log in

        Returns
        -------
        Session object stored internally — subsequent requests are authenticated
        """
        try:
            data = self._http.post(
                f"{_AUTH_URL}/token?grant_type=password",
                json={"email": email, "password": password, "gotrue_meta_security": {}},
            )
        except APIError as e:
            raise AuthError(str(e)) from e

        session = Session.from_dict(data)
        self._http._session_obj = session
        return session

    def logout(self) -> None:
        """Clear the current session locally (does not revoke server-side)"""
        self._http._session_obj = None

    def refresh(self) -> Session:
        """
        refresh ??

        Raises
        ------
        NotAuthenticatedError  If not currently logged in
        """
        if not self._http._session_obj:
            raise NotAuthenticatedError("No active session to refresh.")
        try:
            data = self._http.post(
                f"{_AUTH_URL}/token?grant_type=refresh_token",
                json={"refresh_token": self._http._session_obj.refresh_token},
            )
        except APIError as e:
            raise AuthError(str(e)) from e

        session = Session.from_dict(data)
        self._http._session_obj = session
        return session


class UsersClient:
    def __init__(self, http: _Http) -> None:
        self._http = http

    def list(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "public_uid",
        ascending: bool = True,
    ) -> List[User]:
        """
        Return a paginated list of all users

        Parameters
        ----------
        limit:     Max number of results (default 100)
        offset:    Skip this many rows (for pagination)
        order_by:  Column to sort by (default: 'public_uid')
        ascending: Sort direction (default True)
        """
        params = {
            "select": "*",
            "order": f"{order_by}.{'asc' if ascending else 'desc'}",
            "limit": limit,
            "offset": offset,
        }
        data = self._http.get(f"{_REST_URL}/users", params=params)
        return [User.from_dict(u) for u in data]

    def get(self, user_id: str) -> User:
        """
        Fetch a single user by their UUID

        Raises
        ------
        UserNotFoundError  If no user exists with that id
        """
        params = {"select": "*", "id": f"eq.{user_id}"}
        data = self._http.get(f"{_REST_URL}/users", params=params)
        if not data:
            raise UserNotFoundError(f"No user found with id '{user_id}'.")
        return User.from_dict(data[0])

    def get_by_username(self, username: str) -> User:
        """
        Fetch a single user by their username (case-insensitive)

        Raises
        ------
        UserNotFoundError  If no user exists with that username
        """
        params = {"select": "*", "username": f"ilike.{username}"}
        data = self._http.get(f"{_REST_URL}/users", params=params)
        if not data:
            raise UserNotFoundError(f"No user found with username '{username}'.")
        return User.from_dict(data[0])

    def get_by_public_uid(self, public_uid: int) -> User:
        """
        Fetch a user by their numeric public UID

        Raises
        ------
        UserNotFoundError  If no user exists with that public_uid
        """
        params = {"select": "*", "public_uid": f"eq.{public_uid}"}
        data = self._http.get(f"{_REST_URL}/users", params=params)
        if not data:
            raise UserNotFoundError(f"No user found with public_uid '{public_uid}'.")
        return User.from_dict(data[0])

    def search(self, query: str, *, limit: int = 20) -> List[User]:
        """
        Search users whose username starts with *query* (case-insensitive)

        Parameters
        ----------
        query: Prefix to search for.
        limit: Max number of results (default 20)
        """
        params = {
            "select": "*",
            "username": f"ilike.{query}*",
            "limit": limit,
            "order": "public_uid.asc",
        }
        data = self._http.get(f"{_REST_URL}/users", params=params)
        return [User.from_dict(u) for u in data]

    def me(self) -> User:
        """
        Return the profile of the currently authenticated user

        Raises
        ------
        NotAuthenticatedError  If not logged in
        """
        session = self._http._session_obj
        if session is None:
            raise NotAuthenticatedError("Call client.auth.login() first.")
        return self.get(session.user_id)

    def update(
        self,
        *,
        username: Optional[str] = None,
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        discord_booster: Optional[bool] = None,
        bug_hunter: Optional[bool] = None,
        badge_premium: Optional[bool] = None,
        badge_verified: Optional[bool] = None,
        badge_early: Optional[bool] = None,
        badge_owner: Optional[bool] = None,
        badge_admin: Optional[bool] = None,
        custom_badges: Optional[List[Dict[str, str]]] = None,
        profile_badges_order: Optional[List[str]] = None,
        profile_badges_hidden: Optional[List[str]] = None,
        profile_bg_type: Optional[str] = None,
        profile_bg_url: Optional[str] = None,
        profile_sound_url: Optional[str] = None,
        profile_entry_overlay_text: Optional[str] = None,
        profile_ambient_volume: Optional[int] = None,
        profile_theme_id: Optional[str] = None,
        profile_font_id: Optional[str] = None,
        profile_layout_id: Optional[str] = None,
        profile_motion_id: Optional[str] = None,
        profile_cursor_id: Optional[str] = None,
        profile_custom_cursor_url: Optional[str] = None,
        profile_mouse_follow_id: Optional[str] = None,
        profile_name_effect_id: Optional[str] = None,
        profile_display_name_color: Optional[str] = None,
        profile_shell_backdrop: Optional[str] = None,
        profile_shell_opacity_pct: Optional[int] = None,
        profile_shell_width_pct: Optional[int] = None,
        profile_badge_monochrome: Optional[bool] = None,
        profile_badge_mono_hex: Optional[str] = None,
        profile_badge_neon: Optional[bool] = None,
        profile_badge_monochrome_custom: Optional[bool] = None,
        profile_description: Optional[str] = None,
        profile_location_label: Optional[str] = None,
        steam_showcase_url: Optional[str] = None,
        roblox_showcase_url: Optional[str] = None,
        profile_show_volume_control: Optional[bool] = None,
        profile_show_clip_views: Optional[bool] = None,
        profile_show_profile_views: Optional[bool] = None,
        profile_hide_empty_clips: Optional[bool] = None,
        profile_hide_public_stats: Optional[bool] = None,
        profile_show_discord_on_public: Optional[bool] = None,
        profile_discord_username: Optional[str] = None,
        profile_discord_avatar_url: Optional[str] = None,
        profile_discord_accent_hex: Optional[str] = None,
    ) -> User:
        """
        Update the authenticated user's profile

        Raises
        ------
        NotAuthenticatedError  If not logged in.
        """
        session = self._http._session_obj
        if session is None:
            raise NotAuthenticatedError("Call client.auth.login() first.")

        payload: Dict[str, Any] = {}
        local_vars = {
            "username": username,
            "display_name": display_name,
            "avatar_url": avatar_url,
            "discord_booster": discord_booster,
            "bug_hunter": bug_hunter,
            "badge_premium": badge_premium,
            "badge_verified": badge_verified,
            "badge_early": badge_early,
            "badge_owner": badge_owner,
            "badge_admin": badge_admin,
            "custom_badges": custom_badges,
            "profile_badges_order": profile_badges_order,
            "profile_badges_hidden": profile_badges_hidden,
            "profile_bg_type": profile_bg_type,
            "profile_bg_url": profile_bg_url,
            "profile_sound_url": profile_sound_url,
            "profile_entry_overlay_text": profile_entry_overlay_text,
            "profile_ambient_volume": profile_ambient_volume,
            "profile_theme_id": profile_theme_id,
            "profile_font_id": profile_font_id,
            "profile_layout_id": profile_layout_id,
            "profile_motion_id": profile_motion_id,
            "profile_cursor_id": profile_cursor_id,
            "profile_custom_cursor_url": profile_custom_cursor_url,
            "profile_mouse_follow_id": profile_mouse_follow_id,
            "profile_name_effect_id": profile_name_effect_id,
            "profile_display_name_color": profile_display_name_color,
            "profile_shell_backdrop": profile_shell_backdrop,
            "profile_shell_opacity_pct": profile_shell_opacity_pct,
            "profile_shell_width_pct": profile_shell_width_pct,
            "profile_badge_monochrome": profile_badge_monochrome,
            "profile_badge_mono_hex": profile_badge_mono_hex,
            "profile_badge_neon": profile_badge_neon,
            "profile_badge_monochrome_custom": profile_badge_monochrome_custom,
            "profile_description": profile_description,
            "profile_location_label": profile_location_label,
            "steam_showcase_url": steam_showcase_url,
            "roblox_showcase_url": roblox_showcase_url,
            "profile_show_volume_control": profile_show_volume_control,
            "profile_show_clip_views": profile_show_clip_views,
            "profile_show_profile_views": profile_show_profile_views,
            "profile_hide_empty_clips": profile_hide_empty_clips,
            "profile_hide_public_stats": profile_hide_public_stats,
            "profile_show_discord_on_public": profile_show_discord_on_public,
            "profile_discord_username": profile_discord_username,
            "profile_discord_avatar_url": profile_discord_avatar_url,
            "profile_discord_accent_hex": profile_discord_accent_hex,
        }
        for key, value in local_vars.items():
            if value is not None:
                payload[key] = value

        if not payload:
            return self.me()

        url = f"{_REST_URL}/users?id=eq.{session.user_id}"
        self._http.patch(url, json=payload)
        return self.me()
