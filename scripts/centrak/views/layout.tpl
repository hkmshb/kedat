<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - CENTrak Scripts</title>
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
                <a href="/" class="navbar-brand">CENTrak Scripts</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/home">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">

       % session = request.environ.get('beaker.session', {})
       % if 'errors' in session:
            % msg_errors = session.get('errors', [])
            % del session['errors']
       % end
       % if '__all__' in session:
            % msg_all = session.get('__all__', [])
            % del session['__all__']
       % end
       % session.save()

        % if defined('msg_errors'):
        <div class="alert alert-danger alert-dismissible errors">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          <ul>
          %for m in msg_errors:
            <li>{{ m }}</li>
          %end
          </ul>
        </div>
        % end

        % if defined('msg_all'):
        <div class="alert alert-info alert-dismissible info">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          <ul>
          %for m in msg_all:
            <li>{{ m }}</li>
          %end
          </ul>
        </div>
        % end

        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - CENTrak Scripts</p>
        </footer>
    </div>

    <script src="/static/js/jquery-1.10.2.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/respond.js"></script>

</body>
</html>
