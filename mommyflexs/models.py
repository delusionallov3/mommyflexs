from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class CustomBadge:
    id: str
    name: str
    icon_url: str

    @classmethod
    def from_dict(cls, d: dict) -> "CustomBadge":
        return cls(id=d["id"], name=d["name"], icon_url=d["icon_url"])


@dataclass
class User:
    id: str
    username: str
    public_uid: Optional[int] = None
    display_name: Optional[str] = None
    phone: Optional[str] = None
    views: Optional[int] = None
    monthly_views: Optional[int] = None
    total_views: Optional[int] = None
    total_comments: Optional[int] = None
    avatar: Optional[str] = None
    avatar_url: Optional[str] = None
    discord_booster: bool = False
    bug_hunter: bool = False
    badge_premium: bool = False
    badge_verified: bool = False
    badge_early: bool = False
    badge_owner: bool = False
    badge_admin: bool = False
    custom_badges: List[CustomBadge] = field(default_factory=list)
    profile_bg_type: Optional[str] = None
    profile_bg_url: Optional[str] = None
    profile_sound_url: Optional[str] = None
    profile_entry_overlay_text: Optional[str] = None
    profile_ambient_volume: int = 100
    profile_theme_id: Optional[str] = None
    profile_font_id: Optional[str] = None
    profile_layout_id: Optional[str] = None
    profile_motion_id: Optional[str] = None
    profile_cursor_id: Optional[str] = None
    profile_custom_cursor_url: Optional[str] = None
    profile_mouse_follow_id: Optional[str] = None
    profile_name_effect_id: Optional[str] = None
    profile_display_name_color: Optional[str] = None
    profile_shell_backdrop: Optional[str] = None
    profile_shell_opacity_pct: int = 92
    profile_shell_width_pct: int = 100
    profile_badges_order: List[str] = field(default_factory=list)
    profile_badges_hidden: List[str] = field(default_factory=list)
    profile_badge_monochrome: bool = False
    profile_badge_mono_hex: Optional[str] = None
    profile_badge_neon: bool = False
    profile_badge_monochrome_custom: bool = False
    profile_description: Optional[str] = None
    profile_location_label: Optional[str] = None
    steam_showcase_url: Optional[str] = None
    roblox_showcase_url: Optional[str] = None
    profile_show_volume_control: bool = True
    profile_show_clip_views: bool = True
    profile_show_profile_views: bool = True
    profile_hide_empty_clips: bool = False
    profile_hide_public_stats: bool = False
    profile_show_discord_on_public: bool = False
    profile_discord_username: Optional[str] = None
    profile_discord_avatar_url: Optional[str] = None
    profile_discord_accent_hex: Optional[str] = None
    last_username_change: Optional[str] = None
    username_locked_until: Optional[str] = None
    username_changed_at: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        return cls(
            id=d["id"],
            username=d["username"],
            public_uid=d.get("public_uid"),
            display_name=d.get("display_name"),
            phone=d.get("phone"),
            views=d.get("views"),
            monthly_views=d.get("monthly_views"),
            total_views=d.get("total_views"),
            total_comments=d.get("total_comments"),
            avatar=d.get("avatar"),
            avatar_url=d.get("avatar_url"),
            discord_booster=d.get("discord_booster", False),
            bug_hunter=d.get("bug_hunter", False),
            badge_premium=d.get("badge_premium", False),
            badge_verified=d.get("badge_verified", False),
            badge_early=d.get("badge_early", False),
            badge_owner=d.get("badge_owner", False),
            badge_admin=d.get("badge_admin", False),
            custom_badges=[
                CustomBadge.from_dict(b) for b in d.get("custom_badges", [])
            ],
            profile_bg_type=d.get("profile_bg_type"),
            profile_bg_url=d.get("profile_bg_url"),
            profile_sound_url=d.get("profile_sound_url"),
            profile_entry_overlay_text=d.get("profile_entry_overlay_text"),
            profile_ambient_volume=d.get("profile_ambient_volume", 100),
            profile_theme_id=d.get("profile_theme_id"),
            profile_font_id=d.get("profile_font_id"),
            profile_layout_id=d.get("profile_layout_id"),
            profile_motion_id=d.get("profile_motion_id"),
            profile_cursor_id=d.get("profile_cursor_id"),
            profile_custom_cursor_url=d.get("profile_custom_cursor_url"),
            profile_mouse_follow_id=d.get("profile_mouse_follow_id"),
            profile_name_effect_id=d.get("profile_name_effect_id"),
            profile_display_name_color=d.get("profile_display_name_color"),
            profile_shell_backdrop=d.get("profile_shell_backdrop"),
            profile_shell_opacity_pct=d.get("profile_shell_opacity_pct", 92),
            profile_shell_width_pct=d.get("profile_shell_width_pct", 100),
            profile_badges_order=d.get("profile_badges_order", []),
            profile_badges_hidden=d.get("profile_badges_hidden", []),
            profile_badge_monochrome=d.get("profile_badge_monochrome", False),
            profile_badge_mono_hex=d.get("profile_badge_mono_hex"),
            profile_badge_neon=d.get("profile_badge_neon", False),
            profile_badge_monochrome_custom=d.get(
                "profile_badge_monochrome_custom", False
            ),
            profile_description=d.get("profile_description"),
            profile_location_label=d.get("profile_location_label"),
            steam_showcase_url=d.get("steam_showcase_url"),
            roblox_showcase_url=d.get("roblox_showcase_url"),
            profile_show_volume_control=d.get("profile_show_volume_control", True),
            profile_show_clip_views=d.get("profile_show_clip_views", True),
            profile_show_profile_views=d.get("profile_show_profile_views", True),
            profile_hide_empty_clips=d.get("profile_hide_empty_clips", False),
            profile_hide_public_stats=d.get("profile_hide_public_stats", False),
            profile_show_discord_on_public=d.get(
                "profile_show_discord_on_public", False
            ),
            profile_discord_username=d.get("profile_discord_username"),
            profile_discord_avatar_url=d.get("profile_discord_avatar_url"),
            profile_discord_accent_hex=d.get("profile_discord_accent_hex"),
            last_username_change=d.get("last_username_change"),
            username_locked_until=d.get("username_locked_until"),
            username_changed_at=d.get("username_changed_at"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "public_uid": self.public_uid,
            "display_name": self.display_name,
            "phone": self.phone,
            "views": self.views,
            "monthly_views": self.monthly_views,
            "avatar_url": self.avatar_url,
            "discord_booster": self.discord_booster,
            "bug_hunter": self.bug_hunter,
            "badge_premium": self.badge_premium,
            "badge_verified": self.badge_verified,
            "badge_early": self.badge_early,
            "badge_owner": self.badge_owner,
            "badge_admin": self.badge_admin,
            "custom_badges": [
                {"id": b.id, "name": b.name, "icon_url": b.icon_url}
                for b in self.custom_badges
            ],
            "profile_badges_order": self.profile_badges_order,
            "profile_badges_hidden": self.profile_badges_hidden,
            "profile_bg_type": self.profile_bg_type,
            "profile_bg_url": self.profile_bg_url,
            "profile_sound_url": self.profile_sound_url,
            "profile_entry_overlay_text": self.profile_entry_overlay_text,
            "profile_ambient_volume": self.profile_ambient_volume,
            "profile_theme_id": self.profile_theme_id,
            "profile_font_id": self.profile_font_id,
            "profile_layout_id": self.profile_layout_id,
            "profile_motion_id": self.profile_motion_id,
            "profile_cursor_id": self.profile_cursor_id,
            "profile_custom_cursor_url": self.profile_custom_cursor_url,
            "profile_mouse_follow_id": self.profile_mouse_follow_id,
            "profile_name_effect_id": self.profile_name_effect_id,
            "profile_display_name_color": self.profile_display_name_color,
            "profile_shell_backdrop": self.profile_shell_backdrop,
            "profile_shell_opacity_pct": self.profile_shell_opacity_pct,
            "profile_shell_width_pct": self.profile_shell_width_pct,
            "profile_badge_monochrome": self.profile_badge_monochrome,
            "profile_badge_mono_hex": self.profile_badge_mono_hex,
            "profile_badge_neon": self.profile_badge_neon,
            "profile_badge_monochrome_custom": self.profile_badge_monochrome_custom,
            "profile_description": self.profile_description,
            "profile_location_label": self.profile_location_label,
            "steam_showcase_url": self.steam_showcase_url,
            "roblox_showcase_url": self.roblox_showcase_url,
            "profile_show_volume_control": self.profile_show_volume_control,
            "profile_show_clip_views": self.profile_show_clip_views,
            "profile_show_profile_views": self.profile_show_profile_views,
            "profile_hide_empty_clips": self.profile_hide_empty_clips,
            "profile_hide_public_stats": self.profile_hide_public_stats,
            "profile_show_discord_on_public": self.profile_show_discord_on_public,
            "profile_discord_username": self.profile_discord_username,
            "profile_discord_avatar_url": self.profile_discord_avatar_url,
            "profile_discord_accent_hex": self.profile_discord_accent_hex,
        }


@dataclass
class Session:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: int
    user_id: str
    email: str
    username: str

    @classmethod
    def from_dict(cls, d: dict) -> "Session":
        meta = d.get("user", {}).get("user_metadata", {})
        return cls(
            access_token=d["access_token"],
            refresh_token=d["refresh_token"],
            token_type=d.get("token_type", "bearer"),
            expires_in=d["expires_in"],
            expires_at=d["expires_at"],
            user_id=d["user"]["id"],
            email=d["user"]["email"],
            username=meta.get("username", ""),
        )
