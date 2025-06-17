::: {#mdbook-help-container}
::: {#mdbook-help-popup}
## Keyboard shortcuts {#keyboard-shortcuts .mdbook-help-title}

<div>

Press [←]{.kbd} or [→]{.kbd} to navigate between chapters

Press [S]{.kbd} or [/]{.kbd} to search in the book

Press [?]{.kbd} to show this help

Press [Esc]{.kbd} to hide this help

</div>
:::
:::

::: {#body-container}
::: {#sidebar-resize-handle .sidebar-resize-handle}
::: sidebar-resize-indicator
:::
:::

::: {#page-wrapper .page-wrapper}
::: page
::: {#menu-bar-hover-placeholder}
:::

::: {#menu-bar .menu-bar .sticky}
::: left-buttons

-   Auto
-   Light
-   Rust
-   Coal
-   Navy
-   Ayu
:::

# Kanidm Administration {#kanidm-administration .menu-title}

::: right-buttons
[](print.html "Print this book"){aria-label="Print this book"}
[](https://github.com/kanidm/kanidm "Git repository"){aria-label="Git repository"}
[](https://github.com/kanidm/kanidm/edit/master/book/src/evaluation_quickstart.md "Suggest an edit"){aria-label="Suggest an edit"}
:::
:::

::: {#search-wrapper .hidden}
::: {#searchresults-outer .searchresults-outer .hidden}
::: {#searchresults-header .searchresults-header}
:::
:::
:::

::: {#content .content}
::: {role="main"}
# [Evaluation Quickstart](#evaluation-quickstart){.header}

This section will guide you through a quick setup of Kanidm for
evaluation. It\'s recommended that for a production deployment you
follow the steps in the [installation
chapter](installing_the_server.html) instead as there are a number of
security considerations you should be aware of for production
deployments.

## [Requirements](#requirements){.header}

The only thing you\'ll need for this is Docker, Podman, or a compatible
containerd environment installed and running.

## [Get the software](#get-the-software){.header}

``` bash
docker pull docker.io/kanidm/server:latest
```

## [Create your configuration](#create-your-configuration){.header}

Create `server.toml`. The important parts are the `domain` and `origin`.
For this example, if you use `localhost` and `https://localhost:8443`
this will match later commands.

``` toml
# The server configuration file version.
version = "2"

#   The webserver bind address. Requires TLS certificates.
#   If the port is set to 443 you may require the
#   NET_BIND_SERVICE capability.
#   Defaults to "127.0.0.1:8443"
bindaddress = "[::]:8443"
#
#   The read-only ldap server bind address. Requires
#   TLS certificates. If set to 636 you may require
#   the NET_BIND_SERVICE capability.
#   Defaults to "" (disabled)
# ldapbindaddress = "[::]:3636"
#
#   The path to the kanidm database.
db_path = "/data/kanidm.db"
#
#   If you have a known filesystem, kanidm can tune the
#   database page size to match. Valid choices are:
#   [zfs, other]
#   If you are unsure about this leave it as the default
#   (other). After changing this
#   value you must run a vacuum task.
#   - zfs:
#     * sets database pagesize to 64k. You must set
#       recordsize=64k on the zfs filesystem.
#   - other:
#     * sets database pagesize to 4k, matching most
#       filesystems block sizes.
# db_fs_type = "zfs"
#
#   The number of entries to store in the in-memory cache.
#   Minimum value is 256. If unset
#   an automatic heuristic is used to scale this.
#   You should only adjust this value if you experience
#   memory pressure on your system.
# db_arc_size = 2048
#
#   TLS chain and key in pem format. Both must be present.
#   If the server receives a SIGHUP, these files will be
#   re-read and reloaded if their content is valid.
tls_chain = "/data/chain.pem"
tls_key = "/data/key.pem"
#
#   The log level of the server. May be one of info, debug, trace
#
#   NOTE: this can be overridden by the environment variable
#   `KANIDM_LOG_LEVEL` at runtime
#   Defaults to "info"
# log_level = "info"
#
#   The DNS domain name of the server. This is used in a
#   number of security-critical contexts
#   such as webauthn, so it *must* match your DNS
#   hostname. It is used to create
#   security principal names such as `william@idm.example.com`
#   so that in a (future) trust configuration it is possible
#   to have unique Security Principal Names (spns) throughout
#   the topology.
#
#   ⚠️  WARNING ⚠️
#
#   Changing this value WILL break many types of registered
#   credentials for accounts including but not limited to
#   webauthn, oauth tokens, and more.
#   If you change this value you *must* run
#   `kanidmd domain rename` immediately after.
domain = "idm.example.com"
#
#   The origin for webauthn. This is the url to the server,
#   with the port included if it is non-standard (any port
#   except 443). This must match or be a descendent of the
#   domain name you configure above. If these two items are
#   not consistent, the server WILL refuse to start!
#   origin = "https://idm.example.com"
origin = "https://idm.example.com:8443"

#   HTTPS requests can be reverse proxied by a loadbalancer.
#   To preserve the original IP of the caller, these systems
#   will often add a header such as "Forwarded" or
#   "X-Forwarded-For". Some other proxies can use the PROXY
#   protocol v2 header.
#   This setting allows configuration of the list of trusted
#   IPs or IP ranges which can supply this header information,
#   and which format the information is provided in.
#   Defaults to "none" (no trusted sources)
#   Only one option can be used at a time.
# [http_client_address_info]
# proxy-v2 = ["127.0.0.1", "127.0.0.0/8"]
#   # OR
# x-forward-for = ["127.0.0.1", "127.0.0.0/8"]

#   LDAPS requests can be reverse proxied by a loadbalancer.
#   To preserve the original IP of the caller, these systems
#   can add a header such as the PROXY protocol v2 header.
#   This setting allows configuration of the list of trusted
#   IPs or IP ranges which can supply this header information,
#   and which format the information is provided in.
#   Defaults to "none" (no trusted sources)
# [ldap_client_address_info]
# proxy-v2 = ["127.0.0.1", "127.0.0.0/8"]

[online_backup]
#   The path to the output folder for online backups
path = "/data/kanidm/backups/"
#   The schedule to run online backups (see https://crontab.guru/)
#   every day at 22:00 UTC (default)
schedule = "00 22 * * *"
#    four times a day at 3 minutes past the hour, every 6th hours
# schedule = "03 */6 * * *"
#   We also support non standard cron syntax, with the following format:
#   sec  min   hour   day of month   month   day of week   year
#   (it's very similar to the standard cron syntax, it just allows to specify the seconds
#   at the beginning and the year at the end)
#   Number of backups to keep (default 7)
# versions = 7
```

## [Start the container](#start-the-container){.header}

First we create a docker volume to store the data, then we start the
container.

``` bash
docker volume create kanidmd
docker create --name kanidmd \
  -p '443:8443' \
  -p '636:3636' \
  -v kanidmd:/data \
  docker.io/kanidm/server:latest
```

## [Copy the configuration to the container](#copy-the-configuration-to-the-container){.header}

``` bash
docker cp server.toml kanidmd:/data/server.toml
```

## [Generate evaluation certificates](#generate-evaluation-certificates){.header}

``` bash
docker run --rm -i -t -v kanidmd:/data \
  docker.io/kanidm/server:latest \
  kanidmd cert-generate
```

## [Start Kanidmd Container](#start-kanidmd-container){.header}

``` bash
docker start kanidmd
```

## [Recover the Admin Role Passwords](#recover-the-admin-role-passwords){.header}

The `admin` account is used to configure Kanidm itself.

``` bash
docker exec -i -t kanidmd \
  kanidmd recover-account admin
```

The `idm_admin` account is used to manage persons and groups.

``` shell
docker exec -i -t kanidmd \
  kanidmd recover-account idm_admin
```

## [Setup the client configuration](#setup-the-client-configuration){.header}

This happens on your computer, not in the container.

``` toml
# ~/.config/kanidm

uri = "https://localhost:8443"
verify_ca = false
```

## [Check you can login](#check-you-can-login){.header}

``` bash
kanidm login --name idm_admin
```

## [Create an account for yourself](#create-an-account-for-yourself){.header}

``` shell
kanidm person create <your username> <Your Displayname>
```

## [Set up your account credentials](#set-up-your-account-credentials){.header}

``` shell
kanidm person credential create-reset-token <your username>
```

Then follow the presented steps.

## [What next?](#what-next){.header}

You\'ll probably want to set it up properly, so that other computers can
access it, so [choose a domain name](choosing_a_domain_name.html) and
complete the full server installation.

Alternatively you might like to try configurig one of these:

-   [OAuth2](./integrations/oauth2.html) for web services
-   [PAM and nsswitch](./integrations/pam_and_nsswitch.html) for
    authentication to Linux systems
-   [Replication](repl/), if one Kanidm instance isn\'t enough
:::

[](introduction_to_kanidm.html "Previous chapter"){.mobile-nav-chapters
.previous rel="prev" aria-label="Previous chapter"
aria-keyshortcuts="Left"}
[](supported_features.html "Next chapter"){.mobile-nav-chapters .next
rel="next prefetch" aria-label="Next chapter" aria-keyshortcuts="Right"}

::: {style="clear: both"}
:::
:::
:::

[](introduction_to_kanidm.html "Previous chapter"){.nav-chapters
.previous rel="prev" aria-label="Previous chapter"
aria-keyshortcuts="Left"}
[](supported_features.html "Next chapter"){.nav-chapters .next
rel="next prefetch" aria-label="Next chapter" aria-keyshortcuts="Right"}
:::
:::
