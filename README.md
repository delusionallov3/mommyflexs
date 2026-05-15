# flexslol

> this readme + some comment are gen w ia after work + rework variable cause im not a good boy so

Python client for the **flexs.lol** API (Supabase backend).

---

## Installation

```bash
# From the zip / source
pip install .

# Or
pip install git+https://github.com/delusionallov3/mommyflexs.git
```

**Requires:** Python ≥ 3.8, `requests`

---

## Quick start

```python
from flexslol import Client

client = Client()
print(client)  # <flexslol.Client [unauthenticated]>
```

---

## Users

All user methods work **without logging in**.

```python
# List all users (paginated)
users = client.users.list(limit=50, offset=0, order_by="public_uid")

# Get by UUID
user = client.users.get("af3f73f8-d3c4-4a4a-8d12-27f9cef21e16")

# Get by username (case-insensitive)
user = client.users.get_by_username("V")

# Get by numeric public UID
user = client.users.get_by_public_uid(4)

# Search by username prefix
results = client.users.search("rich", limit=10)

# Pretty print
print(user.username, user.views, user.badge_premium)
print([b.name for b in user.custom_badges])
```

### User fields (all typed)

| Field                    | Type              | Description                              |
| ------------------------ | ----------------- | ---------------------------------------- |
| `id`                     | str               | UUID                                     |
| `username`               | str               | Unique username                          |
| `public_uid`             | int               | Numeric public ID                        |
| `display_name`           | str?              | Display name override                    |
| `avatar_url`             | str?              | Avatar image URL                         |
| `views`                  | int?              | Total profile views                      |
| `monthly_views`          | int?              | Views this month                         |
| `badge_premium`          | bool              | Premium badge                            |
| `badge_verified`         | bool              | Verified badge                           |
| `badge_early`            | bool              | Early adopter badge                      |
| `badge_owner`            | bool              | Owner badge                              |
| `badge_admin`            | bool              | Admin badge                              |
| `bug_hunter`             | bool              | Bug hunter badge                         |
| `discord_booster`        | bool              | Discord booster badge                    |
| `custom_badges`          | List[CustomBadge] | Custom badges                            |
| `profile_theme_id`       | str?              | Theme (e.g. `"noir"`, `"default"`)       |
| `profile_font_id`        | str?              | Font (e.g. `"wide"`, `"sans"`)           |
| `profile_layout_id`      | str?              | Layout (e.g. `"spotlight"`, `"classic"`) |
| `profile_motion_id`      | str?              | Motion effect                            |
| `profile_cursor_id`      | str?              | Cursor style                             |
| `profile_description`    | str?              | Bio                                      |
| `profile_location_label` | str?              | Location string                          |
| `steam_showcase_url`     | str?              | Steam profile URL                        |
| `roblox_showcase_url`    | str?              | Roblox profile URL                       |
| …                        | …                 | (all profile\_\* fields available)       |

---

## Authentication

```python
# Sign up
session = client.auth.signup("me@example.com", "mypassword", username="coolname")

# Log in
session = client.auth.login("me@example.com", "mypassword")

print(session.user_id)
print(session.username)
print(session.access_token)   # JWT
print(session.expires_at)     # Unix timestamp

# Check status
print(client.auth.is_authenticated)  # True
print(client.auth.session)           # Session object

# Refresh token
session = client.auth.refresh()

# Logout (local only)
client.auth.logout()
```

---

## Updating your profile

You must be logged in. Pass **only** the fields you want to change.

```python
client.auth.login("me@example.com", "password")

# Update anything — all kwargs are optional
updated_user = client.users.update(
    display_name="My New Name",
    profile_theme_id="noir",
    profile_font_id="wide",
    profile_description="Hello world",
    profile_location_label="France",
    badge_premium=True,
    profile_badge_monochrome=True,
    profile_badge_mono_hex="#ff0000",
)

print(updated_user.display_name)  # "My New Name"
```

