import jpush
from jpush import common
from . import api
from flask import request

_jpush = jpush.JPush(u'', u'')

@api.route('/notify')
def nofity():
    msg = request.args.get('msg')
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
    return 'notify success'
