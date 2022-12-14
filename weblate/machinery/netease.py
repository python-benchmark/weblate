#
# Copyright ©2018 Sun Zhigang <hzsunzhigang@corp.netease.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import random
import time
from hashlib import sha1

from django.conf import settings

from .base import MachineTranslation, MachineTranslationError
from .forms import KeySecretMachineryForm

NETEASE_API_ROOT = "https://jianwai.netease.com/api/text/trans"


class NeteaseSightTranslation(MachineTranslation):
    """Netease Sight API machine translation support."""

    name = "Netease Sight"
    max_score = 90

    # Map codes used by Netease Sight to codes used by Weblate
    language_map = {"zh_Hans": "zh"}
    settings_form = KeySecretMachineryForm

    @staticmethod
    def migrate_settings():
        return {
            "key": settings.MT_NETEASE_KEY,
            "secret": settings.MT_NETEASE_SECRET,
        }

    def download_languages(self):
        """List of supported languages."""
        return ["zh", "en"]

    def get_authentication(self):
        """Hook for backends to allow add authentication headers to request."""
        nonce = str(random.randint(1000, 99999999))
        timestamp = str(int(1000 * time.monotonic()))

        sign = self.settings["secret"] + nonce + timestamp
        sign = sign.encode()
        sign = sha1(sign).hexdigest()  # nosec

        return {
            "Content-Type": "application/json",
            "appkey": self.settings["key"],
            "nonce": nonce,
            "timestamp": timestamp,
            "signature": sign,
        }

    def download_translations(
        self,
        source,
        language,
        text: str,
        unit,
        user,
        search: bool,
        threshold: int = 75,
    ):
        """Download list of possible translations from a service."""
        response = self.request(
            "post", NETEASE_API_ROOT, json={"lang": source, "content": text}
        )
        payload = response.json()

        if not payload["success"]:
            raise MachineTranslationError(payload["message"])

        translation = payload["relatedObject"]["content"][0]["transContent"]

        yield {
            "text": translation,
            "quality": self.max_score,
            "service": self.name,
            "source": text,
        }
