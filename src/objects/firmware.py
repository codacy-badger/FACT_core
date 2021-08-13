from contextlib import suppress

from helperFunctions.hash import get_md5
from helperFunctions.tag import TagColor
from objects.file import FileObject


class Firmware(FileObject):
    '''
    This class represents a firmware.
    It esentially is a FileObject with some more attributes that only make
    sense for firmware.
    All constructor arguments are passed to the
    :class:`~objects.file.FileObject` constructor
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: The name of the device that the firmware runs on
        self.device_name: str = None
        #: The version of the firmware in no specific format
        self.version: str = None
        #: The type of device that the firmware runs on.
        #: E.g. "router"
        self.device_class: str = None
        self.vendor: str = None
        #: The part of the firmware that is this object represents.
        #: Specifies the parts of an embedded system that are contained in the firmware.
        #: While this meta data string can be freely defined during firmware upload,
        #: FACT provides a preset of frequently used values: 'complete', 'kernel', ' bootloader', and 'root-fs'.
        #: The firmware image is assumed to be 'complete' if the assigned value is an empty string.
        self.part: str = ''
        # The release date of the firmware in the format "YYYY-MM-DD".
        self.release_date: str = None
        #: A dict where the keys represent tags and the values represent the
        #: colors of the tags.
        #: Possible values are defined in :class:`helperFunctions.tag.TagColor`.
        self.tags = dict()
        self._update_root_id_and_virtual_path()

    def set_part_name(self, part):
        if part == 'complete':
            self.part = ''
        else:
            self.part = part

    def set_binary(self, binary):
        super().set_binary(binary)
        self._update_root_id_and_virtual_path()
        self.md5 = get_md5(binary)

    def _update_root_id_and_virtual_path(self):
        self.root_uid = self.uid
        self.virtual_file_path = {self.uid: [self.uid]}

    def set_tag(self, tag, tag_color=TagColor.GRAY):
        self.tags[tag] = tag_color

    def remove_tag(self, tag):
        with suppress(KeyError):
            self.tags.pop(tag)

    def get_hid(self, root_uid=None):
        '''
        return a human readable identifier
        '''
        part = ' - {}'.format(self.part) if self.part else ''
        return '{} {}{} v. {}'.format(self.vendor, self.device_name, part, self.version)

    def __str__(self):
        return '{}\nProcessed Analysis: {}\nScheduled Analysis: {}'.format(self.get_hid(), list(self.processed_analysis.keys()), self.scheduled_analysis)

    def __repr__(self):
        return self.__str__()
