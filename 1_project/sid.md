Let's set up three simple sites (`public`, `internal`, and `secret`) on your Apache2 server and configure Suricata to generate different alerts based on access to these sites. We'll go through the following steps:

1. **Set up the three sites in Apache2**: Create simple HTML pages for each site.
2. **Configure Apache2 to serve these sites**: Create virtual host configurations for each site.
3. **Configure Suricata**: Write custom rules to generate alerts based on access to each site.

### Step 1: Create the Site Directories and Files

1. **Create directories for each site:**

   ```sh
   sudo mkdir -p /var/www/html/public
   sudo mkdir -p /var/www/html/internal
   sudo mkdir -p /var/www/html/secret
   ```

2. **Create simple HTML pages for each site:**

   ```sh
   echo "<html><body><h1>Public Site</h1></body></html>" | sudo tee /var/www/html/public/index.html
   echo "<html><body><h1>Internal Site</h1></body></html>" | sudo tee /var/www/html/internal/index.html
   echo "<html><body><h1>Secret Site</h1></body></html>" | sudo tee /var/www/html/secret/index.html
   ```

### Step 2: Configure Apache2 Virtual Hosts

1. **Create the configuration files for each site:**

   ```sh
   sudo nano /etc/apache2/sites-available/public.conf
   sudo nano /etc/apache2/sites-available/internal.conf
   sudo nano /etc/apache2/sites-available/secret.conf
   ```

2. **Add the following content to each configuration file:**

   **public.conf**:
   ```apache
   <VirtualHost *:80>
       ServerAdmin webmaster@localhost
       DocumentRoot /var/www/html/public
       ServerName public.local

       <Directory /var/www/html/public>
           Options Indexes FollowSymLinks
           AllowOverride None
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/public_error.log
       CustomLog ${APACHE_LOG_DIR}/public_access.log combined
   </VirtualHost>
   ```

   **internal.conf**:
   ```apache
   <VirtualHost *:80>
       ServerAdmin webmaster@localhost
       DocumentRoot /var/www/html/internal
       ServerName internal.local

       <Directory /var/www/html/internal>
           Options Indexes FollowSymLinks
           AllowOverride None
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/internal_error.log
       CustomLog ${APACHE_LOG_DIR}/internal_access.log combined
   </VirtualHost>
   ```

   **secret.conf**:
   ```apache
   <VirtualHost *:80>
       ServerAdmin webmaster@localhost
       DocumentRoot /var/www/html/secret
       ServerName secret.local

       <Directory /var/www/html/secret>
           Options Indexes FollowSymLinks
           AllowOverride None
           Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/secret_error.log
       CustomLog ${APACHE_LOG_DIR}/secret_access.log combined
   </VirtualHost>
   ```

3. **Enable the new site configurations:**

   ```sh
   sudo a2ensite public.conf
   sudo a2ensite internal.conf
   sudo a2ensite secret.conf
   ```

4. **Reload Apache2 to apply the changes:**

   ```sh
   sudo systemctl reload apache2
   ```

### Step 3: Configure Suricata Rules

1. **Create the custom rules file if it doesn't already exist:**

   ```sh
   sudo nano /etc/suricata/rules/custom.rules
   ```

2. **Add the custom rules:**

   ```plaintext
   # Rule for public site (no alert)
   pass http any any -> any any (msg:"Pass: Access to /public"; flow:to_server,established; content:"/public"; http_uri; nocase; sid:1000001; rev:1;)

   # Rule for internal site (warn alert)
   alert http any any -> any any (msg:"Warning: Access to /internal"; flow:to_server,established; content:"/internal"; http_uri; nocase; priority:2; sid:1000002; rev:1;)

   # Rule for secret site (fatal alert)
   alert http any any -> any any (msg:"Fatal: Access to /secret"; flow:to_server,established; content:"/secret"; http_uri; nocase; priority:1; sid:1000003; rev:1;)
   ```

3. **Ensure the custom rules file is included in Suricata's configuration:**

   Edit the `suricata.yaml` configuration file to include the custom rules file.

   ```sh
   sudo nano /etc/suricata/suricata.yaml
   ```

   Add `custom.rules` to the `rule-files` section:

   ```yaml
   rule-files:
     - suricata.rules
     - custom.rules
   ```

4. **Restart Suricata to apply the new rules:**

   ```sh
   sudo systemctl restart suricata
   ```

### Step 4: Test the Setup

1. **Access each site using `curl` or a web browser:**

   ```sh
   curl http://localhost/public
   curl http://localhost/internal
   curl http://localhost/secret
   ```

2. **Check Suricata logs to verify alerts:**

   ```sh
   sudo tail -f /var/log/suricata/fast.log
   ```

You should see different types of alerts for accessing the `/internal` and `/secret` sites, while accessing the `/public` site should not generate any alert.

By following these steps, you will have three simple sites set up on your Apache2 server with Suricata configured to generate different alerts based on access to these sites.
