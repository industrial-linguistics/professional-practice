# genius-of-crowds.com httpd.conf

The following snippet shows the web server configuration for **genius-of-crowds.com**. It defines virtual hosts for plain HTTP and TLS, ACME challenge handling, and CGI execution.

```httpd
server "genius-of-crowds.com" {
        log style combined
        alias "app.genius-of-crowds.com"
        alias "www.genius-of-crowds.com"
        directory { auto index }
        listen on $listen_addr port 80
        listen on $listen_addr tls port 443
        tls {
            key "/etc/ssl/private/genius-of-crowds.com.key"  
            certificate "/etc/ssl/genius-of-crowds.com.crt"
        }
        location "/.well-known/acme-challenge/*" {
            root "/acme"
            request strip 2
        }  
        root "/vhosts/genius-of-crowds.com/htdocs"
        location "/cgi-bin/*" {
            fastcgi
            root "/vhosts/genius-of-crowds.com"
        }  
}
```

