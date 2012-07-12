# -*- coding: utf-8 -*-

from media.monitor.handler import ReportHandler
import media.monitor.pure as mmp
from media.monitor.log import Loggable
from media.monitor.exceptions import BadSongFile

class Organizer(ReportHandler,Loggable):
    def __init__(self, channel, target_path):
        self.channel = channel
        self.target_path = target_path
        super(Organizer, self).__init__(signal=self.channel.signal)
    def handle(self, sender, event):
        """Intercept events where a new file has been added to the organize
        directory and place it in the correct path (starting with self.target_path)"""
        try:
            normal_md = mmp.normalized_metadata(event.metadata, event.path)
            new_path = mmp.organized_path(event.path, self.target_path, normal_md)
            mmp.magic_move(event.path, new_path)
            self.logger.info('Organized: "%s" into "%s"' % (event.path, new_path))
        except BadSongFile as e:
            self.report_problem_file(event=event, exception=e)
        # probably general error in mmp.magic.move...
        except Exception as e:
            self.report_problem_file(event=event, exception=e)

