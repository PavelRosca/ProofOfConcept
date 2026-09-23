# Legacy "Sistema Imprese Italia" page — not in this repo any more

The old manifesto page served at the domain root (`https://sistemaimpreseitalia.it/` and
`/sistema-imprese-italia`) is **owned and edited by the client**, so since 2026-09-23 it lives
only on the VPS, outside this repo:

- File: `/var/www/legacy-site/sistema-imprese-italia.html`, owned by `gianpiero-legacy`
- Client access: SFTP as `gianpiero-legacy` (chrooted to `/home/gianpiero-legacy`; the
  `legacy/` folder there is a bind mount of `/var/www/legacy-site`, see `/etc/fstab`)
- Served by nginx directly (`location = /` and `location = /sistema-imprese-italia` in
  `/etc/nginx/sites-enabled/sistemaimpreseitalia.it`), not by Django

Why it moved: while it was tracked here, every `git pull` that touched it recreated it as
`root:root 644`, so the client's SFTP uploads failed with "Permission denied"; and a client edit
would in turn have blocked `git pull` ("local changes would be overwritten").

Earlier versions are in this repo's git history (`git log -- website-wag/legacy/`).
