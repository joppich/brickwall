import os
import time
import shutil
import asyncio

from io import StringIO
from uuid import uuid4
from base64 import b64decode
from pypandoc import convert_text


async def __write_html(path, file_content):
    """
    Convert a base64 encoded string containing the
    md-formatted post content and write its
    html-conversion to disk.
    """
    with open(path, "w") as _f:
        _f.write(convert_text(b64decode(file_content), "html5", format="md"))


async def __save(path, file_content, backup):
    """
    Perform consistency checks and create backup if requested.
    Schedule format conversion and disk write.
    """
    if os.path.isfile(path):
        if backup:
            shutil.copy2(self.path, ".".join(self.path, time.time()))
        os.remove(self.path)
    await __write_html(path, file_content)


def content_file(file_content, basepath, backup=False):
    """
    Determine filepath and run asynchronous jobs.
    Set the backup-flag to True to create timestamped
    backups of existing files.
    """
    filename = str(uuid4())
    path = os.path.join(basepath, filename)
    asyncio.run(__save(path, file_content, backup))
    return filename
