<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - CENTrak</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/site.css" />
    <script src="/static/js/modernizr-2.6.2.js"></script>
</head>
<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">CENTrak</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/xforms/">XForms</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content {{ "front" if defined('is_front') else "not-front" }}">
        % messages = get_session()['messages']
        % msg_pass = messages.get('pass', None)
        % msg_fail = messages.get('fail', None)
        % msg_warn = messages.get('warn', None)

        % message_list = ((msg_pass, 'success'), (msg_fail, 'danger'), (msg_warn, 'warning'))

        % messages['pass'] = []
        % messages['fail'] = []
        % messages['warn'] = []

        % for entry in message_list:
          % if entry[0]:
        <div class="alert alert-{{entry[1]}} alert-dismissible">
            <button type="button" class="close" data-dismiss="alert">&times</button>
            <ul>
            % for m in entry[0]:
              <li>{{ m }}</li>
            % end
            </ul>
        </div>
          % end
        % end
        
        {{!base}}

        <hr />
        <footer>
            <p>&copy; {{ year }} - CENTrak<p>
        </footer>
    </div>
    
    <script src="/static/js/jquery-1.10.2.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
</body>
</html>