### All updatable fields

| Field                             | Type       |
| --------------------------------- | ---------- |
| `username`                        | str        |
| `display_name`                    | str        |
| `avatar_url`                      | str        |
| `discord_booster`                 | bool       |
| `bug_hunter`                      | bool       |
| `badge_premium`                   | bool       |
| `badge_verified`                  | bool       |
| `badge_early`                     | bool       |
| `badge_owner`                     | bool       |
| `badge_admin`                     | bool       |
| `custom_badges`                   | list[dict] |
| `profile_badges_order`            | list[str]  |
| `profile_badges_hidden`           | list[str]  |
| `profile_bg_type`                 | str        |
| `profile_bg_url`                  | str        |
| `profile_sound_url`               | str        |
| `profile_entry_overlay_text`      | str        |
| `profile_ambient_volume`          | int        |
| `profile_theme_id`                | str        |
| `profile_font_id`                 | str        |
| `profile_layout_id`               | str        |
| `profile_motion_id`               | str        |
| `profile_cursor_id`               | str        |
| `profile_custom_cursor_url`       | str        |
| `profile_mouse_follow_id`         | str        |
| `profile_name_effect_id`          | str        |
| `profile_display_name_color`      | str        |
| `profile_shell_backdrop`          | str        |
| `profile_shell_opacity_pct`       | int        |
| `profile_shell_width_pct`         | int        |
| `profile_badge_monochrome`        | bool       |
| `profile_badge_mono_hex`          | str        |
| `profile_badge_neon`              | bool       |
| `profile_badge_monochrome_custom` | bool       |
| `profile_description`             | str        |
| `profile_location_label`          | str        |
| `steam_showcase_url`              | str        |
| `roblox_showcase_url`             | str        |
| `profile_show_volume_control`     | bool       |
| `profile_show_clip_views`         | bool       |
| `profile_show_profile_views`      | bool       |
| `profile_hide_empty_clips`        | bool       |
| `profile_hide_public_stats`       | bool       |
| `profile_show_discord_on_public`  | bool       |
| `profile_discord_username`        | str        |
| `profile_discord_avatar_url`      | str        |
| `profile_discord_accent_hex`      | str        |

---

## Error handling

```python
from flexslol import (
    Client,
    AuthError,
    NotAuthenticatedError,
    UserNotFoundError,
    APIError,
)

client = Client()

try:
    user = client.users.get_by_username("doesnotexist")
except UserNotFoundError as e:
    print("Not found:", e)

try:
    client.users.update(display_name="oops")
except NotAuthenticatedError as e:
    print("Need to login first:", e)

try:
    client.auth.login("bad@email.com", "wrongpass")
except AuthError as e:
    print("Auth failed:", e)
```

| Exception               | When                                                  |
| ----------------------- | ----------------------------------------------------- |
| `AuthError`             | Signup / login failure                                |
| `NotAuthenticatedError` | Calling an auth-required method without a session     |
| `UserNotFoundError`     | `get()` / `get_by_username()` returns empty           |
| `APIError`              | Unexpected HTTP status — has `.status_code` attribute |
| `FlexslolError`         | Base class for all above                              |

---

## Session object

| Field           | Type                 |
| --------------- | -------------------- |
| `access_token`  | str                  |
| `refresh_token` | str                  |
| `token_type`    | str                  |
| `expires_in`    | int (seconds)        |
| `expires_at`    | int (unix timestamp) |
| `user_id`       | str (UUID)           |
| `email`         | str                  |
| `username`      | str                  |

---

## Project structure

```
flexslol/
├── flexslol/
│   ├── __init__.py      ← Client entry point + public exports
│   ├── client.py        ← AuthClient, UsersClient, _Http
│   ├── models.py        ← User, Session, CustomBadge dataclasses
│   └── exceptions.py    ← Error hierarchy
├── setup.py
└── README.md
```
