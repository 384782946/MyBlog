import jpush
from jpush import common
from . import api

_jpush = jpush.JPush(u'f5bed5a1c355efee733ac6d1', u'5c81a08c6d08339c77a4ed77')

@api.route('/notify')
def nofity():
    msg = reqeust.args.get('msg')
    push = _jpush.create_push()
    # if you set the logging level to "DEBUG",it will show the debug logging.
    #_jpush.set_logging("DEBUG")
    push.audience = jpush.all_
    push.notification = jpush.notification(alert=msg)
    push.platform = jpush.all_
    try:
        response=push.send()
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn error")
    except common.JPushFailure:
        print ("JPushFailure")
    except:
        print ("Exception")
