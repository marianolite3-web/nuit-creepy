# Nuit — épisodes d'horreur automatiques (TikTok)

Chaque jour à 17h30 UTC, GitHub génère une vidéo verticale (animation, voix FR, sous-titres, ambiance sonore) à partir de l'histoire suivante dans `stories/`, puis la publie sur TikTok via Zernio. Aucun serveur à payer : GitHub Actions est gratuit pour un dépôt public.

## Mise en route (une seule fois, depuis le téléphone)
1. **Zernio** : crée un compte sur zernio.com, connecte ton TikTok, puis crée une clé API (Réglages → API Keys) et copie-la.
2. **GitHub** : dans ce dépôt → Settings → Secrets and variables → Actions → New repository secret.
   Nom : `ZERNIO_API_KEY` — Valeur : ta clé.
3. **Test** : onglet Actions → « Épisode du jour » → Run workflow → mode `test`. Après ~8 min, télécharge l'artefact `episode` et regarde la vidéo.
   (Sur téléphone, si le bouton n'apparaît pas : ouvre GitHub en « version pour ordinateur ».)
4. **Premier vrai post** : Run workflow → mode `post`. Vérifie sur TikTok que la vidéo est **publique** (pas en brouillon).
5. C'est tout : ensuite, un épisode par jour, tout seul.

## Détails utiles
- **Rythme** : par défaut 20 posts par mois, répartis régulièrement (environ 2 jours sur 3), pour rester dans le palier gratuit de Zernio. Pour poster tous les jours après un passage en plan payant : GitHub → Settings → Variables → `MAX_PER_MONTH` = `0`.
- 30 histoires dans `stories/` (ep001 → ep030). Après la 30e, la série reprend au début. Pour en ajouter : nouveaux fichiers `epNNN.json` (même format), ou redemande-les à Claude.
- La vidéo est déclarée « générée par IA » à TikTok (`videoMadeWithAi`).
- `state/state.json` mémorise la prochaine histoire ; il est mis à jour chaque jour (cela garde aussi le dépôt « actif », sinon GitHub désactive les tâches planifiées après 60 jours sans activité).
- Mode `test` : génère la vidéo sans rien publier. Sans clé `ZERNIO_API_KEY`, le mode `post` bascule automatiquement en test.
- Palette, voix, décors : dans `engine/`. Voix : SIWIS (CC-BY 4.0) — à créditer dans la description si tu monétises.
