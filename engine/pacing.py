# -*- coding: utf-8 -*-
import calendar, math
def allowed_today(history, max_per_month, now):
    """Étale max_per_month posts régulièrement sur le mois. 0 = illimité. Retourne (ok, faits, autorisés)."""
    if not max_per_month: return True, 0, 0
    month = now.strftime("%Y-%m"); done = sum(1 for h in history if str(h.get("date", "")).startswith(month))
    dim = calendar.monthrange(now.year, now.month)[1]; allowed = math.ceil(max_per_month * now.day / dim)
    return done < allowed, done, allowed
