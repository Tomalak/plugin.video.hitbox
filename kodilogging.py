import xbmc


def debug(message):
    xbmc.log(str(message), xbmc.LOGDEBUG)


def error(message):
    xbmc.log(str(message), xbmc.LOGERROR)


def warning(message):
    xbmc.log(str(message), xbmc.LOGWARNING)


def info(message):
    xbmc.log(str(message), xbmc.LOGINFO)
