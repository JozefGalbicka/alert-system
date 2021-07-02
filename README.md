# alert-system
<h1>crypsde/cryp-alerts</h1>
<p>Cryp Alerting is service that provides web-scrapping of web <a href="https://www.iklub.sk/">iklub.sk</a>. When new articles are found, they will be sent to specified list of recipients.</p>
<h2>Usage</h2>
<p>Here are some example snippets to help you get started creating a container.</p>
<h3>docker-compose (recommended)</h3>
<pre><code class="language-yaml">
services:
  alert-system:
    image: crypsde/alert-system
    container_name: alert-system
    environment:
      - TZ=Europe/Bratislava
    volumes:
      - ./config.json:/app/alert_system/config/config.json
      - ./subscribers.txt:/app/alert_system/config/subscribers.txt
    restart: unless-stopped
</code></pre>

<h3>config.json</h3>
<p>In order to send alerts, you have to log in with your mail account. All needed information can be specified in json configuration file below.</p>
<pre><code class="language-json">
{
  "mail": {
    "login": "&ltusername>@&ltservice>.com",
    "password": "&ltpassword>",
    "display_name": "Cryp Alerts",
    "server": "smtp.&ltservice>.com"
   }
  "twilio": {
    "account_sid": "&ltsid>",
    "auth_token": "&lttoken>",
    "number": "&lttwilio_number>"
  }
}
</code></pre>

<h3>subscribers.txt</h3>
<p>All recipients listed in this file will receive new alerts. Every recipient has to be written on new line.</p>
<pre>
&ltrecipient1>@gmail.com
&ltrecipient2>@gmail.com
</pre>
