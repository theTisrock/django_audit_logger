<h1>An Audit Logger for Django</h1>

<h2>Try the demo</h2>
<p>After cloning this repository and entering into the project directory, in your terminal...</p>

<ol>
    <li>Navigate to the Demo. <code>cd AuditLoggerDemo</code></li>
    <li>Set up the virtual environment. <code>pipenv install</code></li>
    <li>Install django. <code>pipenv install django</code></li>
    <li>Activate the virtual environment <code>pipenv shell</code></li>
    <li>Apply the migrations. Navigate to "my_app". <code>cd my_app</code>
        Then type <code>python manage.py migrate</code>. You should get all "OK's" when the script runs. 
    </li>
    <li>Now run the app: <code>python manage.py runserver</code></li>
</ol>

<p>As you add and delete To-Do list items, you should see the audit logging being printed to standard out (probably your
terminal screen).</p>

<h2>Connect the Audit Logger to your app</h2>

<ol>
    <li>In settings.py, set the log level: <code>AUDIT_LOG_LEVEL = 20</code></li>
    <li>In settings.py, set the log format: <code>AUDIT_LOG_FORMAT = "%(message)s"</code></li>
    <li>In settings.py, under INSTALLED_APPS point to your apps AppConfig subclass: <code>'yourapp.apps.YourAppConfig'</code></li>
    <li>In your app's "apps.py", import the AuditLogEnabledAppConfig. <code>from audit_logger.contrib.app_config import AuditLogEnabledAppConfig</code></li>
    <li>Now subclass it under your app config: 
        <code>class YourAppConfig(AuditLogEnabledAppConfig):</code>
    </li>
    <li>In settings.py, add the audit logger's middleware: <code>'audit_logger.middleware.AuditLogMiddleware',</code></li>
    
</ol>